# -*- coding: utf-8 -*-
# main_gui.py (02:17) - SINGLE FILE FINAL
# - Splash logo first (root hidden)
# - Then fullscreen main window + language selection
# - Triptych: 3x512 canvas (no shrinking)
# - POP-IN + SEGMENTED FLOW:
#     img1 -> sentence1 -> img2 -> sentence2 -> img3 -> rest
#   (Split parts with "||" inside story text)
# - Segments APPEND (all text remains visible)
# - Music (mp3) + footsteps loop (wav)
# - Audio settings overlay (icon button)
# - Typewriter text + tiny click beeps
# - Choice hover previews (next scene image)
#
# UPDATES:
# - Music starts at 5%
# - One-shot footstep.mp3 at FIRST scene first "||" boundary with micro shift
# - Cinematic fade transitions on scene changes (GUARANTEED Canvas overlay, no alpha/Toplevel)

import tkinter as tk
import os
import math

# ----------------------------
# Optional: Pillow for smooth image resizing/animation (recommended)
# ----------------------------
PIL_OK = True
try:
    from PIL import Image, ImageTk
except Exception:
    PIL_OK = False

# ----------------------------
# Import story (robust)
# ----------------------------
try:
    from game_story import story_en as STORY_EN, story_tr as STORY_TR
except Exception:
    from game_story import STORY_EN, STORY_TR

# ----------------------------
# winsound (tiny UI beeps)
# ----------------------------
try:
    import winsound
except Exception:
    winsound = None


def soft_click():
    if winsound:
        try:
            winsound.Beep(1800, 6)
        except:
            pass


# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bg_path = os.path.join(BASE_DIR, "images", "bg.png")
logo_path = os.path.join(BASE_DIR, "images", "logo.png")
settings_icon_path = os.path.join(BASE_DIR, "images", "settings_icon.png")

MUSIC_LOOP = os.path.join(BASE_DIR, "sounds", "atari_loop.mp3")
FOOTSTEPS_LOOP = os.path.join(BASE_DIR, "sounds", "footsteps_loop.wav")

# One-shot sfx (you said you found footstep.mp3)
FOOTSTEP_ONESHOT = os.path.join(BASE_DIR, "sounds", "footstep.mp3")

# ----------------------------
# pygame audio (music + ambience + sfx)
# ----------------------------
PYGAME_OK = True
try:
    import pygame
    pygame.mixer.init()
except Exception as e:
    PYGAME_OK = False
    print("PYGAME INIT ERROR:", e)

music_playing = False
ambient_playing = False

# Start music at 5%
music_volume_percent = 5
music_volume = music_volume_percent / 100.0

steps_sound = None
steps_channel = None

# One-shot cache
_sfx_cache = {}


def set_music_volume_percent(percent: int):
    global music_volume, music_volume_percent
    music_volume_percent = max(0, min(100, int(percent)))
    music_volume = music_volume_percent / 100.0
    if PYGAME_OK:
        try:
            pygame.mixer.music.set_volume(music_volume)
        except:
            pass


def play_music_loop():
    global music_playing
    if not PYGAME_OK:
        print("pygame yok -> müzik çalamam.")
        return
    if music_playing:
        return
    if not os.path.exists(MUSIC_LOOP):
        print("MUSIC MISSING:", MUSIC_LOOP)
        return
    try:
        pygame.mixer.music.load(MUSIC_LOOP)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        music_playing = True
    except Exception as e:
        print("MUSIC PLAY ERROR:", e)


def stop_music():
    global music_playing
    if not PYGAME_OK:
        return
    try:
        pygame.mixer.music.stop()
    except:
        pass
    music_playing = False


def play_steps_loop():
    global ambient_playing, steps_sound, steps_channel
    if not PYGAME_OK:
        return
    if ambient_playing:
        return
    if not os.path.exists(FOOTSTEPS_LOOP):
        print("FOOTSTEPS MISSING:", FOOTSTEPS_LOOP)
        return
    try:
        if steps_sound is None:
            steps_sound = pygame.mixer.Sound(FOOTSTEPS_LOOP)
        if steps_channel is None:
            steps_channel = pygame.mixer.Channel(1)
        steps_channel.set_volume(0.45)
        steps_channel.play(steps_sound, loops=-1)
        ambient_playing = True
    except Exception as e:
        print("FOOTSTEPS PLAY ERROR:", e)


