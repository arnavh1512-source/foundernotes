"""Regression checks for narration faults found in the November 2026 review."""
import json, math, shutil, struct, sys, tempfile, unittest, wave
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import narrate


def fake_voicebox(text, profile, speed, output, **kwargs):
    rate = 48000
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(rate)
        wav.writeframes(b"".join(struct.pack("<h", int(6000 * math.sin(2 * math.pi * 240 * i / rate)))
                                 for i in range(int(0.4 * rate))))


class NarrateFixes(unittest.TestCase):
    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg missing")
    def test_cached_fallback_take_is_not_reused_for_the_owner_voice(self):
        with tempfile.TemporaryDirectory() as td:
            script = Path(td) / "script.json"
            script.write_text(json.dumps({"voice": {"engine": "voicebox", "name": "founder-notes", "chain": "none"},
                                          "segments": [{"id": "s01", "text": "One clear idea."}]}), encoding="utf-8")
            args = [str(script), "--out", str(Path(td) / "o"), "--engine", "voicebox"]
            calls = []
            def synth(text, profile, *a, **k):
                calls.append(profile); fake_voicebox(text, profile, *a, **k)
            with patch.object(narrate, "synth_voicebox", side_effect=synth):
                for profile in ("synth-1", "synth-1", "owner-1"):
                    with patch.object(narrate, "voicebox_channel_profile", return_value=profile):
                        narrate.main(args)
            self.assertEqual(calls, ["synth-1", "owner-1"])   # same profile is cached; a new profile re-voices

    def test_voicebox_url_must_be_local(self):
        with patch.dict("os.environ", {"VOICEBOX_URL": "http://voice.example.com:17493"}):
            with self.assertRaises(SystemExit):
                narrate.voicebox_url()
        with patch.dict("os.environ", {"VOICEBOX_URL": "http://localhost:17493/"}):
            self.assertEqual(narrate.voicebox_url(), "http://localhost:17493")

    def test_segment_id_cannot_leave_the_segments_folder(self):
        with tempfile.TemporaryDirectory() as td:
            script = Path(td) / "script.json"
            script.write_text(json.dumps({"segments": [{"id": "../../escape", "text": "Hello there."}]}), encoding="utf-8")
            with self.assertRaises(SystemExit):
                narrate.load_script(script)

    def test_long_cue_without_a_space_does_not_crash(self):
        cues = narrate.build_captions([{"id": "s01", "start": 0.0, "end": 3.0, "display": "x" * 60}])
        self.assertTrue(cues)

    def test_asr_check_that_did_not_run_reports_none(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(sys.modules, {"faster_whisper": None}):
            self.assertIsNone(narrate.asr_check(Path(td), [], "tiny.en"))
            self.assertFalse((Path(td) / "asr.json").exists())


if __name__ == "__main__":
    unittest.main()
