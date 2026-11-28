import datetime as dt, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import learn


def data():
    return {"skills": [
        {"id": "a", "prereqs": [], "mastery": 3, "next_review": "2026-12-01"},
        {"id": "b", "prereqs": ["a"], "mastery": 1, "next_review": "2026-11-20"},
        {"id": "c", "prereqs": ["b"], "mastery": 0, "next_review": "2026-11-01"},
        {"id": "d", "prereqs": [], "mastery": 0, "next_review": "2026-11-25"}]}


class Next(unittest.TestCase):
    def test_weakest_due_unlocked(self):
        # c is weakest but locked (b < 2); d (0) beats b (1)
        self.assertEqual(learn.pick_next(data(), dt.date(2026, 11, 28))["id"], "d")

    def test_nothing_due(self):
        self.assertIsNone(learn.pick_next(data(), dt.date(2026, 10, 1)))

    def test_curriculum_parses_and_prereqs_exist(self):
        cur = learn.load()
        ids = {s["id"] for s in cur["skills"]}
        for s in cur["skills"]:
            self.assertTrue(set(s["prereqs"]) <= ids, s["id"])
            self.assertTrue(s["criteria"], s["id"])


class Verdicts(unittest.TestCase):
    crit = ["x", "y"]

    def test_requires_finding_and_fix(self):
        errs = learn.validate_verdicts(self.crit, {"x": {"pass": True, "finding": ""}, "y": {"pass": False, "finding": "0.4s thin"}})
        self.assertEqual(len(errs), 2)

    def test_default_needs_work(self):
        self.assertEqual(learn.attempt_verdict({"verdicts": None}), "NEEDS WORK")
        ok = {"x": {"pass": True, "finding": "f"}}
        self.assertEqual(learn.attempt_verdict({"verdicts": ok, "measured": {"m": {"ok": False}}}), "NEEDS WORK")
        self.assertEqual(learn.attempt_verdict({"verdicts": ok, "measured": {"m": {"ok": None}}}), "PASS")


class Measure(unittest.TestCase):
    def test_compare_tolerance(self):
        m = learn.compare({"local_motion_mean_pct": 8.0, "cuts": 2}, {"local_motion_mean_pct": 5.0, "cuts": 3})
        self.assertFalse(m["local_motion_mean_pct"]["ok"])
        self.assertIsNone(m["cuts"]["ok"])

    def test_sheet_grid(self):
        self.assertEqual(learn.sheet_grid(0, 5.0), (20, 8, 3))
        self.assertEqual(learn.sheet_grid(1.0, 1.1), (1, 8, 1))

    def test_text_attempts(self):
        self.assertTrue(learn.is_text("d/draft.MD")); self.assertFalse(learn.is_text("t.mp4"))

    def test_remeasure_replaces_unjudged_attempt(self):
        d = {"attempts": [{"n": 1, "verdicts": {"x": {}}}, {"n": 2, "verdicts": None}]}
        learn.drop_uncritiqued(d); self.assertEqual(len(d["attempts"]), 1)
        learn.drop_uncritiqued(d); self.assertEqual(len(d["attempts"]), 1)

    def test_levels(self):
        self.assertEqual(learn.new_level(1, "passed", []), 3)
        self.assertEqual(learn.new_level(1, "escalated", [{"timing_ok": True}]), 2)
        self.assertEqual(learn.new_level(4, "escalated", []), 4)


if __name__ == "__main__":
    unittest.main()
