#!/usr/bin/env python3
"""Regression tests for the creative-format preflight (no network/dependencies)."""
import copy
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "creative_router.py"
spec = importlib.util.spec_from_file_location("creative_router", MODULE)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class CreativeRouterTests(unittest.TestCase):
    def setUp(self):
        self.plan = router.example_plan()

    def check_error(self, expected, plan):
        errors = router.validate_plan(plan)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_inventory_includes_all_ten_uploaded_formats(self):
        self.assertEqual(len(router.FORMATS), 10)
        self.assertIn("claymation", router.FORMATS)
        self.assertIn("documentary", router.FORMATS)

    def test_valid_preflight_sample(self):
        self.assertEqual(router.validate_plan(self.plan), [])

    def test_rejects_missing_or_wrong_voice(self):
        del self.plan["narrator"]
        self.check_error("narrator must", self.plan)
        self.plan["narrator"] = {"gender": "female", "voice_id": "x", "approved": True}
        self.check_error("gender must", self.plan)

    def test_rejects_unapproved_voice(self):
        self.plan["narrator"]["approved"] = False
        self.check_error("approved must", self.plan)

    def test_rejects_unknown_format(self):
        self.plan["shots"][0]["format"] = "unknown"
        self.check_error(".format must", self.plan)

    def test_rejects_unhashable_format_gracefully(self):
        self.plan["shots"][0]["format"] = ["claymation"]
        self.check_error(".format must", self.plan)

    def test_rejects_duplicate_ids_and_overlapping_shots(self):
        self.plan["shots"][1]["id"] = "s01"
        self.plan["shots"][1]["start_s"] = 4.0
        self.check_error("duplicate", self.plan)
        self.check_error("overlaps", self.plan)

    def test_rejects_unexplained_gap(self):
        self.plan["shots"][1]["start_s"] = 5.5
        self.check_error("picture gap", self.plan)

    def test_rejects_unverified_documentary_claim(self):
        self.plan["claims"]["C1"]["verified"] = False
        self.check_error("not independently verified", self.plan)
        self.plan["claims"]["C1"]["verified"] = True
        self.plan["shots"][0]["claim_id"] = ""
        self.check_error("documentary requires", self.plan)

    def test_rejects_unverified_asset(self):
        self.plan["shots"][0]["asset_ids"] = ["ref01"]
        self.plan["asset_manifest"]["ref01"] = {"source": "src", "license": "CC0", "rights_verified": False}
        self.check_error("lacks source, license", self.plan)

    def test_rejects_paid_generation_without_approval(self):
        self.plan["shots"][0]["paid"] = True
        self.plan["shots"][0]["estimated_cost"] = 4.0
        self.check_error("cost_approved", self.plan)
        self.plan["shots"][0]["cost_approved"] = True
        self.assertEqual(router.validate_plan(self.plan), [])

    def test_rejects_noncommercial_source(self):
        self.plan["shots"][0]["use_noncommercial_source_code"] = True
        self.check_error("noncommercial source code", self.plan)

    def test_detects_duration_drift(self):
        self.plan["narration_duration_s"] = 12.0
        self.check_error("Picture ends", self.plan)

    def test_nonfinite_time_rejected(self):
        self.plan["shots"][0]["end_s"] = float("inf")
        self.check_error("finite", self.plan)

    def test_input_must_be_object(self):
        self.check_error("JSON object", [])
        self.check_error("non-empty array", {"shots": []})


if __name__ == "__main__":
    unittest.main()
