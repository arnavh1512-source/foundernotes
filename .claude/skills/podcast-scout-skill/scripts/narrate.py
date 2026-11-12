#!/usr/bin/env python3
"""Synthesize narration or a multi-speaker cast with Voicebox and write timings + captions.

    python3 narrate.py SCRIPT.json --out DIR [--engine kokoro|piper|edge|voicebox|files]
                                   [--voice NAME] [--speed 1.0] [--allow-non-male]
    python3 narrate.py --list-voices

SCRIPT.json (see assets/narration-script.example.json):
    {"voice": {"engine": "kokoro", "name": "am_michael", "speed": 1.0},
     "lead": 0.3, "tail": 0.8,
     "segments": [{"id": "s01", "text": "Spoken words (respell names here)...", "display": "Same words, correct spelling",
                   "pause_after": 0.4}]}
A plain .txt/.md file also works: each blank-line-separated paragraph becomes one segment.

Outputs in DIR:
    segments/<id>.wav    one take per segment (re-used if text+voice unchanged)
    narration.wav        48 kHz mono master with lead/pauses/tail
    timings.json         start/end of every segment on the master clock (drives scene timing)
    captions.srt/.vtt    single-line captions; word timing inside a segment is ESTIMATED from
                         character counts (good enough for captions, not for lip-sync)

Default voice policy: established male narrator. With a validated Voicebox cast,
individual character segments may use authorized synthetic male or female profiles;
this does NOT change the narrator's identity or permit unapproved cloning.
"""
from __future__ import annotations

import argparse
import hashlib
import json, time
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import wave
from pathlib import Path

SR = 48000
VOICES_DIR = Path(os.environ.get("STUDIO_VOICES_DIR", Path.home() / ".cache" / "studio-voices"))

# Male voices only. Defaults first.
MALE_VOICES = {
    "kokoro": ["am_michael", "am_adam", "am_fenrir", "am_onyx", "am_eric", "am_liam", "am_echo",
               "am_puck", "bm_george", "bm_lewis", "bm_daniel", "bm_fable"],
    "piper": ["en_US-ryan-high", "en_US-ryan-medium", "en_US-joe-medium", "en_US-john-medium",
              "en_US-bryce-medium", "en_US-norman-medium", "en_GB-alan-medium",
              "en_GB-northern_english_male-medium"],
    "edge": ["en-US-AndrewNeural", "en-US-GuyNeural", "en-US-BrianNeural", "en-US-ChristopherNeural",
             "en-US-EricNeural", "en-US-RogerNeural", "en-US-SteffanNeural", "en-GB-RyanNeural",
             "en-GB-ThomasNeural", "en-AU-WilliamNeural", "en-IN-PrabhatNeural",
             "en-US-AndrewMultilingualNeural", "en-US-BrianMultilingualNeural"],
}
DEFAULT_VOICE = {"kokoro": "am_michael", "piper": "en_US-ryan-high", "edge": "en-US-AndrewNeural"}
ENGINE_ORDER = ["kokoro", "piper", "edge"]
# Parler-TTS: the voice is a written DESCRIPTION (no reference recording, no cloning). Chosen by the owner after an
# A/B listen (2026-11): pitch movement 8.6 st vs 3.8 st for Kokoro, earshot "Speech synthesizer" 0.71 vs 0.89.
PARLER_DESC = ("A man with a warm, low-pitched voice speaks in a calm, friendly, conversational tone, like a teacher "
               "explaining something interesting, with natural pauses at a moderate pace. The recording is very clear and "
               "close-sounding, with almost no background noise.")   # owner-approved channel voice ("C"), 2026-11-06
PARLER_MODEL = os.environ.get("PARLER_MODEL", "parler-tts/parler-tts-mini-v1")
PARLER_VOICE_V = "anchor-c1"   # one channel voice: anchor take + best-of-N speaker match + pitch settling (parler_worker.py)


def parler_python():
    return os.environ.get("PARLER_PYTHON") or str(Path.home() / ".cache" / "venv-parler" / "bin" / "python")


def have_parler() -> bool:
    return Path(parler_python()).exists()


def parler_is_male(desc: str) -> bool:
    d = desc.lower()
    return bool(re.search(r"\bmale\b|\bman\b|\bmale's\b", d)) and not re.search(r"female|woman|girl|\blady\b", d)


def die(msg: str, code: int = 2):
    print(f"narrate: {msg}", file=sys.stderr)
    sys.exit(code)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


# ---------------------------------------------------------------- script loading
def load_script(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.lstrip().startswith("#")]
        data = {"segments": [{"id": f"s{i+1:02d}", "text": " ".join(p.split())} for i, p in enumerate(paras)]}
    segs = data.get("segments") or []
    if not segs:
        die("script has no segments")
    seen = set()
    for i, s in enumerate(segs):
        s.setdefault("id", f"s{i+1:02d}")
        if s["id"] in seen:
            die(f"duplicate segment id {s['id']}")
        seen.add(s["id"])
        if not str(s.get("text", "")).strip():
            die(f"segment {s['id']} has no text")
        if s.get("display"):
            a, b = len(str(s["text"]).split()), len(str(s["display"]).split())
            if abs(a - b) > max(2, 0.2 * a):
                print(f"narrate: warning: {s['id']} display has {b} words vs {a} spoken; captions should "
                      f"match speech (use display only for spelling fixes)", file=sys.stderr)
    return data


# ---------------------------------------------------------------- engines
def have_kokoro() -> bool:
    try:
        import kokoro_onnx  # noqa: F401
    except Exception:
        return False
    return (VOICES_DIR / "kokoro-v1.0.onnx").exists() and (VOICES_DIR / "voices-v1.0.bin").exists()


def tool(name: str):
    """Find a console script next to this Python first (venv bin/ or Windows Scripts/), then on PATH."""
    here = Path(sys.executable).parent
    for cand in (here / name, here / f"{name}.exe", here / "Scripts" / f"{name}.exe", here / "bin" / name):
        if cand.exists():
            return str(cand)
    return shutil.which(name)


def have_piper(voice: str) -> bool:
    return tool("piper") is not None and (VOICES_DIR / f"{voice}.onnx").exists()


def have_edge() -> bool:
    try:
        import edge_tts  # noqa: F401
        return True
    except Exception:
        return tool("edge-tts") is not None


