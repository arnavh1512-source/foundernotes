#!/usr/bin/env python3
"""Animation learning engine: pick the next drill, measure it against the reference, critique it, close it.

    learn.py status                         skill tree, mastery and reviews due
    learn.py next                           the drill to do now (reviews due first, then the weakest unlocked skill)
    learn.py start <skill> <ref.mp4|ref.md> [<t0> <t1>] [--name NAME]   (story skills take a text reference, no window)
                                            new drill folder under studio-output/learn/ with the brief and criteria
    learn.py measure <drill_dir> <take.mp4|draft.md>
                                            video: measure reference window and take with ref_motion; draft: log it; adds an attempt
    learn.py critique <drill_dir> <verdicts.json>
                                            the critic's per-criterion verdicts for the latest attempt
    learn.py close <drill_dir> [--lesson lesson.json]
                                            update mastery, schedule the review, add a scoreboard row, record the lesson

Default verdict is NEEDS WORK: an attempt passes only when every criterion passes with a finding and the measured
numbers are within tolerance. Three failed attempts escalate: the gaps are recorded and the drill closes as unfinished.
Measurements are evidence to check by looking at the frames, never a verdict on their own.
"""
import argparse, datetime as dt, json, math, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2]
CURRICULUM = SKILL / "curriculum.json"
DRILLS = REPO / "studio-output" / "learn"
ES = REPO / ".claude" / "skills" / "entertainment-studio"
PLAYBOOK = ES / "references" / "animation-craft-playbook.md"
CV_PY = os.environ.get("LEARN_CV_PYTHON", str(Path.home() / ".cache/venv-rea/bin/python"))
MAX_ATTEMPTS = 3
# measured number -> allowed relative gap to the reference (None: report only)
TOLERANCE = {"local_motion_mean_pct": .25, "repeated_frames_pct": None, "camera_moves": .2, "cuts": None, "holds_over_3": None}


def today():
    return dt.date.fromisoformat(os.environ["LEARN_TODAY"]) if os.environ.get("LEARN_TODAY") else dt.date.today()


def load(path=CURRICULUM):
    return json.loads(Path(path).read_text())


def save(data, path=CURRICULUM):
    tmp = Path(str(path) + ".tmp"); tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n"); os.replace(tmp, path)


def skill(data, sid):
    for s in data["skills"]:
        if s["id"] == sid:
            return s
    raise SystemExit(f"unknown skill {sid!r}; see learn.py status")


def unlocked(data, s):
    return all(skill(data, p)["mastery"] >= 2 for p in s["prereqs"])


def pick_next(data, on=None):
    """Reviews due first (oldest first), then the weakest unlocked skill; ties keep curriculum order."""
    on = on or today()
    due = [s for s in data["skills"] if unlocked(data, s) and dt.date.fromisoformat(s["next_review"]) <= on]
    if not due:
        return None
    return sorted(due, key=lambda s: (s["mastery"], s["next_review"]))[0]


def compare(ref, take):
    """Relative gap per measured number; ok is None when the number has no tolerance."""
    out = {}
    for k, tol in TOLERANCE.items():
        r, t = ref.get(k), take.get(k)
        if r is None or t is None:
            continue
        gap = (t - r) / r if r else (0.0 if t == r else 1.0)
        out[k] = {"ref": r, "take": t, "gap": round(gap, 3), "ok": None if tol is None else abs(gap) <= tol}
    return out


def summary(motion):
    return {"local_motion_mean_pct": motion["local_motion_mean_pct"], "repeated_frames_pct": motion["repeated_frames_pct"],
            "camera_moves": len(motion["camera_moves"]), "cuts": len(motion["cuts"]), "holds_over_3": len(motion["holds_over_3_frames"])}


def validate_verdicts(criteria, verdicts):
    errors = []
    for c in criteria:
        v = verdicts.get(c)
        if not isinstance(v, dict) or not isinstance(v.get("pass"), bool):
            errors.append(f"missing pass true/false for: {c}"); continue
        if not str(v.get("finding", "")).strip():
            errors.append(f"no finding (what you saw, at what time) for: {c}")
        if v["pass"] is False and not str(v.get("fix", "")).strip():
            errors.append(f"failed criterion needs a fix: {c}")
    return errors


def attempt_verdict(attempt):
    crit = attempt.get("verdicts")
    if not crit:
        return "NEEDS WORK"
    measured_ok = all(m["ok"] is not False for m in attempt.get("measured", {}).values())
    return "PASS" if measured_ok and all(v["pass"] for v in crit.values()) else "NEEDS WORK"


def new_level(current, status, attempts):
    if status == "passed":
        return max(current, 3)
    return max(current, 2 if any(a.get("timing_ok") for a in attempts) else 1)


