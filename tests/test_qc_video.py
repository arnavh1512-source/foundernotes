
import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".claude/skills/podcast-scout-skill/scripts/qc_video.py"
)

spec = importlib.util.spec_from_file_location("qc_video", SCRIPT)
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)


def report():
    return {
        "status": "PASS",
        "checks": [],
        "warnings": [],
        "errors": [],
    }


class FakeProcess:
    def __init__(self, data=b"", returncode=0):
        self.stdout = io.BytesIO(data)
        self.returncode = returncode
        self.killed = False

    def wait(self):
        return self.returncode

    def kill(self):
        self.killed = True
        self.returncode = -9


class FilmGateTests(unittest.TestCase):
    def test_missing_numpy_fails(self):
        result = report()

        with patch.object(qc, "HAS_NUMPY", False):
            qc.run_film_gate("fake.mp4", 10, result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("NumPy", " ".join(result["errors"]))

    def test_ffmpeg_start_failure(self):
        result = report()

        with (
            patch.object(qc, "HAS_NUMPY", True),
            patch.object(
                qc.subprocess,
                "Popen",
                side_effect=OSError("ffmpeg missing"),
            ),
        ):
            qc.run_film_gate("fake.mp4", 10, result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("ffmpeg missing", " ".join(result["errors"]))

    def test_ffmpeg_decode_failure(self):
        result = report()

        with (
            patch.object(qc, "HAS_NUMPY", True),
            patch.object(
                qc.subprocess,
                "Popen",
                return_value=FakeProcess(returncode=1),
            ),
        ):
            qc.run_film_gate("fake.mp4", 10, result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("decoding failed", " ".join(result["errors"]))

    def test_partial_frame_fails(self):
        result = report()

        with (
            patch.object(qc, "HAS_NUMPY", True),
            patch.object(
                qc.subprocess,
                "Popen",
                return_value=FakeProcess(data=b"partial"),
            ),
        ):
            qc.run_film_gate("fake.mp4", 10, result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Incomplete", " ".join(result["errors"]))

    def test_insufficient_frames_fails(self):
        result = report()
        frame_bytes = 160 * 90 * 3

        with (
            patch.object(qc, "HAS_NUMPY", True),
            patch.object(
                qc.subprocess,
                "Popen",
                return_value=FakeProcess(
                    data=b"\x00" * (frame_bytes * 4)
                ),
            ),
        ):
            qc.run_film_gate("fake.mp4", 10, result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Insufficient", " ".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()
