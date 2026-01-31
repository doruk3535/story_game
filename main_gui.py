# -*- coding: utf-8 -*-
# main_gui.py (02:17) - SINGLE FILE FINAL (AUDIO FIXED + "TOK TOK" CLICK + GALLERY + BUTTON FRAMES)
# - Splash logo first (root hidden)
# - Then fullscreen main window + language selection
# - Triptych: 3x512 canvas (no shrinking)
# - POP-IN + SEGMENTED FLOW:
#     img1 (LEFT) -> seg1 -> img2 (CENTER) -> seg2 -> img3 (RIGHT) -> rest
#   (Split story text with "||")
# - Segments APPEND (all text remains visible)
# - Music loop (mp3 preferred; auto fallback to wav/ogg) + footsteps ambience loop (wav)
# - Audio settings overlay (music volume)
# - Typewriter text + DEEPER TOK CLICK (in-memory wav) - NO TRAILING
# - Endings Gallery: unlock END_F01..END_F32, save to JSON, view from ending screen
# - Buttons: framed border + hover glow
# - NO PREVIEWS

import tkinter as tk
import os
import math
import time
import io
import wave
import struct
import json

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
# winsound fallback (only if pygame click can't be used)
# ----------------------------
try:
    import winsound
except Exception:
    winsound = None

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bg_path = os.path.join(BASE_DIR, "images", "bg.png")
logo_path = os.path.join(BASE_DIR, "images", "logo.png")
settings_icon_path = os.path.join(BASE_DIR, "images", "settings_icon.png")

MUSIC_LOOP = os.path.join(BASE_DIR, "sounds", "atari_loop.mp3")           # preferred
FOOTSTEPS_LOOP = os.path.join(BASE_DIR, "sounds", "footsteps_loop.wav")   # ambience loop

# Save progress
SAVE_PATH = os.path.join(BASE_DIR, "save_0217.json")
TOTAL_ENDINGS = 32
unlocked_endings = set()

# ----------------------------
# pygame audio (music + ambience + click)
# ----------------------------
PYGAME_OK = True
pygame = None

def _try_init_pygame(buffer_size: int):
    """Try initializing pygame mixer with given buffer size."""
    global pygame
    import pygame as _pg
    _pg.mixer.pre_init(44100, -16, 2, buffer_size)
    _pg.init()
    _pg.mixer.init()
    pygame = _pg

try:
    for buf in (256, 512, 1024):
        try:
            _try_init_pygame(buf)
            print(f"[AUDIO] pygame mixer init OK (buffer={buf})")
            break
        except Exception as e:
            pygame = None
            print(f"[AUDIO] pygame init failed (buffer={buf}): {e}")
    if pygame is None:
        raise RuntimeError("pygame mixer could not be initialized.")
except Exception as e:
    PYGAME_OK = False
    print("[AUDIO] PYGAME INIT ERROR:", e)

music_playing = False
ambient_playing = False

music_volume_percent = 35
music_volume = music_volume_percent / 100.0

steps_sound = None
steps_channel = None

# CLICK via pygame
click_sound = None
click_channel = None

def set_music_volume_percent(percent: int):
    global music_volume, music_volume_percent
    music_volume_percent = max(0, min(100, int(percent)))
    music_volume = music_volume_percent / 100.0
    if PYGAME_OK:
        try:
            pygame.mixer.music.set_volume(music_volume)
        except Exception as e:
            print("[AUDIO] set_volume error:", e)

def _music_candidates(path_mp3: str):
    cands = []
    if path_mp3:
        cands.append(path_mp3)
        root, _ext = os.path.splitext(path_mp3)
        cands.append(root + ".wav")
        cands.append(root + ".ogg")
    seen = set()
    out = []
    for p in cands:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out

def play_music_loop():
    global music_playing
    if not PYGAME_OK:
        print("[AUDIO] pygame yok -> müzik çalamam.")
        return
    if music_playing:
        return

    candidates = _music_candidates(MUSIC_LOOP)
    chosen = None
    for p in candidates:
        if os.path.exists(p):
            chosen = p
            break

    if not chosen:
        print("[AUDIO] MUSIC MISSING. Tried:", candidates)
        return

    try:
        pygame.mixer.music.load(chosen)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        music_playing = True
        print("[AUDIO] Music playing:", os.path.basename(chosen))
    except Exception as e:
        print("[AUDIO] MUSIC PLAY ERROR:", e)
        music_playing = False

