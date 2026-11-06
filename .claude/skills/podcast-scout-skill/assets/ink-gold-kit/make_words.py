"""Word cue map for word-timed punches, stamps, sfx and karaoke: film/words.js ->
window.WORDS = {seg_id: [[word, t0, t1], ...]} (absolute seconds).

The WORDS are always the script's own spoken words (script.json "text", normalised: "fifty-six" -> "fiftysix",
"preregistration", "i", "q"), so K.word cues written against the script always match. Only the TIMES come from
faster-whisper word timestamps: script and transcript are aligned (difflib); matched words copy whisper times, and a
mismatched run ("520" vs "five hundred and twenty", "pre registration" vs "preregistration") spreads the transcript
run's time span across the script words by length. Without whisper (--estimate) words are spread across the segment.
"""
import difflib, json, pathlib, re, sys
here = pathlib.Path(__file__).parent; nar = here.parent / "narration"
t = json.load(open(nar / "timings.json"))
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
def toks(text): return [n for n in (norm(w) for w in re.split(r"[\s–—]+", text)) if n]
try:
    from faster_whisper import WhisperModel
    m = None if "--estimate" in sys.argv else WhisperModel("base.en", device="cpu", compute_type="int8")
except Exception:
    m = None

def spread(words, a, b):
    L = sum(len(w) + 1 for w in words) or 1; c = 0; out = []
    for w in words:
        t0 = a + (b - a) * c / L; c += len(w) + 1; out.append([w, round(t0, 3), round(a + (b - a) * c / L, 3)])
    return out

out, exact = {}, 0
for s in t["segments"]:
    a, b = s["start"], s["end"]
    sw = toks(s["text"])
    if m is None:
        out[s["id"]] = spread(sw, a, b); continue
    segs, _ = m.transcribe(str(nar / "segments" / f"{s['id']}.wav"), word_timestamps=True, language="en")
    hw = [[n, a + w.start, a + w.end] for sg in segs for w in sg.words for n in [norm(w.word)] if n]
    sm = difflib.SequenceMatcher(a=[h[0] for h in hw], b=sw, autojunk=False)
    res = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            res += [[sw[j1 + k], round(hw[i1 + k][1], 3), round(hw[i1 + k][2], 3)] for k in range(j2 - j1)]; exact += j2 - j1
        elif op in ("replace", "insert") and j2 > j1:
            if i2 > i1: lo, hi = hw[i1][1], hw[i2 - 1][2]
            else:
                lo = res[-1][2] if res else a
                hi = hw[i1][1] if i1 < len(hw) else b
                if hi - lo < 0.05 * (j2 - j1): hi = lo + 0.18 * (j2 - j1)
            res += spread(sw[j1:j2], lo, hi)
    out[s["id"]] = res
(here / "words.js").write_text("window.WORDS=" + json.dumps(out) + ";\n")
n = sum(len(v) for v in out.values())
print(f"words.js: {n} script words, " + (f"{exact} with exact whisper times" if m else "(estimate)"))
