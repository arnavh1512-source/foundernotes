#!/usr/bin/env python3
"""FounderNotes creative format router and strict shot-plan preflight.

This tool validates a production plan; it does not synthesize, render or
authorize third-party content. Only Python's standard library is required.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

FORMATS = {
    "3d-animation": ("3D causal explainers", ("3d", "mechanism", "myth")),
    "cartoon-episodes": ("Recurring character/world scenes", ("cartoon", "character", "series")),
    "documentary": ("Evidence-backed case reconstruction", ("documentary", "history", "investigation")),
    "commercial-pipeline": ("Commercial-format sequences", ("commercial", "promo", "advert")),
    "paper-cut-motion": ("Layered paper-cut motion", ("cutout", "paper cut", "motion design")),
    "talking-object": ("Expressive original object character", ("object", "mascot", "talking")),
    "skeleton-ads": ("Stylized articulated character analogy", ("skeleton", "anatomy")),
    "song-style-ad": ("Approved music-first creative", ("song", "jingle", "music")),
    "claymation": ("Physical clay stop-motion", ("clay", "plasticine", "stop motion")),
    "paper-animation": ("Paper collage, origami and parallax", ("paper", "collage", "origami")),
}

def _valid_seconds(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0

def _record_ok(record):
    return (isinstance(record, dict) and record.get("verified") is True
            and isinstance(record.get("source"), str) and bool(record["source"].strip()))

def validate_plan(plan):
    """Return actionable error strings. Never silently waive production gates."""
    errors = []
    if not isinstance(plan, dict):
        return ["Plan must be a JSON object."]
    narrator = plan.get("narrator")
    if not isinstance(narrator, dict):
        errors.append("narrator must be an object.")
    else:
        if narrator.get("gender") != "male":
            errors.append("narrator.gender must be 'male' for this channel.")
        if not isinstance(narrator.get("voice_id"), str) or not narrator["voice_id"].strip():
            errors.append("narrator.voice_id must identify the approved male voice.")
        if narrator.get("approved") is not True:
            errors.append("narrator.approved must be true (voice rights/owner approval).")

    duration = plan.get("narration_duration_s")
    if not _valid_seconds(duration) or duration <= 0:
        errors.append("narration_duration_s must be a measured positive finite number.")

    claims = plan.get("claims", {})
    if not isinstance(claims, dict):
        errors.append("claims must be an object keyed by claim ID.")
        claims = {}
    assets = plan.get("asset_manifest", {})
    if not isinstance(assets, dict):
        errors.append("asset_manifest must be an object keyed by asset ID.")
        assets = {}
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty array.")
        return errors

    ids = set()
    previous_end = 0.0
    for number, shot in enumerate(shots, 1):
        prefix = f"shots[{number - 1}]"
        if not isinstance(shot, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        sid = shot.get("id")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"{prefix}.id must be nonempty.")
        elif sid in ids:
            errors.append(f"{prefix}.id is a duplicate: {sid}")
        else:
            ids.add(sid)

        fmt = shot.get("format")
        if fmt not in FORMATS:
            errors.append(f"{prefix}.format must be one of: {', '.join(FORMATS)}.")
        start, end = shot.get("start_s"), shot.get("end_s")
        if not _valid_seconds(start) or not _valid_seconds(end) or end <= start:
            errors.append(f"{prefix} requires finite 0 <= start_s < end_s.")
        else:
            if number == 1 and start > 0.25:
                errors.append(f"{prefix} leaves an unexplained opening gap of {start:.2f}s.")
            if start < previous_end - 0.05:
                errors.append(f"{prefix} overlaps previous shot by {previous_end - start:.2f}s.")
            if start > previous_end + 0.25:
                errors.append(f"{prefix} leaves an unexplained picture gap of {start - previous_end:.2f}s.")
            previous_end = end

        cid = shot.get("claim_id")
        if cid not in (None, ""):
            record = claims.get(cid) if isinstance(cid, str) else None
            if not _record_ok(record):
                errors.append(f"{prefix}.claim_id '{cid}' is not independently verified with a source.")
        elif fmt == "documentary":
            errors.append(f"{prefix} documentary requires a verified claim_id.")

        asset_ids = shot.get("asset_ids")
        if not isinstance(asset_ids, list):
            errors.append(f"{prefix}.asset_ids must be an array (can be empty for procedural art).")
        else:
            for aid in asset_ids:
                if not isinstance(aid, str) or not aid.strip():
                    errors.append(f"{prefix} has an invalid asset ID.")
                    continue
                asset = assets.get(aid)
                if (not isinstance(asset, dict) or asset.get("rights_verified") is not True
                    or not isinstance(asset.get("source"), str) or not asset["source"].strip()
                    or not isinstance(asset.get("license"), str) or not asset["license"].strip()):
                    errors.append(f"{prefix} asset '{aid}' lacks source, license or verified rights.")

        if shot.get("paid") is not True and shot.get("cost_approved") is True:
            errors.append(f"{prefix} has cost_approved without paid:true.")
        if shot.get("paid") is True:
            if shot.get("cost_approved") is not True:
                errors.append(f"{prefix} paid generation requires cost_approved:true.")
            cost = shot.get("estimated_cost")
            if not _valid_seconds(cost):
                errors.append(f"{prefix} paid generation requires finite estimated_cost >= 0.")
        if shot.get("use_noncommercial_source_code") is True:
            errors.append(f"{prefix} cannot use noncommercial source code in this monetized channel.")
    if _valid_seconds(duration) and duration > 0 and abs(previous_end - duration) > 0.5:
        errors.append(f"Picture ends at {previous_end:.2f}s but measured narration is {duration:.2f}s; repair the edit.")
    return errors

def example_plan():
    return {
        "narrator": {"voice_id": "founder-notes", "gender": "male", "approved": True},
        "narration_duration_s": 10.0,
        "claims": {"C1": {"verified": True, "source": "https://example.org/replace-with-real-evidence"}},
        "asset_manifest": {},
        "shots": [
            {"id": "s01", "format": "documentary", "start_s": 0, "end_s": 5,
             "claim_id": "C1", "asset_ids": [], "paid": False},
            {"id": "s02", "format": "paper-animation", "start_s": 5, "end_s": 10,
             "claim_id": "C1", "asset_ids": [], "paid": False},
        ]
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="Show ten adapted creative formats")
    group.add_argument("--recommend", metavar="TOPIC", help="Rank format keywords for a topic")
    group.add_argument("--validate", metavar="PLAN_JSON", type=Path, help="Preflight a JSON shot plan")
    group.add_argument("--sample", action="store_true", help="Print an illustrative plan; replace example evidence")
    args = parser.parse_args(argv)

    if args.sample:
        print(json.dumps(example_plan(), indent=2))
        return 0
    if args.validate:
        try:
            plan = json.loads(args.validate.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"FAIL: Cannot read plan: {exc}", file=sys.stderr)
            return 2
        errors = validate_plan(plan)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"{'FAIL' if errors else 'PASS'}: {len(errors)} error(s)")
        return 1 if errors else 0
    if args.recommend:
        topic = args.recommend.lower()
        scored = [(sum(term in topic for term in terms), key, label)
                  for key, (label, terms) in FORMATS.items()]
        for score, key, label in sorted(scored, key=lambda item: (-item[0], item[1]))[:5]:
            print(f"{key:22} {label} (keyword matches: {score})")
        return 0
    for key, (label, _) in FORMATS.items():
        print(f"{key:22} {label}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