def stop_music():
    global music_playing
    if not PYGAME_OK:
        return
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print("[AUDIO] stop_music error:", e)
    music_playing = False

def play_steps_loop():
    global ambient_playing, steps_sound, steps_channel
    if not PYGAME_OK:
        return
    if ambient_playing:
        return
    if not os.path.exists(FOOTSTEPS_LOOP):
        print("[AUDIO] FOOTSTEPS MISSING:", FOOTSTEPS_LOOP)
        return
    try:
        if steps_sound is None:
            steps_sound = pygame.mixer.Sound(FOOTSTEPS_LOOP)
        if steps_channel is None:
            steps_channel = pygame.mixer.Channel(1)
        steps_channel.set_volume(0.45)
        steps_channel.play(steps_sound, loops=-1)
        ambient_playing = True
        print("[AUDIO] Footsteps loop started.")
    except Exception as e:
        print("[AUDIO] FOOTSTEPS PLAY ERROR:", e)

def stop_steps_loop():
    global ambient_playing, steps_channel
    if not PYGAME_OK:
        return
    try:
        if steps_channel:
            steps_channel.stop()
    except Exception as e:
        print("[AUDIO] stop_steps_loop error:", e)
    ambient_playing = False

# ============================================================
# CLICK ENGINE (NO FILE) - "TOK TOK" SOUND
# Primary: pygame (reliable while music plays)
# Fallback: winsound (if pygame not available)
# ============================================================

# --- TUNING: "TOK TOK" mechanical keyboard feel ---
# NOTE: Very low freq + very long duration feels "hum". This preset is "tok" without sounding like a beep.
CLICK_EVERY = 2
CLICK_MIN_GAP = 0.012
CLICK_GAIN = 0.95
CLICK_DUR_MS = 52         # tok needs tail; avoid 100-140ms (too long -> hum)
CLICK_FREQ_HZ = 900       # attack brightness reference (body is derived lower)

_last_click_t = 0.0
_CLICK_WAV_BYTES = None

