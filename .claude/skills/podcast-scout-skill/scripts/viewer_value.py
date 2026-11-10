#!/usr/bin/env python3
"""Validate source-video/opt-in competitor viewer-interest reports and render Markdown.

This checks report structure only; the Opus analyst must inspect real media,
and the researcher/critic must verify claims. No browsing or AI analysis occurs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MEDIA = {"video", "video_audio", "video_plus_transcript", "transcript", "partial"}
BASIS = {"video", "frame", "audio", "transcript", "public_comment", "external_verification", "metadata"}


def validate(report, *, competitor_requested=False):
    errors = []

    def need(obj, key, location):
        value = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(value, str) or not value.strip() or re.search(
                r"<[^>\n]+>|\b(TODO|PLACEHOLDER|TBD)\b", value, flags=re.I):
            errors.append(f"{location}.{key}: non-placeholder text required")
            return ""
        return value

    def obj(parent, key, loc):
        value = parent.get(key) if isinstance(parent, dict) else None
        if not isinstance(value, dict):
            errors.append(f"{loc}.{key}: object required")
            return {}
        return value

    def items(parent, key, loc, minimum=1):
        value = parent.get(key) if isinstance(parent, dict) else None
        if not isinstance(value, list) or len(value) < minimum:
            errors.append(f"{loc}.{key}: at least {minimum} item(s) required")
            return []
        return value

    if not isinstance(report, dict):
        return ["report: object required"]
    if report.get("schema_version") != 1 or isinstance(report.get("schema_version"), bool):
        errors.append("schema_version must be 1")
    mode = report.get("mode")
    if mode not in ("source", "competitor"):
        errors.append("mode must be source or competitor")
    if mode == "competitor" and not competitor_requested:
        errors.append("competitor mode requires explicit --competitor-requested opt-in")
    if mode == "source" and (competitor_requested or "competitor" in report):
        errors.append("source mode must not run or contain competitor benchmarking")

    src = obj(report, "source", "report")
    for key in ("title", "locator", "inspected_scope"):
        need(src, key, "source")
    if src.get("access") not in MEDIA:
        errors.append("source.access must identify substantive reviewed video/audio/transcript")
    if src.get("coverage") not in ("complete", "partial"):
        errors.append("source.coverage must be complete or partial")
    if not isinstance(src.get("limitations"), list):
        errors.append("source.limitations must be an array")
    elif src.get("coverage") == "partial" and not src["limitations"]:
        errors.append("source: partial coverage requires a limitation")

    evidence = items(report, "evidence", "report")
    ids = {}
    has_content = False
    for i, e in enumerate(evidence):
        loc = f"evidence[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{loc}: object required")
            continue
        identifier = need(e, "id", loc)
        need(e, "locator", loc)
        need(e, "observation", loc)
        if e.get("basis") not in BASIS:
            errors.append(f"{loc}.basis: invalid source type")
        if e.get("basis") in {"video", "frame", "audio", "transcript"}:
            has_content = True
        if identifier in ids:
            errors.append(f"{loc}.id: duplicate")
        ids[identifier] = e
    if not has_content:
        errors.append("Substantive media or transcript evidence is required; title/metrics are insufficient")

    def refs(item, loc, key="evidence_ids"):
        for identifier in items(item, key, loc):
            if not isinstance(identifier, str) or identifier not in ids:
                errors.append(f"{loc}.{key}: unknown evidence id {identifier!r}")

    audience = obj(report, "audience", "report")
    for k in ("segment", "prior_problem", "why_relevant"):
        need(audience, k, "audience")
    for i, item in enumerate(items(report, "viewer_interest", "report", 2)):
        loc = f"viewer_interest[{i}]"
        for k in ("detail", "interest_mechanism", "why_it_might_interest"):
            need(item, k, loc)
        refs(item, loc)
        if item.get("confidence") not in ("editorial_hypothesis", "observed_public_signal"):
            errors.append(f"{loc}.confidence: must distinguish hypothesis from observed audience signal")
        if item.get("confidence") == "observed_public_signal":
            if not any(isinstance(r, str) and ids.get(r, {}).get("basis") == "public_comment"
                       for r in item.get("evidence_ids", [])):
                errors.append(f"{loc}: observed public interest needs real public-comment evidence")
    why = obj(report, "why_watch", "report")
    for k in ("why_it_matters", "stakes", "why_now", "promised_payoff", "what_is_missed_if_skipped"):
        need(why, k, "why_watch")
    for i, item in enumerate(items(report, "learning_outcomes", "report", 2)):
        loc = f"learning_outcomes[{i}]"
        for k in ("before", "after", "learn", "caveat"):
            need(item, k, loc)
        refs(item, loc)
        action = obj(item, "application", loc)
        for k in ("who", "situation", "action", "what_to_notice", "boundary"):
            need(action, k, loc + ".application")
    hooks = items(report, "hooks", "report", 3)
    openings = set()
    for i, item in enumerate(hooks):
        loc = f"hooks[{i}]"
        for k in ("opening", "curiosity_gap", "payoff", "first_visual", "honesty_risk", "originality_note"):
            need(item, k, loc)
        refs(item, loc, "proof_evidence_ids")
        opening = item.get("opening", "")
        if isinstance(opening, str):
            signature = opening.strip().casefold()
            if signature in openings:
                errors.append(f"{loc}.opening: repeated hook")
            openings.add(signature)
    for i, item in enumerate(items(report, "attention_risks", "report")):
        loc = f"attention_risks[{i}]"
        for k in ("moment", "why_loses_interest", "fix"):
            need(item, k, loc)
        refs(item, loc)
    handoff = obj(report, "script_handoff", "report")
    for k in ("premise", "first_15_seconds", "proof_beat", "useful_end", "difference_from_source"):
        need(handoff, k, "script_handoff")
    best = handoff.get("best_hook_index")
    if isinstance(best, bool) or not isinstance(best, int) or best not in range(len(hooks)):
        errors.append("script_handoff.best_hook_index: must be an existing zero-based hook index")

    if mode == "competitor":
        competitor = obj(report, "competitor", "report")
        if competitor.get("explicit_request") is not True:
            errors.append("competitor.explicit_request: must be true")
        for k in ("requested_scope", "differentiation", "metric_context"):
            need(competitor, k, "competitor")
        if competitor.get("metrics_status") not in ("unavailable", "observed"):
            errors.append("competitor.metrics_status must be unavailable or observed")
        if competitor.get("metrics_status") == "observed" and not any(
                isinstance(e, dict) and e.get("basis") == "metadata" for e in evidence):
            errors.append("Observed competitor metrics must link to retrieved metadata")
        for i, item in enumerate(items(competitor, "observations", "competitor")):
            loc = f"competitor.observations[{i}]"
            for k in ("visible_choice", "strength_or_gap", "original_alternative"):
                need(item, k, loc)
            refs(item, loc)
    return errors


def markdown(report):
    source = report["source"]
    a = report["audience"]
    why = report["why_watch"]
    h = report["script_handoff"]
    lines = [
        "# Viewer Value & Hook Analysis",
        f"**Mode:** {report['mode']} · **Source:** {source['title']}",
        f"**Access:** {source['access']} · **Coverage:** {source['coverage']} · {source['inspected_scope']}",
        "**Limitations:** " + ("; ".join(source["limitations"]) if source["limitations"] else "None reported"),
        "> Curiosity and attention predictions are editorial hypotheses, not measured retention.",
        "## Viewer need",
        f"**Audience:** {a['segment']}",
        f"**Recognizable problem:** {a['prior_problem']}",
        f"**Why they care:** {a['why_relevant']}",
        "## What people may find interesting",
    ]
    for i, item in enumerate(report["viewer_interest"], 1):
        lines += [f"### {i}. {item['detail']}",
                  f"**Trigger:** {item['interest_mechanism']} · **Evidence strength:** {item['confidence']}",
                  f"**Why:** {item['why_it_might_interest']} · **Sources:** {', '.join(item['evidence_ids'])}"]
    lines += ["## Why watch", f"**Importance:** {why['why_it_matters']}",
              f"**Stakes:** {why['stakes']}", f"**Why now:** {why['why_now']}",
              f"**Promise:** {why['promised_payoff']}",
              f"**Missed otherwise:** {why['what_is_missed_if_skipped']}",
              "## Learning outcomes and daily-life applications"]
    for i, item in enumerate(report["learning_outcomes"], 1):
        app = item["application"]
        lines += [f"### {i}. {item['learn']}",
                  f"**Before → after:** {item['before']} → {item['after']}",
                  f"**Everyday use:** {app['who']}, in {app['situation']}: {app['action']}",
                  f"**Notice:** {app['what_to_notice']}",
                  f"**Boundaries:** {app['boundary']} · **Caveat:** {item['caveat']}",
                  f"**Sources:** {', '.join(item['evidence_ids'])}"]
    lines += ["## Original hook proposals"]
    for i, hook in enumerate(report["hooks"]):
        preferred = " (recommended)" if i == h["best_hook_index"] else ""
        lines += [f"### Hook {i+1}{preferred}", f"**Opening:** {hook['opening']}",
                  f"**Curiosity:** {hook['curiosity_gap']}", f"**Payoff:** {hook['payoff']}",
                  f"**First visual:** {hook['first_visual']}", f"**Honesty:** {hook['honesty_risk']}",
                  f"**Originality:** {hook['originality_note']}",
                  f"**Proof:** {', '.join(hook['proof_evidence_ids'])}"]
    lines += ["## Attention and confusion risks"]
    for item in report["attention_risks"]:
        lines.append(f"- **{item['moment']}:** {item['why_loses_interest']} → {item['fix']} (sources: {', '.join(item['evidence_ids'])})")
    lines += ["## Script handoff",
              f"**Premise:** {h['premise']}", f"**First 15s:** {h['first_15_seconds']}",
              f"**Early proof:** {h['proof_beat']}", f"**Final useful payoff:** {h['useful_end']}",
              f"**Original added value:** {h['difference_from_source']}"]
    if report["mode"] == "competitor":
        c = report["competitor"]
        lines += ["## Explicitly requested competitor analysis",
                  f"**Scope:** {c['requested_scope']}",
                  f"**Metrics:** {c['metrics_status']} — {c['metric_context']}",
                  f"**Differentiation:** {c['differentiation']}"]
        for item in c["observations"]:
            lines.append(f"- **Observed:** {item['visible_choice']} · **Gap:** {item['strength_or_gap']} · **Own alternative:** {item['original_alternative']} · Sources: {', '.join(item['evidence_ids'])}")
    lines += ["## Evidence ledger"]
    for e in report["evidence"]:
        lines.append(f"- **{e['id']}** ({e['basis']}) {e['locator']}: {e['observation']}")
    return "\n\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Prepared JSON report")
    parser.add_argument("--competitor-requested", action="store_true",
                        help="Only when the owner explicitly requested competitor benchmarking")
    parser.add_argument("--out", type=Path, help="New Markdown file; refuses overwrite")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, indent=2))
        return 2
    errors = validate(data, competitor_requested=args.competitor_requested)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1
    text = markdown(data)
    if args.out:
        if args.out.exists() or not args.out.parent.is_dir():
            print("Output already exists or parent directory missing", file=sys.stderr)
            return 2
        args.out.write_text(text, encoding="utf-8")
        print(json.dumps({"status": "PASS", "out": str(args.out),
                          "notice": "Structure only; not independent verification of media or audience response."}, indent=2))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
