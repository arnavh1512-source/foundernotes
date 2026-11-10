"""Guard the owner's explanation-first visual storytelling direction.

This checks the documented production contract and agent wiring; it does not
pretend to render scenes or measure a viewer's understanding.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GUIDE = ROOT / ".claude/skills/podcast-scout-skill/references/explanation-first-visual-direction.md"
TEMPLATE = ROOT / ".claude/skills/podcast-scout-skill/assets/visual-treatment-comparison.template.md"

AGENT_PATHS = [
    ".claude/agents/studio-visual-director.md",
    ".claude/agents/studio-animator.md",
    ".claude/agents/studio-reality-checker.md",
]
PRODUCTION_PATHS = [
    "CLAUDE.md",
    "README.md",
    "channel-profile.md",
    ".claude/skills/podcast-scout-skill/SKILL.md",
    ".claude/skills/podcast-scout-skill/assets/production-plan.md",
    ".claude/skills/animation-styles/SKILL.md",
    ".claude/skills/animation-styles/references/workflow.md",
    ".claude/skills/animation-styles/references/checklist.md",
]


class ExplanationFirstDirectionTests(unittest.TestCase):
    def test_guide_prioritizes_meaning_before_visual_style(self):
        text = GUIDE.read_text(encoding="utf-8").lower()
        self.assertIn("choose animation style", text)
        self.assertIn("after", text)
        for topic in (
            "recognize themselves",
            "emotion or social tension",
            "invisible mechanism",
            "research or evidence",
            "important distinction",
            "important insight",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, text)

    def test_psychology_style_is_preference_not_global_requirement(self):
        text = GUIDE.read_text(encoding="utf-8").lower()
        for phrase in (
            "psychology explainers",
            "original illustrated characters",
            "textured backgrounds",
            "restrained colors",
            "reaction",
            "intentional holds",
            "not",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_comparison_requires_identical_real_narration(self):
        guide = GUIDE.read_text(encoding="utf-8").lower()
        template = TEMPLATE.read_text(encoding="utf-8").lower()
        for text in (guide, template):
            self.assertIn("same", text)
            self.assertIn("narration", text)
            self.assertIn("20–40", text)
            self.assertIn("60–90", text)
            self.assertIn("clip", text)
            self.assertIn("captions", text)
        self.assertIn("measured", template)
        self.assertIn("selected", template)
        self.assertIn("not reviewed", template)
        self.assertIn("full-production", template)

    def test_agents_and_production_docs_link_to_the_guide(self):
        for path in AGENT_PATHS + PRODUCTION_PATHS:
            with self.subTest(path=path):
                contents = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("explanation-first-visual-direction.md", contents)

    def test_same_narration_template_is_in_plan_and_director(self):
        for path in (
            ".claude/agents/studio-visual-director.md",
            ".claude/skills/podcast-scout-skill/assets/production-plan.md",
            "README.md",
        ):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("visual-treatment-comparison", text)


if __name__ == "__main__":
    unittest.main()
