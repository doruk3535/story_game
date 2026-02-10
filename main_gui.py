# -*- coding: utf-8 -*-
# main_gui.py (02:17) - FINAL (INTEGRATED SINGLE_FOCUS HERO MODE) + CONDITIONAL 4TH CHOICE + INVENTORY
# - ✅ Normalde 3 buton görünür
# - ✅ 4. buton SADECE sahnede varsa görünür (choices veya choices_if ile)
# - ✅ choices_if şartı yoksa 4. buton "🔒" kilitli görünür
# - ✅ Inventory (Çanta) overlay: I_* item'ları gösterir
# - ✅ GameState apply_effects aktif (flag + item)
# - ✅ NEW: PAGEBREAK SYSTEM with "|||"
IMAGE_TOKEN = "##"  # hide/ignore in text
#    - "||"  -> segment
#    - "|||" -> page break: stop, wait SPACE, clear screen, continue

import tkinter as tk
import tkinter.font as tkfont
import os
import math
import time
import io
import wave
import struct
import json
import random
import re

import threading
import queue
print("[main_gui] overlay_steps patch v3 loaded")

# ============================
# ✅ PAGEBREAK SYSTEM
# ============================
PAGEBREAK_TOKEN = "|||"  # pagebreak/wait token
PAUSE_CHAR = "□"  # 1 kare = 1 saniye bekleme (metinde görünmez)
OVERLAY_TOKEN = "Ξ"  # ardışık overlay görsel tokenı (ortaya ekler)
_overlay_step_points = []
_overlay_step_fired = set()
PAUSE_MS_PER_CHAR = 1000
waiting_pagebreak = False
_pagebreak_continue_cb = None



# ✅ SPACE spam guard
SPACE_COOLDOWN_MS = 500  # min time between SPACE presses
_last_space_ts = 0.0
_space_down = False  # prevents key-repeat when holding space

class GameState:
    def __init__(self):
        self.flags = set()   # F_* ve O* gibi
        self.items = set()   # I_*

    def apply_effects(self, effects):
        if not effects:
            return
        for e in effects:
            if not isinstance(e, str):
                continue
            e = e.strip()
            if not e:
                continue
            if e.startswith("I_"):
                self.items.add(e)
            else:
                self.flags.add(e)

    def has(self, token: str) -> bool:
        return (token in self.flags) or (token in self.items)


# ✅ Global state (choices_if ve inventory buna bakacak)
STATE = GameState()


def resolve_choices(scene: dict, state: GameState) -> dict:
    """
    choices + choices_if (token varsa) birleştirir.
    """
    choices = dict(scene.get("choices", {}))
    cond = scene.get("choices_if", {})
    if isinstance(cond, dict):
        for token, extra in cond.items():
            if state.has(token) and isinstance(extra, dict):
                choices.update(extra)
    return choices


def resolve_redirect(scene: dict, state: GameState, choice_key: str, choice_tuple):
    """
    redirect_if ile aynı choice_key için hedef sahneyi state'e göre değiştirebilirsin.
    """
    redirect_if = scene.get("redirect_if", {})
    if not isinstance(redirect_if, dict):
        return choice_tuple
    for token, mapping in redirect_if.items():
        if state.has(token) and isinstance(mapping, dict) and choice_key in mapping:
            return mapping[choice_key]
    return choice_tuple


def compute_locked_choices(scene: dict, state: GameState) -> dict:
    """
    choices_if bloklarında, state şartı sağlanmadığı için eklenemeyen seçenekleri
    "locked" olarak döndürür. Örn: {"4": "Kilitli kapıyı aç"}
    """
    locked = {}
    cond = scene.get("choices_if", {})
    if not isinstance(cond, dict):
        return locked

    base_choices = dict(scene.get("choices", {}))

    for token, extra in cond.items():
        if not isinstance(extra, dict):
            continue
        if not state.has(token):
            for k, tup in extra.items():
                if k in base_choices:
                    continue
                try:
                    label = tup[0]
                except Exception:
                    label = "Bilinmeyen"
                locked[str(k)] = str(label)
    return locked


# ----------------------------
# Optional: Pillow for smooth image resizing/animation (recommended)
# ----------------------------
PIL_OK = True
try:
    from PIL import Image, ImageTk, ImageEnhance, ImageFilter
except Exception:
    PIL_OK = False

# ============================================================
# ✅ VIDEO (MP4/MOV) SUPPORT for single_focus (hero)
# - Uses imageio + imageio-ffmpeg (no system ffmpeg needed)
# - Updates the EXISTING hero canvas item (no stacking)
# - Stops/cleans up on every scene change
# ============================================================
VIDEO_OK = True
try:
    import imageio.v2 as imageio  # imageio>=2
except Exception:
    try:
        import imageio  # fallback
    except Exception as _e:
        VIDEO_OK = False
        imageio = None
        print("[VIDEO] imageio not available:", _e)

# ----------------------------
# ✅ VIDEO (MP4/MOV) PLAYBACK (thread-buffered, fast-start, no UI freeze)
#    Scene usage example:
#      "video": {"path": "images/portal_anim/portal.mp4", "fps": 24, "loop": True}
# ----------------------------

# Video state
_video_cfg = None
_video_active_scene = None

_video_job = None               # tk after() id for UI tick
_video_thread = None            # background decoder thread
_video_stop_evt = None          # signals decoder to stop
_video_queue = None             # queue of PIL Images (resized)
_video_pil_frames = []          # cached PIL frames for looping
_video_frame_i = 0              # playback index
_video_loaded_all = False
_video_started = False

_video_target_ms = 42           # derived from fps
_video_photo_ref = None         # keep last PhotoImage alive


# Defaults / caps
VIDEO_MAX_FRAMES_DEFAULT = 480          # safety cap (~20s @24fps)
VIDEO_START_BUFFER_DEFAULT = 12          # start after N frames buffered (higher = smoother start)          # start after N frames buffered
VIDEO_QUEUE_MAX_DEFAULT = 64            # decoded frames queue cap            # how many decoded frames can wait in queue


def stop_video():
    """Stop video playback, stop decoder thread, clear buffers."""
    global _video_cfg, _video_active_scene
    global _video_job, _video_thread, _video_stop_evt
    global _video_queue, _video_pil_frames, _video_frame_i
    global _video_loaded_all, _video_started, _video_photo_ref

    _video_cfg = None
    _video_active_scene = None

    # cancel UI tick
    try:
        if _video_job is not None and root is not None:
            root.after_cancel(_video_job)
    except Exception:
        pass
    _video_job = None

    # stop decoder
    try:
        if _video_stop_evt is not None:
            _video_stop_evt.set()
    except Exception:
        pass

    # join briefly (don't freeze UI)
    try:
        if _video_thread is not None and _video_thread.is_alive():
            _video_thread.join(timeout=0.05)
    except Exception:
        pass

    _video_thread = None
    _video_stop_evt = None

    # clear queue/buffers
    _video_queue = None
    _video_pil_frames = []
    _video_frame_i = 0
    _video_loaded_all = False
    _video_started = False
    _video_photo_ref = None


def _video_worker(path_abs: str, target_w: int, target_h: int,
                 stop_evt, out_q, loop: bool, max_frames: int, resize_mode: str = "fast"):
    """
    Decode video frames off the Tk thread.
    Push resized PIL Images into out_q.
    """
    reader = None
    frames_decoded = 0

    # pick resize filter (fast vs high quality)
    if PIL_OK:
        if resize_mode == "high":
            _resample = Image.LANCZOS
        else:
            _resample = Image.BILINEAR
    else:
        _resample = None

    try:
        if not VIDEO_OK:
            return
        reader = imageio.get_reader(path_abs)

        while not stop_evt.is_set():
            # decode sequentially; if loop, reopen when done
            idx = 0
            while not stop_evt.is_set():
                try:
                    fr = reader.get_data(idx)
                except Exception:
                    break  # end or error
                idx += 1

                try:
                    if not PIL_OK:
                        continue
                    im = Image.fromarray(fr)
                    if im.mode != "RGBA":
                        im = im.convert("RGBA")

                    w, h = im.size
                    if w <= 0 or h <= 0:
                        continue

                    # scale-to-fit preserving aspect
                    scale = min(target_w / w, target_h / h)
                    nw = max(1, int(w * scale))
                    nh = max(1, int(h * scale))
                    im = im.resize((nw, nh), _resample)

                    # enqueue (drop oldest if full to keep it moving)
                    put_ok = False
                    for _ in range(2):
                        try:
                            out_q.put(im, timeout=0.05)
                            put_ok = True
                            break
                        except Exception:
                            # queue full -> drop one
                            try:
                                out_q.get_nowait()
                            except Exception:
                                pass

                    if put_ok:
                        frames_decoded += 1
                        if frames_decoded >= max_frames:
                            return
                except Exception:
                    # ignore a bad frame
                    pass

            if not loop:
                return

            # loop: reopen reader
            try:
                if reader is not None:
                    reader.close()
            except Exception:
                pass
            reader = None
            try:
                reader = imageio.get_reader(path_abs)
            except Exception:
                return

    finally:
        try:
            if reader is not None:
                reader.close()
        except Exception:
            pass


