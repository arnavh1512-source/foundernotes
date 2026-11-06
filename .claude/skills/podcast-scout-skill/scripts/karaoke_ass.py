#!/usr/bin/env python3
"""Karaoke captions: SRT cues + word timings -> ASS, where each word lights up as it is spoken.

    python3 karaoke_ass.py narration/captions.srt film/words.js -o narration/captions.ass
    python3 assemble.py ... --captions narration/captions.ass --sub-karaoke

Idea from Hypit's word-anchored caption families (hypit-ai/hypit; our own code): the cue still shows a whole
readable phrase, and the CURRENT spoken word changes colour (cream before, gold once said), so the eye follows the voice.
Each line springs in (86% -> 104% -> 100%, 0.22 s), after MoneyPrinterTurbo's caption spring.
Word times: film/words.js (window.WORDS = {seg: [[word, t0, t1], ...]}, absolute seconds; whisper or estimate).
When a cue's display tokens don't match the spoken words one-to-one ("2017" vs "twenty seventeen"), the cue falls
back to spreading its time across tokens by length, so highlighting never desyncs by more than a word.
"""
import argparse, json, re


def ts(s):
    h, m, r = s.split(":"); sec, ms = r.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def ass_t(x):
    cs = int(round(x * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("srt"); ap.add_argument("words"); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--no-pop", action="store_true", help="no spring pop-in when a caption line appears")
    a = ap.parse_args()
    raw = open(a.words).read()
    W = json.loads(re.search(r"=\s*(\{.*\})\s*;?\s*$", raw, re.S).group(1)) if raw.lstrip().startswith("window") else json.loads(raw)
    words = sorted((w for v in W.values() for w in v), key=lambda w: w[1])
    cues = []
    for blk in re.split(r"\n\s*\n", open(a.srt, encoding="utf-8").read().strip()):
        ln = blk.strip().splitlines()
        if len(ln) < 3: continue
        t0, t1 = [ts(x.strip()) for x in ln[1].split("-->")]
        cues.append((t0, t1, " ".join(ln[2:])))
    norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
    out = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 384", "PlayResY: 288", "WrapStyle: 0", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
           "MarginR, MarginV, Encoding",
           "Style: Default,DejaVu Sans,13,&H0047B8E8,&H00D2E8F3,&H5022180E,&H5022180E,1,0,0,0,100,100,0,0,3,6,0,2,40,40,22,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    exact = 0
    for t0, t1, text in cues:
        toks = text.split()
        spoken = [w for w in words if t0 - 0.15 <= (w[1] + w[2]) / 2 <= t1 + 0.15]
        times = None
        if len(spoken) == len(toks) and all(norm(x) == s[0] or not norm(x).isalpha() for x, s in zip(toks, spoken)):
            times = [(s[1], s[2]) for s in spoken]; exact += 1
        if times is None:                                   # spread across the voiced part of the cue by length
            v0 = spoken[0][1] if spoken else t0; v1 = spoken[-1][2] if spoken else t1
            L = sum(len(x) + 1 for x in toks) or 1; c = 0; times = []
            for x in toks:
                a0 = v0 + (v1 - v0) * c / L; c += len(x) + 1; times.append((a0, v0 + (v1 - v0) * c / L))
        parts, cur = [], t0
        for x, (w0, w1) in zip(toks, times):
            lead = max(0.0, w0 - cur)                        # silence before the word: nothing lights
            if lead > 0.01: parts.append(f"{{\\k{int(round(lead * 100))}}}")
            dur = max(0.05, w1 - max(w0, cur))
            parts.append(f"{{\\k{int(round(dur * 100))}}}{x} "); cur = max(w0, cur) + dur
        # spring pop-in (MoneyPrinterTurbo's caption spring, MIT; as ASS transforms): 86% -> 104% -> 100% in 0.22 s
        pop = "" if a.no_pop else "{\\fscx86\\fscy86\\t(0,120,\\fscx104\\fscy104)\\t(120,220,\\fscx100\\fscy100)}"
        out.append(f"Dialogue: 0,{ass_t(t0)},{ass_t(t1)},Default,,0,0,0,,{pop}{''.join(parts).rstrip()}")
    open(a.out, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"karaoke: {len(cues)} cues, {exact} word-exact, {len(cues) - exact} spread -> {a.out}")


if __name__ == "__main__":
    main()
