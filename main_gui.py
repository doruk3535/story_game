# -*- coding: utf-8 -*-
# main_gui.py (02:17) - FINAL (MP3 music + footsteps + icon settings toggle)

import tkinter as tk
import os
import math

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

bg_path   = os.path.join(BASE_DIR, "images", "bg.png")
logo_path = os.path.join(BASE_DIR, "images", "logo.png")

# --- NEW: settings icon ---
settings_icon_path = os.path.join(BASE_DIR, "images", "settings_icon.png")

MUSIC_LOOP     = os.path.join(BASE_DIR, "sounds", "atari_loop.mp3")
FOOTSTEPS_LOOP = os.path.join(BASE_DIR, "sounds", "footsteps_loop.wav")

# ----------------------------
# pygame audio (music + ambience)
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

music_volume_percent = 35  # 0..100
music_volume = music_volume_percent / 100.0

steps_sound = None
steps_channel = None

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

def stop_all_audio():
    stop_steps_loop()
    stop_music()
    if PYGAME_OK:
        try:
            pygame.mixer.quit()
        except:
            pass

# ----------------------------
# Game state
# ----------------------------
story = None
current = "start"
scene = None

events = {"O1": False, "O2": False, "O3": False, "O4": False, "O5": False}
EVENT_ORDER = ["O1", "O2", "O3", "O4", "O5"]

# ----------------------------
# Typewriter state
# ----------------------------
full_text = ""
index = 0
click_count = 0
typing_done = True

# ----------------------------
# Image caches
# ----------------------------
_img_cache = {}
_preview_cache = {}
logo_img = None
bg_img = None
scene_img = None

# ----------------------------
# Utilities
# ----------------------------
def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)

def load_scaled_photo(path, max_w, max_h, cache_dict):
    if not path:
        return None
    ap = abs_path(path)
    if ap in cache_dict:
        return cache_dict[ap]
    if not os.path.exists(ap):
        cache_dict[ap] = None
        return None

    try:
        img_raw = tk.PhotoImage(file=ap)
        w, h = img_raw.width(), img_raw.height()
        scale = max(w / max_w, h / max_h)
        factor = max(1, math.ceil(scale))
        img = img_raw.subsample(factor, factor) if factor > 1 else img_raw
        cache_dict[ap] = img
        return img
    except Exception as e:
        print("IMAGE LOAD ERROR:", ap, e)
        cache_dict[ap] = None
        return None

def show_logo():
    global logo_img
    logo_img = load_scaled_photo(logo_path, 1600, 550, _img_cache)
    if logo_img:
        top_image_label.config(image=logo_img, text="")
        top_image_label.image = logo_img
    else:
        top_image_label.config(image="", text="LOGO LOAD ERROR", fg="white", font=("Arial", 16))
        top_image_label.image = None

def show_scene_image():
    global scene_img
    if not scene:
        return
    img_path = scene.get("image")
    if not img_path:
        top_image_label.config(image="", text="")
        top_image_label.image = None
        return

    scene_img = load_scaled_photo(img_path, 1050, 340, _img_cache)
    if scene_img:
        top_image_label.config(image=scene_img, text="")
        top_image_label.image = scene_img
    else:
        top_image_label.config(image="", text="IMAGE MISSING", fg="white", font=("Arial", 14))
        top_image_label.image = None

def hide_choice_preview(i):
    preview_labels[i].config(image="", text="", bg="#0b0f1a")
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
        preview_labels[i].config(text="NO SCENE", fg="white", bg="#0b0f1a")
        preview_labels[i].image = None
        return

    nxt_scene = story[nxt]
    img_path = nxt_scene.get("image")
    if not img_path:
        preview_labels[i].config(text="NO IMAGE", fg="white", bg="#0b0f1a")
        preview_labels[i].image = None
        return

    img = load_scaled_photo(img_path, 300, 190, _preview_cache)
    if img:
        preview_labels[i].config(image=img, text="", bg="#0b0f1a")
        preview_labels[i].image = img
    else:
        base = os.path.basename(img_path)
        preview_labels[i].config(text=f"MISSING:\n{base}", fg="white", bg="#0b0f1a", justify="center")
        preview_labels[i].image = None

def refresh_all_previews():
    for idx, k in enumerate(["1", "2", "3"]):
        show_choice_preview(idx, k)

def disable_choices():
    for b in choice_buttons:
        b.config(state="disabled")

def go_to(scene_id):
    global current
    if story and scene_id in story:
        current = scene_id
        load_scene()
    else:
        print("[GO_TO ERROR] missing scene:", scene_id)

# ----------------------------
# Typewriter
# ----------------------------
def start_typewriter(text):
    global full_text, index, click_count, typing_done
    full_text = text or ""
    index = 0
    click_count = 0
    typing_done = False
    story_label.config(text="")
    disable_choices()
    type_step()