def _apply_pil_to_hero(im_pil):
    """Convert PIL Image -> PhotoImage and apply to hero item."""
    global _video_photo_ref
    if im_pil is None or not PIL_OK:
        return
    try:
        ph = ImageTk.PhotoImage(im_pil)
        _video_photo_ref = ph
        if hero_item_id:
            carousel_canvas.itemconfig(hero_item_id, image=ph, state="normal")
        else:
            w = int(carousel_canvas.cget("width"))
            h = int(carousel_canvas.cget("height"))
            carousel_canvas.create_image(w // 2, h // 2, image=ph, tags=("hero",))
        tmp_refs["hero_video"] = ph
    except Exception:
        pass


def start_video(cfg: dict, scene_id: str):
    """
    Start video playback without freezing the UI.
    Frames are decoded in a background thread and pushed via a queue.
    """
    global _video_cfg, _video_active_scene, _video_target_ms
    global _video_thread, _video_stop_evt, _video_queue
    global _video_pil_frames, _video_frame_i, _video_loaded_all, _video_started

    stop_video()

    if not VIDEO_OK or not PIL_OK or not isinstance(cfg, dict):
        return

    rel_path = cfg.get("path") or cfg.get("file") or cfg.get("src")
    if not rel_path:
        return

    ap = abs_path(str(rel_path))
    if not os.path.exists(ap):
        print("[VIDEO] missing:", ap)
        return

    # fps -> ms
    fps = cfg.get("fps", 24)
    try:
        fps = float(fps)
    except Exception:
        fps = 24.0
    fps = max(1.0, min(60.0, fps))
    _video_target_ms = max(10, int(1000.0 / fps))

    loop = bool(cfg.get("loop", True))

    # buffers/caps
    start_buf = cfg.get("start_buffer", VIDEO_START_BUFFER_DEFAULT)
    try:
        start_buf = int(start_buf)
    except Exception:
        start_buf = VIDEO_START_BUFFER_DEFAULT
    start_buf = max(1, min(60, start_buf))

    max_frames = cfg.get("max_frames", VIDEO_MAX_FRAMES_DEFAULT)
    try:
        max_frames = int(max_frames)
    except Exception:
        max_frames = VIDEO_MAX_FRAMES_DEFAULT
    max_frames = max(24, min(5000, max_frames))

    qmax = cfg.get("queue_max", VIDEO_QUEUE_MAX_DEFAULT)
    try:
        qmax = int(qmax)
    except Exception:
        qmax = VIDEO_QUEUE_MAX_DEFAULT
    qmax = max(8, min(240, qmax))

    resize_mode = str(cfg.get("quality", "fast")).lower()  # "fast" | "high"

    # target size from HERO canvas
    try:
        target_w = int(carousel_canvas.cget("width"))
        target_h = int(carousel_canvas.cget("height"))
    except Exception:
        target_w, target_h = 1200, 700

    _video_cfg = dict(cfg)
    _video_active_scene = str(scene_id)

    _video_queue = queue.Queue(maxsize=qmax)
    _video_pil_frames = []
    _video_frame_i = 0
    _video_loaded_all = False
    _video_started = False

    _video_stop_evt = threading.Event()
    _video_thread = threading.Thread(
        target=_video_worker,
        args=(ap, target_w, target_h, _video_stop_evt, _video_queue, loop, max_frames, resize_mode),
        daemon=True
    )
    _video_thread.start()

    # UI tick (pull from queue, cache, display)
    def _tick():
        global _video_job, _video_frame_i, _video_loaded_all, _video_started

        if not _video_cfg:
            _video_job = None
            return

        # scene changed? stop
        if _video_active_scene is not None and str(current) != str(_video_active_scene):
            stop_video()
            return

        # pull all currently available frames (fast, non-blocking)
        pulled = 0
        while True:
            try:
                im = _video_queue.get_nowait()
            except Exception:
                break
            _video_pil_frames.append(im)
            pulled += 1

        # if decoder thread ended, mark loaded_all
        try:
            if _video_thread is not None and (not _video_thread.is_alive()) and (_video_queue is None or _video_queue.empty()):
                _video_loaded_all = True
        except Exception:
            pass

        # start once buffer ready (or at least 1 frame)
        if (not _video_started) and (_video_pil_frames):
            if (len(_video_pil_frames) >= start_buf) or _video_loaded_all:
                _video_started = True

        if _video_started and _video_pil_frames:
            loop_local = bool(_video_cfg.get("loop", True))

            if (not loop_local) and _video_loaded_all and _video_frame_i >= (len(_video_pil_frames) - 1):
                _video_frame_i = len(_video_pil_frames) - 1
            idx = _video_frame_i % len(_video_pil_frames) if loop_local else min(_video_frame_i, len(_video_pil_frames) - 1)

            _apply_pil_to_hero(_video_pil_frames[idx])

            if (not loop_local) and _video_loaded_all and _video_frame_i >= (len(_video_pil_frames) - 1):
                _video_job = None
                return

            _video_frame_i += 1

        # schedule next tick
        _video_job = root.after(_video_target_ms, _tick)

    _tick()

# ----------------------------
# Import story (robust)
# ----------------------------
STORY_EN = None
STORY_TR = None
try:
    # preferred: story_en / story_tr names
    from game_story import story_en as STORY_EN, story_tr as STORY_TR
except Exception:
    try:
        from game_story import STORY_EN, STORY_TR
    except Exception:
        from game_story import STORY_EN
        STORY_TR = STORY_EN  # fallback: TR not provided
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

MUSIC_LOOP = os.path.join(BASE_DIR, "sounds", "atari_loop.mp3")  # preferred

# ✅ ORTAM SESLERİ (SFX) LOOP: önce ambience_loop.* arar, yoksa footstep_loop.* fallback
AMBIENCE_PRIMARY = os.path.join(BASE_DIR, "sounds", "ambience_loop.mp3")
AMBIENCE_FALLBACK = os.path.join(BASE_DIR, "sounds", "footstep_loop.mp3")

# Save progress
SAVE_PATH = os.path.join(BASE_DIR, "save_0217.json")
TOTAL_ENDINGS = 32
unlocked_endings = set()

# ----------------------------
# pygame audio (music + sfx + click)
# ----------------------------
PYGAME_OK = True
pygame = None


def _try_init_pygame(buffer_size: int):
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
sfx_loop_playing = False

music_volume_percent = 5
music_volume = music_volume_percent / 100.0

# ✅ SINGLE SFX VOLUME (ambience loop + tok click)
sfx_volume_percent = 80
sfx_volume = sfx_volume_percent / 100.0

sfx_loop_sound = None
sfx_loop_channel = None

# scene bazlı sfx loop kontrolü
sfx_started_this_scene = False


def start_sfx_this_scene():
    global sfx_started_this_scene
    sfx_started_this_scene = True
    play_sfx_loop()


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


def _sound_candidates(path_any: str):
    cands = []
    if path_any:
        cands.append(path_any)
        root, _ext = os.path.splitext(path_any)
        cands.append(root + ".wav")
        cands.append(root + ".ogg")
        cands.append(root + ".mp3")
    seen = set()
    out = []
    for p in cands:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _choose_ambience_file():
    primary = _sound_candidates(AMBIENCE_PRIMARY)
    for p in primary:
        if os.path.exists(p):
            return p
    fallback = _sound_candidates(AMBIENCE_FALLBACK)
    for p in fallback:
        if os.path.exists(p):
            return p
    return None


def set_music_volume_percent(percent: int):
    global music_volume, music_volume_percent
    music_volume_percent = max(0, min(100, int(percent)))
    music_volume = music_volume_percent / 100.0
    if PYGAME_OK:
        try:
            pygame.mixer.music.set_volume(music_volume)
        except Exception as e:
            print("[AUDIO] set music volume error:", e)


def set_sfx_volume_percent(percent: int):
    """✅ Tek slider: ambience loop + tok click."""
    global sfx_volume, sfx_volume_percent
    sfx_volume_percent = max(0, min(100, int(percent)))
    sfx_volume = sfx_volume_percent / 100.0

    if PYGAME_OK and sfx_loop_channel:
        try:
            sfx_loop_channel.set_volume(sfx_volume)
        except Exception as e:
            print("[AUDIO] set sfx loop volume error:", e)

    if PYGAME_OK:
        try:
            if click_sound:
                click_sound.set_volume(0.80 * sfx_volume)
            if click_channel:
                click_channel.set_volume(1.0)
        except Exception as e:
            print("[AUDIO] set click volume error:", e)


def play_music_loop():
    global music_playing
    if not PYGAME_OK:
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


def play_sfx_loop():
    global sfx_loop_playing, sfx_loop_sound, sfx_loop_channel
    if not PYGAME_OK:
        return
    if sfx_loop_playing:
        return

    chosen = _choose_ambience_file()
    if not chosen:
        print("[AUDIO] AMBIENCE (SFX LOOP) MISSING. Tried:",
              _sound_candidates(AMBIENCE_PRIMARY) + _sound_candidates(AMBIENCE_FALLBACK))
        return

    try:
        sfx_loop_sound = pygame.mixer.Sound(chosen)
        if sfx_loop_channel is None:
            sfx_loop_channel = pygame.mixer.Channel(1)

        sfx_loop_channel.set_volume(sfx_volume)
        sfx_loop_channel.play(sfx_loop_sound, loops=-1)

        sfx_loop_playing = True
        print("[AUDIO] Ambience (SFX) loop started:", os.path.basename(chosen),
              f"vol={sfx_volume_percent}%")
    except Exception as e:
        print("[AUDIO] AMBIENCE LOOP ERROR:", e)
        sfx_loop_playing = False


def stop_sfx_loop():
    global sfx_loop_playing, sfx_loop_channel
    if not PYGAME_OK:
        sfx_loop_playing = False
        return
    try:
        if sfx_loop_channel:
            sfx_loop_channel.stop()
    except Exception as e:
        print("[AUDIO] stop_sfx_loop error:", e)
    sfx_loop_playing = False


# ============================================================
# CLICK ENGINE (NO FILE) - "TOK TOK" SOUND (SFX controlled)
# ============================================================
CLICK_EVERY = 2
CLICK_MIN_GAP = 0.012
CLICK_GAIN = 0.95
CLICK_DUR_MS = 52
CLICK_FREQ_HZ = 900

_last_click_t = 0.0
_CLICK_WAV_BYTES = None

click_sound = None
click_channel = None


def _build_click_wav_bytes_16bit(duration_ms=CLICK_DUR_MS, freq_hz=CLICK_FREQ_HZ, gain=CLICK_GAIN):
    sr = 44100
    n = max(1, int(sr * (duration_ms / 1000.0)))

    g = max(0.0, min(1.0, float(gain)))
    max_amp = int(32767 * g)

    attack_ms = 5
    attack_n = max(1, int(sr * attack_ms / 1000.0))

    body_freq = max(180, int(freq_hz * 0.33))
    noise_amt = 0.06

    frames = bytearray()
    for i in range(n):
        t = i / sr

        if i < attack_n:
            env = 1.0 - (i / attack_n)
        else:
            tail_i = i - attack_n
            tail_n = max(1, n - attack_n)
            env = 0.70 * (1.0 - (tail_i / tail_n))

        if i < attack_n:
            a = 1.0 if (math.sin(2 * math.pi * (freq_hz * 2.0) * t) >= 0) else -1.0
            attack = 0.35 * a
        else:
            attack = 0.0

        b = math.sin(2 * math.pi * body_freq * t)
        body = 0.95 * b
        noise = noise_amt * (random.random() * 2.0 - 1.0)

        sample = (attack + body + noise) * env
        v = int(max_amp * sample)
        v = max(-32768, min(32767, v))
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
            click_sound.set_volume(0.80 * sfx_volume)
            click_channel = pygame.mixer.Channel(2)
            click_channel.set_volume(1.0)
            print("[AUDIO] Click sound ready (pygame) - TOK mode")
        except Exception as e:
            click_sound = None
            click_channel = None
            print("[AUDIO] Click init failed (pygame):", e)


def stop_clicks():
    if PYGAME_OK and click_channel:
        try:
            click_channel.stop()
        except Exception:
            pass
    if winsound:
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass


def soft_click():
    global _last_click_t
    if sfx_volume_percent <= 0:
        return
    now = time.perf_counter()
    if (now - _last_click_t) < CLICK_MIN_GAP:
        return
    _last_click_t = now

    _ensure_click_assets()

    if PYGAME_OK and click_sound and click_channel:
        try:
            click_channel.stop()
            click_channel.play(click_sound)
            return
        except Exception:
            pass

    if winsound and _CLICK_WAV_BYTES:
        try:
            winsound.PlaySound(_CLICK_WAV_BYTES, winsound.SND_MEMORY | winsound.SND_ASYNC)
        except Exception:
            pass


def stop_all_audio():
    stop_clicks()
    stop_sfx_loop()
    stop_music()
    if PYGAME_OK:
        try:
            pygame.mixer.quit()
        except Exception:
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
        data = {"unlocked_endings": sorted(list(unlocked_endings))}
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
_auto_next_scheduled = False
_auto_next_job = None
# Segmented flow state
segments = []
seg_i = 0
after_segment_hook = None

# Image caches
_img_cache = {}

# Triptych layout
IMG_W = 512
IMG_H = 512
GAP = 16

CAROUSEL_W = (IMG_W * 3) + (GAP * 2)
CAROUSEL_H = IMG_H

ORIG_CW = CAROUSEL_W
ORIG_CH = CAROUSEL_H

SLOT_Y = CAROUSEL_H // 2
SLOT_LX = (IMG_W // 2)
SLOT_CX = SLOT_LX + IMG_W + GAP
SLOT_RX = SLOT_CX + IMG_W + GAP

BIG_W, BIG_H = IMG_W, IMG_H

# ✅ HERO (single_focus) layout (ekrana göre büyür)
HERO_W = None
HERO_H = None
HERO_Y = 30  # canvas top offset

# Speed
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

# Hero single-image state
hero_item_id = None
hero_img_path = None

# UI widgets
root = None
bg_label = None
bg_img = None
carousel_canvas = None
card = None
story_label = None
choices_row = None
choice_buttons = []
choice_borders = []
choice_containers = []
audio_ui = None
inv_ui = None

# Main Menu logo-only overlay
menu_logo_label = None
menu_logo_img = None

# Flicker
_flicker_cfg = None
_flicker_running = False
_flicker_job = None
_flicker_slot = None

# ✅ HERO flicker (single_focus)
_hero_flicker_running = False
_hero_flicker_job = None


def stop_flicker():
    global _flicker_running, _flicker_job, _flicker_slot, _hero_flicker_running, _hero_flicker_job
    _flicker_running = False
    _flicker_slot = None
    if _flicker_job is not None and root is not None:
        try:
            root.after_cancel(_flicker_job)
        except Exception:
            pass
    _flicker_job = None

    # ✅ stop HERO flicker (single_focus)
    _hero_flicker_running = False
    if _hero_flicker_job is not None and root is not None:
        try:
            root.after_cancel(_hero_flicker_job)
        except Exception:
            pass
    _hero_flicker_job = None



def _intensity_params(intensity: str):
    intensity = (intensity or "").lower().strip()
    if intensity == "strong":
        return {"min_ms": 40, "max_ms": 110, "bright": 1.35, "dark": 0.55, "blink_chance": 0.22}
    if intensity == "medium":
        return {"min_ms": 60, "max_ms": 140, "bright": 1.22, "dark": 0.70, "blink_chance": 0.15}
    return {"min_ms": 70, "max_ms": 170, "bright": 1.15, "dark": 0.80, "blink_chance": 0.10}


def abs_path(p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(BASE_DIR, p)


def _build_flicker_frames_fit(img_path: str, w: int, h: int, intensity: str):
    if not (PIL_OK and img_path and os.path.exists(abs_path(img_path))):
        return None

    ap = abs_path(img_path)
    try:
        im = Image.open(ap).convert("RGBA")
        iw, ih = im.size
        scale = min(w / iw, h / ih)
        nw = max(1, int(iw * scale))
        nh = max(1, int(ih * scale))
        base = im.resize((nw, nh), Image.LANCZOS)

        p = _intensity_params(intensity)
        bright = ImageEnhance.Brightness(base).enhance(p["bright"])
        dark = ImageEnhance.Brightness(base).enhance(p["dark"])
        off = ImageEnhance.Brightness(base).enhance(0.22)

        return [
            ImageTk.PhotoImage(base),
            ImageTk.PhotoImage(dark),
            ImageTk.PhotoImage(bright),
            ImageTk.PhotoImage(off),
        ]
    except Exception as e:
        print("[FLICKER] build error:", e)
        return None


def try_start_flicker(slot_key: str, img_path: str):
    global _flicker_cfg, _flicker_running, _flicker_job, _flicker_slot

    if not _flicker_cfg:
        return
    if _flicker_running:
        return

    idx_map = {"L": 1, "C": 2, "R": 3}
    want_index = int(_flicker_cfg.get("index", 0) or 0)
    want_slot = str(_flicker_cfg.get("slot", "") or "").upper().strip()
    if want_slot == "" or want_slot != slot_key:
        return
    if want_index != idx_map.get(slot_key, -1):
        return

    item = slot_items.get(slot_key)
    if not item:
        return

    intensity = str(_flicker_cfg.get("intensity", "medium"))
    frames = _build_flicker_frames_fit(img_path, BIG_W, BIG_H, intensity) if PIL_OK else None
    if frames:
        tmp_refs[f"flicker_frames_{slot_key}"] = frames

    params = _intensity_params(intensity)
    _flicker_running = True
    _flicker_slot = slot_key

    def step():
        global _flicker_job, _flicker_running
        if not _flicker_running:
            return

        delay = random.randint(params["min_ms"], params["max_ms"])

        if frames:
            if random.random() < params["blink_chance"]:
                fr = frames[3]
            else:
                fr = random.choice(frames[:3])
            try:
                carousel_canvas.itemconfig(item, image=fr)
                slot_images[slot_key] = fr
            except Exception:
                pass
        else:
            try:
                if random.random() < params["blink_chance"]:
                    carousel_canvas.itemconfig(item, state="hidden")
                else:
                    carousel_canvas.itemconfig(item, state="normal")
            except Exception:
                pass

        _flicker_job = root.after(delay, step)

    step()


# ============================
# DIZZY / BLUR EFFECT (NO SHAKE)
# ============================
_dizzy_cfg = None
_dizzy_running = False
_dizzy_job = None
_dizzy_slot = None

_hero_dizzy_running = False
_hero_dizzy_job = None


def stop_dizzy():
    global _dizzy_running, _dizzy_job, _dizzy_slot, _hero_dizzy_running, _hero_dizzy_job
    _dizzy_running = False
    _dizzy_slot = None
    if _dizzy_job is not None and root is not None:
        try:
            root.after_cancel(_dizzy_job)
        except Exception:
            pass
    _dizzy_job = None

    _hero_dizzy_running = False
    if _hero_dizzy_job is not None and root is not None:
        try:
            root.after_cancel(_hero_dizzy_job)
        except Exception:
            pass
    _hero_dizzy_job = None


def _dizzy_params(intensity: str, mode: str):
    """
    mode:
      - "blur"  : sadece blur pulse
      - "dizzy" : rotate/zoom
    """
    intensity = (intensity or "").lower().strip()
    mode = (mode or "blur").lower().strip()

    if mode == "blur":
        if intensity == "strong":
            return {"speed_ms": 40, "frames": 28, "blur_max": 3.2}
        if intensity == "medium":
            return {"speed_ms": 45, "frames": 26, "blur_max": 2.4}
        return {"speed_ms": 55, "frames": 24, "blur_max": 1.8}

    if intensity == "strong":
        return {"amp_deg": 10.0, "speed_ms": 35, "blur": 1.6, "zoom": 1.06, "frames": 24}
    if intensity == "medium":
        return {"amp_deg": 7.0, "speed_ms": 45, "blur": 1.1, "zoom": 1.04, "frames": 22}
    return {"amp_deg": 5.0, "speed_ms": 55, "blur": 0.8, "zoom": 1.03, "frames": 20}


def _build_blur_frames_fit(img_path: str, target_w: int, target_h: int, intensity: str):
    if not (PIL_OK and img_path and os.path.exists(abs_path(img_path))):
        return None

    params = _dizzy_params(intensity, "blur")
    nframes = int(params["frames"])
    blur_max = float(params["blur_max"])

    try:
        im = Image.open(abs_path(img_path)).convert("RGBA")
        iw, ih = im.size
        scale = min(target_w / iw, target_h / ih)
        nw = max(1, int(iw * scale))
        nh = max(1, int(ih * scale))
        base = im.resize((nw, nh), Image.LANCZOS)

        frames = []
        for i in range(nframes):
            t = i / max(1, nframes)
            wave01 = 0.5 + 0.5 * math.sin(2 * math.pi * t)
            br = blur_max * wave01

            canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            ox = (target_w - nw) // 2
            oy = (target_h - nh) // 2
            canvas.paste(base, (ox, oy), base)

            if br > 0.02:
                canvas = canvas.filter(ImageFilter.GaussianBlur(radius=br))

            frames.append(ImageTk.PhotoImage(canvas))

        return frames
    except Exception as e:
        print("[BLUR] build error:", e)
        return None


def _build_dizzy_frames_fit(img_path: str, target_w: int, target_h: int, intensity: str, mode: str):
    mode = (mode or "blur").lower().strip()
    if mode == "blur":
        return _build_blur_frames_fit(img_path, target_w, target_h, intensity)

    if not (PIL_OK and img_path and os.path.exists(abs_path(img_path))):
        return None

    p = _dizzy_params(intensity, "dizzy")
    amp = float(p["amp_deg"])
    nframes = int(p["frames"])
    blur_base = float(p["blur"])
    zoom = float(p["zoom"])

    try:
        im = Image.open(abs_path(img_path)).convert("RGBA")
        iw, ih = im.size
        scale = min(target_w / iw, target_h / ih)
        nw = max(1, int(iw * scale))
        nh = max(1, int(ih * scale))
        base = im.resize((nw, nh), Image.LANCZOS)

        frames = []
        for i in range(nframes):
            t = i / max(1, nframes)
            ang = amp * math.sin(2 * math.pi * t)
            z = 1.0 + (zoom - 1.0) * (0.5 + 0.5 * math.sin(2 * math.pi * (t + 0.25)))
            br = blur_base * (0.5 + 0.5 * math.sin(2 * math.pi * (t + 0.10)))

            w2 = max(1, int(nw * z))
            h2 = max(1, int(nh * z))
            fr = base.resize((w2, h2), Image.LANCZOS)

            fr = fr.rotate(ang, resample=Image.BICUBIC, expand=True)
            if br > 0.05:
                fr = fr.filter(ImageFilter.GaussianBlur(radius=br))

            fw, fh = fr.size
            cx, cy = fw // 2, fh // 2
            left = max(0, cx - target_w // 2)
            top = max(0, cy - target_h // 2)
            fr = fr.crop((left, top, left + target_w, top + target_h))

            frames.append(ImageTk.PhotoImage(fr))

        return frames
    except Exception as e:
        print("[DIZZY] build error:", e)
        return None


def try_start_dizzy(slot_key: str, img_path: str):
    global _dizzy_cfg, _dizzy_running, _dizzy_job, _dizzy_slot
    if not _dizzy_cfg or _dizzy_running:
        return

    want_slot = str(_dizzy_cfg.get("slot", "") or "").upper().strip()
    if want_slot and want_slot != slot_key:
        return

    mode = str(_dizzy_cfg.get("mode", "blur") or "blur").lower().strip()
    intensity = str(_dizzy_cfg.get("intensity", "medium"))
    params = _dizzy_params(intensity, mode)

    frames = _build_dizzy_frames_fit(img_path, BIG_W, BIG_H, intensity, mode)
    if not frames:
        return

    item = slot_items.get(slot_key)
    if not item:
        return

    tmp_refs[f"dizzy_frames_{slot_key}"] = frames
    _dizzy_running = True
    _dizzy_slot = slot_key

    speed_ms = int(_dizzy_cfg.get("speed_ms", params["speed_ms"]) or params["speed_ms"])

    def step(k=0):
        global _dizzy_job, _dizzy_running
        if not _dizzy_running:
            return
        fr = frames[k % len(frames)]
        try:
            carousel_canvas.itemconfig(item, image=fr)
            slot_images[slot_key] = fr
        except Exception:
            pass
        _dizzy_job = root.after(speed_ms, lambda: step(k + 1))

    step(0)


def try_start_dizzy_hero(img_path: str):
    global _dizzy_cfg, _hero_dizzy_running, _hero_dizzy_job, hero_item_id
    if not _dizzy_cfg or _hero_dizzy_running or not hero_item_id:
        return

    mode = str(_dizzy_cfg.get("mode", "blur") or "blur").lower().strip()
    intensity = str(_dizzy_cfg.get("intensity", "medium"))
    params = _dizzy_params(intensity, mode)

    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))

    frames = _build_dizzy_frames_fit(img_path, w, h, intensity, mode)
    if not frames:
        return

    tmp_refs["hero_dizzy_frames"] = frames
    _hero_dizzy_running = True

    speed_ms = int(_dizzy_cfg.get("speed_ms", params["speed_ms"]) or params["speed_ms"])

    def step(k=0):
        global _hero_dizzy_job, _hero_dizzy_running
        if not _hero_dizzy_running:
            return
        fr = frames[k % len(frames)]
        try:
            carousel_canvas.itemconfig(hero_item_id, image=fr)
        except Exception:
            pass
        _hero_dizzy_job = root.after(speed_ms, lambda: step(k + 1))

    step(0)


def try_start_flicker_hero(img_path: str):
    """✅ Flicker effect for single_focus HERO image.
    Works on carousel_canvas + hero_item_id (same as dizzy_hero)."""
    global _flicker_cfg, _hero_flicker_running, _hero_flicker_job, hero_item_id

    if not _flicker_cfg or _hero_flicker_running or not hero_item_id:
        return

    # treat HERO as slot C (index 2)
    want_slot = str(_flicker_cfg.get("slot", "") or "").upper().strip()
    want_index = int(_flicker_cfg.get("index", 0) or 0)
    if want_slot not in ("C", ""):
        return
    if want_index not in (0, 2):
        return

    intensity = str(_flicker_cfg.get("intensity", "medium"))
    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))

    frames = _build_flicker_frames_fit(img_path, w, h, intensity) if PIL_OK else None
    if frames:
        tmp_refs["hero_flicker_frames"] = frames

    params = _intensity_params(intensity)
    _hero_flicker_running = True

    def step():
        global _hero_flicker_job, _hero_flicker_running
        if not _hero_flicker_running:
            return

        delay = random.randint(params["min_ms"], params["max_ms"])

        if frames:
            if random.random() < params["blink_chance"]:
                fr = frames[3]
            else:
                fr = random.choice(frames[:3])
            try:
                carousel_canvas.itemconfig(hero_item_id, image=fr)
                tmp_refs["hero_img"] = fr
            except Exception:
                pass
        else:
            # no PIL: just occasional hide/show by swapping to blank
            try:
                if random.random() < params["blink_chance"]:
                    carousel_canvas.itemconfig(hero_item_id, state="hidden")
                    root.after(max(30, int(params["min_ms"] / 2)), lambda: carousel_canvas.itemconfig(hero_item_id, state="normal"))
            except Exception:
                pass

        _hero_flicker_job = root.after(delay, step)

    step()



def load_photo_fit(path, target_w, target_h, cache_dict):
    if not path:
        return None
    ap = abs_path(path)
    key = (ap, target_w, target_h)

    if key in cache_dict:
        return cache_dict[key]
    if not os.path.exists(ap):
        cache_dict[key] = None
        print("[IMG] MISSING:", ap)
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
        return list(imgs)
    return []


def split_text_into_segments(txt: str):
    """
    TOKENLAR:
      - "||"   : yeni segment (metin parçası)
      - "|||"  : pagebreak (SPACE bekler)
      - "##"   : görsel getir (bir sonraki resmi pop-in ile göster)
      - "□"    : typewriter içinde 1 saniye bekleme (ekranda görünmez)

    Not: Bu fonksiyon "||" tokenını çıktıya koymaz; sadece segmentlere böler.
    """
    if not txt:
        return [""]

    s = str(txt)
    out = []
    buf = []
    i = 0
    n = len(s)

    def flush():
        nonlocal buf
        if buf:
            chunk = "".join(buf)
            buf = []
            if chunk.strip():
                out.append(chunk.strip())

    while i < n:
        if s.startswith("|||", i):
            flush()
            out.append(PAGEBREAK_TOKEN)
            i += 3
            continue

        if s.startswith(IMAGE_TOKEN, i):
            flush()
            out.append(IMAGE_TOKEN)
            i += len(IMAGE_TOKEN)
            continue

        if s.startswith(OVERLAY_TOKEN, i):
            flush()
            out.append(OVERLAY_TOKEN)
            i += len(OVERLAY_TOKEN)
            continue

        if s.startswith("||", i):
            flush()
            i += 2
            continue

        buf.append(s[i])
        i += 1

    flush()
    return out if out else [""]


# ----------------------------
# Canvas modes
# ----------------------------
def _calc_hero_size():
    global HERO_W, HERO_H
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    HERO_W = max(900, min(sw - 80, 1700))
    HERO_H = max(520, min(int(sh * 0.62), 720))


def set_canvas_triptych_mode():
    try:
        carousel_canvas.config(width=ORIG_CW, height=ORIG_CH)
        carousel_canvas.place(relx=0.5, y=30, anchor="n")
    except Exception:
        pass


def set_canvas_hero_mode(custom_w=None, custom_h=None):
    if HERO_W is None or HERO_H is None:
        _calc_hero_size()

    w = int(custom_w) if custom_w else HERO_W
    h = int(custom_h) if custom_h else HERO_H

    try:
        carousel_canvas.config(width=w, height=h)
        carousel_canvas.place(relx=0.5, y=HERO_Y, anchor="n")
        return w, h
    except Exception:
        return w, h


# ----------------------------
# Carousel helpers
# ----------------------------
def carousel_clear():
    try:
        stop_video()
    except Exception:
        pass
    global hero_item_id, hero_img_path
    carousel_canvas.delete("all")
    for k in ("L", "C", "R"):
        slot_items[k] = None
        slot_images[k] = None
    tmp_refs.clear()
    hero_item_id = None
    hero_img_path = None
    # clear overlays
    global hero_overlay_items, hero_overlay_refs, _overlay_queue, _overlay_i, _overlay_step_points, _overlay_step_fired
    hero_overlay_items = []
    hero_overlay_refs = []
    _overlay_queue = []
    _overlay_i = 0
    _overlay_step_points = []
    _overlay_step_fired = set()


def place_slot(slot_key, photo, x, y):
    if photo is None:
        return
    if slot_items[slot_key] is None:
        slot_items[slot_key] = carousel_canvas.create_image(x, y, image=photo)
    else:
        carousel_canvas.itemconfig(slot_items[slot_key], image=photo, state="normal")
        carousel_canvas.coords(slot_items[slot_key], x, y)
    slot_images[slot_key] = photo


def show_logo_on_canvas():
    carousel_clear()
    logo = load_photo_fit("images/logo.png", int(carousel_canvas.cget("width")),
                          int(carousel_canvas.cget("height")), _img_cache)
    if logo:
        w = int(carousel_canvas.cget("width"))
        h = int(carousel_canvas.cget("height"))
        carousel_canvas.create_image(w // 2, h // 2, image=logo)
        tmp_refs["logo_canvas"] = logo
    else:
        w = int(carousel_canvas.cget("width"))
        h = int(carousel_canvas.cget("height"))
        carousel_canvas.create_text(w // 2, h // 2, text="LOGO LOAD ERROR",
                                   fill="white", font=("Segoe UI Semibold", 18, "bold"))


def show_single_big_image(img_path: str):
    """Show a single (hero) image without briefly blanking the canvas.

    Key idea: DO NOT call carousel_clear() before loading the new image.
    We first load the PhotoImage, then swap the existing hero item (if any).
    This prevents the user from seeing the dark background for a moment,
    especially when a video scene is about to start.
    """
    global hero_item_id, hero_img_path
    global hero_overlay_items, hero_overlay_refs, _overlay_queue, _overlay_i, _overlay_step_points, _overlay_step_fired

    # Stop any running video (but do not clear canvas)
    try:
        stop_video()
    except Exception:
        pass

    # Stop effects tied to the previous hero (but keep the image visible)
    try:
        stop_flicker()
    except Exception:
        pass
    try:
        stop_dizzy()
    except Exception:
        pass

    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))

    # If scene has no image path, keep the current hero image if it exists
    if not img_path:
        if hero_item_id is not None:
            return
        carousel_canvas.create_text(
            w // 2, h // 2,
            text="NO IMAGE",
            fill="white",
            font=("Segoe UI Semibold", 18, "bold"),
        )
        return

    # Pre-load the image FIRST (so we don't blank the screen while loading)
    photo = load_photo_fit(img_path, w, h, _img_cache)

    if not photo:
        # If we already have something on screen, keep it (avoid ugly flash)
        if hero_item_id is not None:
            print("[IMG] failed to load, keeping previous:", img_path)
            return
        carousel_canvas.create_text(
            w // 2, h // 2,
            text="IMAGE LOAD ERROR",
            fill="white",
            font=("Segoe UI Semibold", 18, "bold"),
        )
        return

    # If we are coming from triptych mode and no hero item exists, clear AFTER we have the image ready
    if hero_item_id is None:
        try:
            any_slot = any(slot_items.get(k) is not None for k in ("L", "C", "R"))
        except Exception:
            any_slot = False
        if any_slot:
            # Clear triptych items fast; we already have 'photo' ready, so no visible blank
            carousel_canvas.delete("all")
            for k in ("L", "C", "R"):
                slot_items[k] = None
                slot_images[k] = None
            tmp_refs.clear()

    # Clear overlay items (do not touch base hero item)
    try:
        for it in list(hero_overlay_items):
            try:
                carousel_canvas.delete(it)
            except Exception:
                pass
        hero_overlay_items.clear()
        hero_overlay_refs.clear()
        _overlay_queue = []
        _overlay_i = 0
        _overlay_step_points = []
        _overlay_step_fired = set()
    except Exception:
        pass

    # Swap hero image (no blank)
    hero_img_path = img_path
    cx, cy = w // 2, h // 2
    if hero_item_id is None:
        hero_item_id = carousel_canvas.create_image(cx, cy, image=photo)
    else:
        try:
            carousel_canvas.itemconfig(hero_item_id, image=photo)
            carousel_canvas.coords(hero_item_id, cx, cy)
        except Exception:
            # If canvas item is invalid, recreate safely
            try:
                hero_item_id = carousel_canvas.create_image(cx, cy, image=photo)
            except Exception:
                pass

    tmp_refs["hero_img"] = photo

    # Restart effects for this hero image (if enabled)
    try:
        try_start_dizzy_hero(img_path)
    except Exception:
        pass
    try:
        try_start_flicker_hero(img_path)
    except Exception:
        pass