def drill_file(d):
    return Path(d) / "drill.json"


def cmd_status(a):
    data = load(); on = today()
    for s in data["skills"]:
        lock = "" if unlocked(data, s) else "  (locked: " + ", ".join(s["prereqs"]) + ")"
        due = " DUE" if dt.date.fromisoformat(s["next_review"]) <= on and not lock else ""
        print(f"{s['mastery']} {'#' * s['mastery']:<4} {s['id']:<22} review {s['next_review']}{due}{lock}")
    n = pick_next(data, on)
    print(f"\nnext: {n['id'] if n else 'nothing due'}")


def cmd_next(a):
    data = load(); s = pick_next(data)
    if not s:
        print("nothing due today; raise the weakest skill or study a new reference"); return
    print(json.dumps({"skill": s["id"], "name": s["name"], "mastery": s["mastery"], "level_meaning": data["levels"][str(s["mastery"])],
                      "references": s["refs"], "criteria": s["criteria"], "last_evidence": s["evidence"][-1:] }, indent=1))


def cmd_start(a):
    data = load(); s = skill(data, a.skill)
    DRILLS.mkdir(parents=True, exist_ok=True)
    n = 1 + len([p for p in DRILLS.glob(f"{s['id']}-*") if p.is_dir()])
    d = DRILLS / (a.name or f"{s['id']}-{n:02d}"); (d / "review").mkdir(parents=True, exist_ok=True)
    drill = {"skill": s["id"], "created": today().isoformat(), "reference": {"video": str(Path(a.ref).resolve()), "start": a.t0, "end": a.t1},
             "criteria": s["criteria"], "attempts": [], "status": "open", "max_attempts": MAX_ATTEMPTS}
    drill["kind"] = s.get("kind", "animation")
    drill_file(d).write_text(json.dumps(drill, indent=1))
    if is_text(a.ref) or a.t0 is None:
        print(f"drill {d}\nstory drill: read the reference, write the piece to a .md file, then run: learn.py measure {d} <draft.md>"); return
    sheet = window_sheet(a.ref, a.t0, a.t1, d / "review" / "window_sheet.jpg")
    print(f"window sheet {sheet}: check the window is ONE shot (no roll-zoom, wipe or cut); if not, start again with a shorter window")
    print(f"drill {d}\nstudy the reference window at full size first (ref_compare.py), then build a take and run: learn.py measure {d} <take.mp4>")


def sheet_grid(t0, t1, fps=4, cols=8):
    n = max(1, math.ceil((t1 - t0) * fps)); return n, cols, math.ceil(n / cols)


def window_sheet(video, t0, t1, out):
    """One frame every 0.25 s of the window, tiled, so a window that spans two shots is caught before the drill."""
    n, cols, rows = sheet_grid(t0, t1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-to", str(t1), "-i", str(video), "-vf", f"fps=4,scale=200:-2,tile={cols}x{rows}", "-frames:v", "1", str(out)], check=True)
    return out


def ref_motion(video, out, t0=None, t1=None):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    src = video
    if t0 is not None:
        src = out / "window.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-to", str(t1), "-i", str(video), "-an", "-c:v", "libx264", "-crf", "18", str(src)], check=True)
    subprocess.run([CV_PY, str(ES / "scripts" / "ref_motion.py"), str(src), str(out)], check=True, stdout=subprocess.DEVNULL)
    return json.loads((out / "motion.json").read_text())


def is_text(path):
    return Path(path).suffix.lower() in (".md", ".txt")


def cmd_measure(a):
    d = Path(a.drill); drill = json.loads(drill_file(d).read_text())
    if drill["status"] != "open":
        raise SystemExit(f"drill is {drill['status']}")
    if len(drill["attempts"]) >= drill["max_attempts"]:
        raise SystemExit("attempt limit reached: close the drill and record the gaps")
    if is_text(a.take):  # story drills: a written draft, judged by reading; nothing to measure
        n = len(drill["attempts"]) + 1
        drill["attempts"].append({"n": n, "take": str(Path(a.take).resolve()), "measured": {}, "verdicts": None, "verdict": "NEEDS WORK"})
        drill_file(d).write_text(json.dumps(drill, indent=1))
        print(f"attempt {n} (draft): now read it as an outsider, then: learn.py critique {d} verdicts.json"); return
    r = drill["reference"]; rm = d / "review" / "ref_motion"
    ref = json.loads((rm / "motion.json").read_text()) if (rm / "motion.json").exists() else ref_motion(r["video"], rm, r["start"], r["end"])
    n = len(drill["attempts"]) + 1
    take = ref_motion(a.take, d / "review" / f"take{n}_motion")
    m = compare(summary(ref), summary(take))
    drill["attempts"].append({"n": n, "take": str(Path(a.take).resolve()), "measured": m, "verdicts": None, "verdict": "NEEDS WORK"})
    drill_file(d).write_text(json.dumps(drill, indent=1))
    for k, v in m.items():
        print(f"{k:<24} ref {v['ref']:>7}  take {v['take']:>7}  gap {v['gap']:+.0%}  {'' if v['ok'] is None else ('ok' if v['ok'] else 'OUT')}")
    print(f"attempt {n}: now compare frames at full size, then: learn.py critique {d} verdicts.json")


