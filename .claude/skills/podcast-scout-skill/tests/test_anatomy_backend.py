"""Offline tests for FounderNotes' optional Anatomy figure preview bridge.

Mocks never spawn real Chrome; success here is NOT proof of an actual render.
"""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "anatomy_backend.py"
spec = importlib.util.spec_from_file_location("anatomy_backend", MODULE_PATH)
anatomy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anatomy)


class AnatomyBackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "upstream"
        self.scene = self.root / "owned" / "index.html"
        self.output = self.root / "owned" / "preview.png"
        self.scene.parent.mkdir()
        self.scene.write_text("<html><body>New local scene</body></html>")
        for path in anatomy.REQUIRED:
            target = self.home / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("// fake upstream fixture", encoding="utf-8")

    def test_missing_install_and_node_check(self):
        self.assertEqual(anatomy.status(self.home / "missing")["error"], "ANATOMY_NOT_INSTALLED")
        with patch.object(anatomy, "node_binary", return_value=None):
            self.assertEqual(anatomy.status(self.home)["error"], "NODE_NOT_FOUND")

    def test_status_separates_node_from_actual_rendering(self):
        proc = subprocess.CompletedProcess(["node", "--version"], 0, "v22.11.0\n", "")
        with patch.object(anatomy, "node_binary", return_value="/usr/bin/node"), \
             patch.object(anatomy.subprocess, "run", return_value=proc):
            result = anatomy.status(self.home)
        self.assertTrue(result["ok"])
        self.assertIn("unverified", result["note"])
        self.assertTrue(anatomy.node_supported("v20.10.0"))
        self.assertFalse(anatomy.node_supported("v20.9.5"))
        self.assertFalse(anatomy.node_supported("v19.0.0"))

    def test_rejects_demo_remote_overwrite_and_invalid_options(self):
        with patch.object(anatomy, "node_binary", return_value="node"):
            self.assertEqual(anatomy.still("https://example.com/machine.html", self.output, home=self.home)["error"], "INVALID_LOCAL_SOURCE")
            demo = self.home / "examples" / "demo.html"
            demo.parent.mkdir()
            demo.write_text("<html></html>")
            self.assertEqual(anatomy.still(demo, self.output, home=self.home)["error"], "UPSTREAM_DEMO_FORBIDDEN")
            self.output.write_bytes(b"existing")
            self.assertEqual(anatomy.still(self.scene, self.output, home=self.home)["error"], "OUTPUT_EXISTS")
            self.output.unlink()
            self.assertEqual(anatomy.still(self.scene, self.output, home=self.home, width=10)["error"], "INVALID_OPTIONS")
            self.assertEqual(anatomy.still(self.scene, self.scene, home=self.home)["error"], "INVALID_OUTPUT")

    def test_uses_supported_upstream_cli_and_requires_real_png(self):
        def fake_capture(command, **kwargs):
            self.assertEqual(command[:2], ["/usr/bin/node", str(self.home / "scripts" / "capture.mjs")])
            self.assertEqual(command[2], str(self.scene))
            self.assertEqual(command[command.index("--width") + 1], "1920")
            self.assertEqual(command[command.index("--height") + 1], "1080")
            self.assertEqual(command[command.index("--out") + 1], str(self.output))
            self.assertEqual(kwargs["timeout"], 120)
            self.assertFalse(kwargs["check"])
            self.output.write_bytes(anatomy.PNG_SIGNATURE + b"preview-bytes")
            return subprocess.CompletedProcess(command, 0, "", "")

        with patch.object(anatomy, "node_binary", return_value="/usr/bin/node"):
            ok = anatomy.still(self.scene, self.output, home=self.home, runner=fake_capture)
        self.assertTrue(ok["ok"], ok)
        self.assertEqual(ok["width"], 1920)
        self.output.unlink()

        with patch.object(anatomy, "node_binary", return_value="/usr/bin/node"):
            bad = anatomy.still(
                self.scene, self.output, home=self.home,
                runner=lambda command, **kwargs: subprocess.CompletedProcess(command, 0, "", "")
            )
        self.assertEqual(bad["error"], "MISSING_OUTPUT")

    def test_rejects_invalid_png_even_on_zero_process_exit(self):
        def fake_capture(command, **kwargs):
            self.output.write_bytes(b"not a PNG")
            return subprocess.CompletedProcess(command, 0, "", "")
        with patch.object(anatomy, "node_binary", return_value="node"):
            result = anatomy.still(self.scene, self.output, home=self.home, runner=fake_capture)
        self.assertEqual(result["error"], "INVALID_PNG")


if __name__ == "__main__":
    unittest.main()
