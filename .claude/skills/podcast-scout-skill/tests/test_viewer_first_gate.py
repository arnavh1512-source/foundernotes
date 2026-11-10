"""Offline regression tests for mandatory Viewer-First Production Gate."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("viewer_first_gate", ROOT / "scripts" / "viewer_first_gate.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def sample():
    # Fictitious fixtures only; not factual research or a scored video.
    return {
        "schema_version": 1,
        "viewer_need": {"who": "new students learning to manage study time",
                        "struggling_with": "forgetting which homework to finish first",
                        "daily_life_situation": "seeing three assignments due on the same day",
                        "why_care_now": "a recurring school planning problem"},
        "learning_promise": {"understand": "how task urgency differs from effort",
                             "how_to": "sort their assignments using clear priorities",
                             "specific_outcome": "choose the next task with a reason"},
        "viewer_promise_sentence": (
            "This video is for someone struggling with forgetting which homework to finish first; "
            "they'll understand how task urgency differs from effort and leave knowing how to "
            "sort their assignments using clear priorities."
        ),
        "evidence_and_angle": {
            "fresh_explanation": "explain the mechanism through a tangible, original calendar prop",
            "relevant_limit": "the example does not make a prediction about grades",
            "evidence": [
                {"id": "E1", "locator": "fixture:lesson-1", "what_it_supports": "source claim A", "reviewed": True},
                {"id": "E2", "locator": "fixture:lesson-2", "what_it_supports": "source claim B", "reviewed": True},
            ],
            "what_people_find_interesting": [
                {"detail": "different tasks compete for the same afternoon",
                 "why_this_viewer_cares": "recognition of a common daily choice", "evidence_ids": ["E1"]},
                {"detail": "an easy task can be less urgent than a hard one",
                 "why_this_viewer_cares": "a useful contrast to assumptions", "evidence_ids": ["E2"]},
            ],
        },
        "opening": {"recognizable_problem": "several deadlines appear on one calendar",
                    "curiosity_question": "which assignment should be first?",
                    "early_insight": "urgency and effort are different",
                    "first_visual": "a person compares two physical deadline cards",
                    "first_15_to_30_seconds": "recognition, question, proof, helpful insight",
                    "first_insight_at_seconds": 15, "evidence_ids": ["E1"]},
        "chapters": [
            {"title": "Choose the priority", "new_question": "which due date matters first?",
             "new_insight": "deadlines are separate from task difficulty",
             "distinct_payoff": "reader can separate urgency from ease",
             "daily_life_application_or_knowledge_gain": "sort a study checklist", "evidence_ids": ["E1"]},
            {"title": "Make it doable", "new_question": "how should large tasks start?",
             "new_insight": "break work into checkable steps",
             "distinct_payoff": "reader can turn one goal into smaller tasks",
             "daily_life_application_or_knowledge_gain": "make a short first step", "evidence_ids": ["E2"]},
        ],
        "visual_storytelling": {
            "coherent_style": "simple paper-and-pencil tabletop world",
            "continuity_rule": "the same paper cards stay in the same scene world",
            "scenes": [{"chapter_index": 0, "visible_action": "two cards swap positions",
                        "why_this_scene_earns_its_place": "shows which deadline is earlier",
                        "meaningful_change": "time priority appears"},
                       {"chapter_index": 1, "visible_action": "one task card becomes three steps",
                        "why_this_scene_earns_its_place": "shows a breakdown of work",
                        "meaningful_change": "the viewer sees a practical first step"}],
        },
        "narration_and_sound": {"natural_phrasing": "plain conversational lines",
                                "deliberate_emphasis": "stress the difference between urgency and effort",
                                "comfortable_transitions": "repeat the object, not the lesson",
                                "explain_limits_with_claims": "qualify the study outcome when stated"},
        "runtime_substance": {"no_padding": True,
                              "insufficient_substance_action": "stop_and_research_or_rescope",
                              "why_this_length_is_earned": "separate mechanisms and applications",
                              "substance_per_chapter": "two different mechanisms with unique demonstrations"},
        "pilot": {
            "target_seconds": 75,
            "review_questions": {"outsider_understands_problem": True,
                                 "outsider_wants_answer": True,
                                 "outsider_already_learned_something": True},
            "actual_review": {"status": "pending", "actual_seconds": None, "reviewer": "",
                              "evidence_path": "", "one_insight_already_delivered": "",
                              "outsider_test": {k: False for k in gate.CHECKS}},
        },
    }


class ViewerFirstGateTests(unittest.TestCase):
    def test_pre_script_accepts_complete_structured_plan(self):
        self.assertEqual(gate.validate(sample()), [])

    def test_full_production_requires_real_review_data(self):
        data = sample()
        errors = gate.validate(data, stage="full-production")
        self.assertTrue(any("approved" in issue for issue in errors))
        data["pilot"]["actual_review"].update({
            "status": "approved", "actual_seconds": 79, "reviewer": "pilot reviewer",
            "evidence_path": "local/pilot/qc-report.json",
            "one_insight_already_delivered": "the deadline comparison was understood",
            "outsider_test": {k: True for k in gate.CHECKS},
        })
        self.assertEqual(gate.validate(data, stage="full-production"), [])

    def test_template_does_not_sneak_through(self):
        p = ROOT / "assets" / "viewer-first-plan.template.json"
        template = json.loads(p.read_text(encoding="utf-8"))
        errors = gate.validate(template)
        self.assertTrue(errors)
        self.assertTrue(any("placeholder" in issue for issue in errors))

    def test_lost_viewer_problem_or_promise_fails(self):
        data = sample()
        data["viewer_need"]["daily_life_situation"] = ""
        self.assertTrue(any("daily_life_situation" in x for x in gate.validate(data)))
        data = sample()
        data["viewer_promise_sentence"] = "This is about homework."
        self.assertTrue(any("viewer_promise_sentence" in x for x in gate.validate(data)))

    def test_early_insight_and_factual_interest_are_required(self):
        data = sample()
        data["opening"]["first_insight_at_seconds"] = 48
        data["evidence_and_angle"]["what_people_find_interesting"] = []
        errors = gate.validate(data)
        self.assertTrue(any("first_insight_at_seconds" in x for x in errors))
        self.assertTrue(any("what_people_find_interesting" in x for x in errors))

    def test_duplicate_payoff_and_uncovered_chapter_fail(self):
        data = sample()
        data["chapters"][1]["distinct_payoff"] = data["chapters"][0]["distinct_payoff"]
        data["visual_storytelling"]["scenes"][1]["chapter_index"] = 0
        errors = gate.validate(data)
        self.assertTrue(any("repeats" in x for x in errors))
        self.assertTrue(any("cover every chapter" in x for x in errors))

    def test_unverified_evidence_and_padding_fail(self):
        data = sample()
        data["evidence_and_angle"]["evidence"][0]["reviewed"] = False
        data["runtime_substance"]["no_padding"] = False
        data["opening"]["evidence_ids"] = ["fabricated-id"]
        errors = gate.validate(data)
        self.assertTrue(any(".reviewed" in x for x in errors))
        self.assertTrue(any("no_padding" in x for x in errors))
        self.assertTrue(any("unknown reference" in x for x in errors))

    def test_pilot_below_60_or_above_90_fails(self):
        for seconds in (0, 59, 91, 100):
            data = sample()
            data["pilot"]["target_seconds"] = seconds
            self.assertTrue(any("target_seconds" in x for x in gate.validate(data)))

    def test_real_cli_fails_on_template_and_passes_on_valid_plan(self):
        with tempfile.TemporaryDirectory() as td:
            plan = Path(td) / "plan.json"
            plan.write_text(json.dumps(sample()), encoding="utf-8")
            cmd = [sys.executable, str(ROOT / "scripts" / "viewer_first_gate.py"), str(plan)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "PASS")
            data = sample()
            data["viewer_need"]["who"] = ""
            plan.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
