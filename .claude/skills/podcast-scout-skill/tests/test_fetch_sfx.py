"""Openverse sound downloader regression tests; no network calls."""
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fetch_sfx.py"
spec = importlib.util.spec_from_file_location("fetch_sfx", SCRIPT)
sfx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sfx)


class DownloadSafeguards(unittest.TestCase):
    def test_license_filter_is_strict(self):
        base = {"url": "https://media.example.org/sound.wav"}
        self.assertFalse(sfx.licensed({**base, "license": "by-nc"}, "by"))
        self.assertFalse(sfx.licensed({**base, "license": "by-nd"}, "by"))
        self.assertFalse(sfx.licensed({**base, "license": "by"}, "cc0"))
        self.assertTrue(sfx.licensed({**base, "license": "cc0"}, "cc0"))
        self.assertTrue(sfx.licensed({**base, "license": "by"}, "by"))

    def test_block_private_urls_and_traversal_roles(self):
        for url in ("http://example.com/a.mp3", "https://127.0.0.1/a.wav",
                    "https://localhost/x.wav", "file:///tmp/private.wav",
                    "https://192.168.1.1/audio.mp3"):
            self.assertFalse(sfx.safe_url(url), url)
        self.assertTrue(sfx.safe_url("https://cdn.example.com/audio.wav"))
        with self.assertRaises(ValueError):
            sfx.safe_role("../../outside")
        with self.assertRaises(ValueError):
            sfx.safe_role("paper/slide")

    def test_invalid_content_not_saved(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / "clip.wav"
            with patch.object(sfx, "open_safe", return_value=io.BytesIO(b"<html>wrong content</html>")):
                with self.assertRaisesRegex(ValueError, "signature"):
                    sfx.download_candidate("https://cdn.example.com/x.wav", dst)
            self.assertFalse(dst.exists())
            self.assertEqual(list(Path(temp).glob(".sfx-*")), [])

    def test_truncated_oversized_audio_never_published(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / "clip.wav"
            wave_header = b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 1024
            with patch.object(sfx, "open_safe", return_value=io.BytesIO(wave_header)):
                with self.assertRaisesRegex(ValueError, "maximum"):
                    sfx.download_candidate("https://cdn.example.com/x.wav", dst, max_bytes=128)
            self.assertFalse(dst.exists())

    def test_valid_audio_atomically_published(self):
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / "clip.wav"
            wave_data = b"RIFF" + b"\x00" * 4 + b"WAVE" + b"\x00" * 32
            with patch.object(sfx, "open_safe", return_value=io.BytesIO(wave_data)):
                details = sfx.download_candidate("https://cdn.example.com/x.wav", dst)
            self.assertEqual(dst.read_bytes(), wave_data)
            self.assertEqual(details["bytes"], len(wave_data))
            self.assertEqual(details["detected_format"], "wav")
            self.assertEqual(len(details["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
