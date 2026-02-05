
# game_story.py
# ------------------------------------------------------------
# 02:17 - Story data (EN first, then TR)
# - 3 choices per scene
# - events flags (O1..O5)
# - FINAL_CHECK -> auto routes to one of 32 END_Fxx endings
# ------------------------------------------------------------

EVENTS_DEFAULT = {
    "O1": False,  # Camera truth
    "O2": False,  # Old message / digital proof
    "O3": False,  # Witness (janitor)
    "O4": False,  # Confrontation / acceptance
    "O5": False,  # Alarm / escape attempt
}

EVENT_ORDER = ["O1", "O2", "O3", "O4", "O5"]  # bit order

def events_to_mask(events: dict) -> int:
    """Convert events dict to a 0..31 bitmask using EVENT_ORDER."""
    m = 0
    for i, k in enumerate(EVENT_ORDER):
        if events.get(k, False):
            m |= (1 << i)
    return m

# mask(0..31) -> END_F01..END_F32
ENDING_BY_MASK = {m: f"END_F{m+1:02d}" for m in range(32)}


# ============================================================
# ENGLISH STORY
# ============================================================

STORY_EN = {

    "S01_START": {
    "text": (
        "It's 02:17.\n"
        "Your phone screen is on, but there's no notification.||"
        "You hear steady footsteps from the corridor.||\n"
        "Too steady."
    ),
    "images": [
        "images/s01_1_phone.png",
        "images/s01_2.png",
        "images/s01_3.png",
    ],
    "end_sound": "footstep",
    "choices": {
        "1": ("Go to the door", "S02_CORRIDOR_ENTRY", []),
        "2": ("Check your phone", "S03_PHONE_LOCK", []),
        "3": ("Try to sleep", "END_E01", []),
    },
},


    "S02_CORRIDOR_ENTRY": {
        "text": (
            "You’re at the door.||\n"
            "The footsteps stop right in front of it.||\n"
            "Someone is listening."
        ),
        "images": [
        "images/s02_door.png",
        "images/s02_2.png",
        "images/s02_3.png",
    ],
        "choices": {
            "1": ("Open the door", "S04_CORRIDOR", []),
            "2": ("Lock the door", "S09_LOOP_ROOM", []),
            "3": ("Look under the door", "S05_FOOTPRINT", []),
        },
    },

    "S03_PHONE_LOCK": {
        "text": (
            "On the lock screen you see an old notification.||\n"
            "Not from today.||\n"
            "Sender: Unknown."
        ),
    "images": [
        "images/s03_phone.png",
        "images/s03_2.png",
        "images/s03_3.png",
    ],
        "choices": {
            "1": ("Open the notification", "S04_CORRIDOR", ["O2"]),
            "2":  ("Turn the phone off", "S09_LOOP_ROOM", []),
            "3": ("Open the gallery", "S06_GALLERY", []),
        },
    },

    "S04_CORRIDOR": {
        "text": (
            "The corridor is empty.||"
            "The lights flicker softly.||"
            "The footsteps are gone."
        ),
        "images": [None, "images/s04_corridor.png", None],

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Head toward the camera room", "S07_CAMERA_DOOR", []),
            "2": ("Approach the cleaning cart", "S08_JANITOR", []),
            "3": ("Go back to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S05_FOOTPRINT": {
        "text": (
            "A shoeprint on the floor.\n\n"
            "It matches yours."
        ),
        "image": "images/s05_footprint.png",
        "choices": {
            "1": ("Follow the print", "S04_CORRIDOR", []),
            "2": ("Ignore it", "S09_LOOP_ROOM", []),
            "3": ("Take a photo", "S06_GALLERY", []),
        },
    },

    "S06_GALLERY": {
        "text": (
            "Old photos fill your gallery.\n"
            "You don’t remember most of them.||"
            "One stands out:||"
            "The corridor "
            "night "
            "and you."
        ),
        "images": [
        "images/s06_gallery.png",   # sol
        "images/s06_2.png",   # orta
        "images/s06_3.png",   # sağ
    ],"effects": ["SET_FLAG_GALLERY_SEEN"],
        "choices": {
            "1": ("Study the photo", "S10_MEMORY_GLITCH", []),
            "2": ("Leave the gallery", "S04_CORRIDOR", []),
            "3": ("Delete the photo", "S09_LOOP_ROOM", []),
        },
    },

    "S07_CAMERA_DOOR": {
        "text": (
            "You’re at the camera room door.\n"
            "A faint hum comes from inside.\n\n"
            "It isn’t locked."
        ),
        "images": [None, "images/s07_camera_door", None],
        "choices": {
            "1": ("Open the door", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Listen closely", "S12_CAMERA_HINT", []),
            "3": ("Back away", "S04_CORRIDOR", []),
        },
    },

    "S08_JANITOR": {
        "text": (
            "Someone stands beside the cleaning cart.||"
            "The night janitor.||"
            "He frowns when he sees you.\n"
            "As if he knows you."
        ),
    "images": [
        "images/s08_janitor.png",
        "images/s08_2.png",
        "images/s08_3.png",
    ],
        "choices": {
            "1": ("Talk to him", "S13_JANITOR_DIALOGUE", ["O3"]),
            "2": ("Walk away quietly", "S04_CORRIDOR", []),
            "3": ("Run", "S09_LOOP_ROOM", []),
        },
    },

    "S09_LOOP_ROOM": {
        "text": (
            "You’re in bed.\n"
            "Same room.\n\n"
            "02:17 again.\n"
            "But this time you notice."
        ),
        "image": "images/s09_loop_room.png",
        "choices": {
            "1": ("This happened before", "S10_MEMORY_GLITCH", []),
            "2": ("Get up fast", "S04_CORRIDOR", []),
            "3": ("Don’t move", "END_E02", []),
        },
    },

    "S10_MEMORY_GLITCH": {
        "text": (
            "Your head spins.\n"
            "For a second, everything overlaps.\n\n"
            "Corridor.\n"
            "Voices.\n"
            "An argument."
        ),
        "image": "images/s10_glitch.png",
        "choices": {
            "1": ("Force the memory", "S14_PRE_CONFRONT", []),
            "2": ("Stop yourself", "S09_LOOP_ROOM", []),
            "3": ("Follow the sound", "S04_CORRIDOR", []),
        },
    },

    "S11_CAMERA_ROOM": {
        "text": (
            "You’re inside the camera room.\n"
            "Screens show the corridor.\n\n"
            "On one screen...\n"
            "You are there."
        ),
        "image": "images/s11_camera_room.png",
        "choices": {
            "1": ("Watch the footage", "S15_CAMERA_TRUTH", []),
            "2": ("Turn the screens off", "END_E03", []),
            "3": ("Leave the room", "S04_CORRIDOR", []),
        },
    },

    "S12_CAMERA_HINT": {
        "text": (
            "You listen at the door.\n"
            "No one inside.\n\n"
            "But the screen glow is on."
        ),
        "image": "images/s12_camera_hint.png",
        "choices": {
            "1": ("Open the door", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Step back", "S04_CORRIDOR", []),
            "3": ("Make a note of it", "S10_MEMORY_GLITCH", []),
        },
    },

    # -------- PART 3 (EN) --------

    "S13_JANITOR_DIALOGUE": {
        "text": (
            "The janitor leans on the cart and studies you.\n\n"
            "\"You again?\" he says.\n"
            "\"Last time it was the same hour. 02:17.\"\n\n"
            "He doesn’t sound scared.\n"
            "He sounds tired."
        ),
        "image": "images/s13_janitor_dialogue.png",
        "choices": {
            "1": ("What do you mean, 'last time'?", "S16_JANITOR_INFO", []),
            "2": ("Ignore him and leave", "S04_CORRIDOR", []),
            "3": ("Accuse him of lying", "S17_JANITOR_REACT", []),
        },
    },

    "S14_PRE_CONFRONT": {
        "text": (
            "Your breathing quickens.\n"
            "Images fracture and fuse in your mind.\n\n"
            "An argument.\n"
            "A door.\n"
            "A sentence:\n"
            "\"No one can know.\""
        ),
        "image": "images/s14_pre_confront.png",
        "choices": {
            "1": ("Accept the memory", "S18_ACCEPT_MEMORY", ["O4"]),
            "2": ("Reject it", "S09_LOOP_ROOM", []),
            "3": ("Focus and keep walking", "S04_CORRIDOR", []),
        },
    },

    "S15_CAMERA_TRUTH": {
        "text": (
            "The footage starts.\n"
            "The corridor appears.\n\n"
            "Then... you.\n"
            "But your walk is wrong.\n"
            "Not rushing.\n"
            "As if you're waiting.\n\n"
            "The corner timestamp reads:\n"
            "02:17"
        ),
        "image": "images/s15_camera_truth.png",
        "choices": {
            "1": ("Fast-forward", "S19_CAMERA_ADVANCE", []),
            "2": ("Record the screen on your phone", "S20_SAVE_PROOF", []),
            "3": ("Panic and leave", "S04_CORRIDOR", []),
        },
    },

    "S16_JANITOR_INFO": {
        "text": (
            "He goes quiet.\n"
            "\"Some nights repeat here,\" he says.\n\n"
            "\"People either don't notice...\n"
            "or they notice too late.\"\n\n"
            "He whispers:\n"
            "\"Have you been to the camera room?\""
        ),
        "image": "images/s16_janitor_info.png",
        "choices": {
            "1": ("Say yes (mention the footage)", "S21_JANITOR_PROOF", []),
            "2": ("Say no (lie)", "S17_JANITOR_REACT", []),
            "3": ("Ask about the footsteps", "S22_JANITOR_FOOTSTEPS", []),
        },
    },

    "S17_JANITOR_REACT": {
        "text": (
            "He narrows his eyes.\n"
            "\"You’re still denying it,\" he says.\n\n"
            "He pushes the cart slowly.\n"
            "\"Then it happens again.\""
        ),
        "image": "images/s17_janitor_react.png",
        "choices": {
            "1": ("Follow him", "S22_JANITOR_FOOTSTEPS", []),
            "2": ("Go back to the camera room", "S07_CAMERA_DOOR", []),
            "3": ("Run to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S18_ACCEPT_MEMORY": {
        "text": (
            "You close your eyes.\n"
            "This time you don’t run.\n\n"
            "A face—blurred.\n"
            "But the voice is clear:\n"
            "\"Close the door.\"\n\n"
            "And your answer:\n"
            "\"No.\"\n\n"
            "Your chest tightens.\n"
            "You know you’ve lived this moment."
        ),
        "image": "images/s18_accept_memory.png",
        "choices": {
            "1": ("Go to the corridor—find the truth", "S04_CORRIDOR", []),
            "2": ("Find the janitor (witness)", "S08_JANITOR", []),
            "3": ("Go to the camera room (proof)", "S07_CAMERA_DOOR", []),
        },
    },

    "S19_CAMERA_ADVANCE": {
        "text": (
            "You fast-forward.\n\n"
            "The video stutters.\n"
            "The image breaks.\n\n"
            "Then—one frame:\n"
            "The camera swings away from you...\n"
            "toward something watching you.\n\n"
            "Not clear.\n"
            "Just a shadow."
        ),
        "image": "images/s19_camera_advance.png",
        "choices": {
            "1": ("Replay it again and again", "S23_CAMERA_LOOP", []),
            "2": ("Check the date", "S24_CAMERA_DATE", []),
            "3": ("Pull the plug", "END_E04", []),
        },
    },

    "S20_SAVE_PROOF": {
        "text": (
            "You record the screen.\n"
            "File saved.\n\n"
            "But in your gallery...\n"
            "it's gone.\n\n"
            "Only an empty thumbnail remains.\n"
            "Name:\n"
            "0217.mp4"
        ),
        "image": "images/s20_save_proof.png",
        "choices": {
            "1": ("Try to open the file", "S25_FILE_OPEN", []),
            "2": ("Show the janitor", "S13_JANITOR_DIALOGUE", []),
            "3": ("Leave", "S04_CORRIDOR", []),
        },
    },

    "S21_JANITOR_PROOF": {
        "text": (
            "He holds his breath.\n"
            "\"Show me,\" he says.\n\n"
            "When you explain, his face drains.\n"
            "\"Footage disappears sometimes.\n"
            "Because that night hides itself.\""
        ),
        "image": "images/s21_janitor_proof.png",
        "choices": {
            "1": ("Press: What happened that night?", "S26_TRUTH_PRESSURE", []),
            "2": ("Ask him to get you out", "S27_ESCAPE_HINT", []),
            "3": ("Run back to the camera room", "S11_CAMERA_ROOM", []),
        },
    },

    "S22_JANITOR_FOOTSTEPS": {
        "text": (
            "He looks down the corridor.\n"
            "\"Footsteps sometimes mimic you,\" he says.\n\n"
            "\"Because some nights, this place is full of you.\n"
            "What you did.\n"
            "What you didn’t leave behind.\""
        ),
        "image": "images/s22_janitor_footsteps.png",
        "choices": {
            "1": ("What did I leave behind?", "S26_TRUTH_PRESSURE", []),
            "2": ("Head for the fire stairs", "S28_FIRE_STAIRS_DOOR", []),
            "3": ("Go back to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S23_CAMERA_LOOP": {
        "text": (
            "You replay the same moment.\n\n"
            "The shadow looks different each time.\n"
            "But one thing stays:\n"
            "You don’t step back.\n\n"
            "As if you called it."
        ),
        "image": "images/s23_camera_loop.png",
        "choices": {
            "1": ("Stop and leave", "S04_CORRIDOR", []),
            "2": ("Zoom in on the shadow", "S29_ENHANCE", []),
            "3": ("Find the janitor", "S08_JANITOR", []),
        },
    },

    "S24_CAMERA_DATE": {
        "text": (
            "You check the date.\n\n"
            "Not today.\n"
            "Not even a day listed.\n\n"
            "Only:\n"
            "02:17\n"
            "02:17\n"
            "02:17\n\n"
            "As if the recording is trapped inside a single second."
        ),
        "image": "images/s24_camera_date.png",
        "choices": {
            "1": ("Try to export the clip", "S25_FILE_OPEN", []),
            "2": ("Leave the camera room", "S04_CORRIDOR", []),
            "3": ("Consider deleting everything", "S30_DELETE_DILEMMA", []),
        },
    },

    "S25_FILE_OPEN": {
        "text": (
            "You open 0217.mp4.\n"
            "Black screen.\n\n"
            "Then a voice:\n"
            "\"Close the door.\"\n\n"
            "It’s your voice."
        ),
        "image": "images/s25_file_open.png",
        "choices": {
            "1": ("Follow the sound (to the corridor)", "S04_CORRIDOR", []),
            "2": ("Play it for the janitor", "S13_JANITOR_DIALOGUE", []),
            "3": ("Throw the phone", "S09_LOOP_ROOM", []),
        },
    },

    "S26_TRUTH_PRESSURE": {
        "text": (
            "The janitor stays silent for a long time.\n\n"
            "\"Some nights someone stands at a door,\" he says.\n"
            "\"The door opens.\n"
            "And no one steps in.\n\n"
            "They just... leave you inside.\""
        ),
        "image": "images/s26_truth_pressure.png",
        "choices": {
            "1": ("Did I do this?", "S14_PRE_CONFRONT", []),
            "2": ("How do I end it?", "S27_ESCAPE_HINT", []),
            "3": ("Sprint to the camera room", "S07_CAMERA_DOOR", []),
        },
    },

    "S27_ESCAPE_HINT": {
        "text": (
            "He nods toward the fire stairs.\n"
            "\"Alarm,\" he says.\n\n"
            "\"Sometimes, if everyone wakes up...\n"
            "the hour lets go.\""
        ),
        "image": "images/s27_escape_hint.png",
        "choices": {
            "1": ("Go to the fire stairs", "S28_FIRE_STAIRS_DOOR", []),
            "2": ("Get proof first", "S11_CAMERA_ROOM", []),
            "3": ("Return to your room (prepare)", "S09_LOOP_ROOM", []),
        },
    },

    "S28_FIRE_STAIRS_DOOR": {
        "text": (
            "You’re at the fire stairs door.\n"
            "Cold air spills through the crack.\n\n"
            "From below comes a faint metal sound.\n"
            "As if someone waits on the steps."
        ),
        "image": "images/s28_fire_stairs_door.png",
        "choices": {
            "1": ("Open and go down", "S31_FIRE_STAIRS", []),
            "2": ("Close it and go back", "S04_CORRIDOR", []),
            "3": ("Listen at the door", "S32_STAIRS_LISTEN", []),
        },
    },

    "S29_ENHANCE": {
        "text": (
            "You zoom in.\n"
            "Pixels fall apart.\n\n"
            "But one detail shows:\n"
            "The shadow holds something—like a key.\n\n"
            "A tag on it reads:\n"
            "\"217\""
        ),
        "image": "images/s29_enhance.png",
        "choices": {
            "1": ("Search the corridor for '217'", "S04_CORRIDOR", []),
            "2": ("Tell the janitor", "S13_JANITOR_DIALOGUE", []),
            "3": ("Leave and return to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S30_DELETE_DILEMMA": {
        "text": (
            "Delete screen.\n"
            "Your finger hovers over 'Delete'.\n\n"
            "It feels like this could end everything.\n"
            "Or start something worse."
        ),
        "image": "images/s30_delete_dilemma.png",
        "choices": {
            "1": ("Don’t delete", "S15_CAMERA_TRUTH", []),
            "2": ("Delete", "END_E05", []),
            "3": ("Leave it and go", "S04_CORRIDOR", []),
        },
    },

    "S31_FIRE_STAIRS": {
        "text": (
            "You’re in the fire stairs.\n"
            "The steps are cold.\n\n"
            "The door above slowly closes.\n"
            "A step sounds below.\n\n"
            "In your rhythm."
        ),
        "image": "images/s31_fire_stairs.png",
        "choices": {
            "1": ("Go down", "S33_DOWNSTAIRS", []),
            "2": ("Go up", "S04_CORRIDOR", []),
            "3": ("Wait", "S34_STANDOFF", []),
        },
    },

    "S32_STAIRS_LISTEN": {
        "text": (
            "You press your ear to the door.\n\n"
            "From the steps below...\n"
            "one word.\n\n"
            "\"Open.\""
        ),
        "image": "images/s32_stairs_listen.png",
        "choices": {
            "1": ("Open the door", "S31_FIRE_STAIRS", []),
            "2": ("Step away", "S04_CORRIDOR", []),
            "3": ("Go back to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S33_DOWNSTAIRS": {
        "text": (
            "One floor down.\n"
            "Door numbers look wrong.\n\n"
            "Like a different version of the building.\n"
            "And here...\n"
            "there is no clock."
        ),
        "image": "images/s33_downstairs.png",
        "choices": {
            "1": ("Enter the corridor", "S35_ALT_CORRIDOR", []),
            "2": ("Go back up", "S31_FIRE_STAIRS", []),
            "3": ("Catch your breath", "S14_PRE_CONFRONT", []),
        },
    },

    "S34_STANDOFF": {
        "text": (
            "You wait.\n"
            "Footsteps approach.\n\n"
            "A shape forms in the dark.\n"
            "Your height.\n"
            "Your gait.\n\n"
            "It stops.\n"
            "Right in front of you."
        ),
        "image": "images/s34_standoff.png",
        "choices": {
            "1": ("Speak: Who are you?", "S36_SHADOW_TALK", []),
            "2": ("Run back", "S04_CORRIDOR", []),
            "3": ("Walk into it", "S37_PHYSICAL", ["O4"]),
        },
    },

    "S35_ALT_CORRIDOR": {
        "text": (
            "The lower corridor is silent.\n"
            "Old notices on the walls.\n\n"
            "One has your name.\n"
            "No date.\n\n"
            "Only:\n"
            "02:17"
        ),
        "image": "images/s35_alt_corridor.png",
        "choices": {
            "1": ("Rip the notice down", "S14_PRE_CONFRONT", []),
            "2": ("Walk to the end", "S38_STORAGE_DOOR", []),
            "3": ("Go back", "S31_FIRE_STAIRS", []),
        },
    },

    "S36_SHADOW_TALK": {
        "text": (
            "It doesn’t speak.\n"
            "But it breathes like you.\n\n"
            "One step forward.\n"
            "Then it stops.\n\n"
            "Waiting for your decision."
        ),
        "image": "images/s36_shadow_talk.png",
        "choices": {
            "1": ("Get close—see its face", "S37_PHYSICAL", ["O4"]),
            "2": ("Slam the door and run", "S31_FIRE_STAIRS", []),
            "3": ("Close your eyes", "END_E06", []),
        },
    },

    "S37_PHYSICAL": {
        "text": (
            "You touch it.\n\n"
            "Cold.\n"
            "Real.\n\n"
            "For a second, both of you speak at once:\n"
            "\"I started this.\""
        ),
        "image": "images/s37_physical.png",
        "choices": {
            "1": ("Accept it", "S14_PRE_CONFRONT", ["O4"]),
            "2": ("Deny it", "S09_LOOP_ROOM", []),
            "3": ("Decide to find the alarm", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S38_STORAGE_DOOR": {
        "text": (
            "A storage door.\n"
            "Old label:\n"
            "\"Lost & Found\"\n\n"
            "Light leaks through the crack."
        ),
        "image": "images/s38_storage_door.png",
        "choices": {
            "1": ("Enter", "S39_STORAGE_INSIDE", []),
            "2": ("Close it and leave", "S35_ALT_CORRIDOR", []),
            "3": ("Peek inside", "S40_STORAGE_PEEK", []),
        },
    },

    "S39_STORAGE_INSIDE": {
        "text": (
            "Boxes everywhere.\n"
            "Some are already open.\n\n"
            "Inside one box:\n"
            "your keychain.\n\n"
            "You thought you lost it."
        ),
        "image": "images/s39_storage_inside.png",
        "choices": {
            "1": ("Take the keychain", "S14_PRE_CONFRONT", []),
            "2": ("Close the box and leave", "S35_ALT_CORRIDOR", []),
            "3": ("Check underneath", "S41_HINT_ALARM", []),
        },
    },

    "S40_STORAGE_PEEK": {
        "text": (
            "No one inside.\n"
            "But a chair sits in the center.\n\n"
            "Like someone stood up seconds ago.\n\n"
            "Behind the chair:\n"
            "an alarm access card."
        ),
        "image": "images/s40_storage_peek.png",
        "choices": {
            "1": ("Go in and take the card", "S41_HINT_ALARM", []),
            "2": ("Back away", "S35_ALT_CORRIDOR", []),
            "3": ("Run upstairs", "S31_FIRE_STAIRS", []),
        },
    },

    "S41_HINT_ALARM": {
        "text": (
            "A small card in your hand.\n"
            "It reads:\n"
            "\"ALARM PANEL - ACCESS\"\n\n"
            "Under it, the same number:\n"
            "02:17"
        ),
        "image": "images/s41_hint_alarm.png",
        "choices": {
            "1": ("Return to the fire stairs", "S28_FIRE_STAIRS_DOOR", []),
            "2": ("Go to the alarm panel", "S42_ALARM_PANEL", []),
            "3": ("Go back to your room and think", "S09_LOOP_ROOM", []),
        },
    },

    # -------- PART 4 (EN) --------

    "S42_ALARM_PANEL": {
        "text": (
            "You stand before the alarm panel.\n"
            "A red cover hangs half-open.\n\n"
            "The screen flashes one line:\n"
            "02:17\n\n"
            "As if it’s waiting for you."
        ),
        "image": "images/s42_alarm_panel.png",
        "choices": {
            "1": ("Trigger the alarm", "S43_ALARM_TRIGGER", ["O5"]),
            "2": ("Inspect the panel", "S44_ALARM_LOGS", []),
            "3": ("Step back", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S43_ALARM_TRIGGER": {
        "text": (
            "You lift the cover fully.\n"
            "Your finger hits the button.\n\n"
            "A second of silence...\n"
            "then the building erupts in alarm.\n\n"
            "Lights blaze on."
        ),
        "image": "images/s43_alarm_trigger.png",
        "choices": {
            "1": ("Run downstairs", "S45_ALARM_ESCAPE", []),
            "2": ("Go to the corridor", "S46_ALARM_CORRIDOR", []),
            "3": ("Stay and listen", "S47_ALARM_WAIT", []),
        },
    },

    "S44_ALARM_LOGS": {
        "text": (
            "Old logs fill the panel.\n"
            "Most dates are missing.\n\n"
            "But the time repeats:\n"
            "02:17\n"
            "02:17\n"
            "02:17\n\n"
            "Some lines include your name."
        ),
        "image": "images/s44_alarm_logs.png",
        "choices": {
            "1": ("Read the logs", "S48_LOG_REALIZATION", []),
            "2": ("Trigger the alarm now", "S43_ALARM_TRIGGER", ["O5"]),
            "3": ("Leave the panel", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S45_ALARM_ESCAPE": {
        "text": (
            "You sprint down the stairs.\n"
            "Alarm and footsteps blend.\n\n"
            "But lower down the sound changes.\n"
            "Not an alarm...\n"
            "a breathing thing."
        ),
        "image": "images/s45_alarm_escape.png",
        "choices": {
            "1": ("Keep running", "S49_EXIT_DOOR", []),
            "2": ("Stop and look back", "S34_STANDOFF", []),
            "3": ("Cut into the lower corridor", "S35_ALT_CORRIDOR", []),
        },
    },

    "S46_ALARM_CORRIDOR": {
        "text": (
            "The corridor is bright now.\n"
            "Doors sit half-open.\n\n"
            "No people.\n\n"
            "The alarm here is muffled.\n"
            "Like it comes from inside the walls."
        ),
        "image": "images/s46_alarm_corridor.png",
        "choices": {
            "1": ("Run to the camera room", "S11_CAMERA_ROOM", []),
            "2": ("Search for the janitor", "S08_JANITOR", []),
            "3": ("Return to your room", "S09_LOOP_ROOM", []),
        },
    },

    "S47_ALARM_WAIT": {
        "text": (
            "You stay still.\n\n"
            "The alarm slowly fades.\n"
            "Then stops.\n\n"
            "Silence.\n"
            "And you are not alone."
        ),
        "image": "images/s47_alarm_wait.png",
        "choices": {
            "1": ("Turn to what’s behind you", "S34_STANDOFF", []),
            "2": ("Slip away quietly", "S46_ALARM_CORRIDOR", []),
            "3": ("Close your eyes", "END_E07", []),
        },
    },

    "S48_LOG_REALIZATION": {
        "text": (
            "The logs finally make sense.\n\n"
            "Each time the alarm triggers, someone disappears.\n"
            "But sometimes...\n"
            "two people appear.\n\n"
            "One is always you.\n"
            "The other has no name."
        ),
        "image": "images/s48_log_realization.png",
        "choices": {
            "1": ("Accept what it means", "S50_SELF_REALIZE", ["O4"]),
            "2": ("Close the logs", "S42_ALARM_PANEL", []),
            "3": ("Compare with the camera footage", "S15_CAMERA_TRUTH", []),
        },
    },

    "S49_EXIT_DOOR": {
        "text": (
            "Emergency exit.\n"
            "Chained shut.\n\n"
            "A tag on the chain:\n"
            "\"217\"\n\n"
            "Same number.\n"
            "Same key."
        ),
        "image": "images/s49_exit_door.png",
        "choices": {
            "1": ("Try the key", "S51_KEY_USE", []),
            "2": ("Force the chain", "S52_FORCE_EXIT", []),
            "3": ("Go back", "S45_ALARM_ESCAPE", []),
        },
    },

    "S50_SELF_REALIZE": {
        "text": (
            "You can’t deny it anymore.\n\n"
            "This building isn’t holding you.\n"
            "You are holding this moment.\n\n"
            "02:17 won’t move\n"
            "until you let it."
        ),
        "image": "images/s50_self_realize.png",
        "choices": {
            "1": ("Everything clicks (face it)", "S53_ALMOST_END", ["O4"]),
            "2": ("Return to the alarm panel", "S42_ALARM_PANEL", []),
            "3": ("Go back to your room (one last time)", "S09_LOOP_ROOM", []),
        },
    },

    "S51_KEY_USE": {
        "text": (
            "The key fits perfectly.\n\n"
            "You turn it.\n"
            "Nothing opens.\n\n"
            "A voice behind you:\n"
            "\"Not yet.\""
        ),
        "image": "images/s51_key_use.png",
        "choices": {
            "1": ("Turn toward the voice", "S34_STANDOFF", []),
            "2": ("Pocket the key and step back", "S45_ALARM_ESCAPE", []),
            "3": ("Throw the key down", "S52_FORCE_EXIT", []),
        },
    },

    "S52_FORCE_EXIT": {
        "text": (
            "Metal screams as you force the chain.\n\n"
            "It loosens—just a little.\n"
            "Then you feel a hand on your shoulder.\n\n"
            "Cold.\n"
            "Familiar."
        ),
        "image": "images/s52_force_exit.png",
        "choices": {
            "1": ("Grab the hand and turn", "S37_PHYSICAL", ["O4"]),
            "2": ("Scream", "END_E08", []),
            "3": ("Drop to the floor", "S47_ALARM_WAIT", []),
        },
    },

    "S53_ALMOST_END": {
        "text": (
            "Everything clicks into place.\n\n"
            "Camera.\n"
            "Alarm.\n"
            "Witness.\n"
            "And you.\n\n"
            "No more running.\n"
            "Only a choice."
        ),
        "image": "images/s53_almost_end.png",
        "choices": {
            "1": ("Accept it completely", "S54_FINAL_GATE", []),
            "2": ("Reject it all", "END_E09", []),
            "3": ("Try to run anyway", "S45_ALARM_ESCAPE", []),
        },
    },

    "S54_FINAL_GATE": {
        "text": (
            "The building holds its breath.\n\n"
            "For the first time, the hour trembles.\n"
            "02:17 isn’t fixed.\n\n"
            "It can pass.\n"
            "But there’s a price."
        ),
        "image": "images/s54_final_gate.png",
        "choices": {
            "1": ("Pay the price", "S55_FINAL_ENTRY", []),
            "2": ("Step back", "S09_LOOP_ROOM", []),
            "3": ("Trigger the alarm again", "S43_ALARM_TRIGGER", ["O5"]),
        },
    },

    "S55_FINAL_ENTRY": {
        "text": (
            "You stand before the last door.\n\n"
            "Behind it:\n"
            "either 02:17 ends\n"
            "or you do.\n\n"
            "The door opens—slowly."
        ),
        "image": "images/s55_final_entry.png",
        "choices": {
            "1": ("Enter", "FINAL_CHECK", []),
            "2": ("Shut it", "END_E10", []),
            "3": ("Look back", "S34_STANDOFF", []),
        },
    },

    # -------- Special / endings (EN early) --------

    "FINAL_CHECK": {
        "text": (
            "Everything freezes.\n\n"
            "You remember how you got here.\n"
            "What you saw.\n"
            "What you saved.\n"
            "Who witnessed it.\n"
            "What you admitted.\n"
            "What you triggered.\n\n"
            "The hour stares at you."
        ),
        "image": "images/final_check.png",
        "final_check": True
    },

    "END_E01": {"text": "You close your eyes.\nThe footsteps stop.\n\nThe time doesn’t change.\nStill 02:17.", "image": "images/end_e01.png", "ending": True},
    "END_E02": {"text": "You don’t move.\nTick… tick…\n\nThe footsteps come closer.\nThis time, they don’t stop.", "image": "images/end_e02.png", "ending": True},
    "END_E03": {"text": "You turn the screens off.\n\nBut you can still feel someone watching.", "image": "images/end_e03.png", "ending": True},
    "END_E04": {"text": "You pull the plug.\nScreens die.\nLights die.\n\nDarkness.\n\nThen the footsteps start.\nNo exit.", "image": "images/end_e04.png", "ending": True},
    "END_E05": {"text": "You delete the footage.\nRelief—one second.\n\nThen the screens show:\n02:17\n\nUnder it:\n\"TRY AGAIN.\"", "image": "images/end_e05.png", "ending": True},
    "END_E06": {"text": "You close your eyes.\n\nWhen you open them, you’re back in bed.\n02:17.\nAnd the breathing is closer.", "image": "images/end_e06.png", "ending": True},
    "END_E07": {"text": "You close your eyes.\n\nThe alarm fades.\nThe breathing doesn’t.\n02:17 remains.", "image": "images/end_e07.png", "ending": True},
    "END_E08": {"text": "Your scream bounces through the building.\n\nNo one answers.\nOnly the sound of 02:17.", "image": "images/end_e08.png", "ending": True},
    "END_E09": {"text": "You reject everything.\n\nThe building lets go.\nBut you don’t.\n02:17 stays with you.", "image": "images/end_e09.png", "ending": True},
    "END_E10": {"text": "You shut the door.\n\nA lock clicks.\nThis time, you’re the one trapped inside.", "image": "images/end_e10.png", "ending": True},
}

# 32 final endings (EN) generated by bitmask 0..31
# Each one is distinct in consequence + tone.
for _m in range(32):
    _eid = f"END_F{_m+1:02d}"
    # build a readable label of triggered events
    _flags = [EVENT_ORDER[i] for i in range(5) if (_m >> i) & 1]
    _tag = " + ".join(_flags) if _flags else "NO_EVENTS"

    # short, distinct endings
    # (Hand-crafted themes by mask tier)
    if _m == 0:
        _text = (
            "You reach the last door with nothing in your hands.\n"
            "No proof. No witness. No admission.\n\n"
            "02:17 doesn’t punish you.\n"
            "It simply resets you.\n\n"
            "You wake up.\n"
            "02:17."
        )
    elif _m == 31:
        _text = (
            "You did everything.\n"
            "You saw the footage.\n"
            "You kept the message.\n"
            "You had a witness.\n"
            "You faced yourself.\n"
            "You woke the building.\n\n"
            "For the first time, the hour moves.\n"
            "02:17 becomes 02:18.\n\n"
            "And the corridor is finally… empty."
        )
    else:
        # make endings feel different based on the combination count
        c = bin(_m).count("1")
        if c == 1:
            _text = (
                f"Only one thread reaches the end: {_tag}.\n\n"
                "It isn’t enough to break the hour.\n"
                "But it is enough to change you.\n\n"
                "02:17 keeps going.\n"
                "Just not the same way."
            )
        elif c == 2:
            _text = (
                f"Two pieces align: {_tag}.\n\n"
                "The door opens—then hesitates.\n"
                "The building recognizes you.\n\n"
                "You escape one loop.\n"
                "But you inherit another."
            )
        elif c == 3:
            _text = (
                f"Three truths collide: {_tag}.\n\n"
                "The hour cracks.\n"
                "Not fully.\n"
                "Just enough for something to slip out.\n\n"
                "When you step outside, you realize:\n"
                "you weren’t the only one leaving."
            )
        elif c == 4:
            _text = (
                f"Everything except one: {_tag}.\n\n"
                "The door opens wide.\n"
                "The corridor breathes.\n\n"
                "You almost win.\n"
                "Almost is the most dangerous kind of victory."
            )
        else:
            _text = (
                f"{_tag}.\n\n"
                "The final door opens.\n"
                "A different ending takes your hand.\n\n"
                "02:17 doesn’t end.\n"
                "It chooses where to continue."
            )

    STORY_EN[_eid] = {
        "text": _text,
        "image": f"images/{_eid.lower()}.png",
        "ending": True,
        "mask": _m,
    }

# ============================================================
# TURKISH STORY (EN ile birebir ID + uzunluk)
# ============================================================

STORY_TR = {

"S01_START": {
    "text": (
        "Saat 02:17.||"
        "Telefon ekranın açık ama bildirim yok.||"
        "Koridordan düzenli ayak sesleri geliyor.||"
        "Çok düzenli."
    ),
    "images": [
        "images/s01_1_phone.png",
        "images/s01_2.png",
        "images/s01_3.png",
    ],

    # ✅ 2. segment başlarken ayak sesi girer
    "footstep_on_segment": 2,

    # ❌ bunu kaldır (yoksa tekrar tetikleyebilir)
    # "end_sound": "footstep",

    "choices": {
        "1": ("Kapıya yaklaş", "S02_CORRIDOR_ENTRY", []),
        "2": ("Telefonuna bak", "S03_PHONE_LOCK", []),
        "3": ("Uyumaya çalış", "END_E01", []),
    },
},

"S02_CORRIDOR_ENTRY": {
    "text": (
        "Kapının önündesin.\n"
        "Ayak sesleri kapının tam önünde duruyor.||\n"
        "Biri seni dinliyor.||\n"
        "Nefesini bile duyuyorsun."
    ),
    "images": [
        "images/s02_door.png",
        "images/s02_2.png",
        "images/s02_3.png",
    ],
    "choices": {
        "1": ("Kapıyı aç", "S04_CORRIDOR", []),
        "2": ("Kapıyı kilitle", "S09_LOOP_ROOM", []),
        "3": ("Kapının altına bak", "S05_FOOTPRINT", []),
    },
},


"S03_PHONE_LOCK": {
    "text": (
        "Kilit ekranına bakıyorsun.||"
        "Eski bir bildirim var.||"
        "Bugüne ait değil. Gönderen bilinmiyor.||\n"
        
    ),
    "images": [
        "images/s03_phone.png",
        "images/s03_2.png",
        "images/s03_3.png",
    ],
    "choices": {
        "1": ("Bildirimi aç", "S03.5_NOTİFİCATİON", ["O2"]),
        "2": ("Telefonu kapat", "S09_LOOP_ROOM", []),
        "3": ("Galeriyi aç", "S06_GALLERY", []),
    },
},
"S03.5_NOTİFİCATİON": {
    "text": (
        "Kurtul ordan çabuk.||"
        "Orası artık güvenli değil.|| "
        'Kimseye güvenme.'
        
        
    ),
    "images": [
        "images/s03.5_NOTİFİCATİON.png",
       
    ],
    "choices": {
        "1": ("Koridora çık", "S04_CORRIDOR_After_NOTİFİCATİON", ["O2"]),
        "2": ("Telefonu kapat", "S09_LOOP_ROOM", []),
        "3": ("Galeriyi aç", "S06_GALLERY", []),
    },
},

    "S04_CORRIDOR": {
        "text": (
            "Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},


        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
        },
    },
    "S04_CORRIDOR_After_NOTİFİCATİON": {
        "text": (
            "Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},


        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },
        "S04_CORRIDOR_after_footprint": {
        "text": (
            "Ayak izleri ileri uzanıyor||"
            "Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},


        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },
    "S04_CORRIDOR_AFTER_GALERY": {
        "text": (
            "Bi saniye .||"
            "Bu koridoru tanıyorum .||"
            "Neden hatırlamıyorum  ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},


        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki adama sor", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },

        
       
     "S04_CORRIDOR_After_camera": {
    "text": (
        "Koridordasın.||"
        "Boş.||"
        "Az önce biri vardı ama artık yok.||"
        "Ayak sesi yok."
    ),
    "images": [None, "images/s04_corridor.png", None],
    "choices": {
        "1": ("Yangın merdivenine git", "S15_FIRE_EXIT", []),
        "2": ("Yemekhaneye yönel", "S16_CAFETERIA", []),
        "3": ("Odana geri dön", "S09_LOOP_ROOM_4", []),
    },
},
   
"S15_FIRE_EXIT_LOCKED": {
    "text": (
        "Yangın kapısının önündesin.||"
        "Kolu indiriyorsun.||"
        "Kımıldamıyor.||"
        "Kilitli.||"
        
    ),
    "images": [None, "images/s15_fire_exit.png", None],
    "effects": ["SET_FLAG_FIRE_EXIT_TRIED"],
    "choices": {
        "1": ("Geri dön", "S04_CORRIDOR_After_camera", []),
        "2": ("Odana dön", "S09_LOOP_ROOM_4", []),
    },
},

    # ✅ sadece bu sahnede, 2. görsel geldiğinde C slot flicker olsun
    "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},


        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },
    "S05_FOOTPRINT": {
        "layout": "single",
        "text": (
            "Yerde bir ayakkabı izi.\n"
            "Nedense çok tanıdık."
        ),
        "image": "images/s05_footprint.png",
        "choices": {
            "1": ("İzi takip et", "S04_CORRIDOR_after_footprint", []),
            "2": ("Görmezden gel", "S09_LOOP_ROOM_2", []),
            "3": ("Fotoğrafını çek", "S06_GALLERY_after_footprint", []),
        },
    },
    "S06_GALLERY_after_footprint": {
    "text": (
        "Fotoğrafını çektin ve bakmak için galeriyi açtın \n"
        "Galerinde eski fotoğraflar var.\n"
        "Çoğunu hatırlamıyorsun.||"
        "Ama biri öne çıkıyor:||"
        "Koridor,"
        "Gece,"
        "Ve sen."
    ),
    "images": [
        "images/s06_gallery.png",   # sol
        "images/s06_2.png",   # orta
        "images/s06_3.png",   # sağ
    ],"effects": ["SET_FLAG_GALLERY_SEEN"],
    "choices": {
        "1": ("Fotoğrafı incele", "S10_MEMORY_GLITCH", []),
        "2": ("Galeriden çık ve dışarıyı incele", "S04_CORRIDOR_AFTER_GALERY", []),
        "3": ("Fotoğrafı sil", "S09_LOOP_ROOM_2", []),
    },
},
    "S06_GALLERY": {
    "text": (
        "Galerinde eski fotoğraflar var.\n"
        "Çoğunu hatırlamıyorsun.||"
        "Ama biri öne çıkıyor:||"
        "Koridor,"
        "Gece,"
        "Ve sen."
    ),
    "images": [
        "images/s06_gallery.png",   # sol
        "images/s06_2.png",   # orta
        "images/s06_3.png",   # sağ
    ],
    "choices": {
        "1": ("Fotoğrafı incele", "S10_MEMORY_GLITCH", []),
        "2": ("Galeriden çık", "S04_CORRIDOR_AFTER_GALERY", []),
        "3": ("Fotoğrafı sil", "S09_LOOP_ROOM_2", []),
    },"effects": ["SET_FLAG_GALLERY_SEEN"],
},


    "S07_CAMERA_DOOR": {
        "text": (
            "Kamera odasının kapısındasın.\n"
            "İçeriden hafif bir uğultu geliyor.\n\n"
            "Kilitli değil."
        ),
        "images": [None, "images/s07_camera_door.png", None],
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("içeriyi dinle", "S12_CAMERA_HINT", []),
            "3": ("koridora geri dön", "S04_CORRIDOR_After_camera", []),
        },
    },

"S08_JANITOR": {
    "text": (
        "Temizlik arabasının yanında biri duruyor.||"
        "Gece temizlikçisi.||"
        "Seni görünce kaşlarını çatıyor.\n"
        "Sanki seni tanıyor."
    ),
    "images": [
        "images/s08_janitor.png",
        "images/s08_2.png",
        "images/s08_3.png",
    ],
    "choices": {
        "1": ("Onunla konuş", "S13_JANITOR_DIALOGUE", ["O3"]),
        "2": ("Sessizce yanından geç", "S08.5_DONT_LOOK_HİM", []),
        "3": ("Odana geri dön", "S09_LOOP_ROOM_3", []),
    },
},

"S08.5_DONT_LOOK_HİM": {
    "text": (
        "Sana baktı ve dediki.||"
        "'Bu saatte koridorda gezmenin yasak olduğunu bilmiyormusun '.||"

    ),
   "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
    "choices": {
        "1": ("Tersle", "S8.4_ANSWER_HİM", ["O3"]),
        "2": ("Aldırış etmeden yanından geç", "S8.6_go_to_caffeteria", []),
        "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
    },
},

"S8.4_ANSWER_HİM": {
    "text": (
        "Sen kendi işine bak.||"
        "Bunu pek hoş karşılamyan bi ses tonu ve bakışla.||"
        "'Çabuk odana dön' dedi .||"

    ),
   "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
    "choices": {
        "1": ("Haddini bildir", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
        "2": ("Aldırış etmeden yanında geç", "S8.6_go_to_caffeteria", []),
        "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
    },
},
"S8.6_go_to_caffeteria": {
    "text": (
        "Bir anda koşmaya başlıyorsun.||"
        "Adımların koridorda yankılanıyor.||"
        "Işıklar uzuyor, daralıyor.||"
        "Dönüşü alırken biriyle sertçe çarpışıyorsun.||"
        "İkiniz de sendeleyip duruyorsunuz."
        "'Bu kişi banamı benziyor ?'"
    ),
    "images": [
        'images/s08_6_collision.png',
        "images/s08_6_3.png",
        'images/s08_6_3.png',
    ],#süre barı olucak burada
    "choices": {
        "1": ("Onu görmezden gel ve saklan", "S16_CAFETERIA_SOLO", []),
        "2": ("Onunla birlikte hareket et", "S16_CAFETERIA_WITH_MIDDLE", []),
        "3": ("Kim olduğunu anlamaya çalış ", "END_CAUGHT_WHILE_REALIZING"), 
    },
},
"S16_CAFETERIA_SOLO": {
    "text": (
        "Kafeteryaya tek başına giriyorsun.||"
        "Işıklar açık.||"
        "Masa ve sandalyeler düzgün.|||"
        "Her şey fazla normal.||"
        "Kapıyı arkandan kapatıyorsun.||"
        "Nefesini yavaşlatmaya çalışıyorsun.|||"
        "Bir anlığına…||"
        "arkadan boğuk bir ses geliyor.||"
        "Sanki biri itiraz etmek ister gibi.|||"
        "Sonra kesiliyor.||"
        "Sessizlik geri geliyor.||"
        "Bununla ilgilenmemeye karar veriyorsun."
    ),
    "choices": {
        "1": ("Tezgâhın arkasına bak", "S16_CAFETERIA_CHESS_SETUP", []),
        "2": ("Saklanacak bir yer ara", "", []),
        "3": ("Sesin geldiği yöne kulak kesil", "S16_CAFETERIA_LISTEN", []),
    },
},

"S16_CAFETERIA_CHESS_SETUP": {
    "text": (
        "Tezgâhın arkasına geçiyorsun.||"
        "Burası çalışanlara ait gibi duruyor.||"
        "Çekmeceler düzenli, ama biri denense şifreyle kilitlenmiş .|||"
        "Çekmeceyi zorluyorsun ama açılmıyor .||"
        "Etrafı incelediğnde iki şey görüyorsun .||"
        "Bir satranç tahtası.||"
        "Ve bir yangın tüpü:||"
        "Ne yapmalıyım”||"
   
    ),
    "choices": {
        "1": ("Satranç tahtasını incele", "S16_CHESS_PUZZLE_SCREEN", []),
        "2": ("Yangın tüpüyle kilidi kırmaya çalış", "S16_yangın_tüpü", []),
        "3": ("Yaşlı adam gelemden saklanıcak biyer bul", "S16_CAFETERIA_HIDE", []),
    },
},
"S16_CAFETERIA_HIDE": {
  "text": (
    "Tezgâhın altına giriyorsun.|| Dizlerin taş zemine gömülüyor.||"
    "Kapı açılıyor.|||"
    "Hademe: 'Nerdesin... orada olduğunu biliyorum.'|||"
    "Ayakkabısının sesi... duruyor. Tam önünde."
  ),
  "choices": {
    "1": ("Sessiz kal / nefesini tut", "15_HIDE_SILENT_1", ["F_HIDE"]),
    "2": ("Ses çıkar (tıkırtı)", "S16_HIDE_DISTRACT", ["F_NOISE"]),
    "3": ("Etrafı Aaramya başla.'", "S16_CAFETERIA_CHESS_SETUP", []),
  }
},
"S15_HIDE_SILENT_1": {
    "text": (
        "Nefesini kesiyorsun. Göğsün yanıyor.||"
        "Hademe kıpırdamıyor. Sanki dinlemiyor... sanki zaten biliyor.||"
        "Fısıltı gibi: 'Bu kadar sessizlik... hep aynı.'"
    ),
    "choices": {
        "1": ("Sessiz kal / kıpırdama", "S15_HIDE_SILENT_2", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},
"S15_HIDE_SILENT_2": {
    "text": (
        "Parmakların istemsiz titriyor ama durduruyorsun.||"
        "Ayakkabı sesi bir adım sağa kayıyor... sonra geri geliyor.||"
        "Hademe: 'Beni oyalama. Zaman bunu sevmez.'"
    ),
    "choices": {
        "1": ("Sessiz kal / dayan", "S15_HIDE_FORCED", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},
"S15_HIDE_FORCED": {
    "text": (
        "Sessizliğin içine batıyorsun. Bu artık saklanmak değil.||"
        "Hademe tam önünde duruyor. Eğilmiyor.||"
        "Sadece başını yana eğiyor: .'|||"
        "Saklanarak buradan çıkamayacağını anlıyorsun."
    ),
    "choices": {
        "2": ("dikkati başka yöne çek  (sesle)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},
"S15_HIDE_DISTRACT": {
    "text": (
        "Etrafta bulduğun metal bi şişeyi fırlatttın... küçük ama yeterli.||"
        "Hademe başını aniden çeviriyor.||"
        "'Güzel... sonunda bir kaçmak için bi fırsat.|||'"
        "Tam zamanı bi anda fırlıyosun.||"
        "Ama hademe bunu farkediyiyo.'|||"
        "Olabildiğinde hızlı kafeteryanın kapısından kaçmaya çalışıyosun.||"
        "Ama hademe bunu düşünmüş ve kapıyı kitlemiş.||"
        "Sen daha ne olduğnun bile anlamadan arkanı döndüğün anda seni yakalıyo.||"
    ),
  "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
    "auto_delay_ms": 500,   # istersen 0 da yapabilirsin
},
"S15_CAFETERIA_STORAGE_LOCK": {
    "text": (
        "Depoya atılıyorsun. Kapı arkandan tek hamlede kapanıyor.||"
        "Kilit sesi… kapıyı üstüne kapatıyor.|||"
        "ieçride biri daha var||"
        "Ayak sesleri… uzaklaşıyor.|||"
        "Ve o ses geliyor. Kendi sesin. biraz daha büyük |||"
        "ORTANCA: \"Bunun olucağını biliyordum.\"||"
        "Sen: \"Kim var orada?\"||"
        "ORTANCA: \"Bence kim olduğumu biliyosun.\"|||"
        "Sen: \"Hayır bilmiyorum \"||"
        "ORTANCA: \"Şu yüzü bak .\"||"
        "ORTANCA: \"İyi bak*.\"|||"
        "Sen: \"Sen kimsin?\"||"
        "ORTANCA: \"Ben senim .\"||"
        "ORTANCA: \" 6 yıl sonraki halinim .\"|||"
        "Sen: \"Saçmalama.\"||"
        "ORTANCA: \"Saçmalamdığımı biliyosun ilk gördüğün andan itibaren biliyosun.\"||"
        "Sen: \"Kanıtla ozaman …\"||"
        "ORTANCA: \" 7 yaşındaydık yaz ayıydı|| yazlıktaki o kız|| ikimizde hatırlıyoruz  nasıl unuturuzki\"|||"
        "ORTANCA: \"Cesaratimizi toplayıp ona açılmaya hazırlanmıştık. \"||"
        "ORTANCA: \"Ama hert zamanki gibi korkaklık yapıp mahvetmiştik.\"|||"
         "ORTANCA: \"Değilmi .\"|||"
        "Sen: \"…\"||"
        "ORTANCA: \"Ve bunu kimsiye anlatamamıştık.\"|||"
        "ORTANCA: \"Kendimize bile.\"|||"
        "Sen: \"O zaman sen gerçekten…\"||"
        "ORTANCA: \"Evet.\"|||"
        "Sen: \"Ama bu nasıl olur?\"||"
        "Sen: \"Peki neden buradayım?\"||"
        "ORTANCA: \"Çünkü bir seçim yapman gerekiyor.\"||"
        "ORTANCA: \"Ama önce… gerçeği bilmen lazım.\"|||"
        "Sen: \"Hangi gerçeği?\"||"
        "ORTANCA: \"o hademede sanada garip gelen bişey yokmu.\"|||"
        "ORTANCA: \"Tanıdık bişey.\"|||"
        "Sen: \"Dur tahmin ediyim ?\"||"
        "ORTANCA: \"evet... doğru tahmin ettin .\"||"
        "ORTANCA: \"hepimiz aynı kişiyiz farklı zamanlardan.\"||"
        "ORTANCA: \"seni uyarmaya gelmiştim \"|||"
        "Sen: \"Peki bu nasıl oluyor neden 3 farklı zaman birbiri içinde\"||"
        "ORTANCA: \"O kadarını bilmiyorum .\"|||"
        "ORTANCA: \"tek bildiğim seni burda tutmak istiyo .\"|||"
        "ORTANCA: \"Ve benim seni burda çıkarmam gerek .\"|||"
        "Sen: \"Ama bunu nasıl yapıcaz.\"||"
        
    ),
    "choices": {
        "1": ("Havalandırmayı kullan(tek başına kurtul odadan)", "S15_RAY_VENT_ESCAPE_SOLO", []),
        "2": ("Hademeye seslen", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
        "3": ("Sessiz kal", "S15_STORAGE_LISTEN", []),
    },
},
"S17_ESCAPE_TOGETHER_OVERCOME_JANITOR": {
    "text": (
        "ORTANCA: \"Tamam. Dinle.\"|||"
        "ORTANCA: \"Onu yenemeyiz.||"
        "Ama onu kandirabiliriz.\"|||"
        "Sen: \"Nasıl?\"|||"
        "ORTANCA: Bilmiyiyorum|||"
        "ORTANCA: Onunla konuşmalıyız.||"
        "Kapıyı tıklatıyorsun.\"|||"
        "Tak.|||"
        "Tak.|||"
        "Tak.|||"
        "Hademe Kapıyı açıyor |||"
        "Hademe:ne istiyorsunuz\"||"
        "ORTANCA: \"anlaşma yapmak istiyoruz.\"|||"
        "Hademe:Neden size güveniyim.||"
        "ORTANCA :Bizi sonsuza kadar burda tutamazsın.|||"
        "Hademe: Aslında yapabilirim |||"
        "ORTANCA :Hayır yapamazsınn aynı zamanda 3 farklı varyantın bulunamsın risklerini biliyosun .||"
        "Hademe:P ekalaNe istiyorsunuz.|||"
        "ORTANCA :ne istediğimi biliyosun.||"
        "ORTANCA :çocuğun burdan gitmesi.||"
        "Hademe:Bunun olmucağını biliyosun .||"
        "Hademe:Neden olamıcağınıda biliyosun .||"
        "Sen'burda neler oluyo:.||"
        "ORTANCA :Anlat ona.||"
        "Hademe:Pekİ.||"
        "Hademe:Ama bunun hoşuna gidiceğini sanmıyorum .||"
        'Hademe:Şuan geçmiş ve gelecek senin burda kalmana bağlı'
        'Hademe:Sen bi anomalisin zamanı bir arada tutuyorsun '
        'Sen:peki neden ben '
        'Hademe:Çünkü hepsi benim hatam '
        'Hademe:Ve sen bensin '
        'Hademe:Burdan çıkmıyorsun '
        'Deyip kapıyı üzerine kapıyı kapatmak için arkasını dönüyor çıkmaya hazırlanıyor '
        
        
    ),
    "choices": {
        "1": ("İtiraz et", "S18_ARGUE_WITH_JANITOR", []),
        "2": ("Hademeye saldır", "S18_ATTACK_JANITOR", []),
        "3": ("Orada kalmaya karar ver", "S18_DECIDE_STAY", []),
    },
},
"S18_ARGUE_WITH_JANITOR": {
    "text": (
        "Sen: \"Hayır.\"|||"
        "Sen: \"Bu benim hayatım değil.\"|||"
        "Hademe gözlerini kısıyor…||"
        'Başka çaren yok'
        'Duvardaki saate bakıyorsun 02:17'
        '02:17'
        've hep 02:17'
        'Zamanda sıkışıp kaldın'
        'En azından yanlız değilsin'    ),

        "ending_id": "END_LOCKED_FOR_TIME",
        
  
    
},
"S18_DECIDE_STAY": {
    "text": (
        "Sen: yapabilceğimiz bişey yok.\"|||"
        "Sen:  fazla güçlü.\"|||"
        "Hademe gözlerini kısıyor…||"
        'Bende öyle düşünmüştüm'
        'Duvardaki saate bakıyorsun 02:17'
        '02:17'
        've hep 02:17'
        'Zamanda sıkışıp kaldın'
        'En azından yanlız değilsin'    ),

        "ending_id": "END_LOCKED_FOR_TIME",
        
  
    
},
"S18_ATTACK_JANITOR": {
    "text": (
        "Sen: \"Hayır.\"|||"
        "Sen: \"Bu benim hayatım değil.\"|||"
        "Böyle bitemez deyip saldırıyorsun…||"
        "Seni geçen seferki gibi kolayca itiyor||"
        "Ama busefer yanlız değilsin ||"
        "Senin ittiği esnada arkandan genç halin gelip|| onu itiyor ve adam yalpalayıp yere düşüyor|||"
        "Bu ikiniz içinde bir fırsat hemen koridora koşuyorsunuz"
        "Yangın çıkışına doğru koşuyorsunuz"
        "Çıkışa vardığında cebinden anahtarı çıkartıp kilide takıyorsun"
        "Yangın çıkışının kapısı açıldığında bi zaman portalı çıkıyor"
        "O sırada yalpalıyan hademe ayağı kalkıyor ve belindeki silahı çıkarıyor"
        "Ve bi el havaya ateş ediyor"
        "ÇABUK DURUN !!!!"
        "Beni buna mecbur bırakmayın"
        "Silahı sana doğru doğrultuyor.|||"
        "O an genç halinin de belinde bir silah olduğunu fark ediyorsun.|||"
        "Genç halin sana bakıyor.||"
        "Sanki kararını senden bekliyor.|||"
        "Portalın içi dalgalanıyor.||"
        "Bir saniyen var."
    ),
    "choices": {
        "1": ("Genç halini tut ve portala atla", "END_ATTACK_PORTAL_JUMP", []),
        "2": ("Silahı indir ve teslim ol", "END_ATTACK_SURRENDER", []),
        "3": ("Hademeyi durdurmaya çalış", "END_ATTACK_DISARM_ATTEMPT", []),
    },
},
"END_ATTACK_PORTAL_JUMP": {
    "text": (
        "Genç halinin bileğini yakalıyorsun.|||"
        "Sen: \"ŞİMDİ!\"|||"
        "O seni anlıyor.||"
        "Bir an bile tereddüt etmiyor.|||"
        "İkiniz birden portala atlamak içiçn hamle ediyorsunuz.|||"
        "Hademe bunun olmasına izin veremem deyip ateş ediyor.|||"
        'Elinle karnını tutuyorsun'
        'Heryer kan olmuş'
        'Aynı anda hepiniz karnınızı tutuyorsunuz'
        'Sen ölünce gelecekti varyantlarında ölüyo'
        'Neden yaptın diye soruyorsun son nefesinsle'
        'oda son nefesiyle cevap veriyor'
        'Mecburdum...'
    ),
    "ending_id": "END_ATTACK_PORTAL_JUMP",
},
"END_ATTACK_SURRENDER": {
    "text": (
        "Genç halin sana bakıyor.||"
        "Gözleri ‘soru’ değil… ‘öfke’.|||"
        "Sen bir adım öne çıkıyorsun.|||"
        "Sen: \"Yapma.\"|||"
        'Genç halin:Napıyorsun teslim olamazsın'
        'Sen: biz bu değiliz biz katil değiliz'
        'Genç halin: seni dinlemiyor ve silahına davranırken'
        'Genç halin vururluyor'
        'Ve karnını tutmaya başlıyor '
        'Aynı anda yaşlı halinde karnını tutuyor'
        'Genç halin olmadan yaşlı halin olamaz'
        'Genç halininin suratında tatlı bi tebessüm'
        'Sen:bunun olucağını biliyordun değilmi'
        'Son nefesiyle özgür olmanı istedim '
        'artık öözgürsün kendini ve geleceğini kurtar'
        'gözlerini yumuyor'
        'Onun ölümünün anlanlandırman gerek'
        'herşeye rağmen portal giriyorusun '
        'Ardına bakmadan '
        'Portaldan geçtikten sonra'
        'Gözün kakarırıyor'
        'Ve yatağında uynaıyorsun'
        'Yine aynı odadasın '
        'Doğrulup telefonuna bakıyorsun '
        'saat 02:18 '
        'Ve bir bildirim var'
        'Bugünden değil gelecekten'
        'Ve şöyle diyor en yaptın bilmiyorum||'
        'Ama doğru olanı yaptın'
    ),
    "ending_id": "END_ATTACK_SURRENDER",
},

"END_ATTACK_DISARM_ATTEMPT": {
    "text": (
        "Genç halin sana bakıyor.||"
        "Gözleri ‘soru’ değil… ‘öfke’.|||"
        'O zaten kararnı vermiş '
        "Sen bir adım öne çıkıyorsun.|||"
        "Sen: \"Yapma.\"|||"
        "Ama kelime havada kalıyor.|||"
        "Silahına davranıyor ve:|||"
        "Hademe karnını tutmaya başlıyor…||"
        "hademe nefes nefese kalıyor…||"
        "Ve yere yığılıyor …|||"
        "Son nefesiyle 'herşey benim suçumdu'.|||"
        'Genç haline bakıyorsun sen ne yaptın der gibi'
        'Bana öyle bakamyı kes bunu yapmak zorundaydım'
        'Hademe o zamanı bir arada tutmadığı için ozaman yokolmaya başlıyor'
        'Saatler 02:18i göstermeye başlıyor'
        'Portaldan geçmekten başka bi seçeeğiniz yok'
        'Genç haline bakıp diyorsunki '
        'Bakalım gelcek bize ne getirecek'
        'Sana bakıp gülümsüyor ve diyorki'
        'Daaha kötü olamaz'
    ),
    "ending_id": "END_ATTACK_DISARM_ATTEMPT",
},

"S15_RAY_VENT_ESCAPE_SOLO": {
    "text": (
        "Gözlerin karanlığa alışırken tavandaki metal ızgarayı fark ediyorsun.||"
        "Havalandırma.|||"
        'Ama çok yüksekte'
        'birinin diğerini kaldırması gerek'
        "ORTANCA: \"Madem yanlız birimiz burdan çıkabilir bu sen olmalısın \"|||"
        " \"İtiraz etmiyorsun  \"|||"
        "Ellerin ızgaraya gidiyor.||"
        "Vida yok.||"
        "Sadece eski, gevşek bir kilit.|||"
        "Parmaklarını araya sokuyorsun.||"
        "Çıt.|||"
        "Izgara hafifçe açılıyor.||"
        "İçeriden kuru, tozlu bir hava yüzüne vuruyor.|||"
        "Sürünerek içeri giriyorsun.||"
        "Omuzların zor sığıyor.|||"
        "Karanlık bir tünel.||"
        "Her hareketinde metal inliyor.|||"
        "Bir yerde tünel ikiye ayrılıyor gibi.||"
        "Hangisi doğru bilmiyorsun.|||"
        "Ama bir şeyi biliyorsun:||"
        "Geri dönmeyeceksin.|||"
        "Bir çıkış ızgarası.|||"
        "İtiyorsun.||"
        "Kendini dışarı bırakıyorsun.|||"
        "Kafeterya koridoru.||"
        "Boş gibi…|||"
        "Ama ışıklar titriyor.||"
        "Sanki senin geldiğini haber veriyor."
    ),
    "auto_next": "END_SOLO_ESCAPE",
},

"S16_CHESS_PUZZLE_SCREEN": {
    "text": (
        "Tahtaya bakıyorsun.||"
        "Taşlar sana bir şey ima ediyor.|||"
        "Oyun sonu çok yakın gibi.||"
        "Taşların koordinatları sana bir şeyler anlatıyor.|||"
        "Şifre bu olabilir mi?||"
        "Ama hangi taş ve hangi koordinat?|||"
        "Biraz düşündükten sonra fark ediyorsun:||"
        "BULDUM! Tek hamlede mat var.|||"
        "ŞİFRE BU OLMALI."
    ),
    "choices": {
        "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A", []),
        "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
        "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
    },
},

    "S16_CHESS_TRY_A": {
    "text": (
        "Kale h7 gibi ama emin değilim .||"
        "Ozaman şifre h7 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"

    ),
    "choices": {
        "1": ("Şifreyi deneyelim bakalım", "S16_UNLOCK_SEQUENCE", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
    },
},
"S16_CHESS_TRY_B": {
    "text": (
        "Atı g6'ya oynuyorsun.||"
        "Ozaman şifre g6 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"
    ),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
    },
},
"S16_CHESS_TRY_C": {
    "text": (
        "Atı f7'ya oynuyorsun.||"
        "Ozaman şifre f7 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"
    ),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
    },
},
"S16_UNLOCK_SEQUENCE": {
    "text": (
        "Tezgâhın altına eğiliyorsun.||"
        " şifreli olan kilidi şifreni girmeye hazırlanıyorsun.||"

    ),
    "choices": {
        "1": ("h7 ", "S16_kilit_açılmıyor", []),
        "2": ("g6", "S16_şifre_doğru", []),
        "3": ("f7", "S16_kilit_açılmıyor", []),
    },
},
"S16_kilit_açılmıyor": {
    "text": (
        "Yanlış hesaplamış olmalıyım.||"
        "Bidaha denemeliyim .||"

    ),
    "choices": {
        "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_Again", []),
        "2": ("Yangın söndürücüyü al", "S16_şifre_doğru", []),
        "3": ("SAKLAN !!!", []),
    },
},
"S16_CHESS_PUZZLE_SCREEN_Again": {
    "text": (
        "Tekrar tahtaya bakıyorsun.||"
        "Bu sefer doğru hamleyi yapman gerek."
    ),
    "choices": {
        "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A", []),
        "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
        "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
    },
},
"S16_şifre_doğru": {
    "text": (
        "Biliyordum.||"
        "Kilit açıldı.||"
        "İçinde bir anahtar var.||"
    ),
    "choices": {
        "2": ("Anahtarı al", "S16_KEY_TAKEN_SOLO", ["I_KEY"]),
    },
},

"S16_KEY_TAKEN_SOLO": {
    "text": (
        "Anahtarı aldın.||"
        "Ne açtığını bilmiyorsun ama doğru olduğunu hissediyorsun.|||"
        "Tam cebine koyacakken…|||"
        "Yan taraftaki kapıdan bir ses geliyor.||"
        "Hafif bir tıkırtı.||"
        "Sanki biri kapının arkasında nefes alıyor.|||"
        "Kafeterya koridoru ise bomboş.||"
        "Işıklar titriyor."
    ),
    "choices": {
        "1": ("Koridora git ve anahtarla kaç", "END_SOLO_ESCAPE", []),
        "2": ("Ses gelen deponnun kapısına doğru yaklaş", "S15_CAFETERIA_STORAGE_LOCK", []),
    },
},

"S16_RAY_TO_S15_CAPTURE": {
    "text": (
        "Kapıya yaklaşıyorsun.||"
        "Ses çok yakın….|||"
        "Elin, istemsizce anahtarı sıkıyor.||"
        "Metal avucunda sıkıca duruyor.|||"
        "Kulağını kapıya yaklaştırıyorsun.||"
        "içeriyi duymak için.||"
        "Ve tam o boşlukta—|||"
        "Arkandan bir gölge düşüyor.||"
        "Ne olduğunu anlamadan bileğin kavranıyor.|||"
        "Hademe.||"
        "Tek kelime etmeden seni çekiyor.|||"
        "Kapı açılıyor.||"
        "İçeriden ağır bir depo kokusu vuruyor.|||"
        "Bir itiş…||"
        "Kapı kapanıyor.||"
        "Kilit sesi."
    ),
    "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
},
"END_SOLO_ESCAPE": {
    "text": (
        "Kafeteryadan fırlıyorsun.||"
        "Koridorun ucunda, paslı bir tabela:||"
        "YANGIN ÇIKIŞI.|||"
        "Kapının etrafındaki ışık diğerlerinden farklı…||"
        "Garip bi his veriyo .|||"
        "Arkana bakıyorsun—|||"
        "Hademe beliriyor.||"
        "Yaşlı… omuzları çökmüş… ama gözleri keskin.|||"
        "Koşamıyor.||"
        "Ama seni durdurmaya çalışıyor.|||"
        "Sen kapıya doğru hızlanıyorsun.||"
        "Elin kolu titreyerek anahtarı çıkarıyor.|||"
        "Kilit…|||"
        "Tık.|||"
        "Kapıyı açıyorsun ve—|||"
        "Bir koridor değil.||"
        "bu bir kapı değil.|||"
        "Kapının içinde… dönüp duran bir boşluk var.||"
        "Işık değil— sanki zamanın kendisi kıvrılıyor.|||"
        "Bir ZAMAN PORTALI.|||"
        "Hademe arkanıdan bağırıyor:|||"
        "\"Dur!\"||"
        "\"Her şeyi mahvedeceksin!\"|||"
        "Sesi çatlıyor.||"
        "Sanki bu cümleyi daha önce de söylemiş gibi…|||"
        "Parmakların kapı kolunda.||"
        "Bir adım… ya da bir soru."
    ),
    "choices": {
        "1": ("Hademeye ne olduğunu sor", "END_SOLO_ESCAPE_ASK", []),
        "2": ("Kapıdan geç", "END_SOLO_ESCAPE_PORTAL", []),
    },
},
"END_SOLO_ESCAPE_PORTAL": {
    "text": (
        "Kapıdan geçiyorsun.|||"
        "Ne ‘özgürlük’ diyebiliyorsun…||"
        "Ne ‘kaçış’.|||"
        "Sadece… geçiyorsun.|||"
        "Hademe arkandan bağırıyor .||"
        "Dur herşeyi mahvediceksin .|||"
        "Ona aldrırış etmeden portaldan geçiyorsun  .|||"
        "—|||"
        "Gözlerini açıyorsun.|||"
        "Yatak.||"
        "Tavan.||"
        "Odanın kokusu.|||"
        "Her şey… aynı.|||"
        "Doğrulup saate bakıyorsun.||"
        "Saat: 02:18.||"
        'Ama neden herşey yolunamı girdi'
        'Tam o sırada bir ses duyuyosun '
        
        
    ),
    "ending_id": "END_SOLO_ESCAPE_PORTAL",
},

"END_SOLO_ESCAPE_ASK": {
    "text": (
        "Yutkunuyorsun.||"
        "\"Bunu neden yapıyorsun?\"|||"
        "\"Bu kapı ne?\"|||"
        "\"Neden bu zamanda sıkışıp kaldım?\"|||"
        "Hademe birkaç adım daha atıyor.||"
        "Nefes nefese… ama gözlerini senden ayırmıyor.|||"
        "\"Ben…\"||"
        "Cümle boğazında takılıyor.|||"
        "\"Ben, bunların hepsini ben başlattım.\"|||"
        "Nasıl yani diye soruyorsun.||"
        "Hiç geçmişe gidip bir şeyleri yeniden başlatmak istedin mi?|||"
        "\"Her şeyi düzeltmek…\"||"
        "\"Ben istedim.\"|||"
        "\"Karımı ve kızımı kaybettikten sonra.\"|||"
        "Benim hatamdı. Onları korumalıydım.||"
        "Ama yapamadım.|||"
        "\"Her şeyimi kaybetmiştim.\"|||"
        "\"Ama bir gün ikinci bir şans yaratmanın mümkün olduğunu öğrendim.\"||"
        "\"Karımı ve kızımı kurtarabilirdim.\"||"
        "\"Öyle de yaptım.\"|||"
        "Zaman portalını o kaza gününe ayarladım.||"
        "Nihayet o kazayı hiç yaşanmamış kılabilecektim.|||"
        "\"Öyle de yaptım.\"|||"
        "Bir süre mutluydum.||"
        "Hayatım tekrar karımla ve kızımla mutlu olduğum günlere geri dönmüştü.|||"
        "Sonra ne oldu?|||"
        "Zamanla ilgili bilmen gereken şey şu:|||"
        "Ne kadar kurcalarsan o kadar kontrolden çıkar.|||"
        "Bir süre sonra yaptığım değişikliğin bedelini ödedim.|||"
        "Kendi zamanım içine çöktü.||"
        "Tamamen karanlık ve boş bir zaman…|||"
        "\"Milyarlarca hayat… o zamanda yaşayan insanlar…\"|||"
        "Kiminin geleceği, kiminin geçmişi…||"
        "Hepsi yok oldu. Zamanın içinde bir yarık açıldı.|||"
        "Yaptığım hatayı fark ettiğimde her şey çok geçti.|||"
        "\"Ama yaptığım şeyi düzeltebilirdim.\"|||"
        "30 yıl öncesine gittim.||"
        "Genç halime bunu anlattım ve durması gerektiğini söyledim.|||"
        "\"Ama bunu anlayamayacak kadar kibirli ve toydu.\"|||"
        "Ben de ona engel olamayacak kadar yaşlıydım.|||"
        "O yüzden daha da geçmişe gitmeye karar verdim.|||"
        'Yılanın başını küçükken ezmeye.||'
        "Ama tam oradan ayrılırken genç halim beni takip etti.||"
        "Ve bu zamanda sıkıştık… hepimiz.|||"
        "Ve seni buradan kurtarıp yaptığım şeye engel olmaya çalışıyordu.|||"
        "\"O yüzden onu durdurdum.\"|||"
        "Şimdi de seni durduracaM.||"
        "Zamanı korumak zorundayım."
    ),
    "choices": {
        "1": ("Kal ve zamanı koru", "END_SOLO_STAY_PROTECT_TIME", []),
        "2": ("Ayrıl ve özgür ol", "END_SOLO_LEAVE_FREE", []),
    },
},
"END_SOLO_STAY_PROTECT_TIME": {
    "text": (
        "Hademe elini uzatıyor.||"
        "Bu fedakarlığı yapmak zorundayız.||"
        "Portal arkanda dönmeye devam ediyor.||"
        "Ama sesi artık daha kısık.|||"
        "Kapıyı kapatıp kilitliyorsun.|||"
        "Sanırım haklısın.||"
        "Bu fedakarlığı yapmalıyım.|||"
        "İnsanlığı kurtarmak için||"
        "Ve orda kalıyorsun.|||"
        "Yıllar boyunca.\\\"|||"
        "Hayatın boşa geçiyor.\\\"|||"
        "Ama en azından biliyorsun.\\\"|||"
        "Zaman artık güvende.\\\"|||"
    ),
    "ending_id": "END_SOLO_STAY_PROTECT_TIME",
},

"END_SOLO_LEAVE_FREE": {
    "text": (
        "Geri çekilmiyorsun.||"
        "Bir adım ileri gidiyorsun.|||"
        "Hademe ‘dur’diye sesleniyor.||"
        "Herşeyi mahvediceksin.|||"
        "Hapis ve güvenli bi ömür geçirmektense.||"
        "Özgür bi bilinmez bi sonu tercih ederim.|||"
        "Portalın içi dalgalanıyor.||"
        "\"Özgürlük,\" diyorsun.||"
        "\"Buna ihtiyacım var.\"|||"
        "Hademenin sesi çok kısık:|||"
        "\"Özgürlük değil o…\"||"
        "\"O bir son.\"|||"
        "Geçiyorsun.|||"
        "Gözlerin yanıyor.||"
        "Kulakların uğulduyor.|||"
        "Dünya… bir anlığına üst üste biniyor.|||"
        "Ve sonra—|||"
        "Sessizlik.|||"
        "Yatağında uyanıyorsun.||"
        "Herşey aynı.|||"
        "Gine aynı oda .|||"
        "Az önce yaşadıklarım bir rüyamıydı.|||"
        "Doğrulup telefoan bakıyorsun:|||"
        "Saat: 02:18|||"
        "Sanki bişeyleri doğru yapmış gibisin:|||"
        "\"Ama kim bilir bunu zaman göstericek .\""
    ),
    "ending_id": "END_SOLO_LEAVE_FREE",
},

"S09_LOOP_ROOM": {
    "text": (
        "Yatağındasın.\n"
        "Aynı oda.\n\n"
        "Yine 02:17.\n"
        "Ama bu sefer fark ediyorsun neden zaman ilerlemiyo."
    ),
"images": [
        None,
        "images/s09_loop_room.png",
        None,
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalkSanki", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S09_LOOP_ROOM_after_cleaner_men": {
    "text": (
        "Karnına doğru bi hamle yaptın.||"
        "Ama senin yumruğunu tutup seni yere yatırdı||"
        "Ve seni odana geri postaladı||"
        "Bi hademe neden dövüşmeyi bilirki amk."
    ),
"images": [
        None,('dövüş sahneleri'),
        "images/s09_loop_room.png",
        None,
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk ve tekrar koridora çık", "S04_CORRIDOR_after_fight", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S09_LOOP_ROOM_1": {
    "text": (
        "Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Dakikalar geçmiyor.||"
        "Telefonun ekranı bile aynı saniyede takılı kalmış gibi.||"
        "Bu bir bekleme değil… kilit."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},

"S09_LOOP_ROOM_2": {
    "text": (
        "Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Nefes alıyorsun ama göğsün sanki geç tepki veriyor.||"
        "Ellerini oynatıyorsun… gecikmeli.||"
        "Bedenin burada, sen bir tık geridesin."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Zorla hatırlamaya çalış", "S10_MEMORY_GLITCH", []),
        "2": ("Ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Hiç hareket etme", "END_E02", []),
    },
},

"S09_LOOP_ROOM_3": {
    "text": (
        "Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Duvarlar tanıdık… ama neden tanıdık olduğunu bilmiyorsun.||"
        "Bir şeyi az önce gördün gibi.||"
        "Hatırlamayı denedikçe aklın kayıyor."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Hatırayı zorla", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Gözlerini kapat", "END_E03", []),
    },
},

"S09_LOOP_ROOM_4": {
    "text": (
        "Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Oda bu sefer sessiz değil.||"
        "Sessizlik… seni izliyor gibi.||"
        "Bir suç duygusu geliyor, ama kime ait bilmiyorsun."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Artık kaçma", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E04", []),
    },
},


    "S10_MEMORY_GLITCH": {
        "text": (
            "Başın dönüyor.||"
            "Bir an her şey üst üste biniyor.||"
            "Koridor.\n"
            "Sesler.\n"
            "Bir tartışma."
        ),
"images": [
    "images/s10_glitch.png",     # SOL (blur loop bu olacak)
    "images/s10_center.png",     # ORTA (sabit)
    "images/s10_right.png",      # SAĞ (sabit)
],
        "choices": {
            "1": ("Hatırayı zorla", "S14_PRE_CONFRONT", []),
            "2": ("Kendini durdur", "S09_LOOP_ROOM", []),
            "3": ("Sesin peşinden git", "S04_CORRIDOR", []),
        },
    },

"S11_CAMERA_ROOM": {
    "layout": "single_focus",
    "image": "images/s11_camera_room.png",
    "text": "Kamera odasındasın.||Ekranlar açık.||Koridorda biri var.",
        "choices": {
            "1": ("Kayıtları izle", "S11.1_CAMERA_REALIZATION", []),
            "2": ("Tüm Ekranları kapat", "END_E03", []),
            "3": ("Odadan çık", "S04_CORRIDOR_After_camera", []),
        },
    },
"S11.1_CAMERA_REALIZATION": {
    "text": (
        "Görüntüdeki kişi başını çeviriyor.||"
        "Görüntüdüki kişi gözüküyor ama net değil."
    ),
    "images": [None, "images/s11_camera_you.png", None],
    "choices": {
        "1": ("Kamerayı kapat", "S11.2_CAMERA_ZOOM", []),
         "2": ("Kamerayı kapat",  "END_E03", []),
         "3": ("Geri çekil", "S04_CORRIDOR_After_camera", []),
    },
},
"S11.2_CAMERA_ZOOM": {
    "text": (
        "Yakınlaştırıyorsun.||"
        "Pikseller büyüyor, görüntü daha da bozuluyor.||"
        "Ama bir anlığına…||"
        "yüz hatları tanıdık geliyor.||"
        "Çok tanıdık"
        "Sanki aynaya bakmak gibi ama farklı."
    ),
    "images": [None, "images/s11_camera_you_close.png", None],
    "choices": {
        "1": ("Artık burda işin \n kalmadı odadan çık", "S04_CORRIDOR_After_camera", []),
        "2": ("Bir kez daha zoom", "S11.3_CAMERA_ZOOM_BREAK", []),
    },
},
"S11.3_CAMERA_AUTO_SHUTDOWN": {
    "text": (
        "Bir kez daha yakınlaştırıyorsun.||"
        "Ekran bir an donar.||"
        "Sonra monitörler tek tek sönmeye başlar.||"
        "Odanın ışığı da zayıflıyor.||"
        "Karanlıkta kalmak… iyi bir fikir değil.||"
        "Geri çekilip kapıdan çıkıyorsun."
    ),
    "images": [None, "images/s11_camera_shutdown.png", None],
    "choices": {
        "1": ("Çık", "S04_CORRIDOR_After_camera", []),
    },
},

    "S12_CAMERA_HINT": {
"text": (
    "Gelip kapıyı dinliyor.\n"
    "Ama yürüşüşü.\n\n"
    "Durma ...\n"
    "Sanki senmişsin  gibi."
),
        "image": "images/s12_camera_hint.png",
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Geri çekil", "S04_CORRIDOR_After_camera", []),
            "3": ("Bunu aklında tut", "S10_MEMORY_GLITCH", []),
        },
    },

    # -------- PART 3 (TR) --------

    "S13_JANITOR_DIALOGUE": {
        "text": (
            "Temizlikçi arabaya yaslanıp seni süzüyor.\n\n"
            "\"Yine sen mi?\" diyor.\n"
            "\"Geçen sefer de aynı saatti. 02:17.\"\n\n"
            "Korkmuş gibi değil.\n"
            "Yorgun gibi."
        ),
        "image": "images/s13_janitor_dialogue.png",
        "choices": {
            "1": ("\"Geçen sefer\" ne demek?", "S16_JANITOR_INFO", []),
            "2": ("Görmezden gel ve uzaklaş", "S04_CORRIDOR", []),
            "3": ("Yalan söylediğini ima et", "S17_JANITOR_REACT", []),
        },
    },

    "S14_PRE_CONFRONT": {
        "text": (
            "Nefesin hızlanıyor.\n"
            "Zihninde görüntüler parçalanıp birleşiyor.\n\n"
            "Bir tartışma.\n"
            "Bir kapı.\n"
            "Bir cümle:\n"
            "\"Kimse bilmemeli.\""
        ),
        "image": "images/s14_pre_confront.png",
        "choices": {
            "1": ("Hatırayı kabul et", "S18_ACCEPT_MEMORY", ["O4"]),
            "2": ("Reddet", "S09_LOOP_ROOM", []),
            "3": ("Odaklan ve yürümeye devam et", "S04_CORRIDOR", []),
        },
    },

    "S15_CAMERA_TRUTH": {
        "text": (
            "Kayıt başlıyor.\n"
            "Koridor görünüyor.\n\n"
            "Sonra... sen.\n"
            "Ama yürüyüşün tuhaf.\n"
            "Acele yok.\n"
            "Sanki bekliyorsun.\n\n"
            "Köşede zaman damgası:\n"
            "02:17"
        ),
        "image": "images/s15_camera_truth.png",
        "choices": {
            "1": ("İleri sar", "S19_CAMERA_ADVANCE", []),
            "2": ("Ekranı telefonla kaydet", "S20_SAVE_PROOF", []),
            "3": ("Panikle çık", "S04_CORRIDOR", []),
        },
    },

    "S16_JANITOR_INFO": {
        "text": (
            "Bir süre susuyor.\n"
            "\"Bazı geceler burada tekrar eder,\" diyor.\n\n"
            "\"İnsanlar ya fark etmez...\n"
            "ya da fark ettiğinde çok geç olur.\"\n\n"
            "Sonra fısıldıyor:\n"
            "\"Kamera odasına gittin mi?\""
        ),
        "image": "images/s16_janitor_info.png",
        "choices": {
            "1": ("Evet de (kayıttan bahset)", "S21_JANITOR_PROOF", []),
            "2": ("Hayır de (yalan söyle)", "S17_JANITOR_REACT", []),
            "3": ("Ayak seslerini sor", "S22_JANITOR_FOOTSTEPS", []),
        },
    },

    "S17_JANITOR_REACT": {
        "text": (
            "Gözlerini kısıyor.\n"
            "\"Hâlâ inkâr ediyorsun,\" diyor.\n\n"
            "Arabayı yavaşça itiyor.\n"
            "\"O zaman yine olur.\""
        ),
        "image": "images/s17_janitor_react.png",
        "choices": {
            "1": ("Peşinden git", "S22_JANITOR_FOOTSTEPS", []),
            "2": ("Kamera odasına dön", "S07_CAMERA_DOOR", []),
            "3": ("Odaya kaç", "S09_LOOP_ROOM", []),
        },
    },

 
    # -------- Erken Sonlar (TR) --------
    "END_E01": {"text": "Gözlerini kapatırsın.\nAyak sesleri durur.\n\nSaat değişmez.\nHâlâ 02:17.", "image": "images/end_e01.png", "ending": True},
    "END_E02": {"text": "Kıpırdamazsın.\nTik… tak…\n\nAyak sesleri yaklaşır.\nBu sefer durmaz.", "image": "images/end_e02.png", "ending": True},
    "END_E03": {"text": "Böyle bi ortamda karanlıkta kalmak pekte iyi bi fikir değil.", "image": "images/end_e03.png", "ending": True},
    "END_E04": {"text": "Fişi çekersin.\nEkranlar söner.\nIşıklar söner.\n\nKaranlık.\n\nSonra ayak sesleri başlar.\nÇıkış yok.", "image": "images/end_e04.png", "ending": True},
    "END_E05": {"text": "Kayıtları silersin.\nBir saniyelik rahatlama.\n\nSonra ekranlar şunu yazar:\n02:17\n\nAltında:\n\"TEKRAR DENE.\"", "image": "images/end_e05.png", "ending": True},
    "END_E06": {"text": "Gözlerini kapatırsın.\n\nAçtığında tekrar yatağındasın.\n02:17.\nVe nefes daha yakın.", "image": "images/end_e06.png", "ending": True},
    "END_E07": {"text": "Gözlerini kapatırsın.\n\nAlarm sönümlenir.\nNefes sönümlenmez.\n02:17 kalır.", "image": "images/end_e07.png", "ending": True},
    "END_E08": {"text": "Çığlığın binada yankılanır.\n\nKimse cevap vermez.\nSadece 02:17’nin sesi kalır.", "image": "images/end_e08.png", "ending": True},
    "END_E09": {"text": "Her şeyi reddedersin.\n\nBina bırakır.\nAma sen bırakamazsın.\n02:17 seninle kalır.", "image": "images/end_e09.png", "ending": True},
    "END_E10": {"text": "Kapıyı kapatırsın.\n\nBir kilit sesi.\nBu sefer içeride kalan sensin.", "image": "images/end_e10.png", "ending": True},
    "END_CAUGHT_WHILE_REALIZING": {
    "text": (
        "Kaçmıyorsun.||"
        "Bakıyorsun.||"
        "Yüz hatları tanıdık… ama nedenini çıkaramıyorsun.|||"
        "Bu an çok kısa sürüyor.||"
        "Arkana dönmeye fırsatın olmuyor.||"
        "Bir kol göğsünü sıkıca kavrıyor.|||"
        "Nefesin kesiliyor.||"
        "Bu gücü tanıyorsun.||"
        "Direnmiyorsun bile.|||"
        "Çünkü geç kaldığını biliyorsun.||"
        "Bir süre sonra yatağındasın.||"
        "Kolların ve bacakların bağlı.|||"
        "Oda karanlık.||"
        "Saat: 02:17.||"
        "Bu sefer kaçmayı denemedin bile."
    ),
    "ending": "CAUGHT_WHILE_REALIZING"
}

}

