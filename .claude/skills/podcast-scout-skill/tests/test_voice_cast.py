"""Unit and actual audio assembly tests for optional multi-speaker Voicebox casting."""
import importlib.util
import io
import json
import math
import shutil
import tempfile
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "narrate.py"
spec = importlib.util.spec_from_file_location("narrate_cast", SCRIPT)
narrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(narrate)
EXAMPLE = SCRIPT.parent.parent / "assets" / "voice-cast.example.json"


def example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def fake_voicebox(text, profile, speed, output, **kwargs):
    import struct
    rate = 48000
    duration = 0.38
    frequency = 240 if profile == "narrator-id" else 360
    samples = [int(6000 * math.sin(2 * math.pi * frequency * i / rate))
               for i in range(int(duration * rate))]
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(struct.pack("<" + "h" * len(samples), *samples))


class CastPolicy(unittest.TestCase):
    def test_valid_multiple_genders_and_narrator(self):
        data = example()
        self.assertEqual(narrate.validate_voice_cast(data), data["cast"])
        self.assertEqual(len(data["cast"]), 5)

    def test_legacy_single_voice_unaffected(self):
        script = {"voice": {"engine": "kokoro"}, "segments": [{"id": "a", "text": "Hi"}]}
        self.assertIsNone(narrate.validate_voice_cast(script))

    def test_requires_narrator_locked_male(self):
        script = example()
        script["cast"]["narrator"]["gender"] = "female"
        with self.assertRaisesRegex(ValueError, "established male"):
            narrate.validate_voice_cast(script)

    def test_requires_approved_synthetic_voices(self):
        for field, value in (("approved", False), ("synthetic_voice", False)):
            with self.subTest(field=field):
                script = example()
                script["cast"]["investor"][field] = value
                with self.assertRaisesRegex(ValueError, "approved:true and synthetic_voice:true"):
                    narrate.validate_voice_cast(script)

    def test_rejects_undeclared_and_duplicate_profile(self):
        script = example()
        script["segments"][0]["speaker"] = "unknown"
        with self.assertRaisesRegex(ValueError, "undeclared speaker"):
            narrate.validate_voice_cast(script)
        script = example()
        script["cast"]["investor"]["profile_name"] = script["cast"]["analyst"]["profile_name"]
        with self.assertRaisesRegex(ValueError, "assigned to multiple"):
            narrate.validate_voice_cast(script)

    def test_rejects_unsafe_segment_id(self):
        script = example()
        script["segments"][0]["id"] = "../private"
        with self.assertRaisesRegex(ValueError, "safe filename"):
            narrate.validate_voice_cast(script)

    def test_builtin_kokoro_preset_requires_no_samples(self):
        script = example()
        profiles = [{
            "name": entry["profile_name"], "id": f"p-{speaker}", "sample_count": 0,
            "voice_type": "preset", "preset_engine": "kokoro",
            "preset_voice_id": entry["preset_voice_id"]
        } for speaker, entry in script["cast"].items() if speaker != "narrator"]
        with patch.object(narrate, "voicebox_channel_profile", return_value="narrator-id"), \
             patch.object(narrate.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(profiles).encode())):
            result = narrate.resolve_voice_cast(script["cast"])
        self.assertEqual(result["investor"], {"id": "p-investor", "engine": "kokoro",
                                              "voice_type": "preset"})
        self.assertEqual(result["narrator"]["engine"], "chatterbox")

    def test_designed_profile_routes_through_qwen_voice_design(self):
        script = example()
        script["cast"] = {"narrator": script["cast"]["narrator"], "investor": {
            "profile_name": "FN Character Investor F1", "gender": "female",
            "synthetic_voice": True, "approved": True, "voice_type": "designed"
        }}
        profiles = [{"name": "FN Character Investor F1", "id": "designed-id",
                     "sample_count": 0, "voice_type": "designed",
                     "default_engine": "qwen_voice_design",
                     "design_prompt": "Original adult female voice, clear and conversational."}]
        with patch.object(narrate, "voicebox_channel_profile", return_value="narrator-id"), \
             patch.object(narrate.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(profiles).encode())):
            result = narrate.resolve_voice_cast(script["cast"])
        self.assertEqual(result["investor"]["engine"], "qwen_voice_design")

    def test_gender_mismatch_for_known_preset_is_rejected(self):
        script = example()
        script["cast"]["investor"]["gender"] = "male"
        profiles = [{"name": script["cast"]["investor"]["profile_name"],
                     "id": "bad-preset", "voice_type": "preset", "preset_engine": "kokoro",
                     "preset_voice_id": "af_heart", "sample_count": 0}]
        with patch.object(narrate, "voicebox_channel_profile", return_value="narrator-id"), \
             patch.object(narrate.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(profiles).encode())):
            with self.assertRaisesRegex(ValueError, "gender does not match"):
                narrate.resolve_voice_cast({"narrator": script["cast"]["narrator"],
                                           "investor": script["cast"]["investor"]})

    def test_resolves_only_existing_voicebox_profiles(self):
        script = example()
        profiles = [{"name": cast["profile_name"], "id": f"p-{key}", "sample_count": 1}
                    for key, cast in script["cast"].items() if key != "narrator"]
        with patch.object(narrate, "voicebox_channel_profile", return_value="narrator-id"), \
             patch.object(narrate.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(profiles).encode())):
            resolved = narrate.resolve_voice_cast(script["cast"])
        self.assertEqual(resolved["narrator"]["id"], "narrator-id")
        self.assertEqual(resolved["investor"]["id"], "p-investor")
        profiles[0]["sample_count"] = 0
        with patch.object(narrate, "voicebox_channel_profile", return_value="narrator-id"), \
             patch.object(narrate.urllib.request, "urlopen", return_value=io.BytesIO(json.dumps(profiles).encode())):
            with self.assertRaisesRegex(ValueError, "expected one active"):
                narrate.resolve_voice_cast(script["cast"])