def _build_click_wav_bytes_16bit(duration_ms=CLICK_DUR_MS, freq_hz=CLICK_FREQ_HZ, gain=CLICK_GAIN):
    """Thick keyboard click: small attack + dominant low body + tiny noise."""
    import random

    sr = 44100
    n = max(1, int(sr * (duration_ms / 1000.0)))

    g = max(0.0, min(1.0, float(gain)))
    max_amp = int(32767 * g)

    attack_ms = 5
    attack_n = max(1, int(sr * attack_ms / 1000.0))

    # BODY is where "tok" lives
    body_freq = max(180, int(freq_hz * 0.33))   # ~300Hz
    noise_amt = 0.06

    frames = bytearray()

    for i in range(n):
        t = i / sr

        # envelope: quick drop then long-ish tail
        if i < attack_n:
            env = 1.0 - (i / attack_n)
        else:
            tail_i = i - attack_n
            tail_n = max(1, n - attack_n)
            env = 0.70 * (1.0 - (tail_i / tail_n))

        # small attack (click)
        if i < attack_n:
            a = 1.0 if (math.sin(2 * math.pi * (freq_hz * 2.0) * t) >= 0) else -1.0
            attack = 0.35 * a
        else:
            attack = 0.0

        # dominant body (thock)
        b = math.sin(2 * math.pi * body_freq * t)
        body = 0.95 * b

        noise = noise_amt * (random.random() * 2.0 - 1.0)

        sample = (attack + body + noise) * env
        v = int(max_amp * sample)

        if v > 32767:
            v = 32767
        elif v < -32768:
            v = -32768

        frames += struct.pack("<h", v)

    bio = io.BytesIO()
    with wave.open(bio, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(bytes(frames))
    return bio.getvalue()

def _ensure_click_assets():
    global _CLICK_WAV_BYTES, click_sound, click_channel
    if _CLICK_WAV_BYTES is None:
        _CLICK_WAV_BYTES = _build_click_wav_bytes_16bit()

    if PYGAME_OK and click_sound is None:
        try:
            click_sound = pygame.mixer.Sound(file=io.BytesIO(_CLICK_WAV_BYTES))
            click_sound.set_volume(0.80)
            click_channel = pygame.mixer.Channel(2)
            click_channel.set_volume(1.0)
            print("[AUDIO] Click sound ready (pygame) - TOK mode")
        except Exception as e:
            click_sound = None
            click_channel = None
            print("[AUDIO] Click init failed (pygame):", e)

def stop_clicks():
    # stop click immediately (no trailing)
    if PYGAME_OK and click_channel:
        try:
            click_channel.stop()
        except:
            pass
    if winsound:
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except:
            pass

def soft_click():
    global _last_click_t
    now = time.perf_counter()
    if (now - _last_click_t) < CLICK_MIN_GAP:
        return
    _last_click_t = now

    _ensure_click_assets()

    # Primary: pygame click (reliable)
    if PYGAME_OK and click_sound and click_channel:
        try:
            click_channel.stop()  # kill previous click (no queue)
            click_channel.play(click_sound)
            return
        except:
            pass

    # Fallback: winsound (rare)
    if winsound and _CLICK_WAV_BYTES:
        try:
            winsound.PlaySound(_CLICK_WAV_BYTES, winsound.SND_MEMORY | winsound.SND_ASYNC)
        except:
            pass

def stop_all_audio():
    stop_clicks()
    stop_steps_loop()
    stop_music()
    if PYGAME_OK:
        try:
            pygame.mixer.quit()
        except:
            pass

# ----------------------------
# Save / Load progress
# ----------------------------
def load_progress():
    global unlocked_endings
    try:
        if os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            unlocked_endings = set(data.get("unlocked_endings", []))
        else:
            unlocked_endings = set()
    except Exception as e:
        print("[SAVE] load error:", e)
        unlocked_endings = set()

def save_progress():
    try:
        data = {
            "unlocked_endings": sorted(list(unlocked_endings))
        }
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[SAVE] save error:", e)

def unlock_if_ending(scene_id: str):
    if not scene_id:
        return
    sid = str(scene_id)
    if sid.startswith("END_"):
        if sid not in unlocked_endings:
            unlocked_endings.add(sid)
            save_progress()

# ----------------------------
# Global UI / Game state
# ----------------------------
BG_COLOR = "#0b0f1a"

story = None
current = "start"
scene = None
current_lang = None  # "EN" or "TR"

events = {"O1": False, "O2": False, "O3": False, "O4": False, "O5": False}
EVENT_ORDER = ["O1", "O2", "O3", "O4", "O5"]

# Typewriter state
full_text = ""
index = 0
click_count = 0
typing_done = True

# Segmented flow state
segments = []
seg_i = 0
after_segment_hook = None

# Image caches
_img_cache = {}

# ----------------------------
# Triptych canvas layout (3 x 512)
# ----------------------------
IMG_W = 512
IMG_H = 512
GAP = 16

CAROUSEL_W = (IMG_W * 3) + (GAP * 2)
CAROUSEL_H = IMG_H

SLOT_Y = CAROUSEL_H // 2
SLOT_LX = (IMG_W // 2)
SLOT_CX = SLOT_LX + IMG_W + GAP
SLOT_RX = SLOT_CX + IMG_W + GAP

BIG_W, BIG_H = IMG_W, IMG_H

# ----------------------------
# SPEED TUNING
# ----------------------------
POP_MS = 360
POP_FRAMES = 14
POP_DELAY_12 = 140
POP_DELAY_23 = 170

TYPE_MS = 22
PUNCT_MS = 260
HOOK_MS = 110

# Carousel state
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
choice_borders = []  # NEW: frames around buttons
audio_ui = None

# ----------------------------
# Utility
# ----------------------------
def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)

def load_photo_fit(path, target_w, target_h, cache_dict):
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
    if not scn:
        return []
    imgs = scn.get("images", None)
    if imgs is None:
        single = scn.get("image")
        return [single] if single else []
    if isinstance(imgs, (list, tuple)):
        return [p for p in imgs if p]
    return []

def split_text_into_segments(txt: str):
    if not txt:
        return [""]
    if "||" in txt:
        parts = [p.strip() for p in txt.split("||")]
        parts = [p for p in parts if p != ""]
        return parts if parts else [""]
    return [txt]

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
            fill="white", font=("Segoe UI Semibold", 18, "bold")
        )