_KOKORO = None


def synth_kokoro(text, voice, speed, out: Path):
    global _KOKORO
    from kokoro_onnx import Kokoro
    import soundfile as sf
    if _KOKORO is None:
        _KOKORO = Kokoro(str(VOICES_DIR / "kokoro-v1.0.onnx"), str(VOICES_DIR / "voices-v1.0.bin"))
    lang = "en-gb" if voice.startswith("b") else "en-us"
    samples, sr = _KOKORO.create(text, voice=_kokoro_voice(voice), speed=float(speed), lang=lang)
    tmp = out.with_suffix(".raw.wav")
    sf.write(str(tmp), samples, sr)
    to_master_format(tmp, out)
    tmp.unlink(missing_ok=True)


def _kokoro_voice(voice):
    """'am_fenrir+am_puck' or 'am_fenrir:0.6+am_puck:0.4' → a blended style vector (all parts must be male)."""
    if "+" not in voice:
        return voice
    parts = [(p.split(":")[0], float(p.split(":")[1]) if ":" in p else 1.0) for p in voice.split("+")]
    tot = sum(w for _, w in parts)
    return sum(_KOKORO.get_voice_style(n) * (w / tot) for n, w in parts)


_NUMWORD = re.compile(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|"
                      r"sixty|seventy|eighty|ninety|hundred|thousand|million|percent)\b", re.I)


def perform_plan(sentences, seed_text):
    """Delivery for each sentence, like a human explainer: (speed multiplier, pitch shift in semitones, gain dB,
    pause after in s). Deterministic: jitter is seeded from the text, so the same script always sounds the same."""
    plan = []
    for i, snt in enumerate(sentences):
        h = int(hashlib.sha256(f"{seed_text}|{i}|{snt}".encode()).hexdigest()[:8], 16)
        j = lambda k, amp: ((h >> (k * 8)) % 1000 / 1000 - 0.5) * 2 * amp     # noqa: E731
        n = len(snt.split()); q = snt.rstrip().endswith("?"); ex = snt.rstrip().endswith("!")
        short = n <= 5; long_ = n >= 18; nums = bool(_NUMWORD.search(snt))
        turn = bool(re.match(r"(but|so|yet|and yet|still|now)\b", snt.strip(), re.I))
        sp = 1.0 + (-0.08 if short else 0) + (-0.05 if q else 0) + (-0.05 if nums else 0) + (0.04 if long_ else 0) + j(0, 0.025)
        st = (0.35 if i == 0 else 0) + (0.55 if q else 0) + (0.3 if ex else 0) + (-0.35 if short and not q else 0) \
            + (0.25 if turn else 0) + j(1, 0.25)
        db = (0.8 if short else 0) + (-0.4 if long_ else 0) + j(2, 0.5)
        nxt = sentences[i + 1] if i + 1 < len(sentences) else ""
        # pauses breathe like speech: longer after questions, before a punchline, at a turn; never metronomic
        pause = 0.34 + (0.22 if q else 0) + (0.16 if nxt and len(nxt.split()) <= 5 else 0) + (0.2 if "..." in snt[-4:] else 0) \
            + (0.14 if re.match(r"(but|so|yet|now)\b", nxt.strip(), re.I) else 0) + j(3, 0.12)
        plan.append((max(0.85, min(1.08, sp)), max(-0.8, min(0.9, st)), db, max(0.18, pause)))
    return plan


PERFORM_VERSION = "p3"


def synth_kokoro_performed(text, voice, speed, out: Path, mode="pace"):
    """Sentence-by-sentence synthesis with varied pace, pitch, level and pauses (see perform_plan)."""
    global _KOKORO
    from kokoro_onnx import Kokoro
    import numpy as np, soundfile as sf
    if _KOKORO is None:
        _KOKORO = Kokoro(str(VOICES_DIR / "kokoro-v1.0.onnx"), str(VOICES_DIR / "voices-v1.0.bin"))
    v = _kokoro_voice(voice)
    lang = "en-gb" if voice.startswith("b") else "en-us"
    sentences = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x.strip()]
    chunks, sr = [], 24000
    with tempfile.TemporaryDirectory() as td:
        for k, (snt, (sp, st, db, pause)) in enumerate(zip(sentences, perform_plan(sentences, text))):
            y, sr = _KOKORO.create(snt, voice=v, speed=float(speed) * sp, lang=lang)
            a = Path(td) / f"s{k}.wav"; b = Path(td) / f"s{k}p.wav"
            sf.write(str(a), y, sr)
            # earshot listening (2026-11): pitch-shifting each sentence made the voice read as "glitchy / speech
            # synthesizer", so the default mode is "pace" (pace, pauses only); "full" keeps pitch + level
            af = [f"volume={db:.2f}dB" if mode == "full" else "anull"]
            if mode == "full" and abs(st) > 0.05 and has_rubberband():
                af.insert(0, f"rubberband=pitch={2 ** (st / 12):.5f}:formant=preserved:pitchq=quality")
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(a), "-af", ",".join(af), str(b)])
            y2, _ = sf.read(str(b), dtype="float32")
            # trim engine silence at both ends so our pause is the pause
            nz = np.flatnonzero(np.abs(y2) > 0.004)
            if nz.size:
                y2 = y2[max(nz[0] - int(0.02 * sr), 0): nz[-1] + int(0.06 * sr)]
            chunks.append(y2)
            if k < len(sentences) - 1:
                chunks.append(np.zeros(int(pause * sr), dtype="float32"))
        tmp = out.with_suffix(".raw.wav")
        y_all = np.concatenate(chunks) if chunks else np.zeros(1, "float32")
        pk = float(np.max(np.abs(y_all))) or 1.0
        sf.write(str(tmp), y_all * min(1.0, 0.89 / pk), sr)       # never clip (peak <= -1 dBFS)
    to_master_format(tmp, out)
    tmp.unlink(missing_ok=True)


_RB = None


def has_rubberband():
    global _RB
    if _RB is None:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True)
        _RB = " rubberband " in r.stdout
    return _RB


