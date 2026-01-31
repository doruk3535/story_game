
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
        "Your phone screen is on, but there's no notification||.\n"
        "You hear steady footsteps from the corridor||.\n"
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
            "You’re at the door.\n"
            "The footsteps stop right in front of it.\n\n"
            "Someone is listening."
        ),
        "image": "images/s02_door.png",
        "choices": {
            "1": ("Open the door", "S04_CORRIDOR", []),
            "2": ("Lock the door", "S09_LOOP_ROOM", []),
            "3": ("Look under the door", "S05_FOOTPRINT", []),
        },
    },

    "S03_PHONE_LOCK": {
        "text": (
            "On the lock screen you see an old notification.\n"
            "Not from today.\n\n"
            "Sender: Unknown."
        ),
        "image": "images/s03_phone.png",
        "choices": {
            "1": ("Open the notification", "S04_CORRIDOR", ["O2"]),
            "2":  ("Turn the phone off", "S09_LOOP_ROOM", []),
            "3": ("Open the gallery", "S06_GALLERY", []),
        },
    },

    "S04_CORRIDOR": {
        "text": (
            "The corridor is empty.\n"
            "The lights flicker softly.\n\n"
            "The footsteps are gone."
        ),
        "image": "images/s04_corridor.png",
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
            "You don’t remember most of them.\n\n"
            "One stands out:\n"
            "The corridor.\n"
            "Night.\n"
            "And you."
        ),
        "image": "images/s06_gallery.png",
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
        "image": "images/s07_camera_door.png",
        "choices": {
            "1": ("Open the door", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Listen closely", "S12_CAMERA_HINT", []),
            "3": ("Back away", "S04_CORRIDOR", []),
        },
    },

    "S08_JANITOR": {
        "text": (
            "Someone stands beside the cleaning cart.\n"
            "The night janitor.\n\n"
            "He frowns when he sees you.\n"
            "As if he knows you."
        ),
        "image": "images/s08_janitor.png",
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
        "Saat 02:17.\n"
        "Telefon ekranın açık ama bildirim yok.||\n"
        "Koridordan düzenli ayak sesleri geliyor.||\n"
        "Çok düzenli."
    ),
    "images": [
        "images/s01_1_phone.png",
        "images/s01_2.png",
        "images/s01_3.png",
    ],
    "end_sound": "footstep",
    "choices": {
        "1": ("Kapıya yaklaş", "S02_CORRIDOR_ENTRY", []),
        "2": ("Telefonuna bak", "S03_PHONE_LOCK", []),
        "3": ("Uyumaya çalış", "END_E01", []),
    },
},


    "S02_CORRIDOR_ENTRY": {
        "text": (
            "Kapının önündesin.\n"
            "Ayak sesleri kapının tam önünde duruyor.\n\n"
            "Biri seni dinliyor."
        ),
        "image": "images/s02_door.png",
        "choices": {
            "1": ("Kapıyı aç", "S04_CORRIDOR", []),
            "2": ("Kapıyı kilitle", "S09_LOOP_ROOM", []),
            "3": ("Kapının altına bak", "S05_FOOTPRINT", []),
        },
    },

    "S03_PHONE_LOCK": {
        "text": (
            "Kilit ekranında eski bir bildirim görüyorsun.\n"
            "Bugüne ait değil.\n\n"
            "Gönderen: Bilinmiyor."
        ),
        "image": "images/s03_phone.png",
        "choices": {
            "1": ("Bildirimi aç", "S04_CORRIDOR", ["O2"]),
            "2":  ("Telefonu kapat", "S09_LOOP_ROOM", []),
            "3": ("Galeriyi aç", "S06_GALLERY", []),
        },
    },

    "S04_CORRIDOR": {
        "text": (
            "Koridor boş.\n"
            "Işıklar hafifçe titriyor.\n\n"
            "Ayak sesleri kaybolmuş."
        ),
        "image": "images/s04_corridor.png",
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("Temizlik arabasına yaklaş", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
        },
    },

    "S05_FOOTPRINT": {
        "text": (
            "Yerde bir ayakkabı izi.\n\n"
            "Seninkiyle aynı."
        ),
        "image": "images/s05_footprint.png",
        "choices": {
            "1": ("İzi takip et", "S04_CORRIDOR", []),
            "2": ("Görmezden gel", "S09_LOOP_ROOM", []),
            "3": ("Fotoğraf çek", "S06_GALLERY", []),
        },
    },

    "S06_GALLERY": {
        "text": (
            "Galerinde eski fotoğraflar var.\n"
            "Çoğunu hatırlamıyorsun.\n\n"
            "Ama biri öne çıkıyor:\n"
            "Koridor.\n"
            "Gece.\n"
            "Ve sen."
        ),
        "image": "images/s06_gallery.png",
        "choices": {
            "1": ("Fotoğrafı incele", "S10_MEMORY_GLITCH", []),
            "2": ("Galeriden çık", "S04_CORRIDOR", []),
            "3": ("Fotoğrafı sil", "S09_LOOP_ROOM", []),
        },
    },

    "S07_CAMERA_DOOR": {
        "text": (
            "Kamera odasının kapısındasın.\n"
            "İçeriden hafif bir uğultu geliyor.\n\n"
            "Kilitli değil."
        ),
        "image": "images/s07_camera_door.png",
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Daha dikkatli dinle", "S12_CAMERA_HINT", []),
            "3": ("Geri çekil", "S04_CORRIDOR", []),
        },
    },

    "S08_JANITOR": {
        "text": (
            "Temizlik arabasının yanında biri duruyor.\n"
            "Gece temizlikçisi.\n\n"
            "Seni görünce kaşlarını çatıyor.\n"
            "Sanki seni tanıyor."
        ),
        "image": "images/s08_janitor.png",
        "choices": {
            "1": ("Onunla konuş", "S13_JANITOR_DIALOGUE", ["O3"]),
            "2": ("Sessizce uzaklaş", "S04_CORRIDOR", []),
            "3": ("Koş", "S09_LOOP_ROOM", []),
        },
    },

    "S09_LOOP_ROOM": {
        "text": (
            "Yatağındasın.\n"
            "Aynı oda.\n\n"
            "Yine 02:17.\n"
            "Ama bu sefer fark ediyorsun."
        ),
        "image": "images/s09_loop_room.png",
        "choices": {
            "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
            "2": ("Hızla ayağa kalk", "S04_CORRIDOR", []),
            "3": ("Kıpırdama", "END_E02", []),
        },
    },

    "S10_MEMORY_GLITCH": {
        "text": (
            "Başın dönüyor.\n"
            "Bir an her şey üst üste biniyor.\n\n"
            "Koridor.\n"
            "Sesler.\n"
            "Bir tartışma."
        ),
        "image": "images/s10_glitch.png",
        "choices": {
            "1": ("Hatırayı zorla", "S14_PRE_CONFRONT", []),
            "2": ("Kendini durdur", "S09_LOOP_ROOM", []),
            "3": ("Sesin peşinden git", "S04_CORRIDOR", []),
        },
    },

    "S11_CAMERA_ROOM": {
        "text": (
            "Kamera odasındasın.\n"
            "Ekranlarda koridor görünüyor.\n\n"
            "Bir ekranda...\n"
            "Sen varsın."
        ),
        "image": "images/s11_camera_room.png",
        "choices": {
            "1": ("Kayıtları izle", "S15_CAMERA_TRUTH", []),
            "2": ("Ekranları kapat", "END_E03", []),
            "3": ("Odayı terk et", "S04_CORRIDOR", []),
        },
    },

    "S12_CAMERA_HINT": {
        "text": (
            "Kapının önünde dinliyorsun.\n"
            "İçeride kimse yok.\n\n"
            "Ama ekranların ışığı yanıyor."
        ),
        "image": "images/s12_camera_hint.png",
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("Geri çekil", "S04_CORRIDOR", []),
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

    "S18_ACCEPT_MEMORY": {
        "text": (
            "Gözlerini kapatıyorsun.\n"
            "Bu sefer kaçmıyorsun.\n\n"
            "Bir yüz—bulanık.\n"
            "Ama ses net:\n"
            "\"Kapıyı kapat.\"\n\n"
            "Ve senin cevabın:\n"
            "\"Hayır.\"\n\n"
            "Göğsün sıkışıyor.\n"
            "Bu anı yaşadığını biliyorsun."
        ),
        "image": "images/s18_accept_memory.png",
        "choices": {
            "1": ("Koridora çık—gerçeği ara", "S04_CORRIDOR", []),
            "2": ("Temizlikçiyi bul (tanık)", "S08_JANITOR", []),
            "3": ("Kamera odasına git (kanıt)", "S07_CAMERA_DOOR", []),
        },
    },

    "S19_CAMERA_ADVANCE": {
        "text": (
            "İleri sarıyorsun.\n\n"
            "Video takılıyor.\n"
            "Görüntü bozuluyor.\n\n"
            "Sonra—tek bir kare:\n"
            "Kamera senden uzaklaşıp...\n"
            "sana bakan şeye dönüyor.\n\n"
            "Net değil.\n"
            "Sadece bir gölge."
        ),
        "image": "images/s19_camera_advance.png",
        "choices": {
            "1": ("Defalarca tekrar oynat", "S23_CAMERA_LOOP", []),
            "2": ("Tarihe bak", "S24_CAMERA_DATE", []),
            "3": ("Fişi çek", "END_E04", []),
        },
    },

    "S20_SAVE_PROOF": {
        "text": (
            "Ekranı kaydediyorsun.\n"
            "Dosya kaydoluyor.\n\n"
            "Ama galeride...\n"
            "yok.\n\n"
            "Sadece boş bir küçük resim kalmış.\n"
            "İsmi:\n"
            "0217.mp4"
        ),
        "image": "images/s20_save_proof.png",
        "choices": {
            "1": ("Dosyayı açmayı dene", "S25_FILE_OPEN", []),
            "2": ("Temizlikçiye göster", "S13_JANITOR_DIALOGUE", []),
            "3": ("Çık", "S04_CORRIDOR", []),
        },
    },

    "S21_JANITOR_PROOF": {
        "text": (
            "Nefesini tutuyor.\n"
            "\"Göster,\" diyor.\n\n"
            "Anlatınca yüzü soluyor.\n"
            "\"Kayıtlar bazen kaybolur.\n"
            "Çünkü o gece kendini saklar.\""
        ),
        "image": "images/s21_janitor_proof.png",
        "choices": {
            "1": ("Zorla: O gece ne oldu?", "S26_TRUTH_PRESSURE", []),
            "2": ("\"Beni buradan çıkar\" de", "S27_ESCAPE_HINT", []),
            "3": ("Kamera odasına koş", "S11_CAMERA_ROOM", []),
        },
    },

    "S22_JANITOR_FOOTSTEPS": {
        "text": (
            "Koridora bakıyor.\n"
            "\"Ayak sesleri bazen seni taklit eder,\" diyor.\n\n"
            "\"Çünkü bazı geceler burası seninle dolu olur.\n"
            "Yaptıklarınla.\n"
            "Bırakmadıklarınla.\""
        ),
        "image": "images/s22_janitor_footsteps.png",
        "choices": {
            "1": ("Ben ne bıraktım?", "S26_TRUTH_PRESSURE", []),
            "2": ("Yangın merdivenine yönel", "S28_FIRE_STAIRS_DOOR", []),
            "3": ("Odaya dön", "S09_LOOP_ROOM", []),
        },
    },

    "S23_CAMERA_LOOP": {
        "text": (
            "Aynı anı tekrar tekrar izliyorsun.\n\n"
            "Gölge her seferinde farklı gibi.\n"
            "Ama bir şey sabit:\n"
            "Sen geri çekilmiyorsun.\n\n"
            "Sanki onu çağırmış gibisin."
        ),
        "image": "images/s23_camera_loop.png",
        "choices": {
            "1": ("Dur ve çık", "S04_CORRIDOR", []),
            "2": ("Gölgeyi büyüt", "S29_ENHANCE", []),
            "3": ("Temizlikçiyi bul", "S08_JANITOR", []),
        },
    },

    "S24_CAMERA_DATE": {
        "text": (
            "Tarihe bakıyorsun.\n\n"
            "Bugün değil.\n"
            "Hatta gün bile yazmıyor.\n\n"
            "Sadece:\n"
            "02:17\n"
            "02:17\n"
            "02:17\n\n"
            "Sanki kayıt tek bir saniyenin içine sıkışmış."
        ),
        "image": "images/s24_camera_date.png",
        "choices": {
            "1": ("Klibi dışa aktarmayı dene", "S25_FILE_OPEN", []),
            "2": ("Kamera odasından çık", "S04_CORRIDOR", []),
            "3": ("Her şeyi silmeyi düşün", "S30_DELETE_DILEMMA", []),
        },
    },

    "S25_FILE_OPEN": {
        "text": (
            "0217.mp4 dosyasını açıyorsun.\n"
            "Siyah ekran.\n\n"
            "Sonra bir ses:\n"
            "\"Kapıyı kapat.\"\n\n"
            "Bu... senin sesin."
        ),
        "image": "images/s25_file_open.png",
        "choices": {
            "1": ("Sesi takip et (koridora)", "S04_CORRIDOR", []),
            "2": ("Temizlikçiye dinlet", "S13_JANITOR_DIALOGUE", []),
            "3": ("Telefonu fırlat", "S09_LOOP_ROOM", []),
        },
    },

    "S26_TRUTH_PRESSURE": {
        "text": (
            "Temizlikçi uzun süre susuyor.\n\n"
            "\"Bazı geceler biri bir kapının önünde durur,\" diyor.\n"
            "\"Kapı açılır.\n"
            "Ve kimse içeri girmez.\n\n"
            "Sadece... seni içeride bırakır.\""
        ),
        "image": "images/s26_truth_pressure.png",
        "choices": {
            "1": ("Bunu ben mi yaptım?", "S14_PRE_CONFRONT", []),
            "2": ("Bunu nasıl bitiririm?", "S27_ESCAPE_HINT", []),
            "3": ("Kamera odasına koş", "S07_CAMERA_DOOR", []),
        },
    },

    "S27_ESCAPE_HINT": {
        "text": (
            "Yangın merdivenini işaret ediyor.\n"
            "\"Alarm,\" diyor.\n\n"
            "\"Bazen herkes uyanırsa...\n"
            "bu saat bırakır.\""
        ),
        "image": "images/s27_escape_hint.png",
        "choices": {
            "1": ("Yangın merdivenine git", "S28_FIRE_STAIRS_DOOR", []),
            "2": ("Önce kanıt al", "S11_CAMERA_ROOM", []),
            "3": ("Odaya dön (hazırlan)", "S09_LOOP_ROOM", []),
        },
    },

    "S28_FIRE_STAIRS_DOOR": {
        "text": (
            "Yangın merdiveni kapısındasın.\n"
            "Aralıktan soğuk hava vuruyor.\n\n"
            "Aşağıdan hafif bir metal sesi geliyor.\n"
            "Sanki biri basamaklarda bekliyor."
        ),
        "image": "images/s28_fire_stairs_door.png",
        "choices": {
            "1": ("Aç ve aşağı in", "S31_FIRE_STAIRS", []),
            "2": ("Kapat ve geri dön", "S04_CORRIDOR", []),
            "3": ("Kapıda dinle", "S32_STAIRS_LISTEN", []),
        },
    },

    "S29_ENHANCE": {
        "text": (
            "Yakınlaştırıyorsun.\n"
            "Pikseller dağılıyor.\n\n"
            "Ama bir detay seçiliyor:\n"
            "Gölge elinde bir şey tutuyor—anahtar gibi.\n\n"
            "Üzerinde bir etiket:\n"
            "\"217\""
        ),
        "image": "images/s29_enhance.png",
        "choices": {
            "1": ("Koridorda '217'yi ara", "S04_CORRIDOR", []),
            "2": ("Temizlikçiye anlat", "S13_JANITOR_DIALOGUE", []),
            "3": ("Çıkıp odaya dön", "S09_LOOP_ROOM", []),
        },
    },

    "S30_DELETE_DILEMMA": {
        "text": (
            "Silme ekranı.\n"
            "Parmağın 'Sil' üzerinde.\n\n"
            "Sanki bu her şeyi bitirebilir.\n"
            "Ya da daha kötüsünü başlatabilir."
        ),
        "image": "images/s30_delete_dilemma.png",
        "choices": {
            "1": ("Silme", "S15_CAMERA_TRUTH", []),
            "2": ("Sil", "END_E05", []),
            "3": ("Bırak ve çık", "S04_CORRIDOR", []),
        },
    },

    "S31_FIRE_STAIRS": {
        "text": (
            "Yangın merdivenindesin.\n"
            "Basamaklar buz gibi.\n\n"
            "Yukarıdaki kapı yavaşça kapanıyor.\n"
            "Aşağıdan bir adım sesi geliyor.\n\n"
            "Senin ritminde."
        ),
        "image": "images/s31_fire_stairs.png",
        "choices": {
            "1": ("Aşağı in", "S33_DOWNSTAIRS", []),
            "2": ("Yukarı çık", "S04_CORRIDOR", []),
            "3": ("Bekle", "S34_STANDOFF", []),
        },
    },

    "S32_STAIRS_LISTEN": {
        "text": (
            "Kulağını kapıya dayıyorsun.\n\n"
            "Aşağıdan...\n"
            "tek bir kelime.\n\n"
            "\"Aç.\""
        ),
        "image": "images/s32_stairs_listen.png",
        "choices": {
            "1": ("Kapıyı aç", "S31_FIRE_STAIRS", []),
            "2": ("Uzaklaş", "S04_CORRIDOR", []),
            "3": ("Odaya dön", "S09_LOOP_ROOM", []),
        },
    },

    "S33_DOWNSTAIRS": {
        "text": (
            "Bir kat aşağı.\n"
            "Kapı numaraları yanlış gibi.\n\n"
            "Sanki binanın başka bir versiyonu.\n"
            "Ve burada...\n"
            "saat yok."
        ),
        "image": "images/s33_downstairs.png",
        "choices": {
            "1": ("Koridora gir", "S35_ALT_CORRIDOR", []),
            "2": ("Geri yukarı çık", "S31_FIRE_STAIRS", []),
            "3": ("Nefeslen", "S14_PRE_CONFRONT", []),
        },
    },

    "S34_STANDOFF": {
        "text": (
            "Bekliyorsun.\n"
            "Ayak sesleri yaklaşıyor.\n\n"
            "Karanlıkta bir şekil beliriyor.\n"
            "Senin boyunda.\n"
            "Senin yürüyüşünde.\n\n"
            "Duruyor.\n"
            "Tam karşında."
        ),
        "image": "images/s34_standoff.png",
        "choices": {
            "1": ("Konuş: Sen kimsin?", "S36_SHADOW_TALK", []),
            "2": ("Geri kaç", "S04_CORRIDOR", []),
            "3": ("Üzerine yürü", "S37_PHYSICAL", ["O4"]),
        },
    },

    "S35_ALT_CORRIDOR": {
        "text": (
            "Alt koridor sessiz.\n"
            "Duvarlarda eski duyurular.\n\n"
            "Birinde senin adın yazıyor.\n"
            "Tarih yok.\n\n"
            "Sadece:\n"
            "02:17"
        ),
        "image": "images/s35_alt_corridor.png",
        "choices": {
            "1": ("Duyuruyu sök", "S14_PRE_CONFRONT", []),
            "2": ("Sona doğru yürü", "S38_STORAGE_DOOR", []),
            "3": ("Geri dön", "S31_FIRE_STAIRS", []),
        },
    },

    "S36_SHADOW_TALK": {
        "text": (
            "Konuşmuyor.\n"
            "Ama senin gibi nefes alıyor.\n\n"
            "Bir adım atıyor.\n"
            "Sonra duruyor.\n\n"
            "Kararını bekliyor."
        ),
        "image": "images/s36_shadow_talk.png",
        "choices": {
            "1": ("Yaklaş—yüzünü gör", "S37_PHYSICAL", ["O4"]),
            "2": ("Kapıyı çarpıp kaç", "S31_FIRE_STAIRS", []),
            "3": ("Gözlerini kapat", "END_E06", []),
        },
    },

    "S37_PHYSICAL": {
        "text": (
            "Ona dokunuyorsun.\n\n"
            "Soğuk.\n"
            "Gerçek.\n\n"
            "Bir an ikiniz de aynı anda konuşuyorsunuz:\n"
            "\"Bunu ben başlattım.\""
        ),
        "image": "images/s37_physical.png",
        "choices": {
            "1": ("Kabul et", "S14_PRE_CONFRONT", ["O4"]),
            "2": ("İnkâr et", "S09_LOOP_ROOM", []),
            "3": ("Alarmı bulmaya karar ver", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S38_STORAGE_DOOR": {
        "text": (
            "Bir depo kapısı.\n"
            "Eski etiket:\n"
            "\"Kayıp Eşya\"\n\n"
            "Aralıktan ışık sızıyor."
        ),
        "image": "images/s38_storage_door.png",
        "choices": {
            "1": ("İçeri gir", "S39_STORAGE_INSIDE", []),
            "2": ("Kapat ve uzaklaş", "S35_ALT_CORRIDOR", []),
            "3": ("Aralıktan bak", "S40_STORAGE_PEEK", []),
        },
    },

    "S39_STORAGE_INSIDE": {
        "text": (
            "Her yerde kutular.\n"
            "Bazıları zaten açık.\n\n"
            "Bir kutunun içinde:\n"
            "senin anahtarlığın.\n\n"
            "Kaybettiğini sanıyordun."
        ),
        "image": "images/s39_storage_inside.png",
        "choices": {
            "1": ("Anahtarlığı al", "S14_PRE_CONFRONT", []),
            "2": ("Kutuyu kapatıp çık", "S35_ALT_CORRIDOR", []),
            "3": ("Altına bak", "S41_HINT_ALARM", []),
        },
    },

    "S40_STORAGE_PEEK": {
        "text": (
            "İçeride kimse yok.\n"
            "Ama ortada bir sandalye var.\n\n"
            "Sanki biri saniyeler önce kalkmış.\n\n"
            "Sandalyenin arkasında:\n"
            "alarm erişim kartı."
        ),
        "image": "images/s40_storage_peek.png",
        "choices": {
            "1": ("İçeri girip kartı al", "S41_HINT_ALARM", []),
            "2": ("Geri çekil", "S35_ALT_CORRIDOR", []),
            "3": ("Yukarı koş", "S31_FIRE_STAIRS", []),
        },
    },

    "S41_HINT_ALARM": {
        "text": (
            "Elinde küçük bir kart.\n"
            "Üzerinde:\n"
            "\"ALARM PANELİ - YETKİ\"\n\n"
            "Altında aynı sayı:\n"
            "02:17"
        ),
        "image": "images/s41_hint_alarm.png",
        "choices": {
            "1": ("Yangın merdivenine dön", "S28_FIRE_STAIRS_DOOR", []),
            "2": ("Alarm paneline git", "S42_ALARM_PANEL", []),
            "3": ("Odaya dön ve düşün", "S09_LOOP_ROOM", []),
        },
    },

    # -------- PART 4 (TR) --------

    "S42_ALARM_PANEL": {
        "text": (
            "Alarm panelinin önündesin.\n"
            "Kırmızı kapak yarı açık.\n\n"
            "Ekranda tek satır yanıp sönüyor:\n"
            "02:17\n\n"
            "Sanki seni bekliyor."
        ),
        "image": "images/s42_alarm_panel.png",
        "choices": {
            "1": ("Alarmı çalıştır", "S43_ALARM_TRIGGER", ["O5"]),
            "2": ("Paneli incele", "S44_ALARM_LOGS", []),
            "3": ("Geri çekil", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S43_ALARM_TRIGGER": {
        "text": (
            "Kapağı tamamen kaldırıyorsun.\n"
            "Parmağın düğmeye basıyor.\n\n"
            "Bir saniyelik sessizlik...\n"
            "sonra bina alarmla patlıyor.\n\n"
            "Işıklar birden yanıyor."
        ),
        "image": "images/s43_alarm_trigger.png",
        "choices": {
            "1": ("Aşağı koş", "S45_ALARM_ESCAPE", []),
            "2": ("Koridora çık", "S46_ALARM_CORRIDOR", []),
            "3": ("Kal ve dinle", "S47_ALARM_WAIT", []),
        },
    },

    "S44_ALARM_LOGS": {
        "text": (
            "Panelin içinde eski kayıtlar var.\n"
            "Çoğu tarihsiz.\n\n"
            "Ama saat tekrar ediyor:\n"
            "02:17\n"
            "02:17\n"
            "02:17\n\n"
            "Bazı satırlarda senin adın geçiyor."
        ),
        "image": "images/s44_alarm_logs.png",
        "choices": {
            "1": ("Kayıtları oku", "S48_LOG_REALIZATION", []),
            "2": ("Şimdi alarmı çalıştır", "S43_ALARM_TRIGGER", ["O5"]),
            "3": ("Panelden uzaklaş", "S28_FIRE_STAIRS_DOOR", []),
        },
    },

    "S45_ALARM_ESCAPE": {
        "text": (
            "Merdivenlerden aşağı sprint atıyorsun.\n"
            "Alarm ve ayak sesleri birbirine karışıyor.\n\n"
            "Ama aşağıda ses değişiyor.\n"
            "Alarm değil...\n"
            "nefes alan bir şey."
        ),
        "image": "images/s45_alarm_escape.png",
        "choices": {
            "1": ("Koşmaya devam et", "S49_EXIT_DOOR", []),
            "2": ("Durup arkana bak", "S34_STANDOFF", []),
            "3": ("Alt koridora kır", "S35_ALT_CORRIDOR", []),
        },
    },

    "S46_ALARM_CORRIDOR": {
        "text": (
            "Koridor artık aydınlık.\n"
            "Kapılar yarı aralık.\n\n"
            "İnsan yok.\n\n"
            "Alarm burada boğuk.\n"
            "Sanki duvarların içinden geliyor."
        ),
        "image": "images/s46_alarm_corridor.png",
        "choices": {
            "1": ("Kamera odasına koş", "S11_CAMERA_ROOM", []),
            "2": ("Temizlikçiyi ara", "S08_JANITOR", []),
            "3": ("Odaya dön", "S09_LOOP_ROOM", []),
        },
    },

    "S47_ALARM_WAIT": {
        "text": (
            "Kıpırdamadan duruyorsun.\n\n"
            "Alarm yavaş yavaş sönüyor.\n"
            "Sonra duruyor.\n\n"
            "Sessizlik.\n"
            "Ve yalnız değilsin."
        ),
        "image": "images/s47_alarm_wait.png",
        "choices": {
            "1": ("Arkandaki şeye dön", "S34_STANDOFF", []),
            "2": ("Sessizce uzaklaş", "S46_ALARM_CORRIDOR", []),
            "3": ("Gözlerini kapat", "END_E07", []),
        },
    },

    "S48_LOG_REALIZATION": {
        "text": (
            "Kayıtlar sonunda anlam kazanıyor.\n\n"
            "Alarm her çaldığında biri kayboluyor.\n"
            "Ama bazen...\n"
            "iki kişi beliriyor.\n\n"
            "Biri her zaman sensin.\n"
            "Diğerinin adı yok."
        ),
        "image": "images/s48_log_realization.png",
        "choices": {
            "1": ("Her şey yerine oturuyor (yüzleş)", "S53_ALMOST_END", ["O4"]),
            "2": ("Kayıtları kapat", "S42_ALARM_PANEL", []),
            "3": ("Kamera kaydıyla karşılaştır", "S15_CAMERA_TRUTH", []),
        },
    },

    "S49_EXIT_DOOR": {
        "text": (
            "Acil çıkış.\n"
            "Zincirle kapalı.\n\n"
            "Zincirde bir etiket:\n"
            "\"217\"\n\n"
            "Aynı sayı.\n"
            "Aynı anahtar."
        ),
        "image": "images/s49_exit_door.png",
        "choices": {
            "1": ("Anahtarı dene", "S51_KEY_USE", []),
            "2": ("Zinciri zorla", "S52_FORCE_EXIT", []),
            "3": ("Geri dön", "S45_ALARM_ESCAPE", []),
        },
    },

    "S50_SELF_REALIZE": {
        "text": (
            "Artık inkâr edemiyorsun.\n\n"
            "Seni tutan bina değil.\n"
            "Bu anı tutan sensin.\n\n"
            "02:17 ilerlemeyecek\n"
            "ta ki sen bırakana kadar."
        ),
        "image": "images/s50_self_realize.png",
        "choices": {
            "1": ("Yüzleşmeye git", "S34_STANDOFF", ["O4"]),
            "2": ("Alarm paneline dön", "S42_ALARM_PANEL", []),
            "3": ("Odaya dön (son kez)", "S09_LOOP_ROOM", []),
        },
    },

    "S51_KEY_USE": {
        "text": (
            "Anahtar kusursuz oturuyor.\n\n"
            "Çeviriyorsun.\n"
            "Hiçbir şey açılmıyor.\n\n"
            "Arkandan bir ses:\n"
            "\"Henüz değil.\""
        ),
        "image": "images/s51_key_use.png",
        "choices": {
            "1": ("Sese dön", "S34_STANDOFF", []),
            "2": ("Anahtarı cebine koyup geri çekil", "S45_ALARM_ESCAPE", []),
            "3": ("Anahtarı yere fırlat", "S52_FORCE_EXIT", []),
        },
    },

    "S52_FORCE_EXIT": {
        "text": (
            "Zinciri zorlayınca metal çığlık atıyor.\n\n"
            "Biraz gevşiyor—çok az.\n"
            "Sonra omzunda bir el hissediyorsun.\n\n"
            "Soğuk.\n"
            "Tanıdık."
        ),
        "image": "images/s52_force_exit.png",
        "choices": {
            "1": ("Eli tutup dön", "S37_PHYSICAL", ["O4"]),
            "2": ("Çığlık at", "END_E08", []),
            "3": ("Yere çök", "S47_ALARM_WAIT", []),
        },
    },

    "S53_ALMOST_END": {
        "text": (
            "Her şey yerine oturuyor.\n\n"
            "Kamera.\n"
            "Alarm.\n"
            "Tanık.\n"
            "Ve sen.\n\n"
            "Artık kaçmak yok.\n"
            "Sadece bir seçim."
        ),
        "image": "images/s53_almost_end.png",
        "choices": {
            "1": ("Tamamen kabul et", "S54_FINAL_GATE", []),
            "2": ("Hepsini reddet", "END_E09", []),
            "3": ("Yine de kaçmayı dene", "S45_ALARM_ESCAPE", []),
        },
    },

    "S54_FINAL_GATE": {
        "text": (
            "Bina nefesini tutuyor.\n\n"
            "İlk kez saat titriyor.\n"
            "02:17 sabit değil.\n\n"
            "Geçebilir.\n"
            "Ama bir bedeli var."
        ),
        "image": "images/s54_final_gate.png",
        "choices": {
            "1": ("Bedeli öde", "S55_FINAL_ENTRY", []),
            "2": ("Geri adım at", "S09_LOOP_ROOM", []),
            "3": ("Alarmı bir daha çalıştır", "S43_ALARM_TRIGGER", ["O5"]),
        },
    },

    "S55_FINAL_ENTRY": {
        "text": (
            "Son kapının önündesin.\n\n"
            "Arkasında:\n"
            "ya 02:17 biter\n"
            "ya sen.\n\n"
            "Kapı yavaşça açılıyor."
        ),
        "image": "images/s55_final_entry.png",
        "choices": {
            "1": ("İçeri gir", "FINAL_CHECK", []),
            "2": ("Kapat", "END_E10", []),
            "3": ("Arkaya bak", "S34_STANDOFF", []),
        },
    },

    "FINAL_CHECK": {
        "text": (
            "Her şey donar.\n\n"
            "Buraya nasıl geldiğini hatırlarsın.\n"
            "Ne gördüğünü.\n"
            "Neyi kaydettiğini.\n"
            "Kimin tanık olduğunu.\n"
            "Neyi itiraf ettiğini.\n"
            "Neyi tetiklediğini.\n\n"
            "Saat sana bakar."
        ),
        "image": "images/final_check.png",
        "final_check": True
    },

    # -------- Erken Sonlar (TR) --------
    "END_E01": {"text": "Gözlerini kapatırsın.\nAyak sesleri durur.\n\nSaat değişmez.\nHâlâ 02:17.", "image": "images/end_e01.png", "ending": True},
    "END_E02": {"text": "Kıpırdamazsın.\nTik… tak…\n\nAyak sesleri yaklaşır.\nBu sefer durmaz.", "image": "images/end_e02.png", "ending": True},
    "END_E03": {"text": "Ekranları kapatırsın.\n\nAma hâlâ biri izliyormuş gibi hissedersin.", "image": "images/end_e03.png", "ending": True},
    "END_E04": {"text": "Fişi çekersin.\nEkranlar söner.\nIşıklar söner.\n\nKaranlık.\n\nSonra ayak sesleri başlar.\nÇıkış yok.", "image": "images/end_e04.png", "ending": True},
    "END_E05": {"text": "Kayıtları silersin.\nBir saniyelik rahatlama.\n\nSonra ekranlar şunu yazar:\n02:17\n\nAltında:\n\"TEKRAR DENE.\"", "image": "images/end_e05.png", "ending": True},
    "END_E06": {"text": "Gözlerini kapatırsın.\n\nAçtığında tekrar yatağındasın.\n02:17.\nVe nefes daha yakın.", "image": "images/end_e06.png", "ending": True},
    "END_E07": {"text": "Gözlerini kapatırsın.\n\nAlarm sönümlenir.\nNefes sönümlenmez.\n02:17 kalır.", "image": "images/end_e07.png", "ending": True},
    "END_E08": {"text": "Çığlığın binada yankılanır.\n\nKimse cevap vermez.\nSadece 02:17’nin sesi kalır.", "image": "images/end_e08.png", "ending": True},
    "END_E09": {"text": "Her şeyi reddedersin.\n\nBina bırakır.\nAma sen bırakamazsın.\n02:17 seninle kalır.", "image": "images/end_e09.png", "ending": True},
    "END_E10": {"text": "Kapıyı kapatırsın.\n\nBir kilit sesi.\nBu sefer içeride kalan sensin.", "image": "images/end_e10.png", "ending": True},
}

# ============================================================
# 32 final endings (TR) generated by bitmask 0..31
# ============================================================
for _m in range(32):
    _eid = f"END_F{_m+1:02d}"
    _flags = [EVENT_ORDER[i] for i in range(5) if (_m >> i) & 1]
    _tag = " + ".join(_flags) if _flags else "NO_EVENTS"

    if _m == 0:
        _text = (
            "Son kapıya elinde hiçbir şey olmadan ulaşırsın.\n"
            "Kanıt yok. Tanık yok. İtiraf yok.\n\n"
            "02:17 seni cezalandırmaz.\n"
            "Sadece seni sıfırlar.\n\n"
            "Gözlerini açarsın.\n"
            "02:17."
        )
    elif _m == 31:
        _text = (
            "Her şeyi yaptın.\n"
            "Kayıtları gördün.\n"
            "Mesajı sakladın.\n"
            "Bir tanığın vardı.\n"
            "Kendinle yüzleştin.\n"
            "Binayı uyandırdın.\n\n"
            "İlk kez saat hareket eder.\n"
            "02:17, 02:18 olur.\n\n"
            "Ve koridor sonunda… boş kalır."
        )
    else:
        c = bin(_m).count("1")
        if c == 1:
            _text = (
                f"Sona sadece tek iplikle gelirsin: {_tag}.\n\n"
                "Bu, saati kırmaya yetmez.\n"
                "Ama seni değiştirmeye yeter.\n\n"
                "02:17 devam eder.\n"
                "Sadece artık aynı şekilde değil."
            )
        elif c == 2:
            _text = (
                f"İki parça yerine oturur: {_tag}.\n\n"
                "Kapı açılır—sonra tereddüt eder.\n"
                "Bina seni tanır.\n\n"
                "Bir döngüden çıkarsın.\n"
                "Ama başka bir döngüyü miras alırsın."
            )
        elif c == 3:
            _text = (
                f"Üç gerçek çarpışır: {_tag}.\n\n"
                "Saat çatlar.\n"
                "Tam değil.\n"
                "Sadece bir şeyin sızmasına yetecek kadar.\n\n"
                "Dışarı adım attığında fark edersin:\n"
                "çıkan sadece sen değilsin."
            )
        elif c == 4:
            _text = (
                f"Bir şey hariç her şey tamam: {_tag}.\n\n"
                "Kapı ardına kadar açılır.\n"
                "Koridor nefes alır.\n\n"
                "Neredeyse kazanırsın.\n"
                "Neredeyse, en tehlikeli zaferdir."
            )
        else:
            _text = (
                f"{_tag}.\n\n"
                "Son kapı açılır.\n"
                "Başka bir son elini tutar.\n\n"
                "02:17 bitmez.\n"
                "Sadece nerede devam edeceğini seçer."
            )

    STORY_TR[_eid] = {
        "text": _text,
        "image": f"images/{_eid.lower()}.png",
        "ending": True,
        "mask": _m,
    }