def pop_in_to_slot(slot_key, path, x, y, duration_ms=POP_MS, frames=POP_FRAMES, on_done=None):
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

        frames_list = []
        for i in range(frames):
            t = (i + 1) / frames
            s = start_s + (end_s - start_s) * t
            nw = max(1, int(tw * s))
            nh = max(1, int(th * s))
            fr = base.resize((nw, nh), Image.LANCZOS)
            frames_list.append(ImageTk.PhotoImage(fr))

        item = carousel_canvas.create_image(x, y, image=frames_list[0])

        tmp_refs[f"pop_{slot_key}_frames"] = frames_list
        tmp_refs[f"pop_{slot_key}_item"] = item

        step_ms = max(10, int(duration_ms / max(1, frames)))

        def _anim(k=0):
            if k >= frames:
                place_slot(slot_key, frames_list[-1], x, y)
                try:
                    carousel_canvas.delete(item)
                except:
                    pass
                if on_done:
                    on_done()
                return
            carousel_canvas.itemconfig(item, image=frames_list[k])
            root.after(step_ms, lambda: _anim(k + 1))

        _anim(0)

    except Exception as e:
        print("POP_IN ERROR:", ap, e)
        img = load_photo_fit(ap, BIG_W, BIG_H, _img_cache)
        place_slot(slot_key, img, x, y)
        if on_done:
            on_done()

# ----------------------------
# Button border hover (NEW)
# ----------------------------
BORDER_OFF = "#2a3a6a"
BORDER_ON = "#4f6cff"

def bind_border_hover(btn, border_frame):
    def on(_e=None):
        try:
            border_frame.config(bg=BORDER_ON)
        except:
            pass
    def off(_e=None):
        try:
            border_frame.config(bg=BORDER_OFF)
        except:
            pass
    btn.bind("<Enter>", on)
    btn.bind("<Leave>", off)

def set_border_active(i, active: bool):
    # optional helper if you later want to indicate selected/locked
    try:
        choice_borders[i].config(bg=BORDER_ON if active else BORDER_OFF)
    except:
        pass

# ----------------------------
# Navigation helpers
# ----------------------------
def disable_choices():
    for b in choice_buttons:
        b.config(state="disabled")

def go_to(scene_id):
    global current
    stop_clicks()
    if story and scene_id in story:
        current = scene_id
        load_scene()
    else:
        print("[GO_TO ERROR] missing scene:", scene_id)

# ----------------------------
# Typewriter (APPENDS segments + per-segment hook)
# - "tok tok": every 2 letters
# - NO TRAILING: stop_clicks() when typing ends
# ----------------------------
def start_typewriter(text, on_done=None, clear_first=True):
    global full_text, index, click_count, typing_done, after_segment_hook
    after_segment_hook = on_done

    full_text = text or ""
    index = 0
    click_count = 0
    typing_done = False

    stop_clicks()  # hard cut anything from previous segment

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

        # click only on letters/numbers (no spaces/punct)
        if (not ch.isspace()) and (ch not in ".!?," ):
            click_count += 1
            if click_count % CLICK_EVERY == 0:
                soft_click()

        story_label.config(text=story_label.cget("text") + ch)
        index += 1

        root.after(PUNCT_MS if ch in ".!?" else TYPE_MS, type_step)
        return

    typing_done = True
    stop_clicks()  # MUST stop exactly when finished

    if after_segment_hook:
        cb = after_segment_hook
        after_segment_hook = None
        root.after(HOOK_MS, cb)
        return

    show_buttons_for_scene()

    # ambience trigger
    if scene and scene.get("end_sound") == "footstep":
        play_steps_loop()

# ----------------------------
# Segmented Scene Flow
# img1(L) -> seg1 -> img2(C) -> seg2 -> img3(R) -> rest
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
            if seg_i == 1:
                if p2:
                    pop_in_to_slot("C", p2, SLOT_CX, SLOT_Y,
                                   duration_ms=POP_MS, frames=POP_FRAMES,
                                   on_done=lambda: root.after(POP_DELAY_23, write_next_segment))
                else:
                    root.after(POP_DELAY_23, write_next_segment)

            elif seg_i == 2:
                if p3:
                    pop_in_to_slot("R", p3, SLOT_RX, SLOT_Y,
                                   duration_ms=POP_MS, frames=POP_FRAMES,
                                   on_done=lambda: root.after(POP_DELAY_23, write_next_segment))
                else:
                    root.after(POP_DELAY_23, write_next_segment)
            else:
                root.after(HOOK_MS, write_next_segment)

        start_typewriter(text_part, on_done=after_this_segment, clear_first=(seg_i == 1))

    carousel_clear()

    if p1:
        pop_in_to_slot("L", p1, SLOT_LX, SLOT_Y,
                       duration_ms=POP_MS, frames=POP_FRAMES,
                       on_done=lambda: root.after(POP_DELAY_12, write_next_segment))
    else:
        root.after(POP_DELAY_12, write_next_segment)

