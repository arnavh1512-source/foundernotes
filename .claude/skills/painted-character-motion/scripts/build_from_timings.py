#!/usr/bin/env python3
"""Create a standalone 16:9 HTML scene from measured FounderNotes narration timings.

No voice generation. No imports from unlicensed projects. Uses this original SVG
engine and the existing motion/scripts/render.mjs renderer for eventual MP4 output.
"""
from __future__ import annotations
import argparse
import json
import math
import re
import shutil
from pathlib import Path

DEFAULT_SCENES = {
    "hook": "gate", "gates": "gate", "gate": "gate",
    "intro": "study", "study": "study", "meeting": "study",
    "map": "map", "question": "map", "drawing": "map",
    "stairs": "stairs", "staircase": "stairs", "discovery": "stairs",
    "close": "close", "closing": "close", "ending": "close"
}
SUPPORTED = {"gate", "study", "map", "stairs", "close"}
BASE = Path(__file__).resolve().parent.parent


def problem(message: str) -> ValueError:
    return ValueError(f"build_from_timings: {message}")


def finite_time(value, key):
    if type(value) not in (float, int) or not math.isfinite(value) or value < 0:
        raise problem(f"{key} must be finite and >= 0")
    return float(value)


def collect(source: dict, mapping: dict):
    if not isinstance(source, dict):
        raise problem("timings must be a JSON object")
    rows = source.get("segments")
    if not isinstance(rows, list) or not rows or len(rows) > 500:
        raise problem("timings.json needs 1–500 segments")
    if any(not isinstance(row, dict) for row in rows):
        raise problem("every timing segment must be an object")
    total = finite_time(source.get("duration"), "duration")
    if total <= 0:
        raise problem("duration must be > 0")
    shots = []
    last_end = -0.00001
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise problem(f"segment {index} is not an object")
        start = finite_time(row.get("start"), f"segments[{index}].start")
        end = finite_time(row.get("end"), f"segments[{index}].end")
        if end <= start or start < last_end - 0.02:
            raise problem(f"segment {index} has invalid duration or overlaps a previous line")
        last_end = end
        scene = str(row.get("scene_id") or "study")
        mapped = mapping.get(scene)
        if mapped not in SUPPORTED:
            raise problem(f"unknown scene_id={scene!r}; map it to {sorted(SUPPORTED)}")
        if index + 1 < len(rows):
            nxt = finite_time(rows[index+1].get("start"), f"segments[{index+1}].start")
        else:
            nxt = total
        start_this = 0.0 if index == 0 else start
        if nxt <= start_this:
            raise problem(f"segment {index} leaves a zero-length picture interval")
        if end > total + 0.1:
            raise problem("spoken audio exceeds narration duration")
        shots.append({
            "id": mapped,
            "duration": round(nxt - start_this, 5),
            "speaker": str(row.get("speaker") or "NARRATOR").upper(),
            "text": str(row.get("display") or row.get("text") or "").strip(),
        })
    # Prevent loss of early silence and gaps by assigning the full measured master
    # timeline to picture intervals, rather than summing only actual speech spans.
    last_anchor = 0.0 if len(rows) == 1 else rows[-1]["start"]
    shots[-1]["duration"] = round(total-last_anchor, 5)
    if any(s["duration"] <= 0 for s in shots):
        raise problem("invalid segment timing; picture contains a zero-length interval")
    if abs(sum(s["duration"] for s in shots) - total) > 0.02:
        raise problem("picture durations do not sum to the measured audio duration")
    return shots, total


def build(timings: Path, destination: Path, mapping: dict, captions=False, width=1920, height=1080, fps=30):
    record = json.loads(timings.read_text(encoding="utf-8"))
    shots, total = collect(record, mapping)
    if destination.exists():
        raise problem("output folder already exists; use a fresh folder to preserve previous cuts")
    destination.mkdir(parents=True)
    shutil.copy2(BASE / "engine.js", destination / "engine.js")
    payload = json.dumps(shots, ensure_ascii=False).replace("</", "<\\/")
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>FounderNotes — Original Painted Motion</title>
<style>html,body{{margin:0;background:#111921;width:100%;height:100%;overflow:hidden}}
svg{{width:100%;height:100%;display:block}}</style></head><body>
<svg id="stage" role="img" aria-label="Animated FounderNotes character scene"></svg>
<script src="engine.js"></script><script>
const frames = {payload};
const film = FNPaintedMotion.mount(document.getElementById('stage'),
  {{beats:frames,captions:{str(captions).lower()}}});
window.MOTION={{width:{width},height:{height},fps:{fps},duration:film.duration}};
window.seek=async(t)=>film.seek(t);film.seek(0);
</script></body></html>'''
    (destination / "index.html").write_text(html, encoding="utf-8")
    (destination / "shot-timeline.json").write_text(json.dumps({"format":"16:9", "fps":fps,"duration":total,"shots":shots},indent=2,ensure_ascii=False),encoding="utf-8")
    return shots, total


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("timings",type=Path,help="FounderNotes narration/timings.json")
    p.add_argument("--out",required=True,type=Path,help="output folder for index.html and engine.js")
    p.add_argument("--mapping",type=Path,help="optional JSON mapping scene_id -> supported visual shot")
    p.add_argument("--show-captions",action="store_true",help="preview captions only; normally FounderNotes burns the checked SRT later")
    p.add_argument("--fps",type=int,default=30)
    a=p.parse_args(argv)
    if a.fps<12 or a.fps>60:
        p.error("fps must be 12–60")
    mapping=DEFAULT_SCENES.copy()
    if a.mapping:
        custom=json.loads(a.mapping.read_text(encoding="utf-8"))
        if not isinstance(custom,dict) or any(not isinstance(k,str) or v not in SUPPORTED for k,v in custom.items()):
            p.error("mapping must be a JSON object with known shot values")
        mapping.update(custom)
    try:
        shots,duration=build(a.timings,a.out,mapping,a.show_captions,fps=a.fps)
    except (ValueError,KeyError,TypeError) as e:
        p.error(str(e))
    print(f"Prepared {len(shots)} deterministic SVG shots, {duration:.2f}s, 16:9 at {a.fps}fps → {a.out/'index.html'}")
    print("Rendering still requires Chromium + FounderNotes' motion/scripts/render.mjs; voice not created here")
    return 0

if __name__=='__main__':
    raise SystemExit(main())
