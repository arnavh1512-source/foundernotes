"""Default Agent-Reach research gateway tests; no network and no accounts."""
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "research_gateway.py"
spec = importlib.util.spec_from_file_location("research_gateway", MODULE)
gateway = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gateway)


def completed(payload, code=0):
    return subprocess.CompletedProcess(args=["agent-reach"], returncode=code,
                                       stdout=json.dumps(payload), stderr="")


class ResearchGatewayTests(unittest.TestCase):
    def test_web_search_invokes_agent_reach_first(self):
        response = {"ok": True, "channel": "web", "backend": "exa",
                    "items": [{"title": "Paper", "url": "https://example.org/paper",
                               "text": "Verified by direct reading"}]}
        with patch.object(gateway, "_binary", return_value="/fake/agent-reach"), \
             patch.object(gateway.subprocess, "run", return_value=completed(response)) as runner:
            result = gateway.run("search", "animation research", limit=3)
        self.assertTrue(result["ok"])
        self.assertEqual(result["provider"], "agent-reach")
        self.assertEqual(result["backend"], "exa")
        self.assertEqual(runner.call_args.args[0],
                         ["/fake/agent-reach", "web", "search", "animation research", "--limit", "3"])

    def test_youtube_subtitle_not_just_video_metadata(self):
        response = {"ok": True, "channel": "youtube", "backend": "yt-dlp",
                    "items": [{"url": "https://youtu.be/jNQXAC9IVRw", "text": "Spoken words"}]}
        with patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run", return_value=completed(response)) as runner:
            result = gateway.run("transcript", "https://youtu.be/jNQXAC9IVRw")
        self.assertTrue(result["ok"])
        self.assertEqual(runner.call_args.args[0][1:4], ["youtube", "subtitle", "https://youtu.be/jNQXAC9IVRw"])
        self.assertEqual(result["items"][0]["text"], "Spoken words")

    def test_subtitle_requires_spoken_content(self):
        with patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run",
                          return_value=completed({"ok": True, "channel": "youtube",
                                                  "items": [{"url": "https://youtu.be/jNQXAC9IVRw", "text": None}]})):
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertFalse(result["ok"])
        self.assertTrue(result["fallback"]["allowed"])
        self.assertEqual(result["error"]["code"], "NO_TRANSCRIPT")

    def test_missing_install_uses_host_fallback(self):
        with patch.object(gateway, "_binary", return_value=None):
            result = gateway.run("search", "research")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "NOT_INSTALLED")
        self.assertTrue(result["fallback"]["allowed"])

    def test_no_fallback_that_bypasses_access_control(self):
        for code in ("RATE_LIMITED", "PLATFORM_BLOCKED", "NEED_LOGIN", "BUSY", "BAD_INPUT"):
            with self.subTest(code=code), patch.object(gateway, "_binary", return_value="agent-reach"), \
                 patch.object(gateway.subprocess, "run",
                              return_value=completed({"ok": False, "error": {"code": code,
                                                                            "message": "stop"}}, code=1)):
                result = gateway.run("search", "research")
                self.assertFalse(result["fallback"]["allowed"], result)

    def test_do_not_run_private_urls(self):
        for url in ("file:///etc/passwd", "http://localhost/data",
                    "http://127.0.0.1/", "https://192.168.1.4/",
                    "https://user:password@example.org/", "https://example.org:8000/"):
            with self.subTest(url=url), patch.object(gateway, "_execute") as invoke:
                result = gateway.run("read", url)
                self.assertEqual(result["error"]["code"], "BAD_INPUT")
                invoke.assert_not_called()

    def test_bad_or_missing_json_falls_back_honestly(self):
        with patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run",
                          return_value=subprocess.CompletedProcess(args=[], returncode=0,
                                                                    stdout="not json", stderr="")):
            result = gateway.run("search", "research")
        self.assertEqual(result["error"]["code"], "INVALID_RESPONSE")
        self.assertFalse(result["ok"])

    def test_status_lists_only_default_research_channels(self):
        response = {"ok": True, "channels": [
            {"name": "web", "actions": [{"name": "search"}]},
            {"name": "youtube", "actions": [{"name": "subtitle"}]},
            {"name": "reddit", "actions": [{"name": "search"}]},
        ]}
        with patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run", return_value=completed(response)):
            result = gateway.run("status")
        self.assertEqual([item["name"] for item in result["items"]], ["web", "youtube"])

    def test_timeout_falls_back_without_retry(self):
        with patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run", side_effect=subprocess.TimeoutExpired("agent-reach", 5)) as runner:
            result = gateway.run("read", "https://example.org/paper")
        self.assertEqual(result["error"]["code"], "TIMEOUT")
        self.assertEqual(runner.call_count, 1)


if __name__ == "__main__":
    unittest.main()
