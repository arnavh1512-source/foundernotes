"""Word cue map for word-timed punches/stamps: film/words.js -> window.WORDS = {seg_id: [[word, t0, t1], ...]} (absolute s).
Exact mode (default when faster-whisper is importable): transcribes each segment wav with word timestamps.
Fallback: spreads the script words across the segment by character length (good to ~0.3 s)."""
import json, pathlib, re, sys
here = pathlib.Path(__file__).parent; nar = here.parent / "narration"
t = json.load(open(nar / "timings.json"))
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
out = {}
try:
    from faster_whisper import WhisperModel
    m = WhisperModel("base.en", device="cpu", compute_type="int8")
except Exception:
    m = None
for s in t["segments"]:
    a, b = s["start"], s["end"]
    ws = []
    if m is not None and "--estimate" not in sys.argv:
        segs, _ = m.transcribe(str(nar / "segments" / f"{s['id']}.wav"), word_timestamps=True, language="en")
        lead = 0.0
        for sg in segs:
            for w in sg.words:
                ws.append([norm(w.word), round(a + w.start, 3), round(a + w.end, 3)])
        # segment wavs are trimmed audio placed at `start`; whisper times are relative to the wav
    if not ws:
        words = s["text"].split(); L = sum(len(w) + 1 for w in words); c = 0
        for w in words:
            t0 = a + (b - a) * c / L; c += len(w) + 1
            ws.append([norm(w), round(t0, 3), round(a + (b - a) * c / L, 3)])
    out[s["id"]] = ws
(here / "words.js").write_text("window.WORDS=" + json.dumps(out) + ";\n")
print("words.js:", sum(len(v) for v in out.values()), "words", "(whisper)" if m and "--estimate" not in sys.argv else "(estimate)")
