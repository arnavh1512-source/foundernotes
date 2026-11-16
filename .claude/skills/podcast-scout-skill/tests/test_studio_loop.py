"""Behavioral tests: evidence and state transitions, not AI quality claims."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "studio_loop.py"
spec = importlib.util.spec_from_file_location("studio_loop", SCRIPT)
loop = importlib.util.module_from_spec(spec)
if SCRIPT.exists():
    spec.loader.exec_module(loop)


class StudioLoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def start(self, maximum=2):
        return loop.StudioLoop.create(self.root / "episode", "clear-thoughts", maximum)

    def evidence(self, run, name="evidence.txt", body="Observed at 00:01"):
        path = run.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return name

    def ready(self):
        run = self.start()
        self.evidence(run)
        run.reference({"url": "https://www.youtube.com/watch?v=example", "scope": "frames",
                       "retrieval": {"provider": "manual", "reason": "Agent Reach unavailable"},
                       "observations": [{"dimension": "animation", "time_s": 1,
                                         "observation": "Hand grips a notebook", "evidence": ["evidence.txt"]}]})
        run.learn({"pattern": "Attach the prop to the wrist", "reference_index": 0,
                   "application": "Use a local grip transform", "tags": ["motion"]})
        return run

    def rendered(self):
        run = self.ready()
        self.evidence(run, "cut.mp4", "TEST FIXTURE: not real video")
        self.evidence(run, "qc.json", json.dumps({"status": "PASS", "errors": []}))
        run.register_render("cut.mp4", "qc.json", duration=65, producer="artist", mode="pilot")
        return run

    def review(self, run, fail=False):
        return {"render_sha256": run.state["renders"][-1]["sha256"], "reviewer": "critic",
                "method": "human-audiovisual", "model": None,
                "categories": {key: {"status": "fail" if fail and key == "motion" else "pass",
                                      "evidence": ["evidence.txt"], "finding": "Reviewed at 00:01"}
                               for key in loop.CATEGORIES},
                "findings": ([{"id": "F1", "category": "motion", "start_s": 1, "end_s": 2,
                               "issue": "Prop drifts", "fix": "Nest prop under wrist", "evidence": ["evidence.txt"]}]
                             if fail else [])}

    def test_feature_available(self):
        self.assertTrue(hasattr(loop, "StudioLoop"), "production loop is missing")

    def test_sequence_requires_reference_and_knowledge(self):
        run = self.start()
        with self.assertRaises(ValueError):
            run.learn({"pattern": "unsupported"})
        self.assertEqual(run.state["stage"], "references")

    def test_reference_does_not_become_proven_audience_claim(self):
        run = self.ready()
        self.assertEqual(run.state["knowledge"][0]["confidence"], "hypothesis")
        self.assertEqual(run.state["stage"], "production")
        self.assertEqual(loop.StudioLoop(run.root).state, run.state)

    def test_missing_evidence_and_escape_rejected(self):
        run = self.start()
        for name in ("../outside.txt", "missing.txt"):
            with self.assertRaises(ValueError):
                run.artifact(name)

    def test_reference_scope_requires_matching_observation(self):
        run = self.ready()
        report = copy.deepcopy(run.state["references"][0]["analysis"])
        report["observations"][0]["dimension"] = "voice"
        with self.assertRaises(ValueError):
            run.reference(report)

    def test_stale_render_rejected(self):
        run = self.rendered()
        (run.root / "cut.mp4").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed"):
            run.critic(self.review(run))

    def test_same_producer_cannot_self_approve(self):
        run = self.rendered()
        review = self.review(run)
        review["reviewer"] = "artist"
        with self.assertRaises(ValueError):
            run.critic(review)

    def test_text_review_cannot_pass_voice(self):
        run = self.rendered()
        review = self.review(run)
        review["method"] = "transcript-only"
        with self.assertRaises(ValueError):
            run.critic(review)

    def test_pass_still_requires_owner_and_matching_media(self):
        run = self.rendered()
        run.critic(self.review(run))
        self.assertEqual(run.state["stage"], "owner_review")
        with self.assertRaises(ValueError):
            run.approve("", "evidence.txt")
        run.approve("owner", "evidence.txt")
        self.assertEqual(run.state["stage"], "approved")

    def test_revision_must_cover_findings_and_is_bounded(self):
        run = self.rendered()
        run.critic(self.review(run, True))
        with self.assertRaises(ValueError):
            run.revise({"changes": []})
        run.revise({"changes": [{"finding_id": "F1", "action": "Attach prop"}]})
        self.assertEqual(run.state["revision"], 2)
        self.assertEqual(len(run.state["renders"]), 1)
        with self.assertRaises(ValueError):
            run.register_render("cut.mp4", "qc.json", 65, "artist", "pilot")
        self.evidence(run, "cut2.mp4", "different test fixture")
        run.register_render("cut2.mp4", "qc.json", 65, "artist", "pilot")
        run.critic(self.review(run, True))
        self.assertEqual(run.state["stage"], "stopped")

    def test_out_of_range_finding_rejected_without_state_change(self):
        run = self.rendered()
        report = self.review(run, True)
        report["findings"][0]["end_s"] = 100
        before = copy.deepcopy(run.state)
        with self.assertRaises(ValueError):
            run.critic(report)
        self.assertEqual(run.state, before)

    def test_failed_technical_qc_cannot_pass_creative_gate(self):
        run = self.rendered()
        self.evidence(run, "qc.json", json.dumps({"status": "FAIL", "errors": ["blank frames"]}))
        with self.assertRaises(ValueError):
            run.critic(self.review(run))

    def test_packets_include_limits_and_do_not_claim_agent_ran(self):
        run = self.ready()
        packet = run.packet()
        self.assertEqual(packet["stage"], "production")
        self.assertFalse(packet["agent_executed"])
        self.assertIn("Do not claim", packet["rules"])


if __name__ == "__main__":
    unittest.main()
