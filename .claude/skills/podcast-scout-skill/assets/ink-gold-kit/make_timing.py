import json, pathlib
here = pathlib.Path(__file__).parent
t = json.load(open(here.parent / "narration" / "timings.json"))
seg = {s["id"]: [s["start"], s["end"]] for s in t["segments"]}
scenes = json.load(open(here / "scenes.json"))
out, total = {}, t["duration"]
for i, sc in enumerate(scenes):
    first, last = seg[sc["segments"][0]], seg[sc["segments"][-1]]
    start = 0.0 if i == 0 else out[scenes[i-1]["name"]]["end"]
    if i + 1 < len(scenes):
        nxt = seg[scenes[i+1]["segments"][0]][0]
        end = round(last[1] + (nxt - last[1]) * 0.6, 3)   # cut 60% into the gap
    else:
        end = round(total, 3)
    out[sc["name"]] = {"start": round(start, 3), "end": end}
# snap cut points to whole frames at 30 fps so clip lengths add up exactly
for v in out.values():
    v["start"] = round(round(v["start"] * 30) / 30, 4); v["end"] = round(round(v["end"] * 30) / 30, 4)
seams = json.load(open(here / "seams.json"))
SE = {}
for r in seams["seams"]:
    SE.setdefault(r["a"], {})["out"] = {"vector": r["vector"], "dur": seams["dur"]}
    SE.setdefault(r["b"], {})["in"] = {"vector": r["vector"], "dur": seams["dur"]}
(here / "timing.js").write_text("window.TIMING=" + json.dumps({"scenes": out, "seg": seg}) + ";\nwindow.SEAMS=" + json.dumps(SE) + ";\n")
for k, v in out.items(): print(f"{k:16s} {v['start']:8.3f} {v['end']:8.3f} {v['end']-v['start']:6.2f}s")
