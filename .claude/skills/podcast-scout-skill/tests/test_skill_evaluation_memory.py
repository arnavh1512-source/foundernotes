#!/usr/bin/env python3
"""Regression coverage for persistent skill reviews and lesson memory."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "scripts"

def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

reviews = load("evaluate_skills")
memory = load("record_lesson")

class ContinuousEvaluationTests(unittest.TestCase):
    def review(self, video="pilot01", outcome="pass"):
        return {
            "skill_id": "native/chalkboard",
            "video_id": video,
            "outcome": outcome,
            "evidence": {"sample_path": "samples/pilot.mp4", "qa_report_path": "reports/qc.json",
                         "reviewer": "independent-reviewer", "finding": "tested chalk reveal"},
            "ratings": {dimension: 4 for dimension in reviews.DIMENSIONS},
        }

    def test_catalog_has_three_families(self):
        cat = reviews.catalogue()
        self.assertEqual(len([k for k in cat if k.startswith("native/")]), 17)
        self.assertEqual(len([k for k in cat if k.startswith("uploaded/")]), 10)
        self.assertIn("external/earshot", cat)

    def test_unassessed_by_default(self):
        rows = reviews.status({"schema_version": 1, "reviews": []})
        self.assertTrue(rows)
        self.assertTrue(all(row[2] == "UNASSESSED" for row in rows))

    def test_requires_real_evidence_fields(self):
        item = self.review()
        item["evidence"]["sample_path"] = ""
        self.assertTrue(any("sample_path" in e for e in reviews.validate_review(item)))

    def test_does_not_accept_unbounded_score(self):
        item = self.review()
        item["ratings"]["motion"] = float("nan")
        self.assertTrue(any("motion" in e for e in reviews.validate_review(item)))

    def test_each_video_checked_independently(self):
        data = {"schema_version": 1, "reviews": []}
        reviews.record_review(data, self.review(video="pilot01"))
        reviews.record_review(data, self.review(video="pilot02", outcome="fail"))
        self.assertEqual(reviews.gate(data, "pilot01", ["native/chalkboard"]), [])
        self.assertTrue(reviews.gate(data, "pilot02", ["native/chalkboard"]))
        self.assertTrue(reviews.gate(data, "pilot03", ["native/chalkboard"]))

    def test_later_failure_blocks_same_video(self):
        data = {"schema_version": 1, "reviews": []}
        reviews.record_review(data, self.review(video="pilot01"))
        reviews.record_review(data, self.review(video="pilot01", outcome="fail"))
        self.assertTrue(reviews.gate(data, "pilot01", ["native/chalkboard"]))

class LessonMemoryTests(unittest.TestCase):
    def lesson(self, category="mistake"):
        return {
            "type": category, "video_id": "pilot01", "summary": "Audio transient late",
            "evidence": "reports/audio.json", "cause": "SFX aligned to start, not peak",
            "action": "Align peak to contact frame", "verification": "Pilot second pass listened",
        }

    def test_requires_evidence(self):
        item = self.lesson()
        item["evidence"] = ""
        self.assertTrue(any("evidence" in e for e in memory.validate(item)))

    def test_records_mistake_and_recipe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory.record(self.lesson(), root)
            self.assertIn("Align peak", (root / "mistakes_and_pitfalls.md").read_text())
            item = self.lesson("recipe")
            memory.record(item, root)
            self.assertIn("Pilot second pass", (root / "positive_recipes.md").read_text())

    def test_video_pass_requires_approval(self):
        item = self.lesson("video")
        item.update(status="passed", style_fingerprint="chalk continuity")
        self.assertTrue(any("owner_approved" in e for e in memory.validate(item)))
        item["owner_approved"] = True
        self.assertEqual(memory.validate(item), [])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory.record(item, root)
            data = json.loads((root / "production_ledger.json").read_text())
            self.assertEqual(data["videos"][0]["video_id"], "pilot01")
            with self.assertRaises(ValueError):
                memory.record(item, root)

if __name__ == "__main__":
    unittest.main()