def stop_steps_loop():
    global ambient_playing, steps_channel
    if not PYGAME_OK:
        return
    try:
        if steps_channel:
            steps_channel.stop()
    except:
        pass
    ambient_playing = False


def play_sfx_once(path: str, volume: float = 0.75):
    """Play a one-shot sound effect safely (mp3/wav)."""
    if not PYGAME_OK:
        return
    if not path:
        return

    ap = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)
    if not os.path.exists(ap):
        print("SFX MISSING:", ap)
        return

    try:
        snd = _sfx_cache.get(ap)
        if snd is None:
            snd = pygame.mixer.Sound(ap)
            _sfx_cache[ap] = snd

        try:
            snd.set_volume(max(0.0, min(1.0, float(volume))))
        except:
            pass

        ch = None
        try:
            ch = pygame.mixer.find_channel(True)
        except:
            ch = pygame.mixer.Channel(2)

        if ch:
            ch.play(snd)
        else:
            snd.play()
    except Exception as e:
        print("SFX PLAY ERROR:", ap, e)


def stop_all_audio():
    stop_steps_loop()
    stop_music()
    if PYGAME_OK:
        try:
            pygame.mixer.quit()
        except:
            pass


# ----------------------------
# Global UI / Game state
# ----------------------------
BG_COLOR = "#0b0f1a"

story = None
current = "start"
scene = None

events = {"O1": False, "O2": False, "O3": False, "O4": False, "O5": False}
EVENT_ORDER = ["O1", "O2", "O3", "O4", "O5"]

# Typewriter state
full_text = ""
index = 0
click_count = 0
typing_done = True

# Segmented story flow state
segments = []
seg_i = 0
after_segment_hook = None

# Image caches
_img_cache = {}
_preview_cache = {}

# ----------------------------
# Triptych canvas layout (3 x 512)
# ----------------------------
IMG_W = 512
IMG_H = 512
GAP = 16  # between images

CAROUSEL_W = (IMG_W * 3) + (GAP * 2)
CAROUSEL_H = IMG_H

SLOT_Y = CAROUSEL_H // 2
SLOT_LX = (IMG_W // 2)
SLOT_CX = SLOT_LX + IMG_W + GAP
SLOT_RX = SLOT_CX + IMG_W + GAP

BIG_W, BIG_H = IMG_W, IMG_H

# ----------------------------
# SPEED TUNING (edit these)
# ----------------------------
# Pop-in visuals (slower, premium)
POP_MS = 360         # pop-in duration per image (ms)
POP_FRAMES = 14      # more frames -> smoother
POP_DELAY_12 = 140   # img1 -> seg1 pause
POP_DELAY_23 = 170   # seg->img pause and img->seg pause

# Typewriter (slower)
TYPE_MS = 30         # normal char delay
PUNCT_MS = 340       # delay after . ! ?
HOOK_MS = 110        # small pause between segments/hook calls

# One-shot timing micro shift at "||" boundary
SFX_SHIFT_MS = 40

# Fade transition (GUARANTEED canvas overlay)
FADE_MS = 220
FADE_STEPS = 16

# Carousel state
carousel_animating = False
slot_items = {"L": None, "C": None, "R": None}
slot_images = {"L": None, "C": None, "R": None}
tmp_refs = {}

# UI widgets
root = None
bg_label = None
bg_img = None
carousel_canvas = None
card = None
story_label = None
choices_row = None
choice_buttons = []
preview_labels = []
audio_ui = None

# Fade overlay canvas (guaranteed)
fade_canvas = None
fade_rect = None
fade_animating = False


# ----------------------------
# Utility
# ----------------------------
def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)


def load_photo_fit(path, target_w, target_h, cache_dict):
    """Load image and fit inside target box keeping aspect ratio."""
    if not path:
        return None
    ap = abs_path(path)
    key = (ap, target_w, target_h)

    if key in cache_dict:
        return cache_dict[key]
    if not os.path.exists(ap):
        cache_dict[key] = None
        return None

    if PIL_OK:
        try:
            im = Image.open(ap).convert("RGBA")
            w, h = im.size
            scale = min(target_w / w, target_h / h)
            nw = max(1, int(w * scale))
            nh = max(1, int(h * scale))
            im2 = im.resize((nw, nh), Image.LANCZOS)
            img = ImageTk.PhotoImage(im2)
            cache_dict[key] = img
            return img
        except Exception as e:
            print("PIL LOAD ERROR:", ap, e)

    # Tk fallback
    try:
        img_raw = tk.PhotoImage(file=ap)
        w, h = img_raw.width(), img_raw.height()
        scale = max(w / target_w, h / target_h)
        factor = max(1, math.ceil(scale))
        img = img_raw.subsample(factor, factor) if factor > 1 else img_raw
        cache_dict[key] = img
        return img
    except Exception as e:
        print("TK LOAD ERROR:", ap, e)
        cache_dict[key] = None
        return None