def type_step():
    global index, click_count, typing_done
    if index < len(full_text):
        ch = full_text[index]
        story_label.config(text=story_label.cget("text") + ch)
        index += 1

        if not ch.isspace() and ch not in ".!?":
            click_count += 1
            if click_count % 3 == 0:
                soft_click()

        root.after(220 if ch in ".!?" else 20, type_step)
        return

    typing_done = True
    show_buttons_for_scene()
    refresh_all_previews()

    if scene and scene.get("end_sound") == "footstep":
        play_steps_loop()

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
        end_id = f"END_F{mask+1:02d}"
        root.after(450, lambda: go_to(end_id))
        return

    show_scene_image()
    for i in range(3):
        hide_choice_preview(i)
    start_typewriter(scene.get("text", ""))

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

    current = next_id
    load_scene()

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
    load_scene()

def set_turkish():
    global story, current
    reset_events()
    story = STORY_TR
    current = "S01_START" if "S01_START" in story else "start"
    load_scene()

def on_escape(e=None):
    stop_all_audio()
    root.destroy()

# ============================================================
# Settings-toggle Audio UI (icon button + collapsible panel)
# ============================================================
class AudioSettingsOverlay:
    def __init__(self, master, x=18, y=18):
        self.master = master
        self.x = x
        self.y = y
        self.opened = False
        self.last_nonzero = 35 if music_volume_percent == 0 else music_volume_percent

        # settings button (always visible)
        self.btn = tk.Canvas(master, width=60, height=60,
                     bg=master.cget("bg"),
                     highlightthickness=0, bd=0)
        self.btn.place(x=self.x, y=self.y)

        self.oval_id = self.btn.create_oval(
            3, 3, 55, 55,
            fill="#0f1730", outline="#2a3a6a", width=2, stipple="gray25"
        )

        # --- load icon (keep reference!) ---
        self.icon_img = None
        self.icon_img_raw = None
        try:
            if os.path.exists(settings_icon_path):
                self.icon_img_raw = tk.PhotoImage(file=settings_icon_path)
                w = self.icon_img_raw.width()
                h = self.icon_img_raw.height()
                factor = max(1, math.ceil(max(w / 40, h / 40)))
                self.icon_img = self.icon_img_raw.subsample(factor, factor)
                self.icon_id = self.btn.create_image(30, 30, image=self.icon_img)
            else:
                raise FileNotFoundError(settings_icon_path)
        except Exception as ex:
            print("SETTINGS ICON LOAD ERROR:", ex)
            self.icon_id = self.btn.create_text(20, 20, text="⚙", fill="#cfd6ff",
                                                font=("Arial", 14, "bold"))

        def _hover_on(_):
            self.btn.itemconfig(self.oval_id, outline="#4f6cff")
        def _hover_off(_):
            self.btn.itemconfig(self.oval_id, outline="#2a3a6a")

        self.btn.bind("<Enter>", _hover_on)
        self.btn.bind("<Leave>", _hover_off)
        self.btn.bind("<Button-1>", self._on_btn_click)

        # panel (hidden)
        self.panel = tk.Frame(master, bg="#0b0f1a", bd=0, highlightthickness=0)

        self.canvas = tk.Canvas(self.panel, width=280, height=96, bg="#0b0f1a",
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
        # IMPORTANT: tkraise() is safe for Canvas
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

        if music_volume_percent == 0:
            self.mute_btn.config(text="UNMUTE")
        else:
            self.mute_btn.config(text="MUTE")

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
        if self.opened:
            self.close()
        else:
            self.open()

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
# UI
# ----------------------------
root = tk.Tk()
root.configure(bg="#0b0f1a")
root.title("02:17")
root.attributes("-fullscreen", True)
root.bind("<Escape>", on_escape)
root.protocol("WM_DELETE_WINDOW", on_escape)

audio_ui = AudioSettingsOverlay(root, x=18, y=18)

# Background
try:
    bg_img = tk.PhotoImage(file=bg_path)
except Exception as e:
    bg_img = None
    print("BG LOAD ERROR:", e)

bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_img

# Top image area
top_image_label = tk.Label(root, bd=0, highlightthickness=0, bg="#0b0f1a")
top_image_label.place(relx=0.5, rely=0.05, anchor="n")

# Card panel
card = tk.Frame(root, bg="#0b0f1a", bd=2, relief="groove")
card.pack(padx=30, pady=(600, 22), fill="x")

story_label = tk.Label(
    card,
    text="Select Language / Dil Seç",
    font=("Arial", 18),
    wraplength=1400,
    justify="center",
    bg="#0b0f1a",
    fg="white"
)
story_label.pack(padx=22, pady=(18, 16))

# Choices row
choices_row = tk.Frame(card, bg="#0b0f1a")
choices_row.pack(pady=(0, 18))

choice_buttons = []
preview_labels = []

for col, key in enumerate(["1", "2", "3"]):
    cf = tk.Frame(choices_row, bg="#0b0f1a")
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

    pl = tk.Label(cf, bg="#0b0f1a")
    pl.pack()
    preview_labels.append(pl)

    btn.bind("<Enter>", lambda e, i=col, k=key: show_choice_preview(i, k))

# Initial language buttons
choice_buttons[0].config(text="English", command=set_english, state="normal")
choice_buttons[1].config(text="Türkçe", command=set_turkish, state="normal")
choice_buttons[2].config(text="", state="disabled")

# Layering
bg_label.lower()
card.lift()
top_image_label.lift()
audio_ui.lift()

# Start
show_logo()
play_music_loop()

root.mainloop()
