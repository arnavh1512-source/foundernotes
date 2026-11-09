"""Offline regression tests for the optional raea rendering backend."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import subprocess

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "raea_backend.py"
spec = importlib.util.spec_from_file_location("raea_backend", SCRIPT)
raea = importlib.util.module_from_spec(spec)
spec.loader.exec_module(raea)


class RaeaBackendTests(unittest.TestCase):
    def test_missing_executable_reports_unavailable(self):
        with patch.object(raea.shutil, "which", return_value=None):
            r = raea.status()
        self.assertFalse(r["ok"])
        self.assertEqual(r["error"], "RAEA_NOT_INSTALLED")

    def test_render_requires_source_and_correct_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            missing = root / "missing.tsx"
            self.assertEqual(raea.render(missing, root / "out.mp4")["error"], "BAD_SOURCE")
            source = root / "scene.tsx"
            source.write_text("export {}")
            self.assertEqual(raea.render(source, root / "out.mov")["error"], "BAD_OUTPUT")
            self.assertEqual(raea.render(source, root / "absent" / "out.mp4")["error"], "MISSING_OUTPUT_DIR")
            (root / "out.mp4").write_bytes(b"existing")
            self.assertEqual(raea.render(source, root / "out.mp4")["error"], "OUTPUT_EXISTS")

    def test_render_calls_real_cli_shape_and_defaults_offline(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scene, mp4, manifest = root / "scene.tsx", root / "scene.mp4", root / "manifest.json"
            scene.write_text("export {}")
            def fake_run(args, **kwargs):
                self.assertEqual(args[:2], ["/usr/bin/raea", "render"])
                self.assertIn("--manifest", args)
                self.assertEqual(kwargs["env"]["RAEA_OFFLINE"], "1")
                mp4.write_bytes(b"video")
                return subprocess.CompletedProcess(args, 0, "", "")
            with patch.object(raea.subprocess, "run", side_effect=fake_run):
                result = raea.render(scene, mp4, manifest=manifest, binary="/usr/bin/raea")
            self.assertTrue(result["ok"], result)
            self.assertEqual(result["bytes"], 5)
            self.assertTrue(result["offline"])

    def test_frame_uses_frame_flag_and_png(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scene, image = root / "scene.tsx", root / "frame.png"
            scene.write_text("export {}")
            def fake_run(args, **kwargs):
                self.assertEqual(args[1], "render")
                self.assertEqual(args[-2:], ["--frame", "42"])
                image.write_bytes(b"\x89PNG")
                return subprocess.CompletedProcess(args, 0, "", "")
            with patch.object(raea.subprocess, "run", side_effect=fake_run):
                self.assertTrue(raea.render(scene, image, frame=42, binary="raea")["ok"])
            self.assertEqual(raea.render(scene, root / "bad.png", frame=-2)["error"], "BAD_FRAME")

    def test_failure_on_zero_byte_or_missing_render(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scene, mp4 = root / "scene.tsx", root / "film.mp4"
            scene.write_text("export {}")
            with patch.object(raea.subprocess, "run",
                              return_value=subprocess.CompletedProcess([], 0, "", "")):
                result = raea.render(scene, mp4, binary="raea")
            self.assertEqual(result["error"], "MISSING_RENDER")

    def test_check_requires_existing_video_and_valid_json_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            film, report = root / "video.mp4", root / "check.json"
            film.write_bytes(b"fake video")
            self.assertEqual(raea.check(film, report=report, manifest=root/"missing.json")["error"], "MISSING_MANIFEST")
            def fake_run(args, **kwargs):
                self.assertEqual(args[1:3], ["check", str(film)])
                report.write_text(json.dumps({"checks": [], "findings": []}))
                return subprocess.CompletedProcess(args, 0, "", "")
            with patch.object(raea.subprocess, "run", side_effect=fake_run):
                r = raea.check(film, report=report, binary="raea")
            self.assertTrue(r["ok"], r)

    def test_check_nonzero_exit_does_not_claim_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            film, report = root / "video.mp4", root / "check.json"
            film.write_bytes(b"video")
            with patch.object(raea.subprocess, "run",
                              return_value=subprocess.CompletedProcess([], 1, "", "P0 failure")):
                result = raea.check(film, report=report, binary="raea")
            self.assertEqual(result["error"], "RAEA_CHECK_FAILED")

    def test_no_implicit_install_or_network(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            src, out = root / "scene.tsx", root / "out.mp4"
            src.write_text("export {}")
            def fake_run(args, **kwargs):
                self.assertEqual(kwargs["env"]["RAEA_OFFLINE"], "1")
                self.assertNotIn("install", args)
                out.write_bytes(b"v")
                return subprocess.CompletedProcess(args, 0, "", "")
            with patch.object(raea.subprocess, "run", side_effect=fake_run) as process:
                result = raea.render(src, out, binary="raea")
            self.assertTrue(result["ok"])
            self.assertEqual(process.call_count, 1)

    def test_timeout_rejected_without_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            scene, out = root / "scene.tsx", root / "out.mp4"
            scene.write_text("export {}")
            with patch.object(raea.subprocess, "run") as run:
                result = raea.render(scene, out, timeout=0, binary="raea")
                self.assertEqual(result["error"], "BAD_TIMEOUT")
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