def get_scene_images_list(scn: dict):
    """Support both 'images' list and legacy 'image' string."""
    if not scn:
        return []
    imgs = scn.get("images", None)
    if imgs is None:
        single = scn.get("image")
        return [single] if single else []
    if isinstance(imgs, (list, tuple)):
        return [p for p in imgs if p]
    return []


def load_preview_image_for_scene(nxt_scene: dict):
    """Preview: prefer 'image', else images[0]."""
    if not nxt_scene:
        return None
    p = nxt_scene.get("image")
    if p:
        return p
    imgs = nxt_scene.get("images", [])
    if isinstance(imgs, list) and imgs:
        return imgs[0]
    return None


def split_text_into_segments(txt: str):
    """Story text içinde '||' ile böl."""
    if not txt:
        return [""]
    if "||" in txt:
        parts = [p.strip() for p in txt.split("||")]
        return [p for p in parts if p != ""]
    return [txt]


# ----------------------------
# Fade transition (GUARANTEED Canvas Overlay)
# ----------------------------
def _fade_set_level(level_idx: int):
    """
    Tkinter gerçek opacity yok; stipple ile "fade hissi" veriyoruz.
    level_idx: 0..4
    """
    if fade_canvas is None or fade_rect is None:
        return

    # lighter -> darker
    levels = ["", "gray75", "gray50", "gray25", "gray12"]
    level_idx = max(0, min(4, int(level_idx)))

    try:
        if level_idx <= 0:
            fade_canvas.itemconfig(fade_rect, stipple="")
        else:
            fade_canvas.itemconfig(fade_rect, stipple=levels[level_idx])
    except:
        pass


def fade_transition(do_mid_action, on_done=None):
    """
    Fade to dark -> do_mid_action() -> fade in
    Guaranteed: no alpha, no Toplevel. Uses a canvas overlay.
    """
    global fade_animating
    if fade_animating:
        try:
            do_mid_action()
        except:
            pass
        if on_done:
            on_done()
        return

    if fade_canvas is None or fade_rect is None:
        # If overlay not ready for some reason, fallback to direct
        try:
            do_mid_action()
        except:
            pass
        if on_done:
            on_done()
        return

    fade_animating = True
    step_ms = max(10, int(FADE_MS / max(1, FADE_STEPS)))

    def fade_out(k=0):
        if k >= FADE_STEPS:
            # fully dark
            fade_canvas.lift()
            _fade_set_level(4)

            try:
                do_mid_action()
            except Exception as e:
                print("FADE MID ACTION ERROR:", e)

            fade_in(0)
            return

        fade_canvas.lift()
        idx = min(4, int((k / max(1, (FADE_STEPS - 1))) * 4))
        _fade_set_level(idx)
        root.after(step_ms, lambda: fade_out(k + 1))

    def fade_in(k=0):
        global fade_animating
        if k >= FADE_STEPS:
            _fade_set_level(0)
            fade_canvas.lower()
            fade_animating = False
            if on_done:
                on_done()
            return

        fade_canvas.lift()
        idx = min(4, int(((FADE_STEPS - 1 - k) / max(1, (FADE_STEPS - 1))) * 4))
        _fade_set_level(idx)
        root.after(step_ms, lambda: fade_in(k + 1))

    fade_out(0)


# ----------------------------
# Carousel helpers
# ----------------------------
def carousel_clear():
    carousel_canvas.delete("all")
    for k in ("L", "C", "R"):
        slot_items[k] = None
        slot_images[k] = None
    tmp_refs.clear()


def place_slot(slot_key, photo, x, y):
    if photo is None:
        return
    if slot_items[slot_key] is None:
        slot_items[slot_key] = carousel_canvas.create_image(x, y, image=photo)
    else:
        carousel_canvas.itemconfig(slot_items[slot_key], image=photo)
        carousel_canvas.coords(slot_items[slot_key], x, y)
    slot_images[slot_key] = photo


