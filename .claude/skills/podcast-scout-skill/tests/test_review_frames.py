import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/review_frames.py"
spec = importlib.util.spec_from_file_location("review_frames", SCRIPT)
review = importlib.util.module_from_spec(spec)
if SCRIPT.exists():
    spec.loader.exec_module(review)


class ReviewFramesTests(unittest.TestCase):
    def test_rejects_invalid_frame_and_crop_ranges(self):
        self.assertTrue(hasattr(review, "validate"), "review frame extractor is missing")
        for times, crop in [([0, 2], None), ([float("nan")], None), ([-1], None),
                            ([0], [319, 0, 10, 10]), ([0], [0, 0, -10, 10]), ([], None)]:
            with self.assertRaises(ValueError):
                review.validate(times, 2, 320, 180, crop)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_real_decode_crop_and_contact_sheet(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            video = root / "fixture.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=10",
                            "-t", "2", "-c:v", "mpeg4", str(video)], check=True)
            result = review.extract(video, root / "review", [0, .5, 1.5], [80, 40, 100, 80], 200)
            self.assertEqual(len(result["frames"]), 3)
            self.assertTrue((root / "review/strip.jpg").stat().st_size > 1000)
            self.assertTrue((root / "review/review.json").is_file())
            with self.assertRaises(ValueError):
                review.extract(video, root / "review", [0], None, 200)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_input_seek_is_frame_accurate_and_hash_matches(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            video = root / "fixture.mp4"   # keyframes only every 2 s, so a keyframe-only seek would land on 0 s
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=10", "-t", "3",
                            "-c:v", "mpeg4", "-g", "20", str(video)], check=True)
            result = review.extract(video, root / "review", [1.5], None, 200)
            reference = root / "reference.jpg"   # output-side seek: decodes from 0, always exact
            subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-ss", "1.5", "-frames:v", "1",
                            "-vf", "scale=200:-2", "-q:v", "2", str(reference)], check=True)
            self.assertEqual((root / "review/frame-000.jpg").read_bytes(), reference.read_bytes())
            self.assertEqual(result["source_sha256"], hashlib.sha256(video.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
