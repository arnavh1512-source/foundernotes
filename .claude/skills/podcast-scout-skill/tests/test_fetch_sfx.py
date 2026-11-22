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


def resolve_to(*addresses):
    return lambda host, *a, **k: [(2, 1, 6, "", (address, 443)) for address in addresses]


class DownloadSafeguards(unittest.TestCase):
    def setUp(self):
        # no real DNS in tests: by default every name resolves to one public address
        dns = patch.object(sfx.socket, "getaddrinfo", side_effect=resolve_to("93.184.215.14"))
        dns.start()
        self.addCleanup(dns.stop)

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

    def test_names_resolving_to_private_addresses_are_blocked(self):
        for addresses in (("10.0.0.5",), ("93.184.215.14", "127.0.0.1"), ("::1",), ("169.254.169.254",)):
            with patch.object(sfx.socket, "getaddrinfo", side_effect=resolve_to(*addresses)):
                self.assertFalse(sfx.safe_url("https://cdn.example.com/a.wav"), addresses)
        with patch.object(sfx.socket, "getaddrinfo", side_effect=OSError("no such host")):
            self.assertFalse(sfx.safe_url("https://cdn.example.com/a.wav"))

    def test_numeric_ip_shorthands_are_blocked(self):
        for host in ("2130706433", "0x7f.0.0.1", "127.1", "0x7f000001", "017700000001"):
            self.assertFalse(sfx.safe_url(f"https://{host}/a.wav"), host)

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
