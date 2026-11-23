"""claude-youtube execution scripts: no API key in error output, owner-only token, failing exits, safe cache names.
Works without google-api-python-client (the Google modules are faked); no network."""
import contextlib
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "claude-youtube" / "execution"))
import fetch_channel_data as fcd  # noqa: E402
import fetch_transcript as ft  # noqa: E402
import fetch_video_analytics as fva  # noqa: E402
import search_competitor_videos as scv  # noqa: E402
from utils import quota_tracker as qt  # noqa: E402
from utils import youtube_auth as ya  # noqa: E402

SECRET = "AIzaTEST-not-a-real-key"


def leaky_http_error():
    """An HttpError whose str() carries the request URI with key=..., as googleapiclient's does."""
    e = ya.HttpError.__new__(ya.HttpError)
    e.resp = types.SimpleNamespace(status=403, reason="Forbidden")
    e.content, e.error_details, e.reason = b"{}", "", "API key not valid."
    e.uri = f"https://youtube.googleapis.com/youtube/v3/channels?part=id&key={SECRET}&alt=json"
    e.args = (f"<HttpError 403 when requesting {e.uri}>",)
    return e


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def run_main(self, module, argv):
        out = io.StringIO()
        with patch.object(sys, "argv", ["prog", *argv]), contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(out):
            try:
                module.main()
                code = 0
            except SystemExit as e:
                code = e.code
        return code, out.getvalue()


class ApiKeyNeverPrinted(Base):
    def test_fetch_channel_data_http_error(self):
        self.assertIn(SECRET, str(leaky_http_error()))  # the hazard being guarded
        svc = MagicMock()
        svc.channels.return_value.list.return_value.execute.side_effect = leaky_http_error()
        with patch.object(fcd, "TMP_DIR", self.tmp), patch.object(fcd, "check_quota", return_value={}), \
                patch.object(fcd, "get_data_api_service", return_value=(svc, None)):
            code, out = self.run_main(fcd, ["UC" + "a" * 22])
        self.assertEqual(code, 1)
        self.assertIn("403", out)
        self.assertNotIn(SECRET, out)

    def test_search_competitor_videos_http_error(self):
        svc = MagicMock()
        svc.search.return_value.list.return_value.execute.side_effect = leaky_http_error()
        with patch.object(scv, "check_quota", return_value={"remaining": 10000}), \
                patch.object(scv, "get_data_api_service", return_value=(svc, None)):
            code, out = self.run_main(scv, ["python tutorial"])
        self.assertEqual(code, 1)
        self.assertNotIn(SECRET, out)

    def test_channel_input_that_is_not_a_plain_name_is_refused(self):
        with patch.object(fcd, "TMP_DIR", self.tmp), patch.object(fcd, "check_quota", return_value={}), \
                patch.object(fcd, "get_data_api_service") as service:
            code, _ = self.run_main(fcd, ["@..\\..\\evil"])
        self.assertEqual(code, 1)
        service.assert_not_called()


class TokenFile(Base):
    def test_token_written_owner_only(self):
        token = self.tmp / "tok.json"
        token.write_text("old", encoding="utf-8")
        os.chmod(token, 0o644)
        creds = types.SimpleNamespace(to_json=lambda: '{"refresh_token": "r"}')
        with patch.object(ya, "TOKEN_PATH", token):
            ya._write_token(creds)
        self.assertEqual(token.read_text(encoding="utf-8"), '{"refresh_token": "r"}')
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(token.stat().st_mode), 0o600)


class Analytics(Base):
    def run_analytics(self, **query):
        token = self.tmp / "tok.json"
        token.write_text("{}", encoding="utf-8")
        yt = MagicMock()
        yt.channels.return_value.list.return_value.execute.return_value = {"items": [{"id": "UCx"}]}
        analytics = MagicMock()
        analytics.reports.return_value.query.return_value.execute.configure_mock(**query)
        creds = types.ModuleType("google.oauth2.credentials")
        creds.Credentials = MagicMock()
        discovery = types.ModuleType("googleapiclient.discovery")
        discovery.build = lambda *a, **k: yt
        with patch.dict(sys.modules, {"google.oauth2.credentials": creds, "googleapiclient.discovery": discovery}), \
                patch.object(fva, "get_oauth_service", return_value=(analytics, None)), \
                patch.object(fva, "TOKEN_PATH", token):
            return self.run_main(fva, ["dQw4w9WgXcQ"])

    def test_query_error_exits_nonzero(self):
        code, out = self.run_analytics(side_effect=RuntimeError("quota exceeded"))
        self.assertEqual(code, 1)
        self.assertIn("quota exceeded", out)

    def test_successful_query_exits_zero(self):
        code, out = self.run_analytics(return_value={"columnHeaders": [{"name": "video"}, {"name": "views"}],
                                                     "rows": [["dQw4w9WgXcQ", 3]]})
        self.assertEqual(code, 0, out)
        self.assertNotIn("impressions", fva.DEFAULT_METRICS)


class Transcript(Base):
    def test_ids_and_lang_are_validated(self):
        self.assertEqual(ft.parse_video_id("https://youtu.be/dQw4w9WgXcQ?t=3"), "dQw4w9WgXcQ")
        self.assertIsNone(ft.parse_video_id("../../secrets"))
        with patch.object(ft, "TMP_DIR", self.tmp):
            self.assertEqual(self.run_main(ft, ["../../secrets"])[0], 2)
            self.assertEqual(self.run_main(ft, ["dQw4w9WgXcQ", "--lang", "../x"])[0], 2)
        self.assertEqual(list(self.tmp.iterdir()), [])

    def test_vtt_read_as_utf8(self):
        def fake_run(cmd, **kwargs):
            out = Path(cmd[cmd.index("--output") + 1])
            out.with_name("transcript.en.vtt").write_bytes(
                "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\ncafé 日本\n".encode("utf-8"))
            return subprocess.CompletedProcess(cmd, 0, "", "")
        with patch.object(ft.shutil, "which", return_value="yt-dlp"), patch.object(ft.subprocess, "run", fake_run):
            segments, error = ft.fetch_via_ytdlp("dQw4w9WgXcQ")
        self.assertIsNone(error)
        self.assertEqual(segments[0]["text"], "café 日本")


class Quota(Base):
    def test_failed_write_keeps_previous_quota_file(self):
        with patch.object(qt, "TMP_DIR", self.tmp):
            qt.consume_quota("search.list")
            with patch.object(qt.json, "dump", side_effect=RuntimeError("disk full")), \
                    self.assertRaises(RuntimeError):
                qt.consume_quota("search.list")
            self.assertEqual(qt.check_quota()["consumed"], 100)


if __name__ == "__main__":
    unittest.main()
