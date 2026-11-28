#!/usr/bin/env python3
"""Measure how a reference video moves, frame by frame: camera zoom/pan/roll, motion inside the picture, holds, cuts.

    ~/.cache/venv-rea/bin/python ref_motion.py <video.mp4> <out_dir>      (needs OpenCV: the rea-video venv has it)

Writes out_dir/motion.csv (one row per frame step) and out_dir/motion.json with:
- camera moves: start, end, kind (zoom in/out, pan, roll), size, and easing (where half the move is done: ~0.5 linear,
  near 0.5 with slow ends = ease in-out, early = ease out, late = ease in)
- holds: repeated frames (1 repeat = animating on twos) and still stretches
- cuts and the biggest action peaks (motion left after removing the camera)
Measurements, not judgement: look at the frames around every number before acting on it.
"""
import csv, json, math, sys
from pathlib import Path

import cv2
import numpy as np


def camera(prev, cur, orb, bf):
    """Similarity transform prev->cur (scale, rotation, dx, dy) from ORB matches; None when it can't be found."""
    k1, d1 = orb.detectAndCompute(prev, None); k2, d2 = orb.detectAndCompute(cur, None)
    if d1 is None or d2 is None or len(k1) < 12 or len(k2) < 12:
        return None
    m = sorted(bf.match(d1, d2), key=lambda a: a.distance)[:300]
    if len(m) < 12:
        return None
    a = np.float32([k1[i.queryIdx].pt for i in m]); b = np.float32([k2[i.trainIdx].pt for i in m])
    M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    if M is None or inl is None or inl.sum() < 10:
        return None
    s = math.hypot(M[0, 0], M[1, 0]); return s, math.degrees(math.atan2(M[1, 0], M[0, 0])), M[0, 2], M[1, 2], M


def segments(vals, thr, minlen):
    out, start = [], None
    for i, v in enumerate(list(vals) + [0]):
        if abs(v) > thr and start is None: start = i
        elif (abs(v) <= thr) and start is not None:
            if i - start >= minlen: out.append((start, i))
            start = None
    return out


def easing(steps):
    c = np.cumsum(np.abs(steps)); c = c / c[-1] if c[-1] else c
    half = int(np.searchsorted(c, .5)); n = len(steps)
    ends = (np.abs(steps[:max(1, n // 5)]).mean() + np.abs(steps[-max(1, n // 5):]).mean()) / 2 / (np.abs(steps).mean() + 1e-9)
    return round(half / max(1, n - 1), 2), round(float(ends), 2)


def main(video, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video)); fps = cap.get(cv2.CAP_PROP_FPS) or 30
    orb = cv2.ORB_create(1500); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    rows, prev = [], None
    while True:
        ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); h, w = g.shape; sc = 360 / max(h, w); g = cv2.resize(g, (int(w * sc), int(h * sc)))
        if prev is not None:
            raw = float((cv2.absdiff(prev, g) > 10).mean() * 100)
            cam = camera(prev, g, orb, bf) if raw > .05 else (1.0, 0.0, 0.0, 0.0, None)
            if cam and cam[4] is not None:
                warped = cv2.warpAffine(prev, cam[4], (g.shape[1], g.shape[0]), borderMode=cv2.BORDER_REPLICATE)
                local = float((cv2.absdiff(warped, g) > 18).mean() * 100)
            else:
                local = raw
            s, r, dx, dy = (cam[:4] if cam else (1.0, 0.0, 0.0, 0.0))
            rows.append({"i": len(rows) + 1, "t": round((len(rows) + 1) / fps, 3), "changed_pct": round(raw, 2), "scale": round(s, 4), "rot_deg": round(r, 3),
                         "dx": round(dx / sc, 2), "dy": round(dy / sc, 2), "local_pct": round(local, 2), "cam_ok": cam is not None})
        prev = g
    with open(out / "motion.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    ch = np.array([r["changed_pct"] for r in rows]); loc = np.array([r["local_pct"] for r in rows])
    cuts = [rows[i]["t"] for i in range(len(rows)) if ch[i] > 40 and not rows[i]["cam_ok"]]
    zoom = np.array([math.log(r["scale"]) if r["cam_ok"] else 0 for r in rows]); pan = np.array([math.hypot(r["dx"], r["dy"]) if r["cam_ok"] else 0 for r in rows])
    rot = np.array([r["rot_deg"] if r["cam_ok"] else 0 for r in rows])
    moves = []
    for kind, v, thr in (("zoom", zoom, .002), ("pan", pan, 1.5), ("roll", rot, .15)):
        for a, b in segments(v, thr, 4):
            tot = float(v[a:b].sum()); half, ends = easing(v[a:b])
            moves.append({"kind": kind if kind != "zoom" else ("zoom in" if tot > 0 else "zoom out"), "start": rows[a]["t"], "end": rows[b - 1]["t"],
                          "size": round(math.exp(tot), 2) if kind == "zoom" else round(tot, 1), "half_done_at": half, "end_speed_vs_mean": ends})
    rep = (ch < .01).astype(int); runs, n = [], 0
    for v in list(rep) + [0]:
        if v: n += 1
        elif n: runs.append(n); n = 0
    peaks = sorted(range(len(loc)), key=lambda i: -loc[i])[:12]
    rep_json = {"video": str(video), "fps": fps, "frames": len(rows) + 1, "cuts": cuts, "camera_moves": sorted(moves, key=lambda m: m["start"]),
                "repeated_frames_pct": round(float(rep.mean() * 100), 1), "single_repeats": runs.count(1), "holds_over_3_frames": [x for x in runs if x >= 3],
                "local_motion_mean_pct": round(float(loc.mean()), 2), "action_peaks": sorted({rows[i]["t"] for i in peaks})}
    (out / "motion.json").write_text(json.dumps(rep_json, indent=1))
    print(json.dumps({k: v for k, v in rep_json.items() if k != "camera_moves"}, indent=0)); print(f"camera moves: {len(moves)} -> {out}/motion.json")


if __name__ == "__main__":
    main(*sys.argv[1:3])
