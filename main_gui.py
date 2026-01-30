# main.py  (02:17)
import tkinter as tk
import os
import math

# ----------------------------
# Import story (robust)
# ----------------------------
try:
    # if you renamed to story_en / story_tr
    from game_story import story_en as STORY_EN, story_tr as STORY_TR
except Exception:
    # default names in your file
    from game_story import STORY_EN, STORY_TR

# ---- sound (windows only) ----
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

# optional ambience (put your wav here)
FOOTSTEPS_LOOP = os.path.join(BASE_DIR, "sounds", "footsteps_loop.wav")

# ----------------------------
# Game state
# ----------------------------
story = None
current = "start"
scene = None

# ---- event state ----
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
_img_cache = {}      # scaled images
_preview_cache = {}  # preview images
logo_img = None
bg_img = None
scene_img = None

# ----------------------------
# Ambience state
# ----------------------------
ambient_playing = False

def play_steps_loop():
    """Loop footsteps ambience (Windows+WAV)."""
    global ambient_playing
    if not winsound:
        return
    if ambient_playing:
        return
    if os.path.exists(FOOTSTEPS_LOOP):
        ambient_playing = True
        winsound.PlaySound(FOOTSTEPS_LOOP, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_steps_loop():
    global ambient_playing
    if not winsound:
        return
    if ambient_playing:
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except:
            pass
        ambient_playing = False

# ----------------------------
# Utilities
# ----------------------------
def load_scaled_photo(path, max_w, max_h, cache_dict):
    """
    Tkinter PhotoImage ile ölçekli yükleme (PIL yok).
    subsample sadece küçültür.
    """
    if not path:
        return None

    abs_path = path if os.path.isabs(path) else os.path.join(BASE_DIR, path)

    if abs_path in cache_dict:
        return cache_dict[abs_path]

    if not os.path.exists(abs_path):
        cache_dict[abs_path] = None
        return None

    try:
        img_raw = tk.PhotoImage(file=abs_path)
        w, h = img_raw.width(), img_raw.height()

        scale = max(w / max_w, h / max_h)
        factor = max(1, math.ceil(scale))
        img = img_raw.subsample(factor, factor) if factor > 1 else img_raw

        cache_dict[abs_path] = img
        return img
    except Exception as e:
        print("IMAGE LOAD ERROR:", abs_path, e)
        cache_dict[abs_path] = None
        return None

def show_logo():
    global logo_img
    logo_img = load_scaled_photo(logo_path, max_w=1600, max_h=550, cache_dict=_img_cache)
    if logo_img:
        top_image_label.config(image=logo_img, text="")
        top_image_label.image = logo_img
    else:
        top_image_label.config(image="", text="LOGO LOAD ERROR", fg="white", font=("Arial", 16))
        top_image_label.image = None

def show_scene_image():
    """Show current scene image in the top area."""
    global scene_img
    if not scene:
        return

    img_path = scene.get("image")
    if not img_path:
        top_image_label.config(image="", text="")
        top_image_label.image = None
        return

    scene_img = load_scaled_photo(img_path, max_w=1050, max_h=340, cache_dict=_img_cache)
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
    """Preview = next scene image (under the button)."""
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

    img = load_scaled_photo(img_path, max_w=300, max_h=190, cache_dict=_preview_cache)
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

def enable_choices():
    for b in choice_buttons:
        if b.cget("text").strip():
            b.config(state="normal")

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
    full_text = text
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

        # click sound every few characters (not spaces/punctuation)
        if not ch.isspace() and ch not in ".!?":
            click_count += 1
            if click_count % 3 == 0:
                soft_click()

        # small pause after punctuation
        if ch in ".!?":
            root.after(220, type_step)
        else:
            root.after(20, type_step)
    else:
        typing_done = True
        show_buttons_for_scene()
        refresh_all_previews()

        # scene-based end sound (e.g., first scene ends -> start footsteps)
        if scene.get("end_sound") == "footstep":
            play_steps_loop()

# ----------------------------
# Scene loading / logic
# ----------------------------
def load_scene():
    global scene
    scene = story[current]

    # FINAL_CHECK: auto route to END_Fxx based on events
    if scene.get("final_check") is True:
        mask = 0
        for i, k in enumerate(EVENT_ORDER):
            if events.get(k, False):
                mask |= (1 << i)

        end_id = f"END_F{mask+1:02d}"
        root.after(450, lambda: go_to(end_id))
        return

    # show top image (logo disappears once game starts)
    show_scene_image()

    # clear previews while typing (optional)
    for i in range(3):
        hide_choice_preview(i)

    start_typewriter(scene.get("text", ""))

def show_buttons_for_scene():
    # Ending scene -> show only Exit
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
            btn_text = choices[key][0]
            choice_buttons[i].config(text=btn_text, command=lambda k=key: choose(k), state="normal")
        else:
            choice_buttons[i].config(text="", state="disabled")
            hide_choice_preview(i)

def choose(choice_key):
    global current

    if not typing_done:
        return

    # ending -> exit
    if scene.get("ending") is True:
        stop_steps_loop()
        root.destroy()
        return

    choices = scene.get("choices", {})
    if choice_key not in choices:
        return

    # apply flags (O1..O5)
    choice = choices[choice_key]
    flags = choice[2] if (isinstance(choice, (list, tuple)) and len(choice) >= 3) else []
    for f in flags:
        if f in events:
            events[f] = True

    next_id = choices[choice_key][1]
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

def on_escape(e):
    stop_steps_loop()
    root.destroy()

# ----------------------------
# UI
# ----------------------------
root = tk.Tk()
root.title("02:17")
root.attributes("-fullscreen", True)
root.bind("<Escape>", on_escape)

# Background
try:
    bg_img = tk.PhotoImage(file=bg_path)
except Exception as e:
    bg_img = None
    print("BG LOAD ERROR:", e)

bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_img

# Top image area (logo first, then scene image)
top_image_label = tk.Label(root, bd=0, highlightthickness=0, bg="#0b0f1a")
top_image_label.place(relx=0.5, rely=0.05, anchor="n")

# Card panel (text + choices)
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

# Choices area: 3 columns (side-by-side)
choices_row = tk.Frame(card, bg="#0b0f1a")
choices_row.pack(pady=(0, 18))

choice_buttons = []
preview_labels = []
choice_frames = []

for col, key in enumerate(["1", "2", "3"]):
    cf = tk.Frame(choices_row, bg="#0b0f1a")
    cf.grid(row=0, column=col, padx=64, pady=6, sticky="n")
    choice_frames.append(cf)

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

    # Optional hover refresh (keeps it feeling alive)
    btn.bind("<Enter>", lambda e, i=col, k=key: show_choice_preview(i, k))

# Initial language buttons (2 used)
choice_buttons[0].config(text="English", command=set_english, state="normal")
choice_buttons[1].config(text="Türkçe", command=set_turkish, state="normal")
choice_buttons[2].config(text="", state="disabled")

# Layering
bg_label.lower()
card.lift()
top_image_label.lift()

# Startup: show logo
show_logo()

root.mainloop()