SETUP_SCRIPT = SCRIPT.parent / "provision_voicebox_cast.py"
setup_spec = importlib.util.spec_from_file_location("provision_voicebox_cast", SETUP_SCRIPT)
setup_cast = importlib.util.module_from_spec(setup_spec)
setup_spec.loader.exec_module(setup_cast)


class LocalCastProvisioning(unittest.TestCase):
    def test_rejects_remote_and_malformed_voicebox_base(self):
        for value in ("https://voicebox.example.com", "http://192.168.1.2:17493",
                      "file:///etc/passwd", "http://127.0.0.1:17493/user"):
            with self.subTest(url=value), self.assertRaises(ValueError):
                setup_cast.local_base(value)
        self.assertEqual(setup_cast.local_base("http://127.0.0.1:17493"), "http://127.0.0.1:17493")

    def test_requires_original_synthetic_wav_and_transcript(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            entry = {"profile_name": "Original Character Female 01", "gender": "female",
                     "synthetic_voice": True, "approved": True,
                     "reference_wav": "character.wav", "reference_text": "An original synthetic reference."}
            reference = root / "character.wav"
            with wave.open(str(reference), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(24000)
                wav.writeframes(b"\x01\x00" * 12000)
            self.assertEqual(setup_cast.verify_reference(entry, "character", root), reference)
            entry["synthetic_voice"] = False
            with self.assertRaisesRegex(ValueError, "original synthetic"):
                setup_cast.verify_reference(entry, "character", root)
            entry["synthetic_voice"] = True
            entry["reference_text"] = ""
            with self.assertRaisesRegex(ValueError, "reference_text"):
                setup_cast.verify_reference(entry, "character", root)

@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg required for voice master assembly")
class CastAssembly(unittest.TestCase):
    def test_synthesizes_each_segment_with_own_profile_and_records_speaker(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            script = folder / "script.json"
            data = example()
            script.write_text(json.dumps(data), encoding="utf-8")
            output = folder / "audio"
            profiles = {"narrator": {"id": "narrator-id", "engine": "chatterbox", "voice_type": "cloned"}}
            profiles.update({speaker: {"id": "p-" + speaker, "engine": "kokoro",
                                       "voice_type": "preset"}
                             for speaker in ("founder", "investor", "analyst", "reporter")})
            used = []
            def instrument(text, profile, speed, path, **kwargs):
                used.append(profile)
                fake_voicebox(text, profile, speed, path, **kwargs)
            with patch.object(narrate, "resolve_voice_cast", return_value=profiles), \
                 patch.object(narrate, "synth_voicebox", side_effect=instrument), \
                 patch.object(narrate, "apply_voice_chain", return_value=None):
                exit_code = narrate.main([str(script), "--out", str(output)])
            self.assertEqual(exit_code, 0)
            self.assertEqual(used, ["narrator-id", "p-founder", "p-investor", "p-analyst",
                                    "p-reporter", "narrator-id"])
            meta = json.loads((output / "timings.json").read_text())
            self.assertEqual([x["speaker"] for x in meta["segments"]],
                             ["narrator", "founder", "investor", "analyst", "reporter", "narrator"])
            self.assertEqual(meta["cast"]["investor"]["gender"], "female")
            self.assertEqual(meta["segments"][2]["voice_engine"], "kokoro")
            self.assertEqual(meta["segments"][0]["voice_engine"], "chatterbox")
            self.assertEqual(meta["cast"]["narrator"]["gender"], "male")
            self.assertTrue((output / "narration.wav").stat().st_size > 0)
            self.assertTrue((output / "captions.srt").stat().st_size > 0)


if __name__ == "__main__":
    unittest.main()
