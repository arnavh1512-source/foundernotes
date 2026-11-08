"""Static integration checks for the licensed writing and creator-growth skills.

These checks confirm repository wiring and reference availability. They do
not validate upstream marketing claims or simulate a full Claude Code session.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / ".claude" / "skills"
STUDIO = SKILLS / "podcast-scout-skill"


class EditorialAndMarketingIntegration(unittest.TestCase):
    def test_top_level_skills_have_readable_frontmatter_and_license(self):
        for name in ("humanizer", "i-have-adhd", "marketing-growth"):
            with self.subTest(skill=name):
                path = SKILLS / name / "SKILL.md"
                self.assertTrue(path.is_file(), path)
                content = path.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("---\n"))
                self.assertIn(f"name: {name}\n", content)
                self.assertTrue((SKILLS / name / "LICENSE").is_file())

    def test_all_five_marketing_guides_present(self):
        base = SKILLS / "marketing-growth" / "references"
        for name in ("video", "social", "content-strategy", "analytics", "product-marketing"):
            with self.subTest(guide=name):
                main = base / name / "SKILL.md"
                self.assertTrue(main.is_file(), main)
                self.assertIn(f"name: {name}\n", main.read_text(encoding="utf-8"))

    def test_all_marketing_guide_relative_references_present(self):
        base = SKILLS / "marketing-growth" / "references"
        for name in ("video", "social", "content-strategy", "analytics", "product-marketing"):
            guide = base / name / "SKILL.md"
            content = guide.read_text(encoding="utf-8")
            import re
            references = re.findall(r"\]\((references/[^)#]+\.md)(?:#[^)]*)?\)", content)
            for relative in references:
                with self.subTest(guide=name, reference=relative):
                    self.assertTrue((guide.parent / relative).is_file(), relative)

    def test_humanizer_is_an_explicit_scriptwriting_pass(self):
        writer = (ROOT / ".claude/agents/studio-scriptwriter.md").read_text(encoding="utf-8")
        charter = (STUDIO / "SKILL.md").read_text(encoding="utf-8")
        for content in (writer, charter):
            self.assertIn("humanizer", content.lower())
            self.assertIn("before", content.lower())
            self.assertIn("narration", content.lower())
        reality = (ROOT / ".claude/agents/studio-reality-checker.md").read_text(encoding="utf-8")
        self.assertIn("Humanizer fact-preservation check", reality)

    def test_creator_marketing_is_not_misrepresented_as_full_library(self):
        wrapper = (SKILLS / "marketing-growth" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("5 upstream marketing skills", wrapper)
        self.assertIn("not all copied", wrapper)
        self.assertIn("Owner", wrapper)

    def test_all_new_skills_registered_for_evaluation(self):
        code = (STUDIO / "scripts" / "evaluate_skills.py").read_text(encoding="utf-8")
        for name in ("humanizer", "i-have-adhd", "marketing-video", "marketing-social",
                     "marketing-content-strategy", "marketing-analytics", "marketing-product-marketing"):
            with self.subTest(skill=name):
                self.assertIn(name, code)


if __name__ == "__main__":
    unittest.main()
