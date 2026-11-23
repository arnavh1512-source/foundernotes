
import importlib.util
import io
import shutil
import subprocess
import tempfile
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
    def mock_audio_result(self, stderr="", returncode=0, lufs="-14.0"):
        if lufs is not None:
            stderr += f"\n    I:         {lufs} LUFS\n"
        return CompletedProcess(
            args=[],
            returncode=returncode,
            stdout="",
            stderr=stderr,
        )

    def test_unmeasured_loudness_fails(self):
        result = report()

        with patch.object(
            qc.subprocess,
            "run",
            return_value=self.mock_audio_result(lufs=None),
        ):
            qc.audit_audio_gaps_and_lufs("fake.mp4", result)

        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(
            any("could not be measured" in e for e in result["errors"])
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


class DurationValidationTests(unittest.TestCase):
    def test_invalid_durations_fail(self):
        invalid_values = [
            "nan",
            "inf",
            "-inf",
            "0",
            "-10",
        ]

        for value in invalid_values:
            with self.subTest(duration=value):
                metadata = {
                    "format": {
                        "duration": value,
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
                    saved_reports[0]["status"],
                    "FAIL",
                )
                self.assertTrue(
                    any(
                        "Invalid video duration metadata"
                        in error
                        for error in saved_reports[0]["errors"]
                    )
                )


@unittest.skipUnless(
    qc.HAS_NUMPY and shutil.which("ffmpeg"),
    "numpy and ffmpeg are required",
)
class BlankFrameGateTests(unittest.TestCase):
    def gate(self, source):
        with tempfile.TemporaryDirectory() as directory:
            video = str(Path(directory) / "clip.mp4")
            subprocess.run(
                [
                    "ffmpeg", "-v", "error", "-y",
                    "-f", "lavfi", "-i", source,
                    "-t", "4", "-c:v", "mpeg4", video,
                ],
                check=True,
            )
            result = report()
            qc.run_film_gate(video, 4, result)
            return result

    def test_solid_brand_colour_is_blank(self):
        # A solid colour has spread between channels but none in space.
        result = self.gate("color=c=0xF2B134:s=320x180:r=30")

        self.assertTrue(
            any("Blank/Dead Frame" in e for e in result["errors"]),
            result,
        )

    def test_moving_picture_is_not_blank(self):
        result = self.gate("testsrc2=size=320x180:rate=30")

        self.assertFalse(
            any("Blank/Dead Frame" in e for e in result["errors"]),
            result,
        )


@unittest.skipUnless(
    qc.HAS_NUMPY and shutil.which("ffmpeg"),
    "numpy and ffmpeg are required",
)
class MotionGateTests(unittest.TestCase):
    def render(self, directory, inputs, graph, seconds=6):
        video = str(Path(directory) / "clip.mp4")
        command = ["ffmpeg", "-v", "error", "-y"]
        for source in inputs:
            command += ["-f", "lavfi", "-i", source]
        command += ["-filter_complex", graph, "-t", str(seconds),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", video]
        subprocess.run(command, check=True)
        return video

    def gate(self, inputs, graph, seconds=6):
        with tempfile.TemporaryDirectory() as directory:
            result = report()
            qc.run_film_gate(self.render(directory, inputs, graph, seconds), seconds, result)
            return result

    def test_small_figure_moving_on_still_background_passes(self):
        # The channel's core look: a small figure acting on a still set.
        result = self.gate(
            ["color=c=white:s=640x360:r=30", "color=c=black:s=10x60:r=30"],
            "[0][1]overlay=x='200+120*sin(2*PI*t/2)':y=150:eval=frame",
        )
        self.assertFalse(any("Anti-PPT" in e for e in result["errors"]), result)

    def test_still_cards_with_frequent_cuts_fail(self):
        # Hard cuts every second used to satisfy the whole-frame metric.
        card = "{}=size=640x360:rate=30,trim=0:0.04,loop=29:1,setpts=N/30/TB"
        result = self.gate(
            [card.format("testsrc"), card.format("smptebars")],
            "[0]split=3[a][c][e];[1]split=3[b][d][f];"
            "[a][b][c][d][e][f]concat=n=6:v=1",
        )
        self.assertTrue(any("Anti-PPT" in e for e in result["errors"]), result)

    def test_long_hold_is_a_warning_not_a_failure(self):
        result = self.gate(
            ["color=c=white:s=640x360:r=30", "color=c=black:s=10x60:r=30"],
            "[0][1]overlay=x='if(lt(t,1),200+100*t,if(gt(t,5),300+100*(t-5),300))'"
            ":y=150:eval=frame",
        )
        self.assertTrue(any("holds still" in w for w in result["warnings"]), result)
        self.assertFalse(any("holds still" in e for e in result["errors"]), result)


@unittest.skipUnless(
    qc.HAS_NUMPY and shutil.which("ffmpeg"),
    "numpy and ffmpeg are required",
)
class DurationGateTests(unittest.TestCase):
    def run_qc(self, seconds, extra, vertical=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root / "film.mp4"
            size = "180x320" if vertical else "320x180"
            subprocess.run([
                "ffmpeg", "-v", "error", "-y",
                "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30",
                "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000",
                "-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", str(video),
            ], check=True)
            argv = [str(video), "--json", str(root / "qc.json"),
                    "--sheet", str(root / "sheet.jpg"), *extra]
            for index, item in enumerate(argv):
                if item == "TIMINGS":
                    (root / "timings.json").write_text('{"duration": 2.0}', encoding="utf-8")
                    argv[index] = str(root / "timings.json")
            try:
                qc.main(argv)
            except SystemExit:
                pass
            import json
            return json.loads((root / "qc.json").read_text(encoding="utf-8"))

    def test_short_narration_fails_even_when_the_picture_is_long_enough(self):
        result = self.run_qc(4, ["--min-duration", "3", "--timings", "TIMINGS"])
        self.assertTrue(any("narration in timings.json" in e for e in result["errors"]), result)

    def test_report_is_bound_to_the_video(self):
        result = self.run_qc(4, ["--min-duration", "3"])
        self.assertEqual(len(result["video_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
