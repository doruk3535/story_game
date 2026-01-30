import os
import time
from game_story import STORY, STORY_TR

try:
    import winsound
except:
    winsound = None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def type_writing(text, delay=0.03, pause=0.5, click=True):
    c = 0
    for ch in text:
        print(ch, end="", flush=True)

        
        if click and winsound and (not ch.isspace()) and ch not in ".!?":
            c += 1
            if c % 3 == 0:
                winsound.Beep(1800, 6)

        if ch in ".!?":
            time.sleep(pause)
        else:
            time.sleep(delay)

    print()


def play():
    lang = input("1) English\n2) Türkçe\nSelect: ").strip()
    story = STORY_TR if lang == "2" else STORY

    current = "start"

    while True:
        clear_screen()
        scene = story[current]

        type_writing(scene["text"], delay=0.02, pause=0.5, click=True)

        if "ending" in scene:
            print("\n---", scene["ending"], "---")
            input("\nPress Enter to exit...")
            break

        print()
        for key in scene["choices"]:
            print(f"{key}) {scene['choices'][key][0]}")

        choice = input("\nChoice: ").strip()

        if choice in scene["choices"]:
            current = scene["choices"][choice][1]
        else:
            print("Invalid choice.")
            input("Press Enter...")
