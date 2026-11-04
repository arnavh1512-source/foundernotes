"""Check Podcast Scout report consistency. Standard library only; no network calls.

This is not a general JSON Schema validator or a factual truth checker.
"""
import argparse
from datetime import date
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

WEIGHTS = {"audience_value": 25, "curiosity": 20, "evidence": 25,
           "originality": 15, "visual_potential": 15}
FACTUAL_TYPES = ("primary", "authoritative-secondary", "secondary")
STAMP = r"(?:(?:\d{1,3}):)?[0-5]\d:[0-5]\d(?:[.,]\d{1,3})?"
CUE = re.compile(rf"(?m)^\s*\[?({STAMP})\]?(?=\s|$)")


def normalized(text):
    return " ".join(text.split())


def timestamp_seconds(value):
    if not isinstance(value, str) or not re.fullmatch(STAMP, value):
        return None
    parts = value.replace(",", ".").split(":")
    return sum(float(part) * 60 ** index for index, part in enumerate(reversed(parts)))


def caption_segments(transcript):
    cues = list(CUE.finditer(transcript))
    segments = []
    for index, cue in enumerate(cues):
        end = cues[index + 1].start() if index + 1 < len(cues) else len(transcript)
        content = re.sub(rf"^[ \t]*-->[ \t]*{STAMP}[^\n]*", "", transcript[cue.end():end])
        content = re.sub(r"\r?\n\s*\r?\n\d+\s*$", "", content)
        segments.append((timestamp_seconds(cue.group(1)), normalized(content)))
    return segments


def quote_at_timestamp(transcript, quote, timestamp):
    """Allow cross-cue quotes only when they begin inside the specified cue."""
    segments = caption_segments(transcript)
    expected = timestamp_seconds(timestamp)
    for index, (seconds, content) in enumerate(segments):
        if seconds == expected:
            position = " ".join(text for _, text in segments[index:]).find(normalized(quote))
            if 0 <= position < len(content):
                return True
    return False


def http_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and parsed.username is None and parsed.password is None
    except ValueError:
        return False


