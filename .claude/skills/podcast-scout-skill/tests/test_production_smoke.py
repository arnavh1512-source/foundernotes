"""A minimal real-media smoke test: assemble, then independently inspect the result."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
HAS_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


@unittest.skipUnless(HAS_FF, "FFmpeg/ffprobe unavailable")
class SyntheticProductionSmoke(unittest.TestCase):
    def test_scene_voice_captions_and_qc(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            clip = folder / "scene.mp4"
            voice = folder / "narration.wav"
            captions = folder / "captions.srt"
            movie = folder / "master.mp4"
            report = folder / "qc.json"
            sheet = folder / "sheet.jpg"
            for args in (
                ["-f", "lavfi", "-i", "testsrc2=size=320x180:rate=30",
                 "-t", "4", "-c:v", "mpeg4", str(clip)],
                ["-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000",
                 "-t", "4", str(voice)],
            ):
                subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)
            captions.write_text("1\n00:00:00,200 --> 00:00:03,500\nA synthetic test caption.\n")
            build = subprocess.run(
                [sys.executable, str(SCRIPTS / "assemble.py"), "--scenes", str(clip),
                 "--narration", str(voice), "--captions", str(captions),
                 "--out", str(movie)], capture_output=True, text=True,
            )
            self.assertEqual(build.returncode, 0, build.stderr[-1200:])
            self.assertTrue(movie.is_file() and movie.stat().st_size > 0)
            check = subprocess.run(
                [sys.executable, str(SCRIPTS / "qc_video.py"), str(movie),
                 "--captions", str(captions), "--min-duration", "0",
                 "--sheet", str(sheet), "--json", str(report)],
                capture_output=True, text=True,
            )
            self.assertEqual(check.returncode, 0, (check.stdout + check.stderr)[-1400:])
            result = json.loads(report.read_text())
            self.assertEqual(result["status"], "PASS", result)
            self.assertTrue(sheet.is_file() and sheet.stat().st_size > 0)


if __name__ == "__main__":
    unittest.main()
