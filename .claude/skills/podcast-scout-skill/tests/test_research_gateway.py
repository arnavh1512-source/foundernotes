"""Default Agent-Reach research gateway tests; no network and no accounts."""
import importlib.util
import json
import os
import socket
import subprocess
import tempfile
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


def addresses(*ips):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443)) for ip in ips]


class OfflineDns(unittest.TestCase):
    """Every test resolves names through a mock; no real DNS lookups."""
    def setUp(self):
        dns = patch.object(gateway.socket, "getaddrinfo", return_value=addresses("93.184.216.34"))
        self.dns = dns.start()
        self.addCleanup(dns.stop)


class ResearchGatewayTests(OfflineDns):
    def test_numeric_or_privately_resolving_hosts_are_not_public(self):
        for url in ("http://2130706433/", "http://127.1/", "http://0x7f.0.0.1/",
                    "http://0x7f000001/", "http://0177.0.0.1/", "http://[::1]/"):
            with self.subTest(url=url):
                self.assertFalse(gateway._public_url(url))
        self.assertTrue(gateway._public_url("https://example.org/paper"))
        for answer in (addresses("10.0.0.5"), addresses("93.184.216.34", "127.0.0.1"), []):
            self.dns.return_value = answer
            with self.subTest(answer=answer), patch.object(gateway, "_execute") as invoke:
                self.assertEqual(gateway.run("read", "https://rebind.example/")["error"]["code"], "BAD_INPUT")
                invoke.assert_not_called()
        self.dns.side_effect = socket.gaierror("no network")
        self.assertFalse(gateway._public_url("https://example.org/paper"))

    def test_option_like_values_never_reach_agent_reach_as_flags(self):
        with patch.object(gateway, "_execute") as invoke:
            self.assertEqual(gateway.run("search", "--help")["error"]["code"], "BAD_INPUT")
            invoke.assert_not_called()
        payload = {"ok": True, "channel": "youtube", "items": [{"text": "Words", "url": "u"}]}
        with patch.object(gateway, "_ytdlp_binary", return_value=None), \
             patch.object(gateway, "_execute", return_value=(payload, None, None)) as invoke:
            gateway.run("transcript", "-bcdefghijk")
        self.assertEqual(invoke.call_args.args[0][2], "https://www.youtube.com/watch?v=-bcdefghijk")

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
        with patch.object(gateway, "_ytdlp_binary", return_value=None), \
             patch.object(gateway, "_binary", return_value="agent-reach"), \
             patch.object(gateway.subprocess, "run", return_value=completed(response)) as runner:
            result = gateway.run("transcript", "https://youtu.be/jNQXAC9IVRw")
        self.assertTrue(result["ok"])
        self.assertEqual(runner.call_args.args[0][1:4], ["youtube", "subtitle", "https://youtu.be/jNQXAC9IVRw"])
        self.assertEqual(result["items"][0]["text"], "Spoken words")

    def test_subtitle_requires_spoken_content(self):
        with patch.object(gateway, "_ytdlp_binary", return_value=None), \
             patch.object(gateway, "_binary", return_value="agent-reach"), \
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

    def test_missing_transcript_or_malformed_port_fails_without_running_cli(self):
        for operation, value in (("transcript", None), ("read", "https://example.org:bad/a")):
            with self.subTest(operation=operation), patch.object(gateway, "_execute") as invoke:
                result = gateway.run(operation, value)
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



VTT = "WEBVTT\nKind: captions\n\n00:00:00.000 --> 00:00:02.000\n<c>All right</c> so here\n\n00:00:02.000 --> 00:00:04.000\nAll right so here\nwe are\n"


def fake_ytdlp(stdout="", stderr="", code=0, vtt=None):
    def runner(args, **kwargs):
        if vtt is not None:
            out = Path(args[args.index("-o") + 1].replace("%(ext)s", "en.vtt"))
            out.write_text(vtt, encoding="utf-8")
        return subprocess.CompletedProcess(args=args, returncode=code, stdout=stdout, stderr=stderr)
    return runner


