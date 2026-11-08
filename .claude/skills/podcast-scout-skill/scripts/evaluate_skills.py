#!/usr/bin/env python3
"""Continuous evaluation ledger for *all* FounderNotes skill sources.

Register native + external + owner-uploaded skills, record observed production
evidence, identify stale/unassessed skills, and gate used skills per video.
This script does NOT install tools, run renders or invent successful reviews.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

NATIVE = (
    "pixel-art chalkboard glow-sketch ps2 comic-art flat-vector dan-koe "
    "cgi-motion lego zackd-films one-line-graph one-ball-showreel "
    "ascii-terminal pixel-dither risograph-cutout renaissance-codex ink-in-water"
).split()
UPSTREAM = (
    "bang-motion vox-director huashu-art-motion claude-drawing-skill "
    "code-animation-prompts agency-agents anidoodle ClaudeAnimationBase "
    "motion-skill lottiefiles-motion-design HandDraw-Skill manim_skill "
    "javascript-animation-skills stickman-video-director youtube-agent-skill "
    "OpenMontage voicebox Agent-Reach p5.brush openverse earshot opentoonz "
    "synfig pencil2d vox-ai-motion-graphics-generator pixelfx hyperframes "
    "onetake gbro-collage-broll lemo-opuscar"
).split()
UPLOADED = (
    "3d-animation cartoon-episodes documentary commercial-pipeline "
    "paper-cut-motion talking-object skeleton-ads song-style-ad "
    "claymation paper-animation"
).split()
STALE_AFTER_DAYS = 30
DIMENSIONS = ("clarity", "motion", "continuity", "audio", "reliability", "rights")

def identifier(family, name):
    return family + "/" + name

def catalogue():
    records = {}
    for family, names in (("native", NATIVE), ("external", UPSTREAM), ("uploaded", UPLOADED)):
        for name in names:
            key = identifier(family, name)
            records[key] = {"family": family, "name": name}
    return records

def now_utc():
    return dt.datetime.now(dt.timezone.utc)

def _parse_time(value):
    try:
        date = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return date if date.tzinfo else None
    except (TypeError, ValueError, AttributeError):
        return None

def read_ledger(path):
    if not path.exists():
        return {"schema_version": 1, "reviews": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("reviews"), list):
        raise ValueError("Invalid evaluation ledger schema")
    return data

def latest_reviews(data):
    latest = {}
    for review in data["reviews"]:
        if isinstance(review, dict) and review.get("skill_id") in catalogue():
            timestamp = _parse_time(review.get("evaluated_at"))
            if timestamp and (review["skill_id"] not in latest or timestamp > latest[review["skill_id"]][0]):
                latest[review["skill_id"]] = (timestamp, review)
    return latest

def status(data, at=None):
    at = at or now_utc()
    latest = latest_reviews(data)
    rows = []
    for key, info in catalogue().items():
        record = latest.get(key)
        if record is None:
            state = "UNASSESSED"
        else:
            date, review = record
            age = (at - date).total_seconds() / 86400
            if age > STALE_AFTER_DAYS:
                state = "STALE"
            elif review.get("outcome") == "pass":
                state = "PASS"
            elif review.get("outcome") == "fail":
                state = "FAIL"
            else:
                state = "NEEDS_REVIEW"
        rows.append((key, info["family"], state))
    return rows

def validate_review(review):
    errors = []
    registry = catalogue()
    if not isinstance(review, dict):
        return ["Review must be a JSON object"]
    key = review.get("skill_id")
    if not isinstance(key, str) or key not in registry:
        errors.append("skill_id must be an exact registered ID")
    if review.get("outcome") not in ("pass", "fail", "needs_review"):
        errors.append("outcome must be pass, fail or needs_review")
    video = review.get("video_id")
    if not isinstance(video, str) or not video.strip():
        errors.append("video_id must identify the video or benchmark")
    evidence = review.get("evidence")
    if not isinstance(evidence, dict):
        errors.append("evidence must include source paths for real checks")
    else:
        for field in ("sample_path", "qa_report_path", "reviewer", "finding"):
            if not isinstance(evidence.get(field), str) or not evidence[field].strip():
                errors.append(f"evidence.{field} must be a nonempty string")
    ratings = review.get("ratings")
    if not isinstance(ratings, dict):
        errors.append("ratings must be a complete object")
    else:
        for field in DIMENSIONS:
            rating = ratings.get(field)
            if type(rating) not in (int, float) or not (0 <= rating <= 5):
                errors.append(f"ratings.{field} must be between 0 and 5")
    if review.get("outcome") == "pass" and isinstance(ratings, dict):
        if any(type(ratings.get(field)) in (int, float) and ratings[field] < 3 for field in DIMENSIONS):
            errors.append("passing review cannot have any dimension below 3/5")
    if "evaluated_at" in review and _parse_time(review["evaluated_at"]) is None:
        errors.append("evaluated_at must be an offset-aware ISO 8601 timestamp")
    return errors

def record_review(data, review, timestamp=None):
    issues = validate_review(review)
    if issues:
        raise ValueError("; ".join(issues))
    copy = dict(review)
    copy["evaluated_at"] = (timestamp or now_utc()).isoformat()
    data["reviews"].append(copy)
    return data

def gate(data, video_id, used_ids, at=None):
    if not isinstance(video_id, str) or not video_id.strip():
        return ["video_id is required"]
    current = latest_reviews(data)
    failures = []
    for key in used_ids:
        if key not in catalogue():
            failures.append(f"{key}: unknown skill ID")
            continue
        entry = current.get(key)
        if entry is None:
            failures.append(f"{key}: never evaluated")
            continue
        date, review = entry
        if review.get("video_id") != video_id:
            failures.append(f"{key}: no evaluation recorded for this video")
        elif review.get("outcome") != "pass":
            failures.append(f"{key}: latest review is {review.get('outcome')}, not pass")
    return failures

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(".claude/memory/skill_evaluations.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="List all registered sources with evidence status")
    rec = commands.add_parser("record", help="Validate and append a JSON review")
    rec.add_argument("review_file", type=Path)
    check = commands.add_parser("gate", help="Require per-video PASS reviews for used skills")
    check.add_argument("--video", required=True)
    check.add_argument("--used", nargs="+", required=True, help="Exact skill IDs")
    args = parser.parse_args(argv)

    try:
        data = read_ledger(args.ledger)
        if args.command == "status":
            for key, family, state in status(data):
                print(f"{state:13} {key}")
            return 0
        if args.command == "record":
            review = json.loads(args.review_file.read_text(encoding="utf-8"))
            record_review(data, review)
            args.ledger.parent.mkdir(parents=True, exist_ok=True)
            temp = args.ledger.with_name(args.ledger.name + ".tmp")
            temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            os.replace(temp, args.ledger)
            print(f"RECORDED: {review['skill_id']} ({review['outcome']})")
            return 0
        problems = gate(data, args.video, args.used)
        if problems:
            for error in problems:
                print("FAIL:", error, file=sys.stderr)
            return 1
        print("PASS: all used skills evaluated for this video")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