def cmd_critique(a):
    d = Path(a.drill); drill = json.loads(drill_file(d).read_text())
    if not drill["attempts"]:
        raise SystemExit("measure an attempt first")
    v = json.loads(Path(a.verdicts).read_text())
    timing_ok = bool(v.pop("_timing_ok", False))
    errs = validate_verdicts(drill["criteria"], v)
    if errs:
        raise SystemExit("verdicts rejected:\n- " + "\n- ".join(errs))
    att = drill["attempts"][-1]; att["verdicts"] = v; att["timing_ok"] = timing_ok; att["verdict"] = attempt_verdict(att)
    if att["verdict"] == "PASS":
        drill["status"] = "passed"
    elif len(drill["attempts"]) >= drill["max_attempts"]:
        drill["status"] = "escalated"
    drill_file(d).write_text(json.dumps(drill, indent=1))
    fails = [c for c, x in v.items() if not x["pass"]]
    print(f"attempt {att['n']}: {att['verdict']}" + ("".join(f"\n  fix: {c} -> {v[c]['fix']}" for c in fails)))
    if drill["status"] != "open":
        print(f"drill {drill['status']}: run learn.py close {d}")


def scoreboard_row(drill, s, level):
    last = drill["attempts"][-1] if drill["attempts"] else {}
    v = last.get("verdicts") or {}
    good = "; ".join(c for c, x in v.items() if x["pass"]) or "-"
    gaps = "; ".join(c for c, x in v.items() if not x["pass"]) or "-"
    lm = last.get("measured", {}).get("local_motion_mean_pct")
    still = f"{lm['take']}% local ({lm['ref']}%)" if lm else "-"
    return f"| {today().isoformat()} | learn: {s['id']} ({drill['status']}, {len(drill['attempts'])} tries, level {level}) | {still} | {good} | {gaps} |\n"


def cmd_close(a):
    d = Path(a.drill); drill = json.loads(drill_file(d).read_text())
    if drill["status"] == "open":
        if not drill["attempts"]:
            raise SystemExit("nothing to close: no attempts")
        drill["status"] = "escalated"
    if drill.get("closed"):
        raise SystemExit("already closed")
    data = load(); s = skill(data, drill["skill"])
    level = new_level(s["mastery"], drill["status"], drill["attempts"])
    s["mastery"] = level
    s["next_review"] = (today() + dt.timedelta(days=data["review_days"][min(level, 4)])).isoformat()
    s["evidence"].append(f"{d.name}: {drill['status']} after {len(drill['attempts'])} tries")
    save(data)
    text = PLAYBOOK.read_text(); h = "|---|---|---|---|---|\n"
    if h in text:
        PLAYBOOK.write_text(text.replace(h, h + scoreboard_row(drill, s, level), 1))
    if a.lesson:
        subprocess.run([sys.executable, str(REPO / ".claude/skills/podcast-scout-skill/scripts/record_lesson.py"), a.lesson], check=True)
    drill["closed"] = today().isoformat(); drill_file(d).write_text(json.dumps(drill, indent=1))
    print(f"{s['id']}: level {level}, review {s['next_review']}; scoreboard updated" + ("; lesson recorded" if a.lesson else "; no lesson given"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status"); sub.add_parser("next")
    s = sub.add_parser("start"); s.add_argument("skill"); s.add_argument("ref"); s.add_argument("t0", type=float, nargs="?"); s.add_argument("t1", type=float, nargs="?"); s.add_argument("--name")
    s = sub.add_parser("measure"); s.add_argument("drill"); s.add_argument("take")
    s = sub.add_parser("critique"); s.add_argument("drill"); s.add_argument("verdicts")
    s = sub.add_parser("close"); s.add_argument("drill"); s.add_argument("--lesson")
    a = p.parse_args(argv)
    {"status": cmd_status, "next": cmd_next, "start": cmd_start, "measure": cmd_measure, "critique": cmd_critique, "close": cmd_close}[a.cmd](a)


if __name__ == "__main__":
    main()
