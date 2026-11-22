"""Vendored youtube-agent chapters.py runs standalone (no missing ../yt-edit/deadair import)."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "vendor" / "youtube-agent" / "chapters.py"
spec = importlib.util.spec_from_file_location("yt_chapters", SCRIPT)
chapters = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chapters)

TOPICS = ["apples oranges orchard harvest", "engines pistons cylinders fuel", "planets orbits gravity telescopes"]


def srt():
    blocks, n = [], 1
    for t, words in enumerate(TOPICS):
        for k in range(3):
            start = t * 20 + k * 5
            blocks.append(f"{n}\n00:00:{start:02d},000 --> 00:00:{start + 4:02d},500\n<i>{words}</i> part {k}\n")
            n += 1
    return "\n".join(blocks)


class VendorChapters(unittest.TestCase):
    def test_parse_ts_srt_and_vtt(self):
        self.assertEqual(chapters.parse_ts("01:02:03,450"), 3723.45)
        self.assertEqual(chapters.parse_ts("02:03.5"), 123.5)
        with self.assertRaises(ValueError):
            chapters.parse_ts("soon")

    def test_cli_builds_valid_chapters_from_tiny_srt(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "t.srt"
            path.write_text(srt(), encoding="utf-8")
            cues = chapters.load(str(path))
            self.assertEqual(cues[0], (0.0, 4.5, "apples oranges orchard harvest part 0"))
            out = subprocess.run([sys.executable, str(SCRIPT), str(path), "--target", "3", "--json"],
                                 capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(out.returncode, 0, out.stderr)
        result = json.loads(out.stdout)
        self.assertTrue(result["valid"], result)
        self.assertEqual([c["start"] for c in result["chapters"]], [0.0, 20.0, 40.0])


if __name__ == "__main__":
    unittest.main()
