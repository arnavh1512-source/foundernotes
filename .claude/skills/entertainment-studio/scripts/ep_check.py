#!/usr/bin/env python3
"""Entertainment checks for an episode workspace: every link from script to export must hold.

    python3 ep_check.py <workspace>     exit 1 and list every broken link
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ep_build import asset_file, render_key, resolve, sha  # noqa: E402

ASSET_ID = re.compile(r"^[A-Z]{2,4}-(CHAR|WARD|PROP|LOC)-[A-Z0-9]+(-[A-Z0-9]+)*$")


def check(ws):
    ws = Path(ws)
    err = []
    try:
        m = json.loads((ws / "workspace.json").read_text())
    except (OSError, ValueError) as e:
        return [f"workspace.json unreadable: {e}"]
    if m.get("profile") != "entertainment-ip":
        return [f"profile is {m.get('profile')!r}: Think! (educational) work uses the Think! tools and gates, not these checks"]

    sc = m.get("script", {})
    p = ws / sc.get("path", "")
    if not sc.get("path") or not p.is_file():
        err.append(f"script revision missing: {sc.get('path')}")
    elif sha(p) != sc.get("sha256"):
        err.append(f"script {sc['path']} changed since revision {sc.get('revision')} was pinned (sha256 differs)")

    ids = set()
    for a in m.get("assets", []):
        if not ASSET_ID.match(a.get("id", "")):
            err.append(f"asset id {a.get('id')!r} is not a stable <SERIES>-<CHAR|WARD|PROP|LOC>-<NAME> id")
        if a.get("id") in ids:
            err.append(f"duplicate asset id {a['id']}")
        ids.add(a.get("id"))
        for v in a.get("versions", []):
            f = ws / v.get("file", "")
            if not f.is_file():
                err.append(f"{a['id']} v{v.get('v')}: file missing {v.get('file')}")
            elif sha(f) != v.get("sha256"):
                err.append(f"{a['id']} v{v['v']}: {v['file']} changed after it was versioned (make a new version)")

    shots = {s["id"]: s for s in m.get("shots", [])}
    if len(shots) != len(m.get("shots", [])):
        err.append("duplicate shot ids")
    for s in m.get("shots", []):
        if not (ws / f"scenes/{s.get('scene')}.js").is_file():
            err.append(f"{s['id']}: scene file scenes/{s.get('scene')}.js missing")
        if not s.get("dur", 0) > 0:
            err.append(f"{s['id']}: duration must be positive")
        for u in s.get("uses", []):
            try:
                asset_file(ws, m, u["asset"], u["v"])
            except KeyError:
                err.append(f"{s['id']} uses {u.get('asset')} v{u.get('v')}, which is not a registered asset version")

    variants = [v["id"] for v in m.get("variants", [])]
    for v in m.get("variants", []):
        for sid, ov in v.get("overrides", {}).items():
            if sid not in shots:
                err.append(f"variant {v['id']} overrides unknown shot {sid}")
            if set(ov) - {"dur"}:
                err.append(f"variant {v['id']} changes {sorted(set(ov) - {'dur'})} on {sid}: variants may only change timing, so framing and performance stay identical")
    for c in m.get("audio_cues", []):
        if c.get("shot") not in shots:
            err.append(f"cue {c.get('id')} points at missing shot {c.get('shot')}")
            continue
        for vid in variants:
            d = next(s["dur"] for s in resolve(m, vid) if s["id"] == c["shot"])
            if not 0 <= c.get("t", -1) < d:
                err.append(f"cue {c['id']} at {c.get('t')}s falls outside {c['shot']} ({d}s) in variant {vid}")
        if "dur" in c and not (isinstance(c["dur"], (int, float)) and c["dur"] > 0):
            err.append(f"cue {c['id']}: dur must be a positive number of seconds")
        if c.get("temporary") and not c.get("note"):
            err.append(f"cue {c['id']} is temporary but has no note saying why")
    if err:
        return err  # later checks rely on the plan being sound

    takes = {t["id"]: t for t in m.get("takes", [])}
    for vid in variants:
        t = next((t for t in takes.values() if t["variant"] == vid), None)
        if not t:
            err.append(f"variant {vid} has no take: run ep_build.py")
            continue
        f = ws / t["file"]
        if not f.is_file() or sha(f) != t["sha256"]:
            err.append(f"take {t['id']}: file missing or changed since the build")
        plan = resolve(m, vid)
        if [r["id"] for r in t["shots"]] != [s["id"] for s in plan]:
            err.append(f"take {t['id']}: shot order differs from the plan")
            continue
        for r, s in zip(t["shots"], plan):
            if r["render_key"] != render_key(ws, m, s):
                err.append(f"take {t['id']} {s['id']}: built from an outdated render (scene, assets or timing changed): rebuild")
            c = ws / r["clip"]
            if not c.is_file() or sha(c) != r["clip_sha256"]:
                err.append(f"take {t['id']} {s['id']}: clip missing or changed")

    sel = m.get("selected")
    if sel:
        if sel.get("take") not in takes:
            err.append(f"selected take {sel.get('take')} does not exist")
        if len(sel.get("reason", "")) < 40:
            err.append("selected take needs a reason based on what the review observed")
        if not sel.get("notes"):
            err.append("selected take has no review notes with timestamps")
    exp = m.get("export")
    if exp:
        f = ws / exp.get("file", "")
        if not sel or exp.get("from_take") != sel.get("take"):
            err.append("export is not the selected take")
        elif not f.is_file() or sha(f) != exp.get("sha256") or sha(f) != takes[sel["take"]]["sha256"]:
            err.append("export file missing or out of date with the selected take: re-run ep_build.py --export")
        if any(c.get("temporary") for c in m["audio_cues"]) and "TEMP-AUDIO" not in exp.get("file", ""):
            err.append("export carries temporary sound but its filename does not say TEMP-AUDIO")
    return err


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    problems = check(sys.argv[1])
    for p in problems:
        print("FAIL", p)
    print("PASS: script, assets, shots, cues, takes, selection and export are linked" if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)