# ----------------------------
# Scene logic
# ----------------------------
def load_scene():
    global scene
    stop_clicks()
    scene = story[current]

    # unlock ending if applicable
    unlock_if_ending(current)

    if scene.get("final_check") is True:
        mask = 0
        for i, k in enumerate(EVENT_ORDER):
            if events.get(k, False):
                mask |= (1 << i)
        end_id = f"END_F{mask + 1:02d}"
        root.after(450, lambda: go_to(end_id))
        return

    img_list = get_scene_images_list(scene)
    seg_list = split_text_into_segments(scene.get("text", ""))

    play_scene_segment_flow(img_list, seg_list)

def show_buttons_for_scene():
    # ending screen => Replay / Gallery / Exit
    if scene.get("ending") is True:
        # Replay: restart from first scene in current language
        def _replay():
            stop_clicks()
            stop_steps_loop()
            # keep music on
            if story and "S01_START" in story:
                go_to("S01_START")
            else:
                # fallback: go back to language selection
                show_language_screen()

        choice_buttons[0].config(text="Replay", command=_replay, state="normal")
        choice_buttons[1].config(text="Gallery", command=show_gallery, state="normal")
        choice_buttons[2].config(text="Exit", command=on_escape, state="normal")
        return

    choices = scene.get("choices", {})
    for i, key in enumerate(["1", "2", "3"]):
        if key in choices:
            txt = choices[key][0]
            choice_buttons[i].config(text=txt, command=lambda k=key: choose(k), state="normal")
        else:
            choice_buttons[i].config(text="", state="disabled")

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

    current = next_id
    load_scene()

# ----------------------------
# Endings Gallery (NEW)
# ----------------------------
def show_gallery():
    win = tk.Toplevel(root)
    win.title("Endings Gallery")
    win.configure(bg=BG_COLOR)
    win.transient(root)
    win.grab_set()

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = 760, 520
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    unlocked = len(unlocked_endings)

    title = tk.Label(
        win,
        text=f"Unlocked: {unlocked}/{TOTAL_ENDINGS}",
        bg=BG_COLOR, fg="white",
        font=("Segoe UI Semibold", 16, "bold")
    )
    title.pack(pady=(16, 10))

    info = tk.Label(
        win,
        text="✅ unlocked   🔒 locked",
        bg=BG_COLOR, fg="#cfd6ff",
        font=("Segoe UI Semibold", 10, "bold")
    )
    info.pack(pady=(0, 10))

    lst = tk.Listbox(
        win,
        bg="#0f1730",
        fg="white",
        font=("Consolas", 12),
        bd=0,
        highlightthickness=2,
        highlightbackground="#2a3a6a",
        selectbackground="#24335c",
        activestyle="none"
    )
    lst.pack(fill="both", expand=True, padx=18, pady=10)

    for i in range(1, TOTAL_ENDINGS + 1):
        eid = f"END_F{i:02d}"
        mark = "✅" if eid in unlocked_endings else "🔒"
        lst.insert("end", f"{mark}  {eid}")

    btns = tk.Frame(win, bg=BG_COLOR)
    btns.pack(pady=12)

    def _close():
        try:
            win.grab_release()
        except:
            pass
        win.destroy()

    tk.Button(
        btns, text="Close",
        command=_close,
        bg="#1a2440", fg="white",
        bd=0, padx=18, pady=8,
        activebackground="#24335c",
        activeforeground="white",
        font=("Segoe UI Semibold", 11, "bold")
    ).pack()

# ----------------------------
# Language selection
# ----------------------------
def reset_events():
    for k in events:
        events[k] = False

