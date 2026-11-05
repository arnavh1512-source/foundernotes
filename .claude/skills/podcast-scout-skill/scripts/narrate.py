#!/usr/bin/env python3
"""Synthesize narration with a MALE voice and write timings + captions.

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

Default voice policy: male narrator. The script refuses voices that are not on the male
allowlist unless --allow-non-male is passed (the channel owner must ask for that explicitly).
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
DEFAULT_VOICE = {"kokoro": "am_fenrir+am_puck", "piper": "en_US-ryan-high", "edge": "en-US-AndrewNeural"}
ENGINE_ORDER = ["kokoro", "piper", "edge"]


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


PERFORM_VERSION = "p2"


def synth_kokoro_performed(text, voice, speed, out: Path):
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
            af = [f"volume={db:.2f}dB"]
            if abs(st) > 0.05 and has_rubberband():
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
        sf.write(str(tmp), np.concatenate(chunks) if chunks else np.zeros(1, "float32"), sr)
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


def synth_voicebox(text, voice, speed, out: Path):
    """voicebox (github.com/jamiepine/voicebox) running locally; voice = profile id of a
    MALE preset profile (e.g. kokoro am_michael or Qwen CustomVoice Ryan/Aiden)."""
    base = os.environ.get("VOICEBOX_URL", "http://127.0.0.1:17493")
    body = {"profile_id": voice, "text": text, "language": "en"}
    if os.environ.get("VOICEBOX_ENGINE"):
        body["engine"] = os.environ["VOICEBOX_ENGINE"]
    if os.environ.get("VOICEBOX_INSTRUCT"):
        body["instruct"] = os.environ["VOICEBOX_INSTRUCT"]
    req = urllib.request.Request(f"{base}/generate/stream", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    tmp = out.with_suffix(".raw.wav")
    with urllib.request.urlopen(req, timeout=600) as r:
        tmp.write_bytes(r.read())
    to_master_format(tmp, out, speed=speed)
    tmp.unlink(missing_ok=True)


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
    for eng in ENGINE_ORDER:
        v = voice or DEFAULT_VOICE[eng]
        if eng == "kokoro" and have_kokoro():
            return eng
        if eng == "piper" and have_piper(v if v in MALE_VOICES["piper"] else DEFAULT_VOICE["piper"]):
            return eng
        if eng == "edge" and have_edge():
            return eng
    die("no TTS engine available. Run scripts/setup_studio.sh (installs Kokoro + Piper male voices).")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--engine", choices=["kokoro", "piper", "edge", "voicebox", "files"])
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--files-dir", help="for --engine files: folder of <segment-id>.wav recordings")
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
    vcfg = data.get("voice", {})
    engine = a.engine or vcfg.get("engine")
    voice = a.voice or vcfg.get("name")
    engine = pick_engine(engine, voice)
    if engine in DEFAULT_VOICE:
        voice = voice or DEFAULT_VOICE[engine]
        parts_ = [v.split(":")[0] for v in voice.split("+")] if engine == "kokoro" else [voice]
        if any(p_ not in MALE_VOICES[engine] for p_ in parts_) and not a.allow_non_male:
            die(f"voice '{voice}' is not on the male allowlist for {engine}. "
                f"Male options: {', '.join(MALE_VOICES[engine])}")
    elif engine == "voicebox" and not voice:
        die("voicebox needs --voice <profile id of a male preset profile>")
    speed = a.speed or vcfg.get("speed", 1.0)
    perform = engine == "kokoro" and not a.no_perform and vcfg.get("perform", True)
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
        for i, s in enumerate(data["segments"]):
            text = " ".join(str(s["text"]).split())
            extra = ""
            if engine == "files":                      # a replaced recording must invalidate the cached take
                src = Path(a.files_dir or "recordings") / f"{s['id']}.wav"
                extra = hashlib.sha256(src.read_bytes()).hexdigest() if src.exists() else "missing"
            elif engine == "voicebox":
                extra = "|".join(os.environ.get(k, "") for k in ("VOICEBOX_URL", "VOICEBOX_ENGINE", "VOICEBOX_INSTRUCT"))
            if perform:
                extra += "|" + PERFORM_VERSION
            key = hashlib.sha256(f"{engine}|{voice}|{speed}|{text}|{extra}".encode()).hexdigest()[:16]
            wav = seg_dir / f"{s['id']}.wav"
            stamp = seg_dir / f"{s['id']}.key"
            if not (wav.exists() and stamp.exists() and stamp.read_text() == key):
                print(f"  [{engine}:{voice}] {s['id']}: {text[:60]}{'…' if len(text) > 60 else ''}", file=sys.stderr)
                if engine == "kokoro" and perform:
                    synth_kokoro_performed(text, voice, speed, wav)
                elif engine == "kokoro":
                    synth_kokoro(text, voice, speed, wav)
                elif engine == "piper":
                    synth_piper(text, voice, speed, wav)
                elif engine == "edge":
                    synth_edge(text, voice, speed, wav)
                elif engine == "voicebox":
                    synth_voicebox(text, voice, speed, wav)
                else:
                    synth_files(s["id"], Path(a.files_dir or "recordings"), wav, speed)
                stamp.write_text(key)
            d = wav_seconds(wav)
            timings.append({"id": s["id"], "start": round(clock, 3), "end": round(clock + d, 3),
                            "text": text, "display": " ".join(str(s.get("display", text)).split()),
                            "words": len(text.split())})
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

    total = wav_seconds(out / "narration.wav")
    if total + 0.1 < clock:
        die(f"narration.wav is {total:.2f}s but the segments add up to {clock:.2f}s; concat failed")
    words = sum(t["words"] for t in timings)
    speech = sum(t["end"] - t["start"] for t in timings)
    meta = {"engine": engine, "voice": voice, "speed": speed, "performance": PERFORM_VERSION if perform else "flat", "male_voice_policy": not a.allow_non_male,
            "duration": round(total, 3), "words": words,
            "wpm_speech": round(words / (speech / 60), 1) if speech else None,
            "word_timing": "estimated-from-characters", "segments": timings}
    (out / "timings.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    write_captions(build_captions(timings), out)
    print(json.dumps({k: meta[k] for k in ("engine", "voice", "duration", "words", "wpm_speech")}))
    if a.asr:
        return asr_check(out, timings, a.asr)
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
