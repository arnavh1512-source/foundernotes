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
    def test_all_13_external_sources_and_509_entries_indexed(self):
        sources = catalog.source_registry()
        self.assertEqual(len(sources), 13)
        items = catalog.entries()
        self.assertEqual(len(items), 509)
        self.assertEqual(len({item["id"] for item in items}), len(items))
        counts = {src: len([item for item in items if item["source"] == src])
                  for src in ("native", "lemo-opuscar", "code-animation-prompts",
                              "anidoodle", "huashu-art-motion")}
        self.assertEqual(counts, {"native": 17, "lemo-opuscar": 66,
                                  "code-animation-prompts": 341, "anidoodle": 32,
                                  "huashu-art-motion": 53})

    def test_search_across_sources_and_file_links(self):
        matches = catalog.search("watercolor", limit=30)
        self.assertTrue(matches)
        self.assertTrue(any(x["source"] == "lemo-opuscar" for x in matches))
        self.assertTrue(any(x["source"] == "anidoodle" for x in matches))
        self.assertTrue(all(x["source_url"] for x in matches if x["source"] != "native"))
        self.assertTrue(catalog.search("水墨", source="code-animation-prompts"))

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
            return subprocess.CompletedProcess(args, 0, "frame rendered", "")
        with patch.object(lemo.shutil, "which", return_value="/bin/exe"), \
             patch.object(lemo.subprocess, "run", side_effect=fake_run):
            result = lemo.execute("still", library=self.root, style="watercolor",
                                  project=self.project, seconds=[0, 1.5, 3])
        self.assertTrue(result["ok"], result)

    def test_no_remote_installer_or_dependency_download(self):
        with patch.object(lemo.shutil, "which", return_value=None), \
             patch.object(lemo.subprocess, "run") as invoked:
            answer = lemo.execute("render", library=self.root, style="watercolor",
                                  project=self.project, output=self.out)
        self.assertEqual(answer["error"], "MISSING_DEPENDENCIES")
        invoked.assert_not_called()


if __name__ == "__main__":
    unittest.main()
