"""Offline regression checks for source and opt-in competitor viewer analysis."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("viewer_value", ROOT / "scripts" / "viewer_value.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)
EXAMPLE = ROOT / "assets" / "viewer-value.example.json"


def sample():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


class ViewerValueTests(unittest.TestCase):
    def test_fictional_fixture_has_valid_structure_not_true_research(self):
        self.assertEqual(v.validate(sample()), [])
        doc = v.markdown(sample())
        for key in ("What people may find interesting", "Why watch",
                    "Learning outcomes and daily-life applications", "Original hook proposals",
                    "Attention and confusion risks", "Script handoff"):
            self.assertIn(key, doc)
        self.assertIn("Fictional", doc)

    def test_competitor_mode_needs_explicit_opt_in(self):
        s = sample()
        s["mode"] = "competitor"
        s["competitor"] = {
            "explicit_request": True, "requested_scope": "the user explicitly requested competitor video comparison",
            "differentiation": "add a different original explanation and a practical example",
            "metric_context": "public performance information unavailable",
            "metrics_status": "unavailable",
            "observations": [{"visible_choice": "an opening question in the accessible fixture",
                              "strength_or_gap": "no application shown",
                              "original_alternative": "show a concrete viewer application",
                              "evidence_ids": ["T1"]}],
        }
        self.assertTrue(any("competitor-requested" in x for x in v.validate(s)))
        self.assertEqual(v.validate(s, competitor_requested=True), [])
        s["competitor"]["metrics_status"] = "observed"
        self.assertTrue(any("metadata" in x for x in v.validate(s, competitor_requested=True)))

    def test_source_mode_never_allows_competitor_data(self):
        s = sample()
        s["competitor"] = {}
        self.assertTrue(any("competitor" in x for x in v.validate(s)))
        s = sample()
        self.assertTrue(any("competitor" in x for x in v.validate(s, competitor_requested=True)))

    def test_requires_real_content_evidence_not_just_title(self):
        s = sample()
        for e in s["evidence"]:
            e["basis"] = "metadata"
        self.assertTrue(any("Substantive media" in x for x in v.validate(s)))

    def test_requires_specific_viewer_interest_and_learning_application(self):
        s = sample()
        s["viewer_interest"] = []
        self.assertTrue(any("viewer_interest" in x for x in v.validate(s)))
        s = sample()
        s["learning_outcomes"][0]["application"]["action"] = ""
        self.assertTrue(any("application.action" in x for x in v.validate(s)))
        s = sample()
        s["hooks"][1]["opening"] = s["hooks"][0]["opening"]
        self.assertTrue(any("repeated hook" in x for x in v.validate(s)))

    def test_rejects_fake_observed_audience_reaction(self):
        s = sample()
        s["viewer_interest"][0]["confidence"] = "observed_public_signal"
        self.assertTrue(any("public-comment" in x for x in v.validate(s)))

    def test_cli_writes_new_markdown_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as td:
            data_file = Path(td) / "source.json"
            out = Path(td) / "report.md"
            data_file.write_text(json.dumps(sample()), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts" / "viewer_value.py"), str(data_file), "--out", str(out)]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("What people may find interesting", out.read_text())
            again = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)

if __name__ == "__main__":
    unittest.main()