def synth_piper(text, voice, speed, out: Path):
    tmp = out.with_suffix(".raw.wav")
    length_scale = 1.0 / float(speed) if float(speed) > 0 else 1.0
    subprocess.run([tool("piper") or "piper", "-m", str(VOICES_DIR / f"{voice}.onnx"), "-f", str(tmp),
                    "--length_scale", f"{length_scale:.3f}", "--sentence_silence", "0.25"],
                   input=text.encode(), check=True, capture_output=True)
    to_master_format(tmp, out)
    tmp.unlink(missing_ok=True)


def synth_edge(text, voice, speed, out: Path):
    tmp = out.with_suffix(".mp3")
    rate = f"{int(round((float(speed) - 1) * 100)):+d}%"
    exe = [tool("edge-tts")] if tool("edge-tts") else [sys.executable, "-m", "edge_tts"]
    run(exe + ["--voice", voice, f"--rate={rate}", "--text", text, "--write-media", str(tmp)])
    to_master_format(tmp, out)
    tmp.unlink(missing_ok=True)


VOICE_DIR_REPO = Path(__file__).resolve().parent.parent / "assets" / "voice"
CHANNEL_NARRATOR = "founder-notes"          # alias: the owner-approved channel narrator on voicebox (Chatterbox)
CHANNEL_NARRATOR_NAME = "Founder Notes Narrator"
CHANNEL_NARRATOR_ENGINE = "chatterbox"


def voicebox_url():
    return os.environ.get("VOICEBOX_URL", "http://127.0.0.1:17493")


# Owner rule 2026-11-12: the owner-supplied voice is the channel narrator. It is a real person's voice (consent stated
# by the owner), so its reference clip lives in a git-ignored folder and is never committed to this public repo.
OWNER_NARRATOR_NAME = "Owner-Supplied Narrator (consented)"
OWNER_NARRATOR_REF = VOICE_DIR_REPO / "local" / "owner-narrator-ref.wav"


def pick_channel_profile(profiles, owner_ref_exists):
    """Choose the channel narrator. Returns (profile_id or None, kind): the owner voice if its profile or local
    reference exists, otherwise the synthetic fallback. None means the profile has to be created from the reference."""
    by = {p.get("name"): p["id"] for p in profiles if p.get("sample_count", 1)}
    if OWNER_NARRATOR_NAME in by:
        return by[OWNER_NARRATOR_NAME], "owner"
    if owner_ref_exists:
        return None, "owner"
    return by.get(CHANNEL_NARRATOR_NAME), "synthetic"


