import tkinter as tk
from game_story import STORY, STORY_TR
import os

# ---- sound (windows only) ----
try:
    import winsound
except:
    winsound = None

def soft_click():
    if winsound:
        winsound.Beep(1800, 6)

# ---- paths ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(BASE_DIR, "images", "bg.png")
logo_path = os.path.join(BASE_DIR, "images", "logo.png")

# ---- game state ----
story = None
current = "start"
scene = None

# ---- typewriter state ----
full_text = ""
index = 0
click_count = 0
typing_done = True

# ---- logo state ----
logo_img = None

def show_logo():
    """Load & show logo using Tkinter PhotoImage (no PIL)."""
    global logo_img
    try:
        logo_img = tk.PhotoImage(file=logo_path)
        # Logo boyutu: 2/3/4 dene (küçüldükçe sayı büyür)
        logo_img = logo_img.subsample(2, 2)

        image_label.config(image=logo_img, text="")
        image_label.image = logo_img
    except Exception as e:
        # Eğer buraya düşerse: logo.png Tk'in sevmediği formatta demek
        image_label.config(image="", text="LOGO LOAD ERROR", fg="white", font=("Arial", 16))
        image_label.image = None
        print("LOGO LOAD ERROR:", e)

def clear_logo():
    image_label.config(image="", text="")
    image_label.image = None

def start_typewriter(text):
    global full_text, index, click_count, typing_done
    full_text = text
    index = 0
    click_count = 0
    typing_done = False

    label.config(text="")
    button1.config(state="disabled")
    button2.config(state="disabled")

    type_step()

def type_step():
    global index, click_count, typing_done

    if index < len(full_text):
        ch = full_text[index]
        label.config(text=label.cget("text") + ch)
        index += 1

        # click sound (not on spaces/punctuation, and not every char)
        if not ch.isspace() and ch not in ".!?":
            click_count += 1
            if click_count % 3 == 0:
                soft_click()

        # sentence pause
        if ch in ".!?":
            root.after(220, type_step)
        else:
            root.after(20, type_step)
    else:
        typing_done = True
        show_buttons_for_scene()

def show_buttons_for_scene():
    if "ending" in scene:
        button1.config(text="Exit", command=root.destroy, state="normal")
        button2.config(text="", state="disabled")
        return

    button1.config(text=scene["choices"]["1"][0], command=choose1, state="normal")
    button2.config(text=scene["choices"]["2"][0], command=choose2, state="normal")

def load_scene():
    global scene
    scene = story[current]

    # Oyun başlayınca logo kalksın (sonra sahne görselleri koyacaksın)
    clear_logo()

    start_typewriter(scene["text"])

def choose1():
    global current
    if not typing_done:
        return
    current = scene["choices"]["1"][1]
    load_scene()

def choose2():
    global current
    if not typing_done:
        return
    current = scene["choices"]["2"][1]
    load_scene()

# ---- language selection (logo first, then start) ----
def start_game_with_logo():
    show_logo()
    root.after(1000, load_scene)  # 1 saniye logo, sonra oyun

def set_english():
    global story, current
    story = STORY
    current = "start"
    start_game_with_logo()

def set_turkish():
    global story, current
    story = STORY_TR
    current = "start"
    start_game_with_logo()

# ---- UI ----
root = tk.Tk()
root.title("Story Game")
print(root.winfo_screenwidth(), root.winfo_screenheight())


root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# ---- BACKGROUND IMAGE ----
try:
    bg_img = tk.PhotoImage(file=bg_path)
except Exception as e:
    bg_img = None
    print("BG LOAD ERROR:", e)

bg_label = tk.Label(root, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_img  # keep reference

# --- LOGO AREA (top center) ---
image_label = tk.Label(root, bd=0, highlightthickness=0, bg="#0b0f1a")
# üstte ortalı: anchor="n" (north)
image_label.place(relx=0.5, rely=0.08, anchor="n")

# --- CARD PANEL (text + buttons) ---
card = tk.Frame(root, bg="#0b0f1a", bd=2, relief="groove")
# logonun altına insin diye üst padding verdik
card.pack(padx=30, pady=(660, 15), fill="x")

label = tk.Label(
    card,
    text="Select Language / Dil Seç",
    font=("Arial", 16),
    wraplength=740,
    justify="center",
    bg="#0b0f1a",
    fg="white"
)
label.pack(padx=20, pady=20)

frame = tk.Frame(card, bg="#0b0f1a")
frame.pack(pady=(0, 15))

button1 = tk.Button(frame, text="English", width=20, command=set_english)
button1.grid(row=0, column=0, padx=10)

button2 = tk.Button(frame, text="Türkçe", width=20, command=set_turkish)
button2.grid(row=0, column=1, padx=10)

# ---- layering ----
bg_label.lower()
card.lift()
image_label.lift()  # logo en üstte

# İlk açılışta logo görünsün:
show_logo()

root.mainloop()
