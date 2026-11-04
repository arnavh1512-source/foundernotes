import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_report.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
FIXTURE = json.loads((ROOT / "tests" / "provisional-report.json").read_text(encoding="utf-8-sig"))
TRANSCRIPT = (ROOT / "tests" / "transcript.txt").read_text(encoding="utf-8-sig")


class ReportChecks(unittest.TestCase):
    def setUp(self):
        self.report = copy.deepcopy(FIXTURE)
        self.topic = self.report["topics"][0]

    def errors(self):
        return "\n".join(validator.validate(self.report, TRANSCRIPT))

    def test_honest_shortfall_is_valid(self):
        self.assertEqual(self.errors(), "")

    def test_score_cannot_be_inflated(self):
        self.topic["score"] = 100
        self.assertIn("weighted", self.errors())

    def test_guessed_quote_rejected(self):
        self.topic["moment"]["quote"] = "This sentence never occurred in the podcast."
        self.assertIn("not found", self.errors())

    def test_invented_timestamps_rejected(self):
        self.topic["moment"]["timestamp"] = "00:20"
        self.assertIn("cannot invent timestamps", self.errors())

    def test_timestamp_must_match_own_cue(self):
        text = "[00:20] We remember by testing ourselves.\n[01:00] Sleep matters."
        self.assertTrue(validator.quote_at_timestamp(text, "Sleep matters.", "01:00"))
        self.assertFalse(validator.quote_at_timestamp(text, "Sleep matters.", "00:20"))

    def test_srt_cue_ends_at_next_segment(self):
        text = "1\n00:00:20,000 --> 00:00:30,000\nTest yourself.\n\n2\n00:01:00,000 --> 00:01:10,000\nSleep matters."
        self.assertTrue(validator.quote_at_timestamp(text, "Test yourself.", "00:00:20.000"))
        self.assertFalse(validator.quote_at_timestamp(text, "Sleep matters.", "00:00:20.000"))

    def test_no_false_strong_recommendation(self):
        self.topic["verdict"] = "strong"
        self.assertIn("Verdict should be", self.errors())

    def test_missing_shortfall_explanation_rejected(self):
        self.report["shortfall_reason"] = None
        self.assertIn("shortfall_reason", self.errors())

    def test_timing_mismatch_rejected(self):
        self.topic["duration_seconds"] += 1
        self.assertIn("timings", self.errors())

    def test_unsupported_citation_rejected(self):
        self.topic["findings"] = [{"claim": "An unverified claim", "kind": "supported-finding", "source_urls": ["https://example.org/paper"]}]
        self.assertIn("inspected sources", self.errors())

    def test_empty_demand_measurement_rejected(self):
        self.topic["youtube_demand"]["status"] = "measured"
        self.assertIn("observations", self.errors())

    def test_no_research_evidence_cap(self):
        self.topic["scores"]["evidence"] = 70
        self.assertIn("cap", self.errors())

    def test_missing_coverage_comparison_caps_originality(self):
        self.topic["scores"]["originality"] = 85
        self.assertIn("Originality", self.errors())

    def test_non_numeric_factor_and_malformed_top_level(self):
        self.topic["scores"]["evidence"] = True
        self.assertIn("integer factors", self.errors())
        self.assertTrue(validator.validate([]))

    def test_duplicate_ids_rejected(self):
        self.report["topics"][1]["id"] = self.topic["id"]
        self.assertIn("unique", self.errors())

    def test_malformed_enums_do_not_crash(self):
        self.report["mode"] = []
        self.topic["research_checks"]["central_claim_status"] = []
        self.topic["confidence"] = {}
        self.topic["youtube_demand"]["status"] = []
        self.assertTrue(self.errors())

    def test_measured_demand_requires_dated_metrics(self):
        self.topic["youtube_demand"] = {"status": "measured", "observations": [{}]}
        self.assertIn("observation", self.errors())

    def test_valid_measured_demand(self):
        self.topic["youtube_demand"] = {"status": "measured", "observations": [{
            "provider": "Test fixture provider", "metric": "keyword searches", "value": 120,
            "unit": "searches", "period": "2026-10", "observed_at": "2026-11-04", "url": None,
        }]}
        self.assertEqual(self.errors(), "")

    def test_quote_can_cross_cues_but_must_start_in_own_cue(self):
        text = "1\n00:00:20,000 --> 00:00:30,000\nWe remember by\n\n2\n00:00:30,000 --> 00:00:40,000\ntesting ourselves.\n"
        self.assertTrue(validator.quote_at_timestamp(text, "We remember by testing ourselves.", "00:00:20.000"))
        self.assertFalse(validator.quote_at_timestamp(text, "testing ourselves.", "00:00:20.000"))
        self.topic["moment"].update(quote="We remember by testing ourselves.", timestamp="00:00:20.000", locator_type="caption-segment")
        report = {**self.report, "topics": [self.topic]}
        self.assertEqual(validator.validate(report, text), [])

    def creative_package(self):
        return {
            "concepts": [{"name": name} for name in ("challenge", "mechanism", "decision")],
            "selected_concept": "challenge",
            "hooks": [{"shots": [{"start_seconds": 0, "end_seconds": 5}, {"start_seconds": 5, "end_seconds": 15}, {"start_seconds": 15, "end_seconds": 30}]} for _ in range(3)],
            "packaging_pairs": [{"title": str(i)} for i in range(3)],
        }

    def test_creative_timing_consistency(self):
        self.topic["creative_package"] = self.creative_package()
        self.assertEqual(self.errors(), "")
        self.topic["creative_package"]["hooks"][0]["shots"][1]["start_seconds"] = 6
        self.assertIn("contiguous", self.errors())

    def test_selected_concept_must_exist(self):
        self.topic["creative_package"] = self.creative_package()
        self.topic["creative_package"]["selected_concept"] = "imaginary"
        self.assertIn("selected_concept", self.errors())


if __name__ == "__main__":
    unittest.main()
