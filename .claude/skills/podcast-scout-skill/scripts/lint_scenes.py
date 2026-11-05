#!/usr/bin/env python3
"""Static checks for Ink & Gold scene files, run before rendering (idea from pixelfx's check.mjs; our own code).

    python3 lint_scenes.py film/sc*.html [--timing film/timing.js]

FAIL: anything that breaks the render contract or a channel rule:
  - non-deterministic time or randomness: Math.random, Date, performance.now, requestAnimationFrame, setTimeout/setInterval
  - a scene id passed to K.scene that is missing from timing.js
  - a named source podcast, host or guest in on-screen text (channel rule)
WARN: things worth a look:
  - numbers or percentages on screen but no K.source(...) line
  - text placed in the caption zone (y > 900), where burned subtitles go
  - no K.backdrop(...) call (backgrounds must rotate)
  - K.Hunter built with hand-made colours instead of the film's cast (K.LOOPER / default cast)
"""
import argparse, json, re, sys
from pathlib import Path

NONDET = [r"Math\.random\s*\(", r"\bDate\b(?:\.now|\s*\()", r"performance\.now", r"requestAnimationFrame", r"set(?:Timeout|Interval)\s*\("]
BANNED_NAMES = [r"\bAltman\b", r"Shamani", r"Figuring Out", r"\bFO\d{3}\b", r"\bpodcast\b"]


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"(^|[^:])//[^\n]*", r"\1", src)


def scene_ids(timing):
    if not timing or not Path(timing).exists():
        return None
    m = re.search(r"window\.TIMING=(\{.*?\});", Path(timing).read_text())
    return set(json.loads(m.group(1))["scenes"]) if m else None


def lint(path, ids, extra_names):
    raw = Path(path).read_text(); src = strip_comments(raw)
    fails, warns = [], []
    for pat in NONDET:
        for m in re.finditer(pat, src):
            line = src[: m.start()].count("\n") + 1
            fails.append(f"non-deterministic `{m.group(0).strip()}` (line ~{line}): every frame must be a pure function of t; use K.rand(seed)")
    m = re.search(r'K\.scene\(\s*"([^"]+)"', src)
    if m and ids is not None and m.group(1) not in ids:
        fails.append(f'scene id "{m.group(1)}" is not in timing.js')
    strings = re.findall(r'"((?:[^"\\]|\\.)*)"|`((?:[^`\\]|\\.)*)`', src)
    # internal segment / scene ids ("s03-intro", "sc05-review") never reach the screen
    text = " ".join(x for x in (a or b for a, b in strings) if not re.fullmatch(r"s(?:c)?\d{2}-[\w-]+", x))
    for pat in BANNED_NAMES + extra_names:
        if re.search(pat, text, flags=re.I):
            fails.append(f"on-screen text matches /{pat}/: never name the source podcast, host or guest (channel rule)")
    if re.search(r"\d+(?:\.\d+)?\s*%", text) and "K.source(" not in src:
        warns.append("numbers/percentages on screen but no K.source(...) line")
    for m in re.finditer(r"K\.(?:text|label|title)\([^,]+,[^,]+,\s*[-\d.]+\s*,\s*(\d{3,4})\b", src):
        if int(m.group(1)) > 900:
            warns.append(f"text at y={m.group(1)} sits in the caption zone (> 900)")
    if "K.backdrop(" not in src:
        warns.append("no K.backdrop(...): backgrounds must rotate between adjacent scenes")
    if re.search(r"new K\.Hunter\([^)]*colors:\s*\{", src):
        warns.append("K.Hunter with hand-made colours: use the film's cast (K.DEFAULT_CAST / K.LOOPER …), see CAST.md")
    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenes", nargs="+"); ap.add_argument("--timing"); ap.add_argument("--ban", action="append", default=[],
                    help="extra regex for names that must never appear on screen")
    a = ap.parse_args()
    ids = scene_ids(a.timing); nf = nw = 0
    for p in a.scenes:
        f, w = lint(p, ids, a.ban)
        for x in f: print(f"FAIL  {Path(p).name}: {x}")
        for x in w: print(f"WARN  {Path(p).name}: {x}")
        nf += len(f); nw += len(w)
    print(f"\n{'PASS' if not nf else 'FAIL'}: {nf} fail, {nw} warn ({len(a.scenes)} scenes)")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