def voicebox_channel_profile():
    """Find (or create once) the channel narrator profile in the local voicebox server: the owner-supplied voice when
    its local reference is on this machine, else the SYNTHETIC repo reference (founder-notes-narrator-ref.wav)."""
    base = voicebox_url()
    with urllib.request.urlopen(f"{base}/profiles", timeout=30) as r:
        pid, kind = pick_channel_profile(json.loads(r.read()), OWNER_NARRATOR_REF.exists())
    if kind == "synthetic":
        print(f"narrate: WARNING owner narrator reference not found at {OWNER_NARRATOR_REF}; using the synthetic "
              "fallback voice. Ask the owner for the clip before narrating a real video.", file=sys.stderr)
    if pid:
        return pid
    name, desc, ref = ((OWNER_NARRATOR_NAME, "Cloned from an owner-supplied recording; speaker consent stated by owner", OWNER_NARRATOR_REF)
                       if kind == "owner" else
                       (CHANNEL_NARRATOR_NAME, "Synthetic channel narrator (owner-approved). Not a real person.", VOICE_DIR_REPO / "founder-notes-narrator-ref.wav"))
    req = urllib.request.Request(f"{base}/profiles", headers={"Content-Type": "application/json"}, data=json.dumps(
        {"name": name, "language": "en", "voice_type": "cloned", "description": desc}).encode())
    with urllib.request.urlopen(req, timeout=30) as r:
        pid = json.loads(r.read())["id"]
    txt = ref.with_suffix(".txt").read_text().strip()
    bnd = "----narrate" + hashlib.sha1(txt.encode()).hexdigest()[:12]
    body = (f"--{bnd}\r\nContent-Disposition: form-data; name=\"reference_text\"\r\n\r\n{txt}\r\n"
            f"--{bnd}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"ref.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() \
        + ref.read_bytes() + f"\r\n--{bnd}--\r\n".encode()
    req = urllib.request.Request(f"{base}/profiles/{pid}/samples", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={bnd}"})
    urllib.request.urlopen(req, timeout=60).read()
    print(f"narrate: created the voicebox profile '{name}' from {ref.name}", file=sys.stderr)
    return pid


def trim_tail(path: Path, drop_db=15.0, keep=0.25):
    """Cut what follows the last real speech. Chatterbox sometimes adds a low growl/mumble after the final word
    (measured: up to 6 s at -35 dB, ~64 Hz). Speech end = last 20 ms frame within drop_db of the segment's typical
    voiced level; keep a short natural tail after it."""
    try:
        import numpy as np, soundfile as sf
    except ImportError:
        return
    y, sr = sf.read(str(path), dtype="float32")
    mono = y.mean(axis=1) if y.ndim > 1 else y
    hop = int(0.02 * sr); n = len(mono) // hop
    if n < 10:
        return
    rms = np.sqrt((mono[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(rms); voiced = db[db > db.max() - 40]
    ref = np.median(voiced) if voiced.size else db.max()
    loud = np.flatnonzero(db > ref - drop_db)
    if not loud.size:
        return
    end = min(len(mono), (loud[-1] + 1) * hop + int(keep * sr))
    if len(mono) - end > int(0.3 * sr):
        y = y[:end]
        fade = min(len(y), int(0.03 * sr)); w = np.linspace(1, 0, fade, dtype="float32")
        y[-fade:] = (y[-fade:].T * w).T if y.ndim > 1 else y[-fade:] * w
        sf.write(str(path), y, sr)


def synth_voicebox(text, voice, speed, out: Path, seed=42, engine=None):
    """voicebox (github.com/jamiepine/voicebox) running locally; voice = profile id (the channel narrator by default).
    Each segment is generated in ONE pass, so the voice cannot switch mid-segment."""
    base = voicebox_url()
    body = {"profile_id": voice, "text": text, "language": "en", "seed": int(seed)}
    eng = engine or os.environ.get("VOICEBOX_ENGINE")
    if eng:
        body["engine"] = eng
    if os.environ.get("VOICEBOX_INSTRUCT"):
        body["instruct"] = os.environ["VOICEBOX_INSTRUCT"]
    tmp = out.with_suffix(".raw.wav")
    for attempt in range(3):                 # an engine error on one seed: try again with the next seed
        req = urllib.request.Request(f"{base}/generate/stream", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                tmp.write_bytes(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 2:
                raise
            print(f"  voicebox: server error {e.code}, retrying with seed {body['seed'] + 1}", file=sys.stderr)
            body["seed"] = int(body["seed"]) + 1
            time.sleep(2)
    to_master_format(tmp, out, speed=speed)
    tmp.unlink(missing_ok=True)
    trim_tail(out)


def synth_files(seg_id, voice_dir: Path, out: Path, speed):
    src = voice_dir / f"{seg_id}.wav"
    if not src.exists():
        die(f"files engine: missing recording {src}")
    to_master_format(src, out, speed=speed)


def to_master_format(src: Path, dst: Path, speed=1.0):
    af = ["aresample=48000", "highpass=f=70"]
    if abs(float(speed) - 1.0) > 1e-3:
        af.insert(0, f"atempo={float(speed):.3f}")
    # trim leading/trailing silence so pauses are controlled by the script, not the engine
    af += ["silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05",
           "areverse", "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08", "areverse"]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR),
         "-af", ",".join(af), "-c:a", "pcm_s16le", str(dst)])


# A recording chain for TTS narration, chosen by LISTENING with earshot (2026-11, same passage, loudness-matched):
# AudioSet "Speech synthesizer" 0.88 → 0.33 and "Narration, monologue" 0.17 → 0.30 for am_michael, every word still
# transcribed. Raw TTS is unnaturally clean (noise floor ~-120 dBFS): a small room, a warm mic EQ, gentle compression
# and a pink room tone make it read as a voice recorded in a room. Length is unchanged, so timings stay valid.
VOICE_CHAINS = {
    "studio": ("aecho=0.85:0.58:18|30|44|58:0.13|0.09|0.05|0.03,equalizer=f=170:t=q:w=1:g=2,"
               "equalizer=f=6500:t=q:w=2:g=-1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120", 0.003),
    "dry": ("equalizer=f=170:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120", 0.0016),
}


def apply_voice_chain(path: Path, name: str):
    if name not in VOICE_CHAINS:
        die(f"unknown voice chain '{name}' (choose {', '.join(VOICE_CHAINS)} or none)")
    fx, amp = VOICE_CHAINS[name]
    tmp = path.with_suffix(".chain.wav")
    d = wav_seconds(path)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-f", "lavfi", "-t", f"{d + 1:.3f}", "-i",
         f"anoisesrc=color=pink:amplitude={amp}:seed=11", "-filter_complex",
         f"[0]{fx}[v];[1]lowpass=f=6000,highpass=f=80[n];[v][n]amix=inputs=2:duration=first:normalize=0,"
         f"alimiter=limit=0.89", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(tmp)])
    tmp.replace(path)


def wav_seconds(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / float(w.getframerate())


def silence(seconds: float, out: Path):
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono",
         "-t", f"{max(seconds, 0.01):.3f}", "-c:a", "pcm_s16le", str(out)])


# ---------------------------------------------------------------- captions
# words a caption line should not end on (articles, prepositions, auxiliaries, determiners): the
# reader would be left hanging; keep them with the next words instead
_BAD_END = set("a an the of to in into and or nor for with at on by from that than as not under over about "
               "is was were are be been no so but if when where what how who which whose their his her its my "
               "your our each every only this these those more most less very".split())


def _bad_end(w: str) -> bool:
    if re.search(r"[.!?;:,]$", w):
        return False
    lw = w.lower().strip("\"'“”‘’()")
    # a bare number is half of "number + unit" (30 → days); keep them together
    return lw in _BAD_END or re.fullmatch(r"\d[\d.,]*", lw) is not None


_CONJ = set("and but or because so which who whose where when while though although if than".split())


def _chunk_sentence(words, max_chars):
    cur, out = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > max_chars:
            # best break: after punctuation > before a conjunction > latest word that doesn't dangle
            minlen = max_chars * 0.4
            cands = [j for j in range(len(cur) - 1, 0, -1) if len(" ".join(cur[: j + 1])) >= minlen] or [len(cur) - 1]
            j = next((j for j in cands if re.search(r"[,;:]$", cur[j])), None)
            if j is None:
                j = next((j for j in cands if j + 1 < len(cur) and cur[j + 1].lower() in _CONJ and not _bad_end(cur[j])), None)
            if j is None:
                j = next((j for j in cands if not _bad_end(cur[j])), cands[0])
            out.append(cur[: j + 1]); cur = cur[j + 1:]
        cur.append(w)
    if cur:
        out.append(cur)
    return [" ".join(c) for c in out]


def caption_chunks(text: str, max_chars: int = 42):
    """Semantic caption lines: one sentence never spills into the next cue's start; inside a sentence break
    after punctuation, then before a conjunction, never after a dangling word or a bare number
    (no "within 30 | days", no "of the | doctors")."""
    chunks = []
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if sent:
            chunks += _chunk_sentence(sent.split(), max_chars)
    # fold tiny cues (< 14 chars) into a neighbour when the pair still fits
    out = []
    for c in chunks:
        if out and (len(c) < 14 or len(out[-1]) < 14) and len(out[-1]) + 1 + len(c) <= max_chars:
            out[-1] += " " + c
        else:
            out.append(c)
    return out


def ts(t: float, sep=","):  # noqa: E302
    t = max(t, 0)
    h, rem = divmod(int(round(t * 1000)), 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def build_captions(timings):
    cues = []
    for seg in timings:
        chunks = caption_chunks(seg["display"])
        # keep every cue <= ~6 s: split long chunks further by words
        dur_per_char = (seg["end"] - seg["start"]) / max(sum(len(c) for c in chunks), 1)
        fixed = []
        for c in chunks:
            n = max(1, int(len(c) * dur_per_char // 6) + 1)
            fixed += caption_chunks(c, max_chars=max(18, len(c) // n + 6)) if n > 1 else [c]
        chunks = fixed
        total = sum(len(c) for c in chunks) or 1
        t, dur = seg["start"], seg["end"] - seg["start"]
        for c in chunks:
            d = dur * len(c) / total
            cues.append((t, t + d, c))
            t += d
    # fold flash cues (< 0.8 s) into a neighbour from the same moment so nothing blinks past unread
    merged = []
    for a, b, c in cues:
        if merged and (b - a < 0.8 or merged[-1][1] - merged[-1][0] < 0.8) and abs(merged[-1][1] - a) < 0.05 \
                and len(merged[-1][2]) + 1 + len(c) <= 52:
            pa, _, pc = merged.pop(); merged.append((pa, b, pc + " " + c))
        else:
            merged.append((a, b, c))
    def two_lines(c):          # a merged cue longer than 42 chars becomes two balanced lines
        if len(c) <= 42 or "\n" in c:
            return c
        mid = len(c) // 2
        cut = min((i for i, ch in enumerate(c) if ch == " "), key=lambda i: abs(i - mid))
        return c[:cut] + "\n" + c[cut + 1:]
    cues = [(a, b, two_lines(c)) for a, b, c in merged]
    # small lead-in so captions appear just before the word, never overlapping
    out = []
    for i, (a, b, c) in enumerate(cues):
        a2 = max(a - 0.15, out[-1][1] if out else 0)
        out.append((a2, b, c))
    return out


def write_captions(cues, out_dir: Path):
    srt = "\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n" for i, (a, b, c) in enumerate(cues, 1))
    (out_dir / "captions.srt").write_text(srt, encoding="utf-8")
    vtt = "WEBVTT\n\n" + "\n".join(f"{ts(a, '.')} --> {ts(b, '.')}\n{c}\n" for a, b, c in cues)
    (out_dir / "captions.vtt").write_text(vtt, encoding="utf-8")


# ---------------------------------------------------------------- main
def pick_engine(requested, voice):
    if requested:
        return requested
    if have_parler():                       # owner's choice (2026-11): the expressive engine first
        return "parler"
    for eng in ENGINE_ORDER:
        v = voice or DEFAULT_VOICE[eng]
        if eng == "kokoro" and have_kokoro():
            return eng
        if eng == "piper" and have_piper(v if v in MALE_VOICES["piper"] else DEFAULT_VOICE["piper"]):
            return eng
        if eng == "edge" and have_edge():
            return eng
    die("no TTS engine available. Run scripts/setup_studio.sh (installs Kokoro + Piper male voices).")


# ---------------------------------------------------------------- optional dialogue casting
def validate_voice_cast(data):
    """Validate an opt-in Voicebox character cast without changing solo narration."""
    cast = data.get("cast")
    if cast is None:
        if any("speaker" in seg for seg in data["segments"]):
            raise ValueError("segments with speaker require a cast map")
        return None
    if not isinstance(cast, dict) or "narrator" not in cast:
        raise ValueError("cast must include a narrator entry")
    if data.get("voice", {}).get("engine", "voicebox") != "voicebox":
        raise ValueError("multi-speaker cast requires the voicebox engine")
    seen_profiles = set()
    for key, entry in cast.items():
        if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", key):
            raise ValueError(f"invalid speaker key: {key!r}")
        if not isinstance(entry, dict):
            raise ValueError(f"cast.{key} must be an object")
        if entry.get("approved") is not True or entry.get("synthetic_voice") is not True:
            raise ValueError(f"cast.{key} requires approved:true and synthetic_voice:true")
        if entry.get("gender") not in ("male", "female"):
            raise ValueError(f"cast.{key}.gender must be male or female")
        if key == "narrator":
            if entry["gender"] != "male" or entry.get("profile_name") != CHANNEL_NARRATOR_NAME:
                raise ValueError("narrator must use the established male Founder Notes Narrator profile")
        else:
            name = entry.get("profile_name")
            if not isinstance(name, str) or not name.strip() or name == CHANNEL_NARRATOR_NAME:
                raise ValueError(f"cast.{key} requires an independent named Voicebox character profile")
        name = entry["profile_name"]
        if name in seen_profiles:
            raise ValueError(f"Voicebox profile {name!r} assigned to multiple characters")
        seen_profiles.add(name)
    for seg in data["segments"]:
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", str(seg["id"])):
            raise ValueError(f"cast segment id must be a safe filename: {seg['id']!r}")
        key = seg.get("speaker", "narrator")
        if key not in cast:
            raise ValueError(f"segment {seg['id']} refers to undeclared speaker {key!r}")
    return cast


def resolve_voice_cast(cast):
    """Match original character profiles and their valid Voicebox synthesis engines.

    Voicebox types differ: presets have no samples, voice-designed profiles
    have a prompt, while cloned-from-synthetic profiles require samples.
    """
    narrator_id = voicebox_channel_profile()
    try:
        with urllib.request.urlopen(f"{voicebox_url()}/profiles", timeout=30) as response:
            profiles = json.loads(response.read())
    except Exception as exc:
        raise RuntimeError(f"could not list Voicebox profiles: {exc}") from exc
    if not isinstance(profiles, list):
        raise ValueError("Voicebox /profiles returned an invalid response")
    resolved = {"narrator": {"id": narrator_id, "engine": CHANNEL_NARRATOR_ENGINE,
                              "voice_type": "cloned"}}
    for key, entry in cast.items():
        if key == "narrator":
            continue
        matching = [p for p in profiles if isinstance(p, dict)
                    and p.get("name") == entry["profile_name"]
                    and isinstance(p.get("id"), str) and p["id"]]
        if len(matching) != 1:
            raise ValueError(f"{key}: expected one unique Voicebox profile named "
                             f"{entry['profile_name']!r}; create it first")
        p = matching[0]
        voice_type = p.get("voice_type") or "cloned"
        declared_type = entry.get("voice_type")
        if declared_type and declared_type != voice_type:
            raise ValueError(f"{key}: expected {declared_type} Voicebox profile, got {voice_type}")
        if voice_type == "preset":
            if not p.get("preset_voice_id") or p.get("preset_engine") not in ("kokoro", "qwen_custom_voice"):
                raise ValueError(f"{key}: invalid Voicebox preset metadata")
            engine = p["preset_engine"]
            # Kokoro's built-in voice IDs encode sex in the second character.
            preset = p["preset_voice_id"]
            if engine == "kokoro" and len(preset) >= 3 and preset[1] in "mf":
                expected = "male" if preset[1] == "m" else "female"
                if entry["gender"] != expected:
                    raise ValueError(f"{key}: declared gender does not match Kokoro preset voice")
        elif voice_type == "designed":
            if not p.get("design_prompt") or p.get("default_engine") not in (None, "qwen_voice_design"):
                raise ValueError(f"{key}: invalid Voicebox designed-voice profile")
            engine = "qwen_voice_design"
        elif voice_type == "cloned":
            if p.get("sample_count", 0) <= 0:
                raise ValueError(f"{key}: cloned profile has no approved audio sample")
            engine = p.get("default_engine") or "chatterbox"
            if engine not in ("chatterbox", "chatterbox_turbo", "qwen", "luxtts", "tada", "omnivoice"):
                raise ValueError(f"{key}: unsupported cloning engine: {engine}")
        else:
            raise ValueError(f"{key}: unsupported Voicebox profile type: {voice_type}")
        resolved[key] = {"id": p["id"], "engine": engine, "voice_type": voice_type}
    if len({item["id"] for item in resolved.values()}) != len(resolved):
        raise ValueError("Multiple cast members resolve to the same Voicebox profile")
    return resolved


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--engine", choices=["parler", "kokoro", "piper", "edge", "voicebox", "files"])
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--files-dir", help="for --engine files: folder of <segment-id>.wav recordings")
    ap.add_argument("--retake", type=int, default=2,
                    help="parler: with --asr, re-generate segments whose words dropped (new seed) up to N times")
    ap.add_argument("--no-perform", action="store_true",
                    help="read flat (one take per segment) instead of the human-explainer performance layer")
    ap.add_argument("--allow-non-male", action="store_true",
                    help="only when the channel owner explicitly asked for a non-male narrator")
    ap.add_argument("--list-voices", action="store_true")
    ap.add_argument("--asr", nargs="?", const="base.en", metavar="MODEL",
                    help="round-trip every segment through faster-whisper (default model base.en) and flag dropped words")
    a = ap.parse_args(argv)

    if a.list_voices:
        for eng, vs in MALE_VOICES.items():
            print(f"{eng:7s} (default {DEFAULT_VOICE[eng]}): {', '.join(vs)}")
        print("voicebox: pass the profile id of a male preset profile (see references/voiceover.md)")
        print(f"engines available here: kokoro={have_kokoro()} piper={have_piper(DEFAULT_VOICE['piper'])} edge={have_edge()}")
        return 0
    if not a.script or not a.out:
        ap.error("SCRIPT and --out are required")
    if not shutil.which("ffmpeg"):
        die("ffmpeg not found")

    data = load_script(Path(a.script))
    try:
        cast = validate_voice_cast(data)
    except (ValueError, TypeError) as exc:
        die(f"voice cast: {exc}")
    vcfg = data.get("voice", {})
    engine = a.engine or vcfg.get("engine")
    voice = a.voice or vcfg.get("name")
    if cast:
        if a.engine and a.engine != "voicebox":
            die("multi-speaker cast supports Voicebox only")
        if a.voice:
            die("do not override a multi-speaker cast with --voice")
        engine, voice = "voicebox", CHANNEL_NARRATOR
    engine = pick_engine(engine, voice)
    if engine == "parler":
        voice = voice or PARLER_DESC
        if not parler_is_male(voice) and not a.allow_non_male:
            die("parler: the voice description must describe a MALE speaker (channel rule)")
        if not have_parler():
            die(f"parler: no Parler venv at {parler_python()} (set PARLER_PYTHON; pip install parler-tts there)")
    elif engine in DEFAULT_VOICE:
        voice = voice or DEFAULT_VOICE[engine]
        parts_ = [v.split(":")[0] for v in voice.split("+")] if engine == "kokoro" else [voice]
        if any(p_ not in MALE_VOICES[engine] for p_ in parts_) and not a.allow_non_male:
            die(f"voice '{voice}' is not on the male allowlist for {engine}. "
                f"Male options: {', '.join(MALE_VOICES[engine])}")
    elif engine == "voicebox":
        voice = voice or CHANNEL_NARRATOR
    vb_engine = None
    voice_key = voice
    cast_profiles = None
    if cast:
        try:
            cast_profiles = resolve_voice_cast(cast)
        except Exception as e:
            die(f"voicebox cast: {e}; start voicebox and provision synthetic character profiles first")
        voice = cast_profiles["narrator"]["id"]
        vb_engine = CHANNEL_NARRATOR_ENGINE
    elif engine == "voicebox" and voice == CHANNEL_NARRATOR:
        try:
            voice = voicebox_channel_profile()
        except Exception as e:
            die(f"voicebox: server not reachable at {voicebox_url()} ({e}); start it with scripts/voicebox_server.sh")
        vb_engine = CHANNEL_NARRATOR_ENGINE
    speed = a.speed or vcfg.get("speed", 1.0)
    pv = vcfg.get("perform", False)      # earshot: sentence-split takes read MORE synthetic; opt-in only
    perform = engine == "kokoro" and not a.no_perform and pv not in (False, "flat", "off")
    perform_mode = "full" if pv == "full" else "pace"
    lead, tail = float(data.get("lead", 0.3)), float(data.get("tail", 0.8))

    out = Path(a.out).resolve()
    seg_dir = out / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    timings, parts = [], []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        lead_wav = td / "lead.wav"
        silence(lead, lead_wav)
        parts.append(lead_wav)
        clock = wav_seconds(lead_wav)
        takes = {}
        if engine == "voicebox":
            takes = {s_["id"]: int((seg_dir / f"{s_['id']}.take").read_text()) if (seg_dir / f"{s_['id']}.take").exists() else 0
                     for s_ in data["segments"]}
        vb_made = []
        if engine == "parler":
            takes = {s_["id"]: int((seg_dir / f"{s_['id']}.take").read_text()) if (seg_dir / f"{s_['id']}.take").exists() else 0
                     for s_ in data["segments"]}
            jobs = []
            for s_ in data["segments"]:
                t_ = " ".join(str(s_["text"]).split())
                k_ = hashlib.sha256(f"parler|{voice}|{speed}|{t_}|{PARLER_MODEL}|{PARLER_VOICE_V}|take{takes[s_['id']]}".encode()).hexdigest()[:16]
                st_ = seg_dir / f"{s_['id']}.key"
                if not ((seg_dir / f"{s_['id']}.wav").exists() and st_.exists() and st_.read_text() == k_):
                    jobs.append({"id": s_["id"], "text": t_, "out": str(td / f"{s_['id']}.raw.wav"), "seed": 42 + 7 * takes[s_["id"]]})
            # remember what THIS run generated: auto re-takes may only touch these, never approved earlier takes
            gen_file = out / "_generated_this_run.json"
            prev = json.loads(gen_file.read_text()) if (gen_file.exists() and os.environ.get("NARRATE_RETAKE_CHAIN")) else []
            gen_file.write_text(json.dumps(sorted(set(prev) | {j["id"] for j in jobs})))
            if jobs:
                print(f"  [parler] generating {len(jobs)} segment(s) (about 5x real time on CPU)…", file=sys.stderr)
                jf = td / "parler_jobs.json"
                jf.write_text(json.dumps({"model": PARLER_MODEL, "description": voice, "jobs": jobs}))
                env_ = dict(os.environ)
                env_.setdefault("PARLER_ANCHOR", str(Path(__file__).resolve().parent.parent / "assets" / "voice" / "founder-notes-narrator.wav"))   # the channel voice, kept in the repo
                subprocess.run([parler_python(), str(Path(__file__).with_name("parler_worker.py")), str(jf)], check=True, env=env_)
        for i, s in enumerate(data["segments"]):
            text = " ".join(str(s["text"]).split())
            speaker = s.get("speaker", "narrator") if cast else None
            segment_profile = cast_profiles[speaker] if cast_profiles else None
            segment_voice = segment_profile["id"] if segment_profile else voice
            segment_engine = segment_profile["engine"] if segment_profile else vb_engine
            segment_voice_key = f"{speaker}:{cast[speaker]['profile_name']}:{segment_voice}:{segment_engine}" if cast else voice_key
            extra = ""
            if engine == "files":                      # a replaced recording must invalidate the cached take
                src = Path(a.files_dir or "recordings") / f"{s['id']}.wav"
                extra = hashlib.sha256(src.read_bytes()).hexdigest() if src.exists() else "missing"
            elif engine == "voicebox":
                extra = "|".join(os.environ.get(k, "") for k in ("VOICEBOX_ENGINE", "VOICEBOX_INSTRUCT")) + f"|{segment_engine}|take{takes.get(s['id'], 0)}"
            if perform:
                extra += "|" + PERFORM_VERSION + perform_mode
            if engine == "parler":
                extra = f"{PARLER_MODEL}|{PARLER_VOICE_V}|take{takes.get(s['id'], 0)}"
            key = hashlib.sha256(f"{engine}|{segment_voice_key if engine == 'voicebox' else voice}|{speed}|{text}|{extra}".encode()).hexdigest()[:16]
            wav = seg_dir / f"{s['id']}.wav"
            stamp = seg_dir / f"{s['id']}.key"
            if not (wav.exists() and stamp.exists() and stamp.read_text() == key):
                print(f"  [{engine}:{speaker or 'solo'}:{segment_voice}] {s['id']}: {text[:60]}{'…' if len(text) > 60 else ''}", file=sys.stderr)
                if engine == "parler":
                    raw = td / f"{s['id']}.raw.wav"
                    to_master_format(raw, wav, speed=speed)
                elif engine == "kokoro" and perform:
                    synth_kokoro_performed(text, voice, speed, wav, mode=perform_mode)
                elif engine == "kokoro":
                    synth_kokoro(text, voice, speed, wav)
                elif engine == "piper":
                    synth_piper(text, voice, speed, wav)
                elif engine == "edge":
                    synth_edge(text, voice, speed, wav)
                elif engine == "voicebox":
                    synth_voicebox(text, segment_voice, speed, wav, seed=42 + 7 * takes.get(s["id"], 0), engine=segment_engine)
                    vb_made.append(s["id"])
                else:
                    synth_files(s["id"], Path(a.files_dir or "recordings"), wav, speed)
                stamp.write_text(key)
            d = wav_seconds(wav)
            timing = {"id": s["id"], "start": round(clock, 3), "end": round(clock + d, 3),
                      "text": text, "display": " ".join(str(s.get("display", text)).split()),
                      "words": len(text.split())}
            if cast:
                timing["speaker"] = speaker
                timing["scene_id"] = s.get("scene_id")
                timing["role"] = "narrator" if speaker == "narrator" else "character"
                timing["voice_profile"] = cast[speaker]["profile_name"]
                timing["voice_engine"] = segment_engine
                timing["voice_type"] = segment_profile["voice_type"]
            timings.append(timing)
            parts.append(wav)
            clock += d
            gap = float(s.get("pause_after", 0.35 if i < len(data["segments"]) - 1 else tail))
            gw = td / f"gap{i}.wav"
            silence(gap, gw)
            parts.append(gw)
            clock += wav_seconds(gw)
        listing = td / "list.txt"
        listing.write_text("".join(f"file '{Path(p).resolve().as_posix()}'\n" for p in parts))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
             "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "1", str(out / "narration.wav")])

    chain = vcfg.get("chain", "studio")
    if chain and chain != "none":
        apply_voice_chain(out / "narration.wav", chain)
    total = wav_seconds(out / "narration.wav")
    if total + 0.1 < clock:
        die(f"narration.wav is {total:.2f}s but the segments add up to {clock:.2f}s; concat failed")
    words = sum(t["words"] for t in timings)
    speech = sum(t["end"] - t["start"] for t in timings)
    meta = {"engine": engine, "voice": voice, "speed": speed, "performance": PERFORM_VERSION + perform_mode if perform else "flat",
            "chain": chain, "male_voice_policy": not a.allow_non_male,
            "duration": round(total, 3), "words": words,
            "wpm_speech": round(words / (speech / 60), 1) if speech else None,
            "word_timing": "estimated-from-characters", "segments": timings}
    if cast:
        meta["cast"] = {k: {"gender": v["gender"], "profile_name": v["profile_name"],
                            "synthetic_voice": True, "approved": True}
                        for k, v in cast.items()}
        meta["voice_policy"] = "male principal narrator plus owner-approved synthetic male/female characters"
    (out / "timings.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    write_captions(build_captions(timings), out)
    print(json.dumps({k: meta[k] for k in ("engine", "voice", "duration", "words", "wpm_speech")}))
    if a.asr:
        rc = asr_check(out, timings, a.asr)
        if engine == "voicebox":            # remember what THIS run generated (auto re-takes only touch these)
            gen_file = out / "_generated_this_run.json"
            prev = json.loads(gen_file.read_text()) if (gen_file.exists() and os.environ.get("NARRATE_RETAKE_CHAIN")) else []
            gen_file.write_text(json.dumps(sorted(set(prev) | set(vb_made))))
        if engine in ("parler", "voicebox") and a.retake > 0:
            rep = json.loads((out / "asr.json").read_text())
            rep = rep if isinstance(rep, list) else rep.get("segments", rep.get("report", []))
            NUMW = re.compile(r"^(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|percent)$")
            fresh = set(json.loads((out / "_generated_this_run.json").read_text())) if (out / "_generated_this_run.json").exists() else set()
            bad = [r["id"] for r in rep if r["id"] in fresh and (r.get("critical_missing") or
                   len([m for m in (r.get("missing") or []) if not NUMW.match(str(m).lower())]) >= 2)]
            if bad:
                for sid in bad:
                    f = seg_dir / f"{sid}.take"; f.write_text(str((int(f.read_text()) if f.exists() else 0) + 1))
                print(f"narrate: re-taking {len(bad)} {engine} segment(s) with a new seed: {', '.join(bad)}", file=sys.stderr)
                argv = [x for x in sys.argv[1:]]
                if "--retake" in argv:
                    j = argv.index("--retake"); argv[j + 1] = str(a.retake - 1)
                else:
                    argv += ["--retake", str(a.retake - 1)]
                return subprocess.run([sys.executable, __file__, *argv], env=dict(os.environ, NARRATE_RETAKE_CHAIN="1")).returncode
        return rc
    return 0


NUM_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
             "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
             "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
             "billion", "percent", "half", "quarter"}


def critical_edits(want, heard, critical):
    """Ordered alignment of script vs recognised tokens. Returns every insertion, deletion or substitution
    that touches a meaning-critical token (negation or number) — catches moved negations and added numbers."""
    import difflib
    crit = lambda w: w in critical or w.isdigit() or w in NUM_WORDS
    edits = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=want, b=heard, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        a, b = want[i1:i2], heard[j1:j2]
        if any(crit(w) for w in a + b):
            edits.append({"op": op, "script": " ".join(a), "heard": " ".join(b), "at": i1})
    # anchor check: a critical token must sit at the same place in the non-critical skeleton
    # ("alpha is NOT valid / beta is valid" vs "alpha is valid / beta is NOT valid" keeps every word but moves 'not')
    def anchored(tokens):
        skel, marks = [], []
        for w in tokens:
            if crit(w):
                marks.append((w, len(skel)))
            else:
                skel.append(w)
        return skel, marks
    sw, mw = anchored(want); sh, mh = anchored(heard)
    m = difflib.SequenceMatcher(a=sw, b=sh, autojunk=False)
    remap = {}
    for blk in m.get_matching_blocks():
        for k in range(blk.size + 1):
            remap.setdefault(blk.a + k, blk.b + k)
    expect = sorted((w, remap.get(k, -1)) for w, k in mw)
    if expect != sorted(mh) and not edits:
        edits.append({"op": "moved", "script": " ".join(w for w, _ in mw), "heard": " ".join(w for w, _ in mh), "at": -1})
    return edits


def missing_words(want, heard):
    """Script words not heard, counted with multiplicity (two 'not's scripted, one heard → one missing)."""
    from collections import Counter
    left = Counter(want) - Counter(heard)
    out = []
    for w in want:
        if left[w] > 0:
            out.append(w); left[w] -= 1
    return out


def asr_check(out: Path, timings, model_name: str) -> int:
    """Transcribe each take and report segments whose displayed words are mostly missing.
    Small models mishear short names: confirm flagged lines by listening before re-taking."""
    try:
        from faster_whisper import WhisperModel
    except Exception:
        print("narrate: --asr needs faster-whisper (pip install faster-whisper 'av<19'); check NOT run", file=sys.stderr)
        return 0
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", re.sub(r"[’']", "", s.lower())).split()
    critical = {"not", "no", "never", "nor", "none", "nothing", "nobody", "nowhere", "neither", "cannot",
                "dont", "doesnt", "didnt", "isnt", "arent", "wasnt", "werent", "cant", "couldnt", "wont",
                "wouldnt", "shouldnt", "hasnt", "havent", "hadnt", "aint", "without"}
    report, flagged = [], 0
    for seg in timings:
        res, _ = model.transcribe(str(out / "segments" / f"{seg['id']}.wav"), language="en", beam_size=5)
        heard = " ".join(x.text for x in res).strip()
        want = norm(seg["display"]); got_list = norm(heard)
        # multiset comparison: two "not"s in the script and one heard is a missing "not"
        missing = missing_words(want, got_list)
        # meaning-critical words: a dropped or added negation / number reverses or changes the claim
        neg_want = sum(w in critical for w in want); neg_got = sum(w in critical for w in got_list)
        crit_missing = [w for w in missing if w in critical or w.isdigit()]
        crit_edits = critical_edits(want, got_list, critical)
        bad = (len(missing) > max(1, int(len(want) * 0.08)) or bool(crit_missing) or neg_want != neg_got
               or bool(crit_edits))
        flagged += bad
        report.append({"id": seg["id"], "ok": not bad, "missing": missing, "critical_missing": crit_missing,
                       "critical_edits": crit_edits,
                       "negations_script": neg_want, "negations_heard": neg_got, "heard": heard})
        if bad:
            print(f"  ASR CHECK {seg['id']}: missing {missing[:8]} | heard: {heard[:140]}", file=sys.stderr)
    (out / "asr.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"narrate: ASR round-trip {len(timings) - flagged}/{len(timings)} clean (report: {out / 'asr.json'})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