def validate(report, transcript=None):
    """Return errors for checkable invariants, without claiming sources were read."""
    errors = []
    if not isinstance(report, dict) or report.get("schema_version") != "1.0":
        return ["Expected a report object with schema_version 1.0."]
    mode = report.get("mode")
    if mode not in ("researched", "provisional", "blocked"):
        errors.append("Invalid report mode.")
    topics = report.get("topics")
    if not isinstance(topics, list) or any(not isinstance(t, dict) for t in topics):
        return errors + ["topics must be an array of objects."]
    if mode == "blocked" and topics:
        errors.append("A blocked report cannot contain podcast-derived recommendations.")
    podcast = report.get("podcast", {})
    if not isinstance(podcast, dict):
        return errors + ["podcast must be an object."]
    if podcast.get("coverage") not in ("complete", "unknown", "partial", "unavailable"):
        errors.append("Invalid podcast coverage.")
    if podcast.get("coverage") in ("unknown", "partial", "unavailable") and not podcast.get("coverage_note"):
        errors.append("Limited or unknown coverage needs coverage_note.")
    if podcast.get("coverage") == "unavailable" and mode != "blocked":
        errors.append("Unavailable conversation content requires blocked mode.")
    if sum(t.get("verdict") == "strong" for t in topics) < 5 and not report.get("shortfall_reason"):
        errors.append("Fewer than five strong topics requires shortfall_reason.")
    ids = [t.get("id") for t in topics]
    if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(str(i) for i in ids)) != len(ids):
        errors.append("Topic IDs must be nonempty and unique.")
    for index, topic in enumerate(topics, 1):
        prefix = f"Topic {index}: "
        def fail(message):
            errors.append(prefix + message)
        scores = topic.get("scores")
        if not isinstance(scores, dict) or set(scores) != set(WEIGHTS) or any(type(v) is not int or not 0 <= v <= 100 for v in scores.values()):
            fail("scores must contain the five integer factors, each from 0 to 100.")
            continue
        expected = (sum(scores[key] * weight for key, weight in WEIGHTS.items()) + 50) // 100
        if type(topic.get("score")) is not int or topic["score"] != expected:
            fail(f"score must be {expected} (weighted, halves rounded up).")
        sources = topic.get("sources", [])
        if not isinstance(sources, list) or any(not isinstance(s, dict) for s in sources):
            fail("sources must be an array of objects.")
            sources = []
        if any(not http_url(s.get("url")) for s in sources):
            fail("Every source needs a valid HTTP(S) URL.")
        factual = {s.get("url") for s in sources if s.get("access") == "read" and s.get("type") in FACTUAL_TYPES and http_url(s.get("url"))}
        read_urls = {s.get("url") for s in sources if s.get("access") == "read" and http_url(s.get("url"))}
        checks = topic.get("research_checks", {})
        if not isinstance(checks, dict):
            checks = {}
        central = checks.get("central_claim_status")
        if central not in ("supported", "mixed", "contradicted", "unverified") or type(checks.get("coverage_compared")) is not bool:
            fail("research_checks needs central_claim_status and boolean coverage_compared.")
        confidence, verdict = topic.get("confidence"), topic.get("verdict")
        if confidence not in ("low", "medium", "high"):
            fail("Invalid evidence confidence.")
        if not factual and scores["evidence"] > (35 if not sources or mode == "provisional" else 40):
            fail("Evidence score exceeds the cap for no read factual sources.")
        if not factual and confidence != "low":
            fail("No read factual sources requires low confidence.")
        exception = checks.get("one_source_exception")
        if len(factual) == 1 and scores["evidence"] > 65 and not (isinstance(exception, str) and exception.strip() and any(s.get("type") == "primary" and s.get("access") == "read" for s in sources)):
            fail("One-source evidence above 65 needs a documented narrow primary-specification exception.")
        if not checks.get("coverage_compared") and scores["originality"] > 60:
            fail("Originality above 60 requires comparison of existing coverage.")
        strong = expected >= 75 and scores["evidence"] >= 70 and len(factual) >= 2 and central == "supported"
        promising = expected >= 60 and scores["evidence"] >= 45 and central == "supported"
        expected_verdict = "strong" if strong else "promising" if promising else "needs-research"
        if verdict != expected_verdict:
            fail(f"Verdict should be {expected_verdict} under the evidence gates.")
        if confidence == "high" and (len(factual) < 2 or central != "supported"):
            fail("High confidence needs two distinct read factual sources and a supported central claim.")
        findings = topic.get("findings", [])
        if not isinstance(findings, list) or any(not isinstance(f, dict) for f in findings):
            fail("findings must be an array of objects.")
            findings = []
        for finding in findings:
            urls = finding.get("source_urls", [])
            if not isinstance(urls, list) or any(not isinstance(u, str) for u in urls):
                fail("Finding source_urls must be an array of strings.")
            elif finding.get("kind") == "supported-finding" and (not urls or not set(urls).issubset(read_urls)):
                fail("Supported findings must point to inspected sources in the source ledger.")
        moment = topic.get("moment", {})
        if not isinstance(moment, dict) or not isinstance(moment.get("quote"), str) or not moment["quote"].strip():
            fail("A nonempty exact source quote is required.")
        else:
            if moment.get("verified") is not True:
                fail("The source moment must be verified before recommendation.")
            timestamp = moment.get("timestamp")
            if timestamp is not None and timestamp_seconds(timestamp) is None:
                fail("Invalid timestamp format.")
            if timestamp is not None and moment.get("locator_type") in ("paragraph", "line"):
                fail("Untimed paragraph/line locators cannot invent timestamps.")
            if transcript is not None:
                segments = caption_segments(transcript)
                transcript_text = " ".join(text for _, text in segments) if segments else normalized(transcript)
                if normalized(moment["quote"]) not in transcript_text:
                    fail("Quoted excerpt was not found in the supplied transcript.")
                if timestamp is not None and not quote_at_timestamp(transcript, moment["quote"], timestamp):
                    fail("Quote is not in the specified transcript cue; verify the locator manually if the format is unsupported.")
        outline = topic.get("outline")
        if not isinstance(outline, list) or not outline or any(not isinstance(s, dict) or type(s.get("seconds")) is not int or s["seconds"] <= 0 for s in outline):
            fail("outline must contain scenes with positive integer seconds.")
        elif type(topic.get("duration_seconds")) is not int or sum(s["seconds"] for s in outline) != topic["duration_seconds"]:
            fail("Scene timings do not sum to duration_seconds.")
        demand = topic.get("youtube_demand", {})
        if not isinstance(demand, dict) or demand.get("status") not in ("measured", "proxy", "unavailable"):
            fail("Invalid YouTube demand status.")
        else:
            observations = demand.get("observations")
            if not isinstance(observations, list):
                fail("Demand observations must be an array.")
            elif demand["status"] == "unavailable" and observations:
                fail("Unavailable demand cannot contain observations.")
            elif demand["status"] != "unavailable" and not observations:
                fail("Measured/proxy demand needs actual dated observations.")
            else:
                for observation in observations:
                    if not isinstance(observation, dict):
                        fail("Each demand observation must be an object.")
                        continue
                    valid = all(isinstance(observation.get(k), str) and observation[k].strip() for k in ("provider", "metric", "observed_at"))
                    try:
                        observed = observation.get("observed_at", "")
                        valid = valid and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", observed)) and bool(date.fromisoformat(observed))
                    except (ValueError, TypeError):
                        valid = False
                    value = observation.get("value")
                    if demand["status"] == "measured":
                        valid = valid and type(value) in (int, float) and math.isfinite(value) and value >= 0
                        valid = valid and all(isinstance(observation.get(k), str) and observation[k].strip() for k in ("unit", "period"))
                    else:
                        valid = valid and ((isinstance(value, str) and bool(value.strip())) or (type(value) in (int, float) and math.isfinite(value))) and http_url(observation.get("url"))
                    if not valid:
                        fail("Demand observation needs provider, metric, valid date and concrete evidence; measured values also need numeric value, unit and period.")
        creative = topic.get("creative_package")
        if creative is not None:
            if not isinstance(creative, dict):
                fail("creative_package must be an object.")
                continue
            concepts, hooks, pairs = (creative.get(k) for k in ("concepts", "hooks", "packaging_pairs"))
            if any(not isinstance(items, list) or len(items) != 3 or any(not isinstance(item, dict) for item in items) for items in (concepts, hooks, pairs)):
                fail("Creative package needs three concepts, hooks, and packaging pairs.")
                continue
            if creative.get("selected_concept") not in [c.get("name") for c in concepts]:
                fail("selected_concept must match a supplied concept name.")
            for hook in hooks:
                shots = hook.get("shots")
                if not isinstance(shots, list) or not shots:
                    fail("Each hook needs a 30-second shot plan.")
                    continue
                previous = 0
                for shot in shots:
                    if not isinstance(shot, dict) or any(type(shot.get(k)) not in (int, float) or not math.isfinite(shot[k]) for k in ("start_seconds", "end_seconds")):
                        fail("Hook shot times must be finite numbers.")
                        break
                    if shot["start_seconds"] != previous or not previous < shot["end_seconds"] <= 30:
                        fail("Hook shots must be contiguous positive intervals from 0 to 30 seconds.")
                    previous = shot["end_seconds"]
                if previous != 30:
                    fail("Hook shot plan must end at 30 seconds.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--transcript", type=Path)
    args = parser.parse_args()
    try:
        def invalid_constant(value):
            raise ValueError(f"Invalid JSON constant: {value}")
        report = json.loads(args.report.read_text(encoding="utf-8-sig"), parse_constant=invalid_constant)
        transcript = args.transcript.read_text(encoding="utf-8-sig") if args.transcript else None
        errors = validate(report, transcript)
    except (OSError, ValueError) as error:
        print(f"Cannot validate report: {error}", file=sys.stderr)
        return 2
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Consistency checks passed. Scientific truth, actual source access, full JSON Schema, and semantic originality require separate review.")
    if transcript is None:
        print("Transcript was not supplied; quote and timestamp provenance were not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