def show_logo_on_canvas():
    carousel_clear()
    logo = load_photo_fit("images/logo.png", CAROUSEL_W, CAROUSEL_H, _img_cache)
    if logo:
        carousel_canvas.create_image(CAROUSEL_W // 2, CAROUSEL_H // 2, image=logo)
        tmp_refs["logo_canvas"] = logo
    else:
        carousel_canvas.create_text(
            CAROUSEL_W // 2, CAROUSEL_H // 2,
            text="LOGO LOAD ERROR",
            fill="white", font=("Arial", 18, "bold")
        )


def pop_in_to_slot(slot_key, path, x, y, duration_ms=POP_MS, frames=POP_FRAMES, on_done=None):
    """
    Pop-in: küçükten büyüyerek doğma efekti.
    PIL varsa animasyon; yoksa direkt koyar.
    """
    if not path:
        if on_done:
            on_done()
        return

    ap = abs_path(path)
    if not os.path.exists(ap):
        print("POP_IN MISSING:", ap)
        if on_done:
            on_done()
        return

    if not PIL_OK:
        img = load_photo_fit(ap, BIG_W, BIG_H, _img_cache)
        place_slot(slot_key, img, x, y)
        if on_done:
            on_done()
        return

    try:
        base = Image.open(ap).convert("RGBA")

        bw, bh = base.size
        scale_fit = min(BIG_W / bw, BIG_H / bh)
        tw = max(1, int(bw * scale_fit))
        th = max(1, int(bh * scale_fit))
        base = base.resize((tw, th), Image.LANCZOS)

        start_s = 0.20
        end_s = 1.00

        imgs = []
        for i in range(frames):
            t = (i + 1) / frames
            s = start_s + (end_s - start_s) * t
            nw = max(1, int(tw * s))
            nh = max(1, int(th * s))
            fr = base.resize((nw, nh), Image.LANCZOS)
            imgs.append(ImageTk.PhotoImage(fr))

        item = carousel_canvas.create_image(x, y, image=imgs[0])

        tmp_refs[f"pop_{slot_key}_frames"] = imgs
        tmp_refs[f"pop_{slot_key}_item"] = item

        step_ms = max(10, duration_ms // frames)

        def _anim(k=0):
            if k >= frames:
                place_slot(slot_key, imgs[-1], x, y)
                try:
                    carousel_canvas.delete(item)
                except:
                    pass
                if on_done:
                    on_done()
                return
            carousel_canvas.itemconfig(item, image=imgs[k])
            root.after(step_ms, lambda: _anim(k + 1))

        _anim(0)

    except Exception as e:
        print("POP_IN ERROR:", ap, e)
        img = load_photo_fit(ap, BIG_W, BIG_H, _img_cache)
        place_slot(slot_key, img, x, y)
        if on_done:
            on_done()


# ----------------------------
# Choice previews
# ----------------------------
def hide_choice_preview(i):
    preview_labels[i].config(image="", text="", bg=BG_COLOR)
    preview_labels[i].image = None


def show_choice_preview(i, choice_key):
    if not story or not scene:
        hide_choice_preview(i)
        return

    choices = scene.get("choices", {})
    if choice_key not in choices:
        hide_choice_preview(i)
        return

    nxt = choices[choice_key][1]
    if nxt not in story:
        preview_labels[i].config(text="NO SCENE", fg="white", bg=BG_COLOR)
        preview_labels[i].image = None
        return

    nxt_scene = story[nxt]
    img_path = load_preview_image_for_scene(nxt_scene)
    if not img_path:
        preview_labels[i].config(text="NO IMAGE", fg="white", bg=BG_COLOR)
        preview_labels[i].image = None
        return

    img = load_photo_fit(img_path, 300, 190, _preview_cache)
    if img:
        preview_labels[i].config(image=img, text="", bg=BG_COLOR)
        preview_labels[i].image = img
    else:
        base = os.path.basename(img_path)
        preview_labels[i].config(text=f"MISSING:\n{base}", fg="white", bg=BG_COLOR, justify="center")
        preview_labels[i].image = None


def refresh_all_previews():
    for idx, k in enumerate(["1", "2", "3"]):
        show_choice_preview(idx, k)


# ----------------------------
# Navigation helpers
# ----------------------------
def disable_choices():
    for b in choice_buttons:
        b.config(state="disabled")


def go_to(scene_id):
    global current

    def _mid():
        global current
        if story and scene_id in story:
            current = scene_id
            load_scene()
        else:
            print("[GO_TO ERROR] missing scene:", scene_id)

    fade_transition(_mid)


# ----------------------------
# Typewriter (APPENDS segments + per-segment hook)
# ----------------------------
def start_typewriter(text, on_done=None, clear_first=True):
    """
    clear_first=True  -> label temizlenir (ilk segment)
    clear_first=False -> label'e yeni segment eklenir (sonunda hepsi görünür)
    """
    global full_text, index, click_count, typing_done, after_segment_hook
    after_segment_hook = on_done

    full_text = text or ""
    index = 0
    click_count = 0
    typing_done = False

    if clear_first:
        story_label.config(text="")
    else:
        cur = story_label.cget("text")
        if cur.strip():
            story_label.config(text=cur + "\n\n")

    disable_choices()
    type_step()


def type_step():
    global index, click_count, typing_done, after_segment_hook
    if index < len(full_text):
        ch = full_text[index]
        story_label.config(text=story_label.cget("text") + ch)
        index += 1

        if not ch.isspace() and ch not in ".!?":
            click_count += 1
            if click_count % 3 == 0:
                soft_click()

        root.after(PUNCT_MS if ch in ".!?" else TYPE_MS, type_step)
        return

    typing_done = True

    if after_segment_hook:
        cb = after_segment_hook
        after_segment_hook = None
        root.after(HOOK_MS, cb)
        return

    show_buttons_for_scene()
    refresh_all_previews()

    if scene and scene.get("end_sound") == "footstep":
        play_steps_loop()


# ----------------------------
# Segmented Scene Flow: img1 -> seg1 -> img2 -> seg2 -> img3 -> rest
# ----------------------------
def play_scene_segment_flow(img_list, seg_list):
    global segments, seg_i
    segments = seg_list[:] if seg_list else [""]
    seg_i = 0

    paths = [p for p in (img_list or []) if p]
    while len(paths) < 3:
        paths.append(None)
    p1, p2, p3 = paths[:3]

    def finish_all():
        show_buttons_for_scene()
        refresh_all_previews()
        if scene and scene.get("end_sound") == "footstep":
            play_steps_loop()

    def write_next_segment():
        global seg_i

        if seg_i >= len(segments):
            finish_all()
            return

        text_part = segments[seg_i]
        seg_i += 1

        def after_this_segment():
            # after seg1 -> img2
            if seg_i == 1:
                # One-shot at exact "||" boundary for first scene (micro-shift)
                if current == "S01_START":
                    root.after(SFX_SHIFT_MS, lambda: play_sfx_once(FOOTSTEP_ONESHOT, volume=0.85))

                if p2:
                    pop_in_to_slot(
                        "C", p2, SLOT_CX, SLOT_Y,
                        duration_ms=POP_MS, frames=POP_FRAMES,
                        on_done=lambda: root.after(POP_DELAY_23, write_next_segment)
                    )
                else:
                    root.after(POP_DELAY_23, write_next_segment)

            # after seg2 -> img3
            elif seg_i == 2:
                if p3:
                    pop_in_to_slot(
                        "R", p3, SLOT_RX, SLOT_Y,
                        duration_ms=POP_MS, frames=POP_FRAMES,
                        on_done=lambda: root.after(POP_DELAY_23, write_next_segment)
                    )
                else:
                    root.after(POP_DELAY_23, write_next_segment)

            else:
                root.after(HOOK_MS, write_next_segment)

        # IMPORTANT: first segment clears, others append
        start_typewriter(text_part, on_done=after_this_segment, clear_first=(seg_i == 1))

    carousel_clear()
    if p1:
        pop_in_to_slot(
            "L", p1, SLOT_LX, SLOT_Y,
            duration_ms=POP_MS, frames=POP_FRAMES,
            on_done=lambda: root.after(POP_DELAY_12, write_next_segment)
        )
    else:
        root.after(POP_DELAY_12, write_next_segment)


# ----------------------------
# Scene logic
# ----------------------------
def load_scene():
    global scene
    scene = story[current]

    if scene.get("final_check") is True:
        mask = 0
        for i, k in enumerate(EVENT_ORDER):
            if events.get(k, False):
                mask |= (1 << i)
        end_id = f"END_F{mask + 1:02d}"
        root.after(450, lambda: go_to(end_id))
        return

    img_list = get_scene_images_list(scene)

    for i in range(3):
        hide_choice_preview(i)

    seg_list = split_text_into_segments(scene.get("text", ""))
    play_scene_segment_flow(img_list, seg_list)


def show_buttons_for_scene():
    if scene.get("ending") is True:
        choice_buttons[0].config(text="Exit", command=lambda: choose("1"), state="normal")
        choice_buttons[1].config(text="", state="disabled")
        choice_buttons[2].config(text="", state="disabled")
        for i in range(3):
            hide_choice_preview(i)
        return

    choices = scene.get("choices", {})
    for i, key in enumerate(["1", "2", "3"]):
        if key in choices:
            txt = choices[key][0]
            choice_buttons[i].config(text=txt, command=lambda k=key: choose(k), state="normal")
        else:
            choice_buttons[i].config(text="", state="disabled")
            hide_choice_preview(i)


def choose(choice_key):
    global current

    if not typing_done:
        return

    if scene.get("ending") is True:
        stop_all_audio()
        root.destroy()
        return

    choices = scene.get("choices", {})
    if choice_key not in choices:
        return

    choice = choices[choice_key]
    flags = choice[2] if (isinstance(choice, (list, tuple)) and len(choice) >= 3) else []
    for f in flags:
        if f in events:
            events[f] = True

    next_id = choice[1]
    if next_id not in story:
        print("[BAD NEXT]", current, choice_key, next_id)
        return

    # Fade transition on scene change
    def _mid():
        global current
        current = next_id
        load_scene()

    fade_transition(_mid)


# ----------------------------
# Language selection
# ----------------------------
def reset_events():
    for k in events:
        events[k] = False


def set_english():
    global story, current
    reset_events()
    story = STORY_EN
    current = "S01_START" if "S01_START" in story else "start"
    fade_transition(load_scene)


def set_turkish():
    global story, current
    reset_events()
    story = STORY_TR
    current = "S01_START" if "S01_START" in story else "start"
    fade_transition(load_scene)


def on_escape(e=None):
    stop_all_audio()
    root.destroy()


# ============================================================
# Audio Settings Overlay (icon button + panel)
# ============================================================
class AudioSettingsOverlay:
    def __init__(self, master, x=18, y=18):
        self.master = master
        self.x = x
        self.y = y
        self.opened = False
        self.last_nonzero = 35 if music_volume_percent == 0 else music_volume_percent

        self.btn = tk.Canvas(master, width=60, height=60,
                             bg=master.cget("bg"),
                             highlightthickness=0, bd=0)
        self.btn.place(x=self.x, y=self.y)

        self.oval_id = self.btn.create_oval(
            3, 3, 55, 55,
            fill="#0f1730", outline="#2a3a6a", width=2, stipple="gray25"
        )

        self.icon_img = None
        self.icon_img_raw = None
        try:
            if os.path.exists(settings_icon_path):
                self.icon_img_raw = tk.PhotoImage(file=settings_icon_path)
                w = self.icon_img_raw.width()
                h = self.icon_img_raw.height()
                factor = max(1, math.ceil(max(w / 40, h / 40)))
                self.icon_img = self.icon_img_raw.subsample(factor, factor)
                self.btn.create_image(30, 30, image=self.icon_img)
            else:
                raise FileNotFoundError(settings_icon_path)
        except Exception as ex:
            print("SETTINGS ICON LOAD ERROR:", ex)
            self.btn.create_text(30, 30, text="⚙", fill="#cfd6ff",
                                 font=("Arial", 14, "bold"))

        def _hover_on(_):
            self.btn.itemconfig(self.oval_id, outline="#4f6cff")

        def _hover_off(_):
            self.btn.itemconfig(self.oval_id, outline="#2a3a6a")

        self.btn.bind("<Enter>", _hover_on)
        self.btn.bind("<Leave>", _hover_off)
        self.btn.bind("<Button-1>", self._on_btn_click)

        self.panel = tk.Frame(master, bg=BG_COLOR, bd=0, highlightthickness=0)

        self.canvas = tk.Canvas(self.panel, width=280, height=96, bg=BG_COLOR,
                                highlightthickness=0, bd=0)
        self.canvas.pack()

        self.canvas.create_rectangle(6, 6, 276, 92, fill="#0f1730",
                                     outline="#2a3a6a", width=2, stipple="gray25")
        self.canvas.create_text(18, 22, text="AUDIO", anchor="w",
                                fill="#cfd6ff", font=("Arial", 10, "bold"))
        self.value_id = self.canvas.create_text(246, 22, text=f"{music_volume_percent}%",
                                                anchor="e", fill="white",
                                                font=("Arial", 10, "bold"))

        self.minus_btn = tk.Button(self.panel, text="–", command=self.vol_down,
                                   bg="#1a2440", fg="white", bd=0,
                                   activebackground="#24335c", activeforeground="white",
                                   font=("Arial", 12, "bold"))
        self.plus_btn = tk.Button(self.panel, text="+", command=self.vol_up,
                                  bg="#1a2440", fg="white", bd=0,
                                  activebackground="#24335c", activeforeground="white",
                                  font=("Arial", 12, "bold"))
        self.mute_btn = tk.Button(self.panel, text="MUTE", command=self.mute_toggle,
                                  bg="#111a33", fg="#cfd6ff", bd=0,
                                  activebackground="#24335c", activeforeground="white",
                                  font=("Arial", 9, "bold"))

        self.scale = tk.Scale(self.panel, from_=0, to=100, orient="horizontal",
                              length=150, showvalue=0, command=self.on_slide,
                              bg="#0f1730", fg="white", troughcolor="#121a30",
                              highlightthickness=0, bd=0)
        self.scale.set(music_volume_percent)

        self.minus_btn.place(x=16, y=42, width=32, height=26)
        self.scale.place(x=54, y=44)
        self.plus_btn.place(x=214, y=42, width=32, height=26)
        self.mute_btn.place(x=16, y=70, width=230, height=20)

        self.master.bind("<Button-1>", self._global_click, add="+")

    def lift(self):
        try:
            self.btn.tkraise()
        except:
            pass
        if self.opened:
            try:
                self.panel.tkraise()
            except:
                pass

    def _update_label(self):
        self.canvas.itemconfig(self.value_id, text=f"{music_volume_percent}%")
        if self.scale.get() != music_volume_percent:
            self.scale.set(music_volume_percent)
        self.mute_btn.config(text="UNMUTE" if music_volume_percent == 0 else "MUTE")

    def open(self):
        if self.opened:
            return
        self.opened = True
        self.panel.place(x=self.x + 46, y=self.y)
        self._update_label()
        self.lift()

    def close(self):
        if not self.opened:
            return
        self.opened = False
        self.panel.place_forget()

    def toggle(self):
        self.close() if self.opened else self.open()

    def _on_btn_click(self, e):
        self.toggle()

    def _global_click(self, e):
        if not self.opened:
            return

        wx, wy = e.x_root, e.y_root

        bx1 = self.btn.winfo_rootx()
        by1 = self.btn.winfo_rooty()
        bx2 = bx1 + self.btn.winfo_width()
        by2 = by1 + self.btn.winfo_height()

        px1 = self.panel.winfo_rootx()
        py1 = self.panel.winfo_rooty()
        px2 = px1 + self.panel.winfo_width()
        py2 = py1 + self.panel.winfo_height()

        inside_btn = (bx1 <= wx <= bx2 and by1 <= wy <= by2)
        inside_panel = (px1 <= wx <= px2 and py1 <= wy <= py2)

        if not inside_btn and not inside_panel:
            self.close()

    def on_slide(self, val):
        set_music_volume_percent(int(float(val)))
        if music_volume_percent > 0:
            self.last_nonzero = music_volume_percent
        self._update_label()

    def vol_down(self):
        self.scale.set(max(0, music_volume_percent - 5))

    def vol_up(self):
        self.scale.set(min(100, music_volume_percent + 5))

    def mute_toggle(self):
        if music_volume_percent > 0:
            self.last_nonzero = music_volume_percent
            self.scale.set(0)
        else:
            self.scale.set(self.last_nonzero if self.last_nonzero > 0 else 35)


# ----------------------------
# Main screen show/hide helpers
# ----------------------------
def show_language_screen():
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    show_logo_on_canvas()

    card.pack(padx=30, pady=(600, 22), fill="x")
    story_label.config(text="Select Language / Dil Seç")

    choice_buttons[0].config(text="English", command=set_english, state="normal")
    choice_buttons[1].config(text="Türkçe", command=set_turkish, state="normal")
    choice_buttons[2].config(text="", state="disabled")

    for i in range(3):
        hide_choice_preview(i)

    audio_ui.lift()


def start_main_after_splash(splash):
    try:
        splash.destroy()
    except:
        pass

    root.deiconify()
    root.attributes("-fullscreen", True)
    root.focus_force()

    show_language_screen()
    play_music_loop()


def show_splash_logo(duration_ms=1400):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg=BG_COLOR)

    logo = load_photo_fit("images/logo.png", 900, 360, _img_cache)

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = 900, 360
    x = (sw - w) // 2
    y = (sh - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    lbl = tk.Label(splash, bg=BG_COLOR)
    lbl.pack(expand=True, fill="both")

    if logo:
        lbl.config(image=logo)
        lbl.image = logo
    else:
        lbl.config(text="02:17", fg="white", font=("Arial", 34, "bold"))

    splash.after(duration_ms, lambda: start_main_after_splash(splash))


# ----------------------------
# Build UI
# ----------------------------
root = tk.Tk()
root.configure(bg=BG_COLOR)
root.title("02:17")
root.withdraw()
root.bind("<Escape>", on_escape)
root.protocol("WM_DELETE_WINDOW", on_escape)

# Fade overlay canvas (guaranteed, no alpha)
fade_canvas = tk.Canvas(root, bg="", highlightthickness=0, bd=0)
fade_canvas.place(x=0, y=0, relwidth=1, relheight=1)
fade_rect = fade_canvas.create_rectangle(0, 0, 99999, 99999, fill="black", outline="black")
_fade_set_level(0)
fade_canvas.lower()

# Keep fade canvas always full-screen on resize
def _on_root_configure(_e):
    try:
        w = root.winfo_width()
        h = root.winfo_height()
        fade_canvas.coords(fade_rect, 0, 0, w, h)
    except:
        pass

root.bind("<Configure>", _on_root_configure)

# Background
bg_img = None
try:
    if PIL_OK and os.path.exists(bg_path):
        im = Image.open(bg_path).convert("RGBA")
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        im = im.resize((sw, sh), Image.LANCZOS)
        bg_img = ImageTk.PhotoImage(im)
    else:
        bg_img = tk.PhotoImage(file=bg_path)
except Exception as e:
    bg_img = None
    print("BG LOAD ERROR:", e)

bg_label = tk.Label(root, image=bg_img, bg=BG_COLOR)
bg_label.image = bg_img

# Top triptych canvas
carousel_canvas = tk.Canvas(root, width=CAROUSEL_W, height=CAROUSEL_H,
                           bg=BG_COLOR, highlightthickness=0, bd=0)
carousel_canvas.place(relx=0.5, y=30, anchor="n")

# Card
card = tk.Frame(root, bg=BG_COLOR, bd=2, relief="groove")

story_label = tk.Label(
    card,
    text="Select Language / Dil Seç",
    font=("Arial", 18),
    wraplength=1400,
    justify="center",
    bg=BG_COLOR,
    fg="white"
)
story_label.pack(padx=22, pady=(18, 16))

choices_row = tk.Frame(card, bg=BG_COLOR)
choices_row.pack(pady=(0, 18))

choice_buttons = []
preview_labels = []

for col, key in enumerate(["1", "2", "3"]):
    cf = tk.Frame(choices_row, bg=BG_COLOR)
    cf.grid(row=0, column=col, padx=64, pady=6, sticky="n")

    btn = tk.Button(
        cf,
        text="",
        width=26,
        height=2,
        bd=0,
        relief="flat",
        bg="#1a2440",
        fg="white",
        activebackground="#24335c",
        activeforeground="white",
        font=("Arial", 13)
    )
    btn.pack(pady=(0, 10))
    choice_buttons.append(btn)

    pl = tk.Label(cf, bg=BG_COLOR)
    pl.pack()
    preview_labels.append(pl)

    btn.bind("<Enter>", lambda e, i=col, k=key: show_choice_preview(i, k))

choice_buttons[0].config(text="", state="disabled")
choice_buttons[1].config(text="", state="disabled")
choice_buttons[2].config(text="", state="disabled")

audio_ui = AudioSettingsOverlay(root, x=18, y=18)

card.lift()
audio_ui.lift()

# Start
show_splash_logo(duration_ms=1400)
root.mainloop()
