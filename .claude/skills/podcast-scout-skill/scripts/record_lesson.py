#!/usr/bin/env python3
"""Persist verified FounderNotes defects, positive recipes and completed video records.

No automatic scores or invented results. Recording a lesson requires an
explicit evidence reference. Skill evaluation is handled separately by
evaluate_skills.py and checked per-video before final approval.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(".claude/memory")
FILES = {"mistake": "mistakes_and_pitfalls.md", "recipe": "positive_recipes.md",
         "video": "production_ledger.json"}

def validate(payload):
    if not isinstance(payload, dict):
        return ["lesson must be a JSON object"]
    errors = []
    category = payload.get("type")
    if category not in FILES:
        errors.append("type must be mistake, recipe or video")
    for field in ("video_id", "summary", "evidence", "verification"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            errors.append(f"{field} must be a nonempty string")
    if category in ("mistake", "recipe"):
        for field in ("cause", "action"):
            if not isinstance(payload.get(field), str) or not payload[field].strip():
                errors.append(f"{field} must be a nonempty string")
    if category == "video":
        for field in ("status", "style_fingerprint"):
            if not isinstance(payload.get(field), str) or not payload[field].strip():
                errors.append(f"{field} must be a nonempty string")
        if payload.get("status") not in ("passed", "needs_work"):
            errors.append("video status must be passed or needs_work")
        if payload.get("status") == "passed" and payload.get("owner_approved") is not True:
            errors.append("passing video requires owner_approved:true")
    return errors

def record(payload, root=DEFAULT_ROOT):
    issues = validate(payload)
    if issues:
        raise ValueError("; ".join(issues))
    root.mkdir(parents=True, exist_ok=True)
    category = payload["type"]
    filename = root / FILES[category]
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    if category == "video":
        data = json.loads(filename.read_text(encoding="utf-8")) if filename.exists() else {"schema_version": 1, "videos": []}
        if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("videos"), list):
            raise ValueError("Invalid production ledger schema")
        if any(isinstance(v, dict) and v.get("video_id") == payload["video_id"] for v in data["videos"]):
            raise ValueError("A record for this video_id already exists; do not overwrite history")
        entry = dict(payload)
        entry["recorded_at"] = timestamp
        data["videos"].append(entry)
        tmp = filename.with_name(filename.name + ".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(tmp, filename)
    else:
        def clean(value):
            return str(value).replace("\n", " ").replace("\r", " ").strip()
        entry = (f"\n### {clean(payload['video_id'])} — {clean(payload['summary'])}\n\n"
                 f"- Recorded (UTC): {timestamp}\n"
                 f"- Evidence: {clean(payload['evidence'])}\n"
                 f"- Cause / rationale: {clean(payload['cause'])}\n"
                 f"- Correction / recipe: {clean(payload['action'])}\n"
                 f"- Verification: {clean(payload['verification'])}\n")
        with filename.open("a", encoding="utf-8") as out:
            out.write(entry)
    return filename

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_json", type=Path, help="JSON describing a verified mistake, recipe, or video")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.lesson_json.read_text(encoding="utf-8"))
        filename = record(payload, args.root)
        print(f"RECORDED: {filename}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
