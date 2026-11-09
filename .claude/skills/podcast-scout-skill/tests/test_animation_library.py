"""Offline regression checks for multi-repository animation selection and Lemo routing."""
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILLS = Path(__file__).resolve().parents[2]
SCRIPTS = SKILLS / "podcast-scout-skill" / "scripts"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


catalog = load_module("animation_library", SKILLS / "animation-styles" / "scripts" / "animation_library.py")
lemo = load_module("lemo_backend", SCRIPTS / "lemo_backend.py")


class AnimationLibraryTests(unittest.TestCase):
    def test_all_13_external_sources_and_592_entries_indexed(self):
        sources = catalog.source_registry()
        self.assertEqual(len(sources), 13)
        items = catalog.entries()
        self.assertEqual(len(items), 592)
        self.assertEqual(len({item["id"] for item in items}), len(items))
        counts = {src: len([item for item in items if item["source"] == src])
                  for src in ("native", "lemo-opuscar", "code-animation-prompts",
                              "anidoodle", "huashu-art-motion", "claude-drawing-skill")}
        self.assertEqual(counts, {"native": 17, "lemo-opuscar": 66,
                                  "code-animation-prompts": 341, "anidoodle": 32,
                                  "huashu-art-motion": 53, "claude-drawing-skill": 83})

    def test_search_across_sources_and_file_links(self):
        matches = catalog.search("watercolor", limit=30)
        self.assertTrue(matches)
        self.assertTrue(any(x["source"] == "lemo-opuscar" for x in matches))
        self.assertTrue(any(x["source"] == "anidoodle" for x in matches))
        self.assertTrue(all(x["source_url"] for x in matches if x["source"] != "native"))
        self.assertTrue(catalog.search("水墨", source="code-animation-prompts"))
        self.assertTrue(catalog.search("水墨", source="claude-drawing-skill"))
        self.assertTrue(any(x["source"] == "claude-drawing-skill" for x in catalog.search("watercolor")))

    def test_all_remaining_providers_are_searchable_without_false_styles(self):
        providers = catalog.provider_entries()
        self.assertEqual(len(providers), 8)
        self.assertEqual(len(catalog.entries()), 592)
        self.assertTrue(any(x["id"] == "bang-motion:provider"
                            for x in catalog.search("bang motion")))
        self.assertTrue(any(x["id"] == "manim_skill:provider"
                            for x in catalog.search("manim")))
        self.assertTrue(all(x["status"] == "upstream-skill-not-installed" for x in providers))
        self.assertTrue(all(x["source_url"].startswith("https://github.com/") for x in providers))

    def test_original_skill_and_readme_expose_catalog(self):
        repo = SKILLS.parent.parent
        original = (SKILLS / "animation-styles" / "SKILL.md").read_text(encoding="utf-8")
        readme = (repo / "README.md").read_text(encoding="utf-8")
        studio = (SKILLS / "podcast-scout-skill" / "SKILL.md").read_text(encoding="utf-8")
        for content in (original, readme, studio):
            self.assertIn("592", content)
            self.assertIn("animation-styles", content)
        self.assertIn("scripts/animation_library.py", original)
        self.assertTrue((SKILLS / "animation-styles" / "references" /
                         "community-animation-integration.md").is_file())
        self.assertIn("metadata", readme.lower())

    def test_restricted_metadata_is_not_a_rendering_claim(self):
        prompts = [x for x in catalog.entries() if x["source"] == "code-animation-prompts"]
        self.assertTrue(all(x["status"] == "metadata-only-restricted-sharing" for x in prompts))
        self.assertTrue(any(x["status"].startswith("research") for x in catalog.entries()
                            if x["source"] == "huashu-art-motion"))
        self.assertNotIn("vendor", catalog.source_registry()["code-animation-prompts"]["availability"])


class LemoBackendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.root = base / "lemo"
        self.project = base / "owner-created-scene"
        self.out = base / "scene.mp4"
        for relative in ("core/render", "styles/watercolor"):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "core/render/video.mjs").write_text("upstream node entry")
        (self.root / "core/render/still.mjs").write_text("upstream node entry")
        (self.root / "styles/README.md").write_text("upstream catalog")
        (self.root / "styles/watercolor/STYLE.md").write_text("source style specification")
        self.project.mkdir()
        (self.project / "index.html").write_text("window.READY=true; window.DUR=3; window.render=function(t){}")

    def test_status_checks_external_library(self):
        self.assertIsNone(lemo.validated_library(self.root / "absent"))
        with patch.object(lemo.shutil, "which", side_effect=lambda x: f"/usr/bin/{x}"):
            data = lemo.status(self.root)
        self.assertTrue(data["ok"])
        self.assertTrue(data["installed"])

    def test_styles_are_not_demo_projects(self):
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"):
            result = lemo.execute("render", library=self.root, style="watercolor",
                                  project=self.root / "styles/watercolor", output=self.out)
        self.assertEqual(result["error"], "MISSING_INDEX_HTML")
        (self.root / "styles/watercolor/index.html").write_text("demo")
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"):
            result = lemo.execute("render", library=self.root, style="watercolor",
                                  project=self.root / "styles/watercolor", output=self.out)
        self.assertEqual(result["error"], "UPSTREAM_DEMO_FORBIDDEN")

    def test_unknown_style_and_no_overwrite(self):
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"):
            bad = lemo.execute("render", library=self.root, style="fake",
                               project=self.project, output=self.out)
            self.assertEqual(bad["error"], "UNKNOWN_STYLE")
            self.out.write_bytes(b"existing")
            existing = lemo.execute("render", library=self.root, style="watercolor",
                                    project=self.project, output=self.out)
            self.assertEqual(existing["error"], "OUTPUT_EXISTS")

    def test_real_upstream_command_shape_and_probe_pass(self):
        def fake_run(args, **kwargs):
            self.assertEqual(args[:2], ["node", str(self.root / "core/render/video.mjs")])
            self.assertEqual(args[2], str(self.project))
            self.assertIn("--fps", args)
            self.assertEqual(args[args.index("--fps") + 1], "30")
            self.assertEqual(args[args.index("--size") + 1], "1920x1080")
            self.out.write_bytes(b"video")
            return subprocess.CompletedProcess(args, 0, "", "")
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"), \
             patch.object(lemo.subprocess, "run", side_effect=fake_run), \
             patch.object(lemo, "check_output",
                          return_value=lemo.report("inspect", True, fps=30, width=1920, height=1080)):
            data = lemo.execute("render", library=self.root, style="watercolor",
                                project=self.project, output=self.out, expected_seconds=3)
        self.assertTrue(data["ok"], data)
        self.assertEqual(data["audio"], "none")

    def test_probe_rejects_wrong_rate_and_duration(self):
        def ffprobe_result(payload):
            return subprocess.CompletedProcess(["ffprobe"], 0, json.dumps(payload), "")
        with patch.object(lemo.subprocess, "run", return_value=ffprobe_result({
            "streams": [{"width": 1920, "height": 1080, "r_frame_rate": "24/1", "duration": "3.0"}]
        })):
            data = lemo.check_output(self.out, expected_seconds=3)
        self.assertEqual(data["error"], "WRONG_EXPORT_SPEC")
        with patch.object(lemo.subprocess, "run", return_value=ffprobe_result({
            "streams": [{"width": 1920, "height": 1080, "r_frame_rate": "30/1", "duration": "6.0"}]
        })):
            data = lemo.check_output(self.out, expected_seconds=3)
        self.assertEqual(data["error"], "DURATION_MISMATCH")

    def test_still_calls_upstream_with_requested_seconds(self):
        def fake_run(args, **kwargs):
            self.assertEqual(args[1], str(self.root / "core/render/still.mjs"))
            self.assertIn("1.5", args)
            (self.project / "stills").mkdir(exist_ok=True)
            for seconds in (0, 1.5, 3):
                (self.project / "stills" / f"t_{seconds}.jpg").write_bytes(b"jpeg")
            return subprocess.CompletedProcess(args, 0, "frame rendered", "")
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"), \
             patch.object(lemo.subprocess, "run", side_effect=fake_run):
            result = lemo.execute("still", library=self.root, style="watercolor",
                                  project=self.project, seconds=[0, 1.5, 3])
        self.assertTrue(result["ok"], result)

    def test_still_rejects_success_without_real_frames_and_stale_outputs(self):
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"), \
             patch.object(lemo.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "success", "")):
            no_frames = lemo.execute("still", library=self.root, style="watercolor",
                                     project=self.project, seconds=[0, 1.5])
        self.assertEqual(no_frames["error"], "MISSING_STILL_OUTPUT")
        (self.project / "stills").mkdir()
        (self.project / "stills" / "t_0.jpg").write_bytes(b"old")
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"), \
             patch.object(lemo.subprocess, "run") as invoked:
            stale = lemo.execute("still", library=self.root, style="watercolor",
                                  project=self.project, seconds=[0])
        self.assertEqual(stale["error"], "STILLS_EXIST")
        invoked.assert_not_called()

    def test_no_remote_installer_or_dependency_download(self):
        with patch.object(lemo.shutil, "which", return_value=None), \
             patch.object(lemo.subprocess, "run") as invoked:
            answer = lemo.execute("render", library=self.root, style="watercolor",
                                  project=self.project, output=self.out)
        self.assertEqual(answer["error"], "MISSING_DEPENDENCIES")
        invoked.assert_not_called()


if __name__ == "__main__":
    unittest.main()