class YtDlpFirstTests(OfflineDns):
    def test_transcript_uses_ytdlp_first_and_skips_agent_reach(self):
        with patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
             patch.object(gateway, "_execute") as agent_reach, \
             patch.object(gateway.subprocess, "run", side_effect=fake_ytdlp(vtt=VTT)) as runner:
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertTrue(result["ok"])
        self.assertEqual(result["provider"], "yt-dlp")
        self.assertEqual(result["items"][0]["text"], "All right so here we are")
        args = runner.call_args.args[0]
        self.assertEqual(args[1], "--ignore-config")
        self.assertIn("--skip-download", args)
        self.assertEqual(args[-2:], ["--", "https://www.youtube.com/watch?v=jNQXAC9IVRw"])
        agent_reach.assert_not_called()

    def test_subtitles_kept_even_if_another_language_track_failed(self):
        with patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
             patch.object(gateway.subprocess, "run",
                          side_effect=fake_ytdlp(stderr="ERROR: HTTP Error 429: Too Many Requests",
                                                 code=1, vtt=VTT)):
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertTrue(result["ok"])

    def test_missing_ytdlp_falls_back_to_agent_reach(self):
        payload = {"ok": True, "channel": "youtube", "items": [{"text": "Words", "url": "u"}]}
        with patch.object(gateway, "_ytdlp_binary", return_value=None), \
             patch.object(gateway, "_execute", return_value=(payload, None, None)) as agent_reach:
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertTrue(result["ok"])
        self.assertEqual(result["provider"], "agent-reach")
        self.assertEqual(result["attempts"][0]["code"], "NOT_INSTALLED")
        agent_reach.assert_called_once()

    def test_no_subtitles_falls_back_to_agent_reach(self):
        with patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
             patch.object(gateway.subprocess, "run", side_effect=fake_ytdlp()), \
             patch.object(gateway, "_execute", return_value=(None, "NOT_INSTALLED", "x")) as agent_reach:
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertEqual(result["attempts"][0]["code"], "NO_TRANSCRIPT")
        agent_reach.assert_called_once()

    def test_block_or_rate_limit_stops_without_backup(self):
        for stderr, code in (("ERROR: Sign in to confirm you're not a bot", "PLATFORM_BLOCKED"),
                             ("ERROR: HTTP Error 429: Too Many Requests", "RATE_LIMITED")):
            with self.subTest(code=code), patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
                 patch.object(gateway.subprocess, "run", side_effect=fake_ytdlp(stderr=stderr, code=1)), \
                 patch.object(gateway, "_execute") as agent_reach:
                result = gateway.run("transcript", "jNQXAC9IVRw")
            self.assertEqual(result["error"]["code"], code)
            self.assertFalse(result["fallback"]["allowed"])
            agent_reach.assert_not_called()

    def test_429_digits_in_an_id_are_not_a_rate_limit(self):
        self.assertEqual(gateway._ytdlp_error("ERROR: [youtube] ab429cdefgh: Video unavailable")[0], "NOT_FOUND")
        self.assertEqual(gateway._ytdlp_error("ERROR: unable to parse 4290 bytes")[0], "UPSTREAM_BROKEN")
        self.assertEqual(gateway._ytdlp_error("ERROR: HTTP Error 429: Too Many Requests")[0], "RATE_LIMITED")

    def test_ytdlp_crash_is_reported_as_broken_not_missing_subtitles(self):
        with patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
             patch.object(gateway.subprocess, "run",
                          side_effect=fake_ytdlp(stderr="Traceback\nKeyError: 'formats'", code=1)), \
             patch.object(gateway, "_execute", return_value=(None, "NOT_INSTALLED", "x")) as agent_reach:
            result = gateway.run("transcript", "jNQXAC9IVRw")
        self.assertEqual(result["attempts"][0]["code"], "UPSTREAM_BROKEN")
        self.assertIn("KeyError", result["attempts"][0]["message"])
        agent_reach.assert_called_once()

    def test_studio_venv_binary_is_found_for_this_platform(self):
        with tempfile.TemporaryDirectory() as venv:
            binary = Path(venv) / ("Scripts/yt-dlp.exe" if os.name == "nt" else "bin/yt-dlp")
            binary.parent.mkdir()
            binary.write_text("", encoding="utf-8")
            binary.chmod(0o755)
            with patch.dict(os.environ, {"STUDIO_VENV": venv}), \
                 patch.object(gateway.shutil, "which", return_value=None):
                os.environ.pop("FOUNDERNOTES_YTDLP_BIN", None)
                self.assertEqual(gateway._ytdlp_binary(), str(binary))

    def test_youtube_search_uses_ytdlp(self):
        listing = {"entries": [{"id": "abcdefghijk", "title": "T", "channel": "C"}]}
        with patch.object(gateway, "_ytdlp_binary", return_value="yt-dlp"), \
             patch.object(gateway.subprocess, "run", side_effect=fake_ytdlp(stdout=json.dumps(listing))) as runner, \
             patch.object(gateway, "_execute") as agent_reach:
            result = gateway.run("youtube-search", "compound interest", limit=2)
        self.assertEqual(result["provider"], "yt-dlp")
        self.assertEqual(result["items"][0]["url"], "https://www.youtube.com/watch?v=abcdefghijk")
        self.assertEqual(runner.call_args.args[0][-2:], ["--", "ytsearch2:compound interest"])
        agent_reach.assert_not_called()

    def test_web_search_still_goes_to_agent_reach_only(self):
        with patch.object(gateway, "_ytdlp") as ytdlp, \
             patch.object(gateway, "_execute", return_value=(None, "NOT_INSTALLED", "x")):
            gateway.run("search", "research")
        ytdlp.assert_not_called()


if __name__ == "__main__":
    unittest.main()