def _trigger_overlay_if_any():
    """Trigger next overlay image (single_focus) if configured."""
    try:
        if 'hero_pop_next_overlay' in globals():
            hero_pop_next_overlay()
            return True
    except Exception as _e:
        print("[OVERLAY] trigger error:", _e)
    return False


def pop_in_hero(img_path: str, duration_ms=POP_MS, frames=POP_FRAMES, on_done=None):
    """✅ HERO giriş animasyonu (single_focus sahnelerde 'ekrana gelme' efekti).
    - PIL varsa: küçükten büyüğe pop-in
    - PIL yoksa: normal yükler
    """
    global hero_item_id, hero_img_path
    # NOTE: We intentionally do NOT clear the canvas here.
    # We prepare the first frame first, then swap, to avoid background flashes.

    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))

    if not img_path:
        carousel_canvas.create_text(w // 2, h // 2, text="NO IMAGE",
                                   fill="white", font=("Segoe UI Semibold", 18, "bold"))
        if on_done:
            on_done()
        return

    hero_img_path = img_path
    ap = abs_path(img_path)
    if not os.path.exists(ap):
        print("[IMG] MISSING:", ap)
        carousel_canvas.create_text(w // 2, h // 2, text="IMAGE MISSING",
                                   fill="white", font=("Segoe UI Semibold", 18, "bold"))
        if on_done:
            on_done()
        return

    # Fallback (no PIL)
    if not PIL_OK:
        show_single_big_image(img_path)
        if on_done:
            on_done()
        return

    try:
        base = Image.open(ap).convert("RGBA")
        bw, bh = base.size
        scale_fit = min(w / bw, h / bh)
        tw = max(1, int(bw * scale_fit))
        th = max(1, int(bh * scale_fit))
        base = base.resize((tw, th), Image.LANCZOS)

        start_s = 0.18
        end_s = 1.00
        frames_list = []
        for i in range(int(frames)):
            t = (i + 1) / max(1, int(frames))
            s = start_s + (end_s - start_s) * t
            nw = max(1, int(tw * s))
            nh = max(1, int(th * s))
            fr = base.resize((nw, nh), Image.LANCZOS)

            canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ox = (w - nw) // 2
            oy = (h - nh) // 2
            canvas.paste(fr, (ox, oy), fr)
            frames_list.append(ImageTk.PhotoImage(canvas))

        # Swap hero without blanking: remove previous hero only after first frame is ready
        try:
            if hero_item_id is not None:
                carousel_canvas.delete(hero_item_id)
        except Exception:
            pass
        hero_item_id = carousel_canvas.create_image(w // 2, h // 2, image=frames_list[0])
        tmp_refs["hero_pop_frames"] = frames_list
        tmp_refs["hero_pop_item"] = hero_item_id

        step_ms = max(10, int(duration_ms / max(1, int(frames))))

        def _anim(k=0):
            nonlocal frames_list
            if k >= len(frames_list):
                # Final: cache'e tek photo koymak yerine son frame'i kullan
                carousel_canvas.itemconfig(hero_item_id, image=frames_list[-1])
                try:
                    try_start_dizzy_hero(img_path)
                except Exception:
                    pass
                try:
                    try_start_flicker_hero(img_path)
                except Exception:
                    pass
                if on_done:
                    on_done()
                return

            try:
                carousel_canvas.itemconfig(hero_item_id, image=frames_list[k])
            except Exception:
                pass
            root.after(step_ms, lambda: _anim(k + 1))

        _anim(0)

    except Exception as e:
        print("[HERO POP] ERROR:", e)
        show_single_big_image(img_path)
        if on_done:
            on_done()

def hero_add_overlay_center(img_path: str, scale=1.0):
    """Canvas ortasına bir overlay görsel ekler (üst üste binebilir)."""
    global hero_overlay_items, hero_overlay_refs
    if not img_path:
        return
    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))
    # overlay boyutu: canvas'ın belirli oranı
    if float(scale) >= 0.99:
        ow, oh = w, h
    else:
        ow = max(200, int(w * float(scale)))
        oh = max(200, int(h * float(scale)))

    photo = load_photo_fit(img_path, ow, oh, _img_cache)
    if not photo:
        return
    item = carousel_canvas.create_image(w // 2, h // 2, image=photo)
    hero_overlay_items.append(item)
    hero_overlay_refs.append(photo)
    # üstte kalsın
    try:
        carousel_canvas.tag_raise(item)
    except Exception:
        pass

def hero_replace_overlay_image(img_path: str):
    """Ξ token: mevcut hero görseli OVERWRITE eder (üst üste bindirme yok)."""
    if not img_path:
        return
    # Canvas'ta yalnızca tek hero görsel kalsın
    try:
        carousel_canvas.delete("hero")
    except Exception:
        pass
    try:
        # önceki anim/overlay reflerini temizle
        hero_overlay_items.clear()
        hero_overlay_refs.clear()
    except Exception:
        pass

    w = int(carousel_canvas.cget("width"))
    h = int(carousel_canvas.cget("height"))
    photo = load_photo_fit(img_path, w, h, _img_cache)
    if not photo:
        return

    global hero_item_id, hero_img_path
    hero_img_path = img_path

    if hero_item_id:
        try:
            carousel_canvas.itemconfig(hero_item_id, image=photo)
            carousel_canvas.coords(hero_item_id, w // 2, h // 2)
            carousel_canvas.addtag_withtag("hero", hero_item_id)
        except Exception:
            hero_item_id = None

    if not hero_item_id:
        hero_item_id = carousel_canvas.create_image(w // 2, h // 2, image=photo, tags=("hero",))

        tmp_refs["hero_img"] = photo

    # ✅ Flicker support in single_focus (treat hero as CENTER slot "C")
    try:
        slot_items["C"] = hero_item_id
        slot_images["C"] = photo
    except Exception:
        pass
    try:
        if not _dizzy_cfg:
            try_start_flicker("C", img_path)
    except Exception:
        pass

    try:
        try_start_dizzy_hero(img_path)
        try:
            try_start_flicker_hero(img_path)
        except Exception:
            pass
    except Exception:
        pass
def hero_pop_next_overlay():
    global _overlay_queue, _overlay_i
    if not _overlay_queue:
        return
    while _overlay_i < len(_overlay_queue):
        p = _overlay_queue[_overlay_i]
        _overlay_i += 1
        try:
            ap = abs_path(p)
            ex = os.path.exists(ap)
            print('[OVERLAY] replace:', p, 'exists=' + str(ex))
            if not ex:
                continue
            hero_replace_overlay_image(p)
            return
        except Exception as _e:
            print("[OVERLAY] error:", _e)
            continue





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

        try_start_dizzy(slot_key, path)
        if not _dizzy_cfg:
            try_start_flicker(slot_key, path)

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
                except Exception:
                    pass

                try_start_dizzy(slot_key, path)
                if not _dizzy_cfg:
                    try_start_flicker(slot_key, path)

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

        try_start_dizzy(slot_key, path)
        if not _dizzy_cfg:
            try_start_flicker(slot_key, path)

        if on_done:
            on_done()


# Button hover
BORDER_OFF = "#2a3a6a"
BORDER_ON = "#4f6cff"


def bind_border_hover(btn, border_frame):
    def on(_e=None):
        try:
            border_frame.config(bg=BORDER_ON)
        except Exception:
            pass

    def off(_e=None):
        try:
            border_frame.config(bg=BORDER_OFF)
        except Exception:
            pass

    btn.bind("<Enter>", on)
    btn.bind("<Leave>", off)


# Navigation
def disable_choices():
    for b in choice_buttons:
        b.config(state="disabled")


def hide_choices_ui():
    """Hide all choice buttons/containers (used while text is typing / during scene play)."""
    for cf in choice_containers:
        try:
            cf.pack_forget()
        except Exception:
            pass


def show_choices_ui(indices):
    """Show only specified choice container indices (0..3)."""
    for idx in indices:
        try:
            choice_containers[idx].pack(side="left", padx=44)
        except Exception:
            pass


def go_to(scene_id):
    try:
        stop_video()
    except Exception:
        pass
    global current
    cancel_auto_next()
    stop_clicks()
    if story and scene_id in story:
        current = scene_id
        load_scene()
    else:
        print("[GO_TO ERROR] missing scene:", scene_id)


def cancel_auto_next():
    """Cancel any scheduled auto-next transition."""
    global _auto_next_job, _auto_next_scheduled
    _auto_next_scheduled = False
    if _auto_next_job is not None and root is not None:
        try:
            root.after_cancel(_auto_next_job)
        except Exception:
            pass
    _auto_next_job = None


def schedule_auto_next_after_scene():
    """If current scene requests auto_next AFTER scene finishes, schedule it and return True."""
    global _auto_next_job, _auto_next_scheduled

    if _auto_next_scheduled:
        return True

    if not scene:
        return False

    nxt = scene.get("auto_next")
    if not nxt:
        return False

    wants_after = bool(scene.get("auto_next_after", False)) or ("auto_next_delay_ms" in scene)
    if not wants_after:
        return False

    if not story or nxt not in story:
        print("[AUTO_NEXT] target not found:", nxt, "from", current)
        return False

    # don't auto-next while waiting for pagebreak continue
    try:
        if waiting_pagebreak:
            return False
    except Exception:
        pass

    delay = int(scene.get("auto_next_delay_ms", 0) or scene.get("auto_delay_ms", 0) or 0)

    # hide choices while waiting
    try:
        hide_choices_ui()
        disable_choices()
    except Exception:
        pass

    cancel_auto_next()
    _auto_next_scheduled = True

    sid = str(current)

    def _go():
        global _auto_next_job, _auto_next_scheduled
        _auto_next_job = None
        _auto_next_scheduled = False
        # if scene changed, ignore
        if str(current) != sid:
            return
        go_to(nxt)

    _auto_next_job = root.after(max(0, delay), _go)
    return True


# Typewriter
def start_typewriter(text, on_done=None, clear_first=True):
    global full_text, index, click_count, typing_done, after_segment_hook
    after_segment_hook = on_done

    full_text = text or ""
    index = 0
    click_count = 0
    typing_done = False

    stop_clicks()

    if clear_first:
        story_label.config(text="")
    else:
        cur = story_label.cget("text")
        if cur.strip():
            story_label.config(text=cur + "\n")
    hide_choices_ui()

    disable_choices()
    type_step()


def type_step():
    global index, click_count, typing_done, after_segment_hook

    if index < len(full_text):
        ch = full_text[index]

        # ✅ INLINE OVERLAY TOKEN: allow "ΞHademe..." inside the same segment
        if ch == OVERLAY_TOKEN:
            try:
                _trigger_overlay_if_any()
            except Exception as _e:
                print("[OVERLAY] inline error:", _e)
            index += 1
            # continue immediately without printing the token
            root.after(0, type_step)
            return

        # ✅ PAUSE: "□" karakteri gördüğünde 1 saniye bekle (kare yazılmaz)
        if ch == PAUSE_CHAR:
            index += 1
            root.after(PAUSE_MS_PER_CHAR, type_step)
            return

        if (not ch.isspace()) and (ch not in ".!?," ):
            click_count += 1
            if click_count % CLICK_EVERY == 0:
                soft_click()

        story_label.config(text=story_label.cget("text") + ch)
        index += 1
        root.after(PUNCT_MS if ch in ".!?" else TYPE_MS, type_step)
        return

    typing_done = True
    stop_clicks()

    if after_segment_hook:
        cb = after_segment_hook
        after_segment_hook = None
        root.after(HOOK_MS, cb)
        return

    show_buttons_for_scene()


# ============================================================
# ✅ PAGEBREAK WAIT / CONTINUE
# ============================================================
def _enter_pagebreak(wait_continue_cb):
    global waiting_pagebreak, _pagebreak_continue_cb
    waiting_pagebreak = True
    _pagebreak_continue_cb = wait_continue_cb
    disable_choices()


def _continue_after_pagebreak():
    global waiting_pagebreak, _pagebreak_continue_cb
    waiting_pagebreak = False
    cb = _pagebreak_continue_cb
    _pagebreak_continue_cb = None
    story_label.config(text="")
    if cb:
        cb()


def play_text_segments_only(seg_list):
    global segments, seg_i
    segments = seg_list[:] if seg_list else [""]
    seg_i = 0

    def finish_all():
        if sfx_started_this_scene and not scene.get("keep_sfx_after_scene", False) and scene.get("end_sound") != "ambience":
            stop_sfx_loop()
        if schedule_auto_next_after_scene():
            return
        if schedule_auto_next_after_scene():
            return

        show_buttons_for_scene()

        if scene and scene.get("end_sound") == "ambience":
            start_sfx_this_scene()

    def write_next():
        global seg_i
        if seg_i >= len(segments):
            finish_all()
            return


        # ✅ token-free overlay trigger: if current step index matches overlay_at_steps
        try:
            global _overlay_step_points, _overlay_step_fired
            cur_step = seg_i
            if isinstance(_overlay_step_points, list) and _overlay_step_points:
                # allow multiple triggers at same step
                cnt = _overlay_step_points.count(cur_step)
                if cnt > 0 and cur_step not in _overlay_step_fired:
                    for _ in range(cnt):
                        hero_pop_next_overlay()
                    _overlay_step_fired.add(cur_step)
        except Exception as _e:
            print("[overlay_steps] trigger error:", _e)
        part = segments[seg_i]
        seg_i += 1

        if part == PAGEBREAK_TOKEN:
            _enter_pagebreak(lambda: root.after(HOOK_MS, write_next))
            return
        if part == IMAGE_TOKEN:
            # hero/text-only: IMAGE_TOKEN'u yok say (istersen ileride hero image swap yapılabilir)
            root.after(HOOK_MS, write_next)
            return
        if part == OVERLAY_TOKEN:
            try:
                hero_pop_next_overlay()
            except Exception:
                pass
            root.after(HOOK_MS, write_next)
            return

        start_typewriter(part, on_done=lambda: root.after(HOOK_MS, write_next), clear_first=(seg_i==1))

    write_next()


def play_scene_segment_flow(img_list, seg_list):
    global segments, seg_i
    segments = seg_list[:] if seg_list else [""]
    seg_i = 0

    paths = list(img_list or [])
    while len(paths) < 3:
        paths.append(None)
    p1, p2, p3 = paths[:3]

    img_seq = [p1, p2, p3]
    img_ptr = 0

    def pop_next_image(cb):
        """Show next available image (L->C->R) ONLY when IMAGE_TOKEN ("##") is encountered."""
        nonlocal img_ptr
        while img_ptr < len(img_seq) and not img_seq[img_ptr]:
            img_ptr += 1
        if img_ptr >= len(img_seq):
            cb()
            return

        path = img_seq[img_ptr]

        # map pointer to slot
        slot_map = {
            0: ("L", SLOT_LX),
            1: ("C", SLOT_CX),
            2: ("R", SLOT_RX),
        }
        slot_key, slot_x = slot_map.get(img_ptr, ("R", SLOT_RX))
        img_ptr += 1

        def _done():
            root.after(POP_DELAY_23, cb)

        pop_in_to_slot(slot_key, path, slot_x, SLOT_Y, on_done=_done)

    pre_slot = None
    pre_path = None

    candidates = [("L", p1), ("C", p2), ("R", p3)]
    non_null = [(k, v) for (k, v) in candidates if v]

    if (p1 is None) and (len(non_null) == 1):
        pre_slot, pre_path = non_null[0]
        if pre_slot == "C":
            p2 = None
        elif pre_slot == "R":
            p3 = None

    def finish_all():
        if sfx_started_this_scene and not scene.get("keep_sfx_after_scene", False) and scene.get("end_sound") != "ambience":
            stop_sfx_loop()

        show_buttons_for_scene()

        if scene and scene.get("end_sound") == "ambience":
            start_sfx_this_scene()

    def write_next_segment():
        global seg_i

        sfx_seg = scene.get("sfx_on_segment")
        if isinstance(sfx_seg, int) and sfx_seg >= 1 and seg_i == (sfx_seg - 1):
            print("[AUDIO] sfx_on_segment TRIGGER:", sfx_seg, "scene=", current)
            start_sfx_this_scene()

        if seg_i >= len(segments):
            finish_all()
            return

        text_part = segments[seg_i]
        seg_i += 1

        if text_part == PAGEBREAK_TOKEN:
            _enter_pagebreak(lambda: root.after(HOOK_MS, write_next_segment))
            return
        if text_part == IMAGE_TOKEN:
            pop_next_image(lambda: root.after(HOOK_MS, write_next_segment))
            return
        if text_part == OVERLAY_TOKEN:
            # triptych modda overlay yok say
            root.after(HOOK_MS, write_next_segment)
            return

        def after_this_segment():
            root.after(HOOK_MS, write_next_segment)

        start_typewriter(text_part, on_done=after_this_segment, clear_first=(seg_i==1))

    carousel_clear()

    # ✅ Images appear ONLY when "##" (IMAGE_TOKEN) is encountered in text
    root.after(POP_DELAY_12, write_next_segment)


def _is_single_focus_layout(scn: dict) -> bool:
    lay = str(scn.get("layout", "") or "").strip().lower()
    if lay in ("single", "single_focus", "hero", "singlefocus", "focus"):
        return True
    if scn.get("single_focus") is True:
        return True
    return False


def load_scene():
    try:
        stop_video()
    except Exception:
        pass
    global scene, _flicker_cfg, sfx_started_this_scene, _dizzy_cfg
    stop_clicks()
    cancel_auto_next()
    stop_flicker()
    stop_dizzy()

    stop_sfx_loop()
    sfx_started_this_scene = False

    scene = story[current]
    unlock_if_ending(current)

    # ✅ Yeni sahneye geçince metin alanını temizle (segmentler kendi içinde biriktirir)
    try:
        story_label.config(text="")
    except Exception:
        pass

    # ✅ Yeni sahne başında seçimleri gizle (metin akarken buton görünmesin)
    hide_choices_ui()


    # ✅ AUTO NEXT
    # - auto_next_after=True  => sahne bittikten sonra geç
    # - auto_next_after=False => sahne açılır açılmaz geç (eski davranış)
    auto_next = scene.get("auto_next", None)
    auto_after = bool(scene.get("auto_next_after", False)) or ("auto_next_delay_ms" in scene)

    if auto_next and (not auto_after):
        delay = int(scene.get("auto_delay_ms", 0) or 0)
        if auto_next in story:
            root.after(max(0, delay), lambda: go_to(auto_next))
            return
        else:
            print("[AUTO_NEXT] target not found:", auto_next, "from", current)


    _flicker_cfg = scene.get("flicker", None)
    _dizzy_cfg = scene.get("dizzy", None)

    if str(current).upper().startswith("S10") and _dizzy_cfg is None:
        _dizzy_cfg = {"slot": "L", "mode": "blur", "intensity": "medium", "speed_ms": 45}

    if scene.get("final_check") is True:
        mask = 0
        for i, k in enumerate(EVENT_ORDER):
            if events.get(k, False):
                mask |= (1 << i)
        end_id = f"END_F{mask + 1:02d}"
        root.after(450, lambda: go_to(end_id))
        return

    if _is_single_focus_layout(scene):
        hero_cfg = scene.get("hero_canvas", None)
        cw = None
        ch = None
        if isinstance(hero_cfg, dict):
            cw = hero_cfg.get("w", None)
            ch = hero_cfg.get("h", None)

        set_canvas_hero_mode(custom_w=cw, custom_h=ch)

        one = scene.get("image")
        if not one:
            imgs = scene.get("images", None)
            if isinstance(imgs, (list, tuple)) and len(imgs) > 0:
                one = imgs[0]

        seg_list = split_text_into_segments(scene.get("text", ""))

        # overlay queue: scene['overlay_images'] varsa onu kullan, yoksa hero images listesinin devamı
        global _overlay_queue, _overlay_i
        _overlay_i = 0
        ov = scene.get("overlay_images", None)
        if isinstance(ov, (list, tuple)) and ov:
            _overlay_queue = list(ov)
        else:
            imgs_all = scene.get("images", None)
            if isinstance(imgs_all, (list, tuple)) and len(imgs_all) > 1:
                _overlay_queue = list(imgs_all[1:])
            else:
                _overlay_queue = []


        # ✅ overlay step triggers (token-free)
        global _overlay_step_points, _overlay_step_fired
        raw_steps = scene.get("overlay_at_steps", None)
        pts = []
        if isinstance(raw_steps, (list, tuple)):
            for x in raw_steps:
                try:
                    pts.append(int(x))
                except Exception:
                    pass
        _overlay_step_points = pts
        _overlay_step_fired = set()
        # ✅ HERO giriş animasyonu: önce görsel pop-in, sonra yazı akar
        pop_in_hero(one, on_done=lambda: (start_video(scene.get('video', None), current), play_text_segments_only(seg_list)))

        try:
            if inv_ui:
                inv_ui.refresh()
        except Exception:
            pass
        return

    set_canvas_triptych_mode()
    img_list = get_scene_images_list(scene)
    seg_list = split_text_into_segments(scene.get("text", ""))
    play_scene_segment_flow(img_list, seg_list)

    try:
        if inv_ui:
            inv_ui.refresh()
    except Exception:
        pass


# ============================================================
# ✅ 3 BUTON + (SAHNEDE VARSA) 4. BUTON + 🔒 LOCKED
# ============================================================
def show_buttons_for_scene():
    # auto-next after scene finish (if configured)
    if schedule_auto_next_after_scene():
        return

    # ✅ Dinamik buton sayısı: sahnede kaç seçenek varsa sadece onları göster.
    # - 1 seçenek -> 1 buton
    # - 2 seçenek -> 2 buton
    # - 3 seçenek -> 3 buton
    # - 4 (choices_if/choices ile) -> 4 buton
    def _hide_all_choice_containers():
        for cf in choice_containers:
            try:
                cf.pack_forget()
            except Exception:
                pass

    def _pack_containers(indices):
        # choices_row frame'i kendi içinde center kalır; çocuklar soldan dizilir.
        for idx in indices:
            try:
                choice_containers[idx].pack(side="left", padx=44)
            except Exception:
                pass

    if scene.get("ending") is True:
        def _replay():
            stop_clicks()
            stop_sfx_loop()
            stop_dizzy()
            if story and "S01_START" in story:
                go_to("S01_START")
            else:
                show_language_screen()

        # Ending ekranı: 3 buton
        choice_buttons[0].config(text="Replay", command=_replay, state="normal")
        choice_buttons[1].config(text="Gallery", command=show_gallery, state="normal")
        choice_buttons[2].config(text="Exit", command=on_escape, state="normal")
        choice_buttons[3].config(text="", state="disabled")

        _hide_all_choice_containers()
        _pack_containers([0, 1, 2])
        return

    resolved = resolve_choices(scene, STATE)
    locked = compute_locked_choices(scene, STATE)

    keys = ["1", "2", "3", "4"]

    # Hangi butonlar görünecek?
    visible_indices = []
    for i, k in enumerate(keys):
        exists = False
        if k in resolved:
            exists = True
        elif k in locked:
            exists = True

        if exists:
            visible_indices.append(i)

    # Eğer hiç seçenek yoksa (edge-case), hepsini gizle
    _hide_all_choice_containers()
    if visible_indices:
        _pack_containers(visible_indices)

    # Buton metinlerini/komutlarını ayarla
    for i, k in enumerate(keys):
        if k in resolved:
            txt = resolved[k][0]
            choice_buttons[i].config(text=txt, command=lambda kk=k: choose(kk), state="normal")
        elif k in locked:
            txt = locked[k]
            choice_buttons[i].config(text=f"🔒 {txt}", command=lambda: None, state="disabled")
        else:
            choice_buttons[i].config(text="", state="disabled")
    # ✅ Dinamik genişlik (tek tek) + minimum boy:
    # Her buton kendi metnine göre uzar, ama çok küçülmez.
    if visible_indices:
        try:
            sw = root.winfo_screenwidth()
        except Exception:
            sw = 1600

        # Ekrana göre maksimum genişlik (çok büyüyüp taşmasın)
        usable = int(sw * 0.86)

        MIN_BTN_PX = 360   # ✅ en küçük buton (senin “eski iyi boyut” hissi)
        MAX_BTN_PX = max(520, usable // max(1, len(visible_indices)))  # sahnede az buton varsa daha geniş olabilir

        for vi in visible_indices:
            try:
                t = str(choice_buttons[vi].cget("text") or "")
                f = tkfont.Font(font=choice_buttons[vi].cget("font"))

                char_px = max(8, f.measure("0"))
                text_px = f.measure(t)
                pad_px = 90  # iç boşluk hissi

                # hedef px (min koru, max sınırla)
                want_px = max(MIN_BTN_PX, min(text_px + pad_px, MAX_BTN_PX))

                # Tkinter Button width -> karakter birimi
                width_chars = max(22, int(want_px / char_px))

                # default: tek satır
                choice_buttons[vi].config(width=width_chars, padx=24, pady=8, wraplength=0, justify="center")

                # Eğer metin çok uzunsa, wrap aç (2 satıra düşebilir)
                if (text_px + pad_px) > want_px:
                    wrap_px = max(260, int(want_px - pad_px))
                    choice_buttons[vi].config(wraplength=wrap_px)
            except Exception:
                pass


def choose(choice_key):
    global current
    if not typing_done:
        return

    if scene.get("ending") is True:
        stop_all_audio()
        root.destroy()
        return

    choices = resolve_choices(scene, STATE)
    if choice_key not in choices:
        return

    choice = choices[choice_key]

    effects = choice[2] if (isinstance(choice, (list, tuple)) and len(choice) >= 3) else []
    STATE.apply_effects(effects)

    for f in effects:
        if f in events:
            events[f] = True

    choice = resolve_redirect(scene, STATE, choice_key, choice)

    next_id = choice[1]
    if next_id not in story:
        print("[BAD NEXT]", current, choice_key, next_id)
        return

    current = next_id
    load_scene()

    try:
        if inv_ui:
            inv_ui.refresh()
    except Exception:
        pass


# Endings Gallery
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

    title = tk.Label(win, text=f"Unlocked: {unlocked}/{TOTAL_ENDINGS}", bg=BG_COLOR, fg="white",
                     font=("Segoe UI Semibold", 16, "bold"))
    title.pack(pady=(16, 10))

    info = tk.Label(win, text="✅ unlocked   🔒 locked", bg=BG_COLOR, fg="#cfd6ff",
                    font=("Segoe UI Semibold", 10, "bold"))
    info.pack(pady=(0, 10))

    lst = tk.Listbox(win, bg="#0f1730", fg="white", font=("Consolas", 12), bd=0,
                     highlightthickness=2, highlightbackground="#2a3a6a",
                     selectbackground="#24335c", activestyle="none")
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
        except Exception:
            pass
        win.destroy()

    tk.Button(btns, text="Close", command=_close, bg="#1a2440", fg="white",
              bd=0, padx=18, pady=8, activebackground="#24335c", activeforeground="white",
              font=("Segoe UI Semibold", 11, "bold")).pack()


# Language selection
def reset_events():
    for k in events:
        events[k] = False
    STATE.flags.clear()
    STATE.items.clear()


def _hide_menu_logo_only():
    global menu_logo_label, menu_logo_img
    try:
        if menu_logo_label:
            menu_logo_label.place_forget()
    except Exception:
        pass


def _show_menu_logo_only():
    """
    Ana menü / dil seçimi ekranında: sadece logo görünsün,
    oyun canvas (mavi pencere) görünmesin.
    """
    global menu_logo_label, menu_logo_img

    # canvas'ı tamamen gizle
    try:
        carousel_canvas.place_forget()
    except Exception:
        pass

    if menu_logo_label is None:
        menu_logo_label = tk.Label(root, bg=BG_COLOR, bd=0)

    try:
        logo = load_photo_fit("images/logo.png", 1500, 540, _img_cache)
    except Exception:
        logo = None

    menu_logo_img = logo
    if logo:
        menu_logo_label.config(image=logo, text="")
        menu_logo_label.image = logo
    else:
        menu_logo_label.config(text="02:17", fg="white", font=("Segoe UI Semibold", 34, "bold"))

    menu_logo_label.place(relx=0.5, rely=0.30, anchor="center")


def _enter_game_view():
    _hide_menu_logo_only()
    try:
        carousel_canvas.place(relx=0.5, y=30, anchor="n")
    except Exception:
        pass


def set_english():
    global story, current, current_lang
    reset_events()
    current_lang = "EN"
    story = STORY_EN
    current = "S01_START" if "S01_START" in story else "start"
    _enter_game_view()
    load_scene()


def set_turkish():
    global story, current, current_lang
    if not STORY_TR:
        return
    reset_events()
    current_lang = "TR"
    story = STORY_TR
    current = "S01_START" if "S01_START" in story else "start"
    _enter_game_view()
    load_scene()


def on_escape(e=None):
    stop_all_audio()
    stop_dizzy()
    try:
        root.destroy()
    except Exception:
        pass


# ============================================================
# Audio Settings Overlay (music + SFX)
# ============================================================
class AudioSettingsOverlay:
    def __init__(self, master, x=18, y=18):
        self.master = master
        self.x = x
        self.y = y
        self.opened = False
        self.last_nonzero_music = 35 if music_volume_percent == 0 else music_volume_percent
        self.last_nonzero_sfx = 80 if sfx_volume_percent == 0 else sfx_volume_percent

        self.btn = tk.Canvas(master, width=60, height=60, bg=master.cget("bg"), highlightthickness=0, bd=0)
        self.btn.place(x=self.x, y=self.y)

        self.oval_id = self.btn.create_oval(3, 3, 55, 55, fill="#0f1730", outline="#2a3a6a", width=2, stipple="gray25")

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
            self.btn.create_text(30, 30, text="⚙", fill="#cfd6ff", font=("Segoe UI Semibold", 14, "bold"))

        def _hover_on(_):
            self.btn.itemconfig(self.oval_id, outline="#4f6cff")
        def _hover_off(_):
            self.btn.itemconfig(self.oval_id, outline="#2a3a6a")

        self.btn.bind("<Enter>", _hover_on)
        self.btn.bind("<Leave>", _hover_off)
        self.btn.bind("<Button-1>", self._on_btn_click)

        self.panel = tk.Frame(master, bg=BG_COLOR, bd=0, highlightthickness=0)

        self.canvas = tk.Canvas(self.panel, width=320, height=150, bg=BG_COLOR, highlightthickness=0, bd=0)
        self.canvas.pack()

        self.canvas.create_rectangle(6, 6, 314, 144, fill="#0f1730", outline="#2a3a6a", width=2, stipple="gray25")
        self.canvas.create_text(18, 22, text="AUDIO", anchor="w", fill="#cfd6ff", font=("Segoe UI Semibold", 10, "bold"))

        # Music
        self.canvas.create_text(18, 48, text="MUSIC", anchor="w", fill="#cfd6ff", font=("Segoe UI Semibold", 9, "bold"))
        self.music_value_id = self.canvas.create_text(300, 48, text=f"{music_volume_percent}%", anchor="e", fill="white",
                                                      font=("Segoe UI Semibold", 9, "bold"))
        self.music_scale = tk.Scale(self.panel, from_=0, to=100, orient="horizontal", length=190, showvalue=0,
                                    command=self.on_music_slide, bg="#0f1730", fg="white", troughcolor="#121a30",
                                    highlightthickness=0, bd=0)
        self.music_scale.set(music_volume_percent)
        self.music_scale.place(x=18, y=58)

        # ✅ SFX
        self.canvas.create_text(18, 92, text="SFX (ORTAM SESLERI)", anchor="w", fill="#cfd6ff",
                                font=("Segoe UI Semibold", 9, "bold"))
        self.sfx_value_id = self.canvas.create_text(300, 92, text=f"{sfx_volume_percent}%", anchor="e", fill="white",
                                                    font=("Segoe UI Semibold", 9, "bold"))
        self.sfx_scale = tk.Scale(self.panel, from_=0, to=100, orient="horizontal", length=190, showvalue=0,
                                  command=self.on_sfx_slide, bg="#0f1730", fg="white", troughcolor="#121a30",
                                  highlightthickness=0, bd=0)
        self.sfx_scale.set(sfx_volume_percent)
        self.sfx_scale.place(x=18, y=102)

        self.mute_music_btn = tk.Button(self.panel, text="MUTE MUSIC", command=self.mute_music_toggle,
                                        bg="#111a33", fg="#cfd6ff", bd=0, activebackground="#24335c",
                                        activeforeground="white", font=("Segoe UI Semibold", 9, "bold"))
        self.mute_sfx_btn = tk.Button(self.panel, text="MUTE SFX", command=self.mute_sfx_toggle,
                                      bg="#111a33", fg="#cfd6ff", bd=0, activebackground="#24335c",
                                      activeforeground="white", font=("Segoe UI Semibold", 9, "bold"))
        self.mute_music_btn.place(x=220, y=58, width=90, height=22)
        self.mute_sfx_btn.place(x=220, y=102, width=90, height=22)

        self.master.bind("<Button-1>", self._global_click, add="+")

    def lift(self):
        try:
            self.btn.tkraise()
        except Exception:
            pass
        if self.opened:
            try:
                self.panel.tkraise()
            except Exception:
                pass

    def _update_labels(self):
        self.canvas.itemconfig(self.music_value_id, text=f"{music_volume_percent}%")
        self.canvas.itemconfig(self.sfx_value_id, text=f"{sfx_volume_percent}%")
        if self.music_scale.get() != music_volume_percent:
            self.music_scale.set(music_volume_percent)
        if self.sfx_scale.get() != sfx_volume_percent:
            self.sfx_scale.set(sfx_volume_percent)

        self.mute_music_btn.config(text="UNMUTE M" if music_volume_percent == 0 else "MUTE MUSIC")
        self.mute_sfx_btn.config(text="UNMUTE S" if sfx_volume_percent == 0 else "MUTE SFX")

    def open(self):
        if self.opened:
            return
        self.opened = True
        self.panel.place(x=self.x + 46, y=self.y)
        self._update_labels()
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

    def on_music_slide(self, val):
        set_music_volume_percent(int(float(val)))
        if music_volume_percent > 0:
            self.last_nonzero_music = music_volume_percent
        self._update_labels()

    def on_sfx_slide(self, val):
        set_sfx_volume_percent(int(float(val)))
        if sfx_volume_percent > 0:
            self.last_nonzero_sfx = sfx_volume_percent
        self._update_labels()

    def mute_music_toggle(self):
        if music_volume_percent > 0:
            self.last_nonzero_music = music_volume_percent
            self.music_scale.set(0)
        else:
            self.music_scale.set(self.last_nonzero_music if self.last_nonzero_music > 0 else 35)

    def mute_sfx_toggle(self):
        if sfx_volume_percent > 0:
            self.last_nonzero_sfx = sfx_volume_percent
            self.sfx_scale.set(0)
        else:
            self.sfx_scale.set(self.last_nonzero_sfx if self.last_nonzero_sfx > 0 else 80)


# ============================================================
# ✅ Inventory Overlay (Çanta)
# ============================================================
class InventoryOverlay:
    def __init__(self, master, x=90, y=18):
        self.master = master
        self.x = x
        self.y = y
        self.opened = False

        self.btn = tk.Button(
            master, text="Çanta",
            command=self.toggle,
            bg="#0f1730", fg="#cfd6ff", bd=0,
            activebackground="#24335c", activeforeground="white",
            font=("Segoe UI Semibold", 11, "bold")
        )
        self.btn.place(x=self.x, y=self.y, width=80, height=40)

        self.panel = tk.Frame(master, bg=BG_COLOR, bd=0, highlightthickness=0)
        self.box = tk.Frame(self.panel, bg="#0f1730", bd=2, highlightbackground="#2a3a6a", highlightthickness=2)
        self.box.pack(padx=0, pady=0)

        self.title = tk.Label(self.box, text="ENVANTER", bg="#0f1730", fg="white",
                              font=("Segoe UI Semibold", 11, "bold"))
        self.title.pack(padx=14, pady=(10, 6), anchor="w")

        self.list_lbl = tk.Label(self.box, text="", bg="#0f1730", fg="#cfd6ff",
                                 justify="left", font=("Consolas", 11))
        self.list_lbl.pack(padx=14, pady=(0, 12), anchor="w")

        self.master.bind("<Button-1>", self._global_click, add="+")

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

    def refresh(self):
        items = sorted(list(STATE.items))
        if not items:
            text = "Boş."
        else:
            pretty = [it.replace("I_", "") for it in items]
            text = "\n".join([f"• {p}" for p in pretty])
        self.list_lbl.config(text=text)

    def open(self):
        if self.opened:
            return
        self.opened = True
        self.refresh()
        self.panel.place(x=self.x, y=self.y + 46)
        self.box.pack()

    def close(self):
        if not self.opened:
            return
        self.opened = False
        self.panel.place_forget()

    def toggle(self):
        self.close() if self.opened else self.open()

    def lift(self):
        try:
            self.btn.tkraise()
        except Exception:
            pass
        if self.opened:
            try:
                self.panel.tkraise()
            except Exception:
                pass


# ============================================================
# ✅ MAIN MENU: [ GALLERY ] [ BAŞLA ] [ AYARLAR ] [+ ÇIKIŞ]
# ============================================================
def show_main_menu():
    stop_clicks()
    stop_sfx_loop()
    stop_flicker()
    stop_dizzy()

    _show_menu_logo_only()

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    card.pack(padx=30, pady=(600, 22), fill="x")
    story_label.config(text="02:17\n\nAna Menü")

    def _open_settings():
        try:
            audio_ui.open()
            audio_ui.lift()
        except Exception:
            pass

    choice_buttons[0].config(text="GALLERY", command=show_gallery, state="normal")
    choice_buttons[1].config(text="BAŞLA", command=show_language_screen, state="normal")
    choice_buttons[2].config(text="AYARLAR", command=_open_settings, state="normal")
    choice_buttons[3].config(text="ÇIKIŞ", command=on_escape, state="normal")

    try:
        if not choice_containers[3].winfo_ismapped():
            choice_containers[3].pack(side="left", padx=44)
    except Exception:
        pass

    audio_ui.lift()
    try:
        inv_ui.lift()
    except Exception:
        pass


def show_language_screen():
    stop_clicks()
    stop_sfx_loop()
    stop_flicker()
    stop_dizzy()

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    _show_menu_logo_only()

    card.pack(padx=30, pady=(600, 22), fill="x")
    story_label.config(text="Select Language / Dil Seç")

    choice_buttons[0].config(text="English", command=set_english, state="normal")
    choice_buttons[1].config(text="Türkçe", command=set_turkish, state=("normal" if STORY_TR else "disabled"))
    choice_buttons[2].config(text="Geri (Ana Menü)", command=show_main_menu, state="normal")
    choice_buttons[3].config(text="", state="disabled")
    try:
        choice_containers[3].pack_forget()
    except Exception:
        pass

    audio_ui.lift()
    try:
        inv_ui.lift()
    except Exception:
        pass


def start_main_after_splash(splash):
    try:
        splash.destroy()
    except Exception:
        pass

    root.deiconify()
    root.attributes("-fullscreen", True)
    root.focus_force()

    show_main_menu()
    play_music_loop()


def show_splash_logo(duration_ms=1400):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg=BG_COLOR)

    logo = load_photo_fit("images/logo.png", 1800, 720, _img_cache)

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = 1090, 720
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


# ============================================================
# DEV TOOLS: Jump, Key Choices, Skip Typing
# ============================================================
def normalize_jump_input(raw: str):
    s = (raw or "").strip().upper()
    if not s:
        return None
    if re.fullmatch(r"\d+", s):
        n = int(s)
        return f"S{n:02d}"
    m = re.fullmatch(r"S(\d+)", s)
    if m:
        n = int(m.group(1))
        return f"S{n:02d}"
    return s


def resolve_scene_id(query: str):
    if not story:
        return None

    q = normalize_jump_input(query)
    if not q:
        return None

    if q in story:
        return q

    if re.fullmatch(r"S\d{2}", q):
        prefix = q + "_"
        matches = sorted([k for k in story.keys() if k.startswith(prefix)])
        if matches:
            return matches[0]
        matches2 = sorted([k for k in story.keys() if k.startswith(q)])
        if matches2:
            return matches2[0]

    return None


def open_jump_dialog(e=None):
    if story is None:
        return
    win = tk.Toplevel(root)
    win.title("Jump to Scene")
    win.configure(bg=BG_COLOR)
    win.transient(root)
    win.grab_set()

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    w, h = 520, 200
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    lbl = tk.Label(
        win,
        text="ID yaz: S6 / 6 / S06_GALLERY gibi. Enter'a bas:",
        bg=BG_COLOR, fg="white",
        font=("Segoe UI Semibold", 12, "bold")
    )
    lbl.pack(pady=(18, 10))

    entry = tk.Entry(win, font=("Consolas", 14), bd=0, relief="flat")
    entry.pack(padx=18, fill="x")
    entry.focus_force()

    hint = tk.Label(win, text="", bg=BG_COLOR, fg="#cfd6ff", font=("Segoe UI Semibold", 10, "bold"))
    hint.pack(pady=(8, 0))

    def do_jump(_=None):
        sid = resolve_scene_id(entry.get())
        if sid:
            try:
                win.grab_release()
            except Exception:
                pass
            win.destroy()
            go_to(sid)
        else:
            entry.delete(0, "end")
            entry.insert(0, "NOT FOUND")
            hint.config(text="Örn: S6 yazınca S06_* ilk sahneye atlar.")

    entry.bind("<Return>", do_jump)

    btns = tk.Frame(win, bg=BG_COLOR)
    btns.pack(pady=12)

    tk.Button(btns, text="JUMP", command=do_jump, bg="#1a2440", fg="white", bd=0, padx=18, pady=8,
              activebackground="#24335c", activeforeground="white",
              font=("Segoe UI Semibold", 10, "bold")).pack(side="left", padx=8)

    tk.Button(btns, text="CLOSE", command=lambda: (win.grab_release(), win.destroy()),
              bg="#111a33", fg="#cfd6ff", bd=0, padx=18, pady=8,
              activebackground="#24335c", activeforeground="white",
              font=("Segoe UI Semibold", 10, "bold")).pack(side="left", padx=8)


def key_choice(e):
    k = e.keysym
    if k in ("1", "2", "3", "4"):
        choose(k)


def skip_typing(e=None):
    global index, typing_done, after_segment_hook
    if typing_done:
        return
    remaining = full_text[index:]
    story_label.config(text=story_label.cget("text") + remaining)
    index = len(full_text)
    typing_done = True
    stop_clicks()

    if after_segment_hook:
        cb = after_segment_hook
        after_segment_hook = None
        root.after(0, cb)
    else:
        show_buttons_for_scene()


def on_space(e=None):
    global waiting_pagebreak, _last_space_ts, _space_down

    # ✅ Debounce: ignore OS key-repeat while SPACE is held down
    if _space_down:
        return "break"
    _space_down = True

    # ✅ Minimum interval between accepted SPACE presses
    now = time.perf_counter()
    if (now - _last_space_ts) * 1000.0 < SPACE_COOLDOWN_MS:
        return "break"
    _last_space_ts = now

    if waiting_pagebreak:
        _continue_after_pagebreak()
        return "break"

    skip_typing(e)
    return "break"


def on_space_release(e=None):
    global _space_down
    _space_down = False
    return "break"

    skip_typing(e)
    return "break"


# ----------------------------
# Build UI
# ----------------------------
root = tk.Tk()
root.configure(bg=BG_COLOR)
root.title("02:17")
root.withdraw()
root.bind("<Escape>", on_escape)
root.protocol("WM_DELETE_WINDOW", on_escape)

# DEV binds
root.bind("j", open_jump_dialog)
root.bind("J", open_jump_dialog)
root.bind("1", key_choice)
root.bind("2", key_choice)
root.bind("3", key_choice)
root.bind("4", key_choice)
root.bind("<KeyPress-space>", on_space)
root.bind("<KeyRelease-space>", on_space_release)

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

# Triptych canvas (default)
carousel_canvas = tk.Canvas(root, width=CAROUSEL_W, height=CAROUSEL_H, bg=BG_COLOR, highlightthickness=0, bd=0)
carousel_canvas.place(relx=0.5, y=30, anchor="n")

# Card
card = tk.Frame(root, bg=BG_COLOR, bd=2, relief="groove")

story_label = tk.Label(card, text="Select Language / Dil Seç",
                       font=("Segoe UI Semibold", 18), wraplength=1400, justify="center",
                       bg=BG_COLOR, fg="white")
story_label.pack(padx=22, pady=(18, 16))

choices_row = tk.Frame(card, bg=BG_COLOR)
choices_row.pack(pady=(0, 18))

choice_buttons = []
choice_borders = []
choice_containers = []

for _i in range(4):
    cf = tk.Frame(choices_row, bg=BG_COLOR)
    cf.pack(side="left", padx=44)
    choice_containers.append(cf)

    border = tk.Frame(cf, bg=BORDER_OFF)
    border.pack(pady=(0, 10))
    choice_borders.append(border)

    btn = tk.Button(border, text="", width=24, height=1, bd=0, relief="flat",
                    bg="#1a2440", fg="white", activebackground="#24335c",
                    activeforeground="white", font=("Segoe UI Semibold", 16))
    btn.pack(padx=2, pady=2)
    choice_buttons.append(btn)

    bind_border_hover(btn, border)

for b in choice_buttons:
    b.config(text="", state="disabled")

audio_ui = AudioSettingsOverlay(root, x=18, y=18)
inv_ui = InventoryOverlay(root, x=90, y=18)

card.lift()
audio_ui.lift()
inv_ui.lift()

try:
    _ensure_click_assets()
except Exception:
    pass

# Start
show_splash_logo(duration_ms=1400)
root.mainloop()
