
import importlib.util
import io
import unittest
from pathlib import Path
from subprocess import CompletedProcess
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


class ContactSheetTests(unittest.TestCase):
    def test_contact_sheet_failure_raises_error(self):
        with patch.object(
            qc.subprocess,
            "run",
            side_effect=OSError("ffmpeg unavailable"),
        ):
            with self.assertRaises(OSError):
                qc.generate_contact_sheet(
                    "fake.mp4",
                    "sheet.jpg",
                    10,
                )

    def test_contact_sheet_nonzero_exit_raises_error(self):
        with patch.object(
            qc.subprocess,
            "run",
            return_value=CompletedProcess(
                args=[],
                returncode=1,
                stderr="encoding failed",
            ),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Contact sheet generation failed",
            ):
                qc.generate_contact_sheet(
                    "fake.mp4",
                    "sheet.jpg",
                    10,
                )


class AudioQCTests(unittest.TestCase):
    def mock_audio_result(self, stderr="", returncode=0):
        return CompletedProcess(
            args=[],
            returncode=returncode,
            stdout="",
            stderr=stderr,
        )

    def test_clean_audio_passes(self):
        result = report()

        with patch.object(
            qc.subprocess,
            "run",
            return_value=self.mock_audio_result(),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["errors"])
        self.assertTrue(
            any("Zero audio dead-air" in c for c in result["checks"])
        )

    def test_normal_silence_gap_warns(self):
        result = report()
        log = (
            "[silencedetect] silence_start: 10.0\n"
            "[silencedetect] silence_end: 11.5 | "
            "silence_duration: 1.5\n"
        )

        with patch.object(
            qc.subprocess,
            "run",
            return_value=self.mock_audio_result(log),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["warnings"])
        self.assertFalse(result["errors"])

    def test_long_silence_gap_fails(self):
        result = report()
        log = (
            "[silencedetect] silence_start: 10.0\n"
            "[silencedetect] silence_end: 13.0 | "
            "silence_duration: 3.0\n"
        )

        with patch.object(
            qc.subprocess,
            "run",
            return_value=self.mock_audio_result(log),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Dead audio air", " ".join(result["errors"]))

    def test_trailing_silence_fails(self):
        result = report()
        log = "[silencedetect] silence_start: 7.0\n"

        with (
            patch.object(
                qc.subprocess,
                "run",
                return_value=self.mock_audio_result(log),
            ),
            patch.object(
                qc,
                "run_ffprobe",
                return_value={"format": {"duration": "10.0"}},
            ),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("Dead audio air", " ".join(result["errors"]))

    def test_trailing_silence_missing_metadata_fails(self):
        result = report()
        log = "[silencedetect] silence_start: 7.0\n"

        with (
            patch.object(
                qc.subprocess,
                "run",
                return_value=self.mock_audio_result(log),
            ),
            patch.object(
                qc,
                "run_ffprobe",
                return_value=None,
            ),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "Cannot determine duration",
            " ".join(result["errors"]),
        )

    def test_ffmpeg_audio_failure_fails(self):
        result = report()

        with patch.object(
            qc.subprocess,
            "run",
            return_value=self.mock_audio_result(
                "decoding failed",
                returncode=1,
            ),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "Audio silence inspection failed",
            " ".join(result["errors"]),
        )


class QCIntegrationTests(unittest.TestCase):
    def test_contact_sheet_failure_marks_report_fail(self):
        metadata = {
            "format": {
                "duration": "600.0",
            },
            "streams": [
                {
                    "codec_type": "video",
                    "width": 1920,
                    "height": 1080,
                    "r_frame_rate": "30/1",
                },
                {
                    "codec_type": "audio",
                    "codec_name": "aac",
                },
            ],
        }

        saved_reports = []

        def capture_report(path, result):
            saved_reports.append({
                "path": path,
                "status": result["status"],
                "errors": list(result["errors"]),
            })

        with (
            patch.object(
                qc.sys,
                "argv",
                [
                    "qc_video.py",
                    "fake.mp4",
                    "--json",
                    "fake-qc.json",
                    "--sheet",
                    "fake-sheet.jpg",
                ],
            ),
            patch.object(
                qc.os.path,
                "isfile",
                return_value=True,
            ),
            patch.object(
                qc,
                "run_ffprobe",
                return_value=metadata,
            ),
            patch.object(
                qc,
                "audit_audio_gaps_and_lufs",
            ),
            patch.object(
                qc,
                "run_film_gate",
            ),
            patch.object(
                qc,
                "generate_contact_sheet",
                side_effect=RuntimeError("encoding failed"),
            ),
            patch.object(
                qc,
                "write_report",
                side_effect=capture_report,
            ),
            patch("builtins.print"),
        ):
            with self.assertRaises(SystemExit) as raised:
                qc.main()

        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(len(saved_reports), 1)
        self.assertEqual(
            saved_reports[0]["path"],
            "fake-qc.json",
        )
        self.assertEqual(
            saved_reports[0]["status"],
            "FAIL",
        )
        self.assertTrue(
            any(
                "Contact sheet generation failed"
                in error
                for error in saved_reports[0]["errors"]
            )
        )
        self.assertTrue(
            any(
                "encoding failed" in error
                for error in saved_reports[0]["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
