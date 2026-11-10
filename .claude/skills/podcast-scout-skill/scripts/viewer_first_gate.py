#!/usr/bin/env python3
"""FounderNotes mandatory viewer-first production preflight.

Checks structured evidence of the owner's eight-stage preparation protocol,
not the artistic truth of claims, quality of narration, or pilot effectiveness.
No paid/network operations. No files written unless --out is explicitly set.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CHECKS = ("outsider_understands_problem", "outsider_wants_answer",
          "outsider_already_learned_something")


def nonblank(value):
    return isinstance(value, str) and bool(value.strip()) and not bool(
        re.search(r"<[^>\n]{1,60}>|\b(TODO|TBD|PLACEHOLDER|INSERT HERE)\b", value, re.I)
    )


def validate(plan, *, stage="pre-script"):
    errors = []
    if stage not in {"pre-script", "full-production"}:
        return [f"Invalid gate stage: {stage}"]
    if not isinstance(plan, dict):
        return ["Root must be a JSON object"]
    if plan.get("schema_version") != 1 or isinstance(plan.get("schema_version"), bool):
        errors.append("schema_version must equal 1")

    def object_at(obj, key, where):
        result = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(result, dict):
            errors.append(f"{where}.{key} must be an object")
            return {}
        return result

    def string_at(obj, key, where):
        result = obj.get(key) if isinstance(obj, dict) else None
        if not nonblank(result):
            errors.append(f"{where}.{key} must have meaningful non-placeholder text")
            return ""
        return result.strip()

    def list_at(obj, key, where, *, min_count=1):
        value = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(value, list) or len(value) < min_count:
            errors.append(f"{where}.{key} must have at least {min_count} item(s)")
            return []
        return value

    # 1 — viewer need
    need = object_at(plan, "viewer_need", "plan")
    for k in ("who", "struggling_with", "daily_life_situation", "why_care_now"):
        string_at(need, k, "viewer_need")

    # 2 — learning promise; a filled sentence is mandatory before any script
    learn = object_at(plan, "learning_promise", "plan")
    for k in ("understand", "how_to", "specific_outcome"):
        string_at(learn, k, "learning_promise")
    sentence = string_at(plan, "viewer_promise_sentence", "plan")
    expected = ("This video is for someone struggling with "
                + str(need.get("struggling_with", "")).strip()
                + "; they'll understand " + str(learn.get("understand", "")).strip()
                + " and leave knowing how to " + str(learn.get("how_to", "")).strip()
                + ".")
    if sentence != expected:
        errors.append("viewer_promise_sentence must exactly complete: "
                      '"This video is for someone struggling with ___; '
                      "they'll understand ___ and leave knowing how to ___." + '"')

    # 3 — research/evidence/angle
    research = object_at(plan, "evidence_and_angle", "plan")
    string_at(research, "fresh_explanation", "evidence_and_angle")
    string_at(research, "relevant_limit", "evidence_and_angle")
    ids = set()
    for i, evidence in enumerate(list_at(research, "evidence", "evidence_and_angle")):
        where = f"evidence_and_angle.evidence[{i}]"
        if not isinstance(evidence, dict):
            errors.append(f"{where} must be an object")
            continue
        eid = string_at(evidence, "id", where)
        if eid in ids:
            errors.append(f"{where}.id is duplicated")
        if eid:
            ids.add(eid)
        string_at(evidence, "locator", where)
        string_at(evidence, "what_it_supports", where)
        if evidence.get("reviewed") is not True:
            errors.append(f"{where}.reviewed must be true for a read, checked source")
    interest = list_at(research, "what_people_find_interesting",
                       "evidence_and_angle", min_count=2)

    def evidence_links(value, where):
        refs = list_at(value, "evidence_ids", where)
        for ref in refs:
            if not isinstance(ref, str) or ref not in ids:
                errors.append(f"{where}.evidence_ids has an unknown reference: {ref!r}")

    for i, item in enumerate(interest):
        where = f"evidence_and_angle.what_people_find_interesting[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        for k in ("detail", "why_this_viewer_cares"):
            string_at(item, k, where)
        evidence_links(item, where)

    # 4 — first 15–30 seconds: recognition, curiosity AND delivered insight
    opening = object_at(plan, "opening", "plan")
    for k in ("recognizable_problem", "curiosity_question", "early_insight",
              "first_visual", "first_15_to_30_seconds"):
        string_at(opening, k, "opening")
    evidence_links(opening, "opening")
    try:
        insight_at = float(opening.get("first_insight_at_seconds"))
    except (ValueError, TypeError):
        insight_at = -1
    if not 0 <= insight_at <= 30:
        errors.append("opening.first_insight_at_seconds must be between 0 and 30")

    # 5 — learning progression; every chapter must contribute something distinct
    chapters = list_at(plan, "chapters", "plan", min_count=2)
    signatures = set()
    for i, chapter in enumerate(chapters):
        where = f"chapters[{i}]"
        if not isinstance(chapter, dict):
            errors.append(f"{where} must be an object")
            continue
        for k in ("title", "new_question", "new_insight", "distinct_payoff",
                  "daily_life_application_or_knowledge_gain"):
            string_at(chapter, k, where)
        evidence_links(chapter, where)
        signature = re.sub(r"\s+", " ", str(chapter.get("distinct_payoff", "")).strip().casefold())
        if signature in signatures:
            errors.append(f"{where}.distinct_payoff repeats another chapter")
        signatures.add(signature)

    # 6 — visuals must show meaningful changes while retaining one coherent language
    visuals = object_at(plan, "visual_storytelling", "plan")
    for k in ("coherent_style", "continuity_rule"):
        string_at(visuals, k, "visual_storytelling")
    scenes = list_at(visuals, "scenes", "visual_storytelling",
                     min_count=len(chapters) if chapters else 1)
    covered = set()
    for i, scene in enumerate(scenes):
        where = f"visual_storytelling.scenes[{i}]"
        if not isinstance(scene, dict):
            errors.append(f"{where} must be an object")
            continue
        index = scene.get("chapter_index")
        if isinstance(index, bool) or not isinstance(index, int) or index not in range(len(chapters)):
            errors.append(f"{where}.chapter_index must point to an existing chapter (zero-based)")
        else:
            covered.add(index)
        for k in ("visible_action", "why_this_scene_earns_its_place", "meaningful_change"):
            string_at(scene, k, where)
    if chapters and covered != set(range(len(chapters))):
        errors.append("visual_storytelling.scenes must cover every chapter")

    # 7 — spoken language, qualified claims and musical restraint
    sound = object_at(plan, "narration_and_sound", "plan")
    for k in ("natural_phrasing", "deliberate_emphasis",
              "comfortable_transitions", "explain_limits_with_claims"):
        string_at(sound, k, "narration_and_sound")

    runtime = object_at(plan, "runtime_substance", "plan")
    if runtime.get("no_padding") is not True:
        errors.append("runtime_substance.no_padding must be true")
    if runtime.get("insufficient_substance_action") != "stop_and_research_or_rescope":
        errors.append("runtime_substance.insufficient_substance_action must equal stop_and_research_or_rescope")
    for k in ("why_this_length_is_earned", "substance_per_chapter"):
        string_at(runtime, k, "runtime_substance")

    # 8 — 60–90s pilot, with stronger gate after the actual review
    pilot = object_at(plan, "pilot", "plan")
    target = pilot.get("target_seconds")
    if isinstance(target, bool) or not isinstance(target, (int, float)) or not 60 <= target <= 90:
        errors.append("pilot.target_seconds must be 60–90")
    checks = object_at(pilot, "review_questions", "pilot")
    for check in CHECKS:
        if checks.get(check) is not True:
            errors.append(f"pilot.review_questions.{check} must be true (planned review criteria)")
    if stage == "full-production":
        review = object_at(pilot, "actual_review", "pilot")
        if review.get("status") != "approved":
            errors.append("pilot.actual_review.status must be approved before full production")
        actual = review.get("actual_seconds")
        if isinstance(actual, bool) or not isinstance(actual, (int, float)) or not 60 <= actual <= 90:
            errors.append("pilot.actual_review.actual_seconds must be 60–90")
        for k in ("reviewer", "evidence_path", "one_insight_already_delivered"):
            string_at(review, k, "pilot.actual_review")
        answers = object_at(review, "outsider_test", "pilot.actual_review")
        for key in CHECKS:
            if answers.get(key) is not True:
                errors.append(f"pilot.actual_review.outsider_test.{key} must be true")
    return errors


def result(plan, stage):
    problems = validate(plan, stage=stage)
    return {"gate": "viewer-first", "stage": stage, "status": "PASS" if not problems else "FAIL",
            "errors": problems,
            "notice": ("Structural gate only: researcher and independent critic must "
                       "verify actual sources, artistic quality, pilot playback, and reviewer claims.")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--stage", choices=("pre-script", "full-production"),
                        default="pre-script")
    parser.add_argument("--out", type=Path, help="Optional report JSON; refuses to overwrite")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"gate": "viewer-first", "status": "FAIL",
                          "errors": [f"Cannot load plan: {exc}"]}, indent=2))
        return 2
    report = result(data, args.stage)
    if args.out:
        if args.out.exists() or not args.out.parent.is_dir():
            print("Cannot write report: output exists or parent directory missing", file=sys.stderr)
            return 2
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