def set_english():
    global story, current, current_lang
    reset_events()
    current_lang = "EN"
    story = STORY_EN
    current = "S01_START" if "S01_START" in story else "start"
    load_scene()

def set_turkish():
    global story, current, current_lang
    reset_events()
    current_lang = "TR"
    story = STORY_TR
    current = "S01_START" if "S01_START" in story else "start"
    load_scene()

def on_escape(e=None):
    stop_all_audio()
    root.destroy()

# ============================================================
# Audio Settings Overlay (music volume)
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
                                 font=("Segoe UI Semibold", 14, "bold"))

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
                                fill="#cfd6ff", font=("Segoe UI Semibold", 10, "bold"))
        self.value_id = self.canvas.create_text(246, 22, text=f"{music_volume_percent}%",
                                                anchor="e", fill="white",
                                                font=("Segoe UI Semibold", 10, "bold"))

        self.minus_btn = tk.Button(self.panel, text="–", command=self.vol_down,
                                   bg="#1a2440", fg="white", bd=0,
                                   activebackground="#24335c", activeforeground="white",
                                   font=("Segoe UI Semibold", 12, "bold"))
        self.plus_btn = tk.Button(self.panel, text="+", command=self.vol_up,
                                  bg="#1a2440", fg="white", bd=0,
                                  activebackground="#24335c", activeforeground="white",
                                  font=("Segoe UI Semibold", 12, "bold"))
        self.mute_btn = tk.Button(self.panel, text="MUTE", command=self.mute_toggle,
                                  bg="#111a33", fg="#cfd6ff", bd=0,
                                  activebackground="#24335c", activeforeground="white",
                                  font=("Segoe UI Semibold", 9, "bold"))

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

    def _on_btn_click(self, _e):
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
    # reset story selection state visually
    stop_clicks()
    stop_steps_loop()

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    show_logo_on_canvas()

    card.pack(padx=30, pady=(600, 22), fill="x")
    story_label.config(text="Select Language / Dil Seç")

    choice_buttons[0].config(text="English", command=set_english, state="normal")
    choice_buttons[1].config(text="Türkçe", command=set_turkish, state="normal")
    choice_buttons[2].config(text="", state="disabled")

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
        lbl.config(text="02:17", fg="white", font=("Segoe UI Semibold", 34, "bold"))

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

# Load progress early
load_progress()

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

# Triptych canvas
carousel_canvas = tk.Canvas(root, width=CAROUSEL_W, height=CAROUSEL_H,
                            bg=BG_COLOR, highlightthickness=0, bd=0)
carousel_canvas.place(relx=0.5, y=30, anchor="n")

# Card
card = tk.Frame(root, bg=BG_COLOR, bd=2, relief="groove")

story_label = tk.Label(
    card,
    text="Select Language / Dil Seç",
    font=("Segoe UI Semibold", 18),
    wraplength=1400,
    justify="center",
    bg=BG_COLOR,
    fg="white"
)
story_label.pack(padx=22, pady=(18, 16))

choices_row = tk.Frame(card, bg=BG_COLOR)
choices_row.pack(pady=(0, 18))

choice_buttons = []
choice_borders = []

for _i in range(3):
    cf = tk.Frame(choices_row, bg=BG_COLOR)
    cf.pack(side="left", padx=64)

    # NEW: border frame around the button
    border = tk.Frame(cf, bg=BORDER_OFF)
    border.pack(pady=(0, 10))
    choice_borders.append(border)

    btn = tk.Button(
        border,
        text="",
        width=24,
        height=1,
        bd=0,
        relief="flat",
        bg="#1a2440",
        fg="white",
        activebackground="#24335c",
        activeforeground="white",
        font=("Segoe UI Semibold", 16)   # ✅ sadece burası büyüdü (13 -> 18)
    )
    btn.pack(padx=2, pady=2)  # padding = border thickness
    choice_buttons.append(btn)

    bind_border_hover(btn, border)

# Init buttons
choice_buttons[0].config(text="", state="disabled")
choice_buttons[1].config(text="", state="disabled")
choice_buttons[2].config(text="", state="disabled")

audio_ui = AudioSettingsOverlay(root, x=18, y=18)

card.lift()
audio_ui.lift()

# Ensure click assets ready early (optional)
try:
    _ensure_click_assets()
except:
    pass

# Start
show_splash_logo(duration_ms=1400)
root.mainloop()
