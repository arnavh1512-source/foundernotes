"""run_jobs must not buy the same job twice; the MuAPI client keeps the key off argv and only talks https."""
import io
import os
import subprocess
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "collage-director" / "scripts"))
import muapi_client  # noqa: E402
import provider  # noqa: E402


class FakeProvider:
    def __init__(self, statuses):
        self.statuses = iter(statuses)

    def get_status(self, job_id):
        return {"status": next(self.statuses), "output": "https://example.invalid/out.mp4", "error": "boom"}


class RunJobsTests(unittest.TestCase):
    def run_one(self, statuses):
        submitted = []
        specs = {"shot1": lambda: submitted.append(1) or f"job{len(submitted)}"}
        done = provider.run_jobs(FakeProvider(statuses), specs, poll_s=0, stall_s=0, max_retries=2, deadline_s=30)
        return submitted, done

    def test_slow_job_is_submitted_once(self):
        submitted, done = self.run_one(["pending"] * 5 + ["completed"])
        self.assertEqual(len(submitted), 1)
        self.assertEqual(done["shot1"], "https://example.invalid/out.mp4")

    def test_failed_job_is_retried(self):
        submitted, done = self.run_one(["failed", "completed"])
        self.assertEqual(len(submitted), 2)
        self.assertTrue(done["shot1"])

    def test_refused_status_lookup_is_not_resubmitted(self):
        class Refused:
            def get_status(self, job_id):
                return {"status": "failed", "output": None, "error": "401", "retry": False}
        submitted = []
        specs = {"shot1": lambda: submitted.append(1) or "job1"}
        done = provider.run_jobs(Refused(), specs, poll_s=0, max_retries=2, deadline_s=30)
        self.assertEqual(len(submitted), 1)
        self.assertIsNone(done["shot1"])


def http_error(code):
    return urllib.error.HTTPError("https://api.muapi.ai/x", code, "err", {}, io.BytesIO(b"{}"))


ENV = {"MUAPI_API_KEY": "test-key-not-real"}


class StatusTests(unittest.TestCase):
    def test_auth_error_is_failed_not_pending(self):
        with patch.dict(os.environ, ENV), patch.object(muapi_client.urllib.request, "urlopen",
                                                       side_effect=http_error(401)) as opened, \
                patch.object(muapi_client.time, "sleep"):
            res = provider.MuapiProvider().get_status("job1")
        self.assertEqual(res["status"], "failed")
        self.assertFalse(res["retry"])
        self.assertEqual(opened.call_count, 2)  # one try per endpoint, no blind retries of a 401

    def test_network_error_stays_pending(self):
        with patch.dict(os.environ, ENV), patch.object(muapi_client.urllib.request, "urlopen",
                                                       side_effect=urllib.error.URLError("dns")), \
                patch.object(muapi_client.time, "sleep"):
            self.assertEqual(provider.MuapiProvider().get_status("job1")["status"], "pending")


class ClientTests(unittest.TestCase):
    def test_api_key_is_not_forwarded_on_redirect(self):
        seen = []
        def fake_open(req, timeout=0):
            seen.append(req)
            return io.BytesIO(b'{"ok": true}')
        with patch.dict(os.environ, ENV), patch.object(muapi_client.urllib.request, "urlopen", side_effect=fake_open):
            muapi_client._post("/x", {"a": 1})
        req = seen[0]
        self.assertEqual(req.get_header("X-api-key"), "test-key-not-real")
        self.assertNotIn("X-api-key", req.headers)   # only unredirected headers are dropped on redirect

    def test_missing_key_fails_unless_proxy_flag(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(muapi_client, "_load_env"):
            with self.assertRaisesRegex(muapi_client.MuapiError, "MUAPI_API_KEY"):
                muapi_client._key()
            os.environ["MUAPI_KEY_PROXY"] = "1"
            self.assertEqual(muapi_client._key(), "proxy-injected")

    def test_base_url_must_be_https(self):
        with patch.dict(os.environ, {"MUAPI_BASE_URL": "http://evil.example/api"}):
            with self.assertRaisesRegex(muapi_client.MuapiError, "https"):
                muapi_client._base()

    def test_upload_keeps_key_off_argv_and_quotes_path(self):
        done = subprocess.CompletedProcess([], 0, stdout='{"url": "https://cdn.example/x.jpg"}')
        with patch.dict(os.environ, ENV), patch.object(muapi_client.subprocess, "run", return_value=done) as run:
            url = muapi_client.upload('/tmp/a;type=text/html,b"c.jpg')
        self.assertEqual(url, "https://cdn.example/x.jpg")
        cmd, kwargs = run.call_args.args[0], run.call_args.kwargs
        self.assertFalse(any("test-key-not-real" in part for part in cmd))
        self.assertIn("x-api-key: test-key-not-real", kwargs["input"])
        self.assertIn('file=@"/tmp/a;type=text/html,b\\"c.jpg"', cmd)
        self.assertEqual(cmd[cmd.index("--proto") + 1], "=https")

    def test_download_is_https_only(self):
        with patch.object(muapi_client.subprocess, "run") as run, \
                patch.object(muapi_client.os.path, "exists", return_value=True), \
                patch.object(muapi_client.os.path, "getsize", return_value=10):
            muapi_client.download("-oops", "/tmp/out.mp4")
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[cmd.index("--proto") + 1], "=https")
        self.assertEqual(cmd[cmd.index("--proto-redir") + 1], "=https")
        self.assertEqual(cmd[-2:], ["--", "-oops"])


if __name__ == "__main__":
    unittest.main()
