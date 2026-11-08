"""Behavioral regressions for storyboard, scene list and timeline preflight."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lint_scenes.py"
spec = importlib.util.spec_from_file_location("lint_scenes", SCRIPT)
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class SceneLintRegressionTests(unittest.TestCase):
    def test_explicit_timing_column_and_cap(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "storyboard.md"
            p.write_text("| shot_id | start_s | end_s | camera_move | screen_text |\n"
                         "|---|---|---|---|---|\n"
                         "| 1 | 12.0 | 21.5 | static | Example |\n")
            problems, warnings = [], []
            lint.lint_storyboard(p, problems, warnings)
            self.assertTrue(any("9.50s exceeds" in error for error in problems), problems)

    def test_time_span_does_not_parse_prose_number(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "storyboard.md"
            p.write_text("| shot | time | camera | screen_text |\n"
                         "|---|---|---|---|\n"
                         "| 1 | 0.0–3.0 | static | 2026–2027 is the topic |\n")
            errors, warnings = [], []
            lint.lint_storyboard(p, errors, warnings)
            self.assertEqual(errors, [])

    def test_detects_invalid_start_end_and_overlaps(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "storyboard.md"
            p.write_text("| shot | start_s | end_s | camera_move |\n"
                         "|---|---|---|---|\n"
                         "| 1 | 0 | 4 | push |\n"
                         "| 2 | 3.5 | 7 | push |\n"
                         "| 3 | 7 | 7 | push |\n")
            errors, warnings = [], []
            lint.lint_storyboard(p, errors, warnings)
            self.assertTrue(any("overlaps" in e for e in errors), errors)
            self.assertTrue(any("invalid start/end" in e for e in errors), errors)
            self.assertTrue(any("three consecutive" in e for e in errors), errors)

    def test_scene_manifest_quoted_file_and_simple_path(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / "first clip.mp4").write_bytes(b"video")
            (base / "second.mp4").write_bytes(b"video")
            manifest = base / "list.txt"
            manifest.write_text("ffconcat version 1.0\nfile 'first clip.mp4'\nsecond.mp4\n")
            errors = []
            clips = lint.parse_scene_list(manifest, errors)
            self.assertEqual(errors, [])
            self.assertEqual(clips, [base / "first clip.mp4", base / "second.mp4"])

    def test_scene_manifest_rejects_bad_lines(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp) / "list.txt"
            manifest.write_text("file 'unfinished\nsomething unexpected here\n")
            errors = []
            lint.parse_scene_list(manifest, errors)
            self.assertGreaterEqual(len(errors), 2)

    def test_missing_and_invalid_timings_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "timings.json"
            errors, warns = [], []
            self.assertIsNone(lint.lint_timings(p, 480, errors, warns))
            self.assertTrue(errors)
            p.write_text('{"total_duration": "NaN", "segments": []}')
            errors = []
            self.assertIsNone(lint.lint_timings(p, 480, errors, warns))
            self.assertTrue(errors)

    def test_postrender_checks_duration_with_mock(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / "storyboard.md").write_text("| shot | start_s | end_s |\n|---|---|---|\n| 1 | 0 | 3 |\n")
            (base / "timings.json").write_text(json.dumps({"total_duration": 3, "segments": [{"id": "a"}]}))
            (base / "list.txt").write_text("file 'clip.mp4'\n")
            (base / "clip.mp4").write_bytes(b"x")
            original = lint.probe_duration
            lint.probe_duration = lambda path: 1.0
            try:
                code = lint.main(["--storyboard", str(base / "storyboard.md"),
                                  "--timings", str(base / "timings.json"),
                                  "--scenes", str(base / "list.txt"),
                                  "--min-duration", "0", "--require-clips"])
                self.assertEqual(code, 1)
            finally:
                lint.probe_duration = original

    def test_static_hook_check_does_not_claim_runtime_determinism(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "scene.html"
            p.write_text("<script>window.renderAt=t=>{Math.random();}</script>")
            errors, warns = [], []
            lint.lint_html_scene(p, errors, warns)
            self.assertFalse(errors)
            self.assertTrue(any("random" in item for item in warns))


if __name__ == "__main__":
    unittest.main()
