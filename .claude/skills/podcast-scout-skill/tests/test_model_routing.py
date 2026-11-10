"""Enforce available task-based Claude model routing for FounderNotes agents.

Static policy/wiring tests only; actual model access and runtime identity must
be verified on the user's Claude Code host.
"""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
AGENTS = ROOT / ".claude" / "agents"
ROUTING = ROOT / ".claude" / "skills" / "podcast-scout-skill" / "references" / "model-routing.md"

CORE = {
    "studio-researcher": "opus",
    "studio-scriptwriter": "opus",
    "studio-visual-director": "opus",
    "studio-animator": "sonnet",
    "studio-sound-engineer": "sonnet",
    "studio-editor": "sonnet",
    "studio-reality-checker": "opus",
    "studio-packager": "sonnet",
}
HELPERS = {"studio-source-indexer", "studio-qc-log-reader"}


def frontmatter(name):
    source = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
    if not source.startswith("---\n") or "\n---\n" not in source[4:]:
        raise AssertionError(f"{name}: missing YAML frontmatter")
    header = source.split("\n---\n", 1)[0]
    return dict(re.findall(r"^([a-z][a-z_-]*):\s*(.*?)\s*$", header, re.MULTILINE)), source


class ClaudeModelRoutingTests(unittest.TestCase):
    def test_all_eight_core_agents_have_expected_model_and_effort(self):
        for name, expected in CORE.items():
            with self.subTest(agent=name):
                meta, body = frontmatter(name)
                self.assertEqual(meta.get("model"), expected)
                self.assertEqual(meta.get("effort"), "medium")
                self.assertIn("model-routing.md", body)

    def test_viewer_analyst_is_an_opt_in_opus_preproduction_specialist(self):
        meta, body = frontmatter("studio-viewer-analyst")
        self.assertEqual(meta.get("model"), "opus")
        self.assertEqual(meta.get("effort"), "medium")
        self.assertIn("competitor", body.lower())
        self.assertIn("viewer-first-production-rule.md", body)

    def test_helpers_are_haiku_and_have_no_write_or_command_tools(self):
        for name in HELPERS:
            with self.subTest(agent=name):
                meta, body = frontmatter(name)
                self.assertEqual(meta.get("model"), "haiku")
                self.assertEqual(meta.get("effort"), "medium")
                self.assertEqual(meta.get("tools"), "Read, Grep, Glob")
                self.assertIn("read-only", body.lower())
                self.assertIn("model-routing.md", body)

    def test_primary_policy_contains_only_supported_model_families(self):
        content = ROUTING.read_text(encoding="utf-8").lower()
        self.assertIn("opus", content)
        self.assertIn("sonnet", content)
        self.assertIn("haiku", content)
        self.assertNotIn("fable", content)
        self.assertIn("verify", content)

    def test_no_disallowed_model_in_frontmatter(self):
        for name in (*CORE, *HELPERS):
            with self.subTest(agent=name):
                meta, _ = frontmatter(name)
                self.assertIn(meta["model"], ("opus", "sonnet", "haiku"))

    def test_master_docs_refer_to_same_routing_policy(self):
        for path in (
            ROOT / "CLAUDE.md",
            ROOT / "README.md",
            ROOT / ".claude/skills/podcast-scout-skill/SKILL.md",
            ROOT / ".claude/skills/podcast-scout-skill/references/agency-production-system.md",
            ROOT / ".claude/skills/podcast-scout-skill/references/studio-crew.md",
        ):
            with self.subTest(path=path):
                self.assertIn("model-routing.md", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
