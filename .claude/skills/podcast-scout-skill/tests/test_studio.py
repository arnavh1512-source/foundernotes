"""Tests for the studio scripts. Run: python3 -m unittest discover -s tests"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


narrate = load("narrate")
lint = load("package_lint")
qc = load("qc_video")
HAVE_FFMPEG = shutil.which("ffmpeg") is not None


class MaleVoicePolicy(unittest.TestCase):
    def test_defaults_are_male(self):
        for engine, voice in narrate.DEFAULT_VOICE.items():
            for part in voice.split("+"):          # a blend: every component must be male
                self.assertIn(part.split(":")[0], narrate.MALE_VOICES[engine])
        self.assertEqual(narrate.DEFAULT_VOICE["kokoro"], "am_michael")

    def test_kokoro_allowlist_is_male_only(self):
        for v in narrate.MALE_VOICES["kokoro"]:
            self.assertEqual(v[1], "m", v)  # kokoro ids: <lang><gender>_<name>

    @unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
    def test_female_voice_refused(self):
        with tempfile.TemporaryDirectory() as td:
            script = Path(td) / "s.json"
            script.write_text(json.dumps({"segments": [{"text": "hello"}]}))
            with self.assertRaises(SystemExit) as cm:
                narrate.main([str(script), "--out", td, "--engine", "kokoro", "--voice", "af_heart"])
            self.assertEqual(cm.exception.code, 2)

    def test_example_script_uses_male_voice(self):
        data = json.loads((ROOT / "assets" / "narration-script.example.json").read_text())
        v = data["voice"]
        self.assertIn(v["name"], narrate.MALE_VOICES[v["engine"]])


class Captions(unittest.TestCase):
    def test_chunks_respect_length(self):
        text = "This is a fairly long sentence that should be split into several caption lines for reading."
        for c in narrate.caption_chunks(text):
            self.assertLessEqual(len(c), 42)

    def test_cues_monotonic(self):
        timings = [{"start": 0.3, "end": 3.0, "display": "One two three four five six seven eight nine ten eleven twelve"},
                   {"start": 3.4, "end": 5.0, "display": "Next."}]
        cues = narrate.build_captions(timings)
        for (a, b, _), (c, d, _) in zip(cues, cues[1:]):
            self.assertLessEqual(b, c + 1e-9)
            self.assertLess(a, b)

    def test_srt_parse_roundtrip(self):
        cues = [(0.15, 2.0, "Hello there."), (2.0, 4.5, "Second line.")]
        with tempfile.TemporaryDirectory() as td:
            narrate.write_captions(cues, Path(td))
            parsed = qc.parse_srt((Path(td) / "captions.srt").read_text())
        self.assertEqual(len(parsed), 2)
        self.assertAlmostEqual(parsed[1][1], 4.5, places=2)

    def test_plain_text_script(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.txt"
            p.write_text("# heading ignored\n\nFirst para\nwraps.\n\nSecond para.")
            data = narrate.load_script(p)
        self.assertEqual([s["text"] for s in data["segments"]], ["First para wraps.", "Second para."])


class PackageLint(unittest.TestCase):
    def run_lint(self, pkg, *extra):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "p.json"
            p.write_text(json.dumps(pkg))
            return lint.main([str(p), *extra])

    def good(self):
        return {"titles": ["You Read It. Can You Explain It?"],
                "thumbnails": [{"title_index": 0, "text": "BLANK PAGE", "focal": "empty speech bubble"}],
                "description": "Explaining beats rereading for spotting gaps.\n00:00 Test\n00:41 Why\n02:10 How",
                "chapters": [["00:00", "Test"], ["00:41", "Why"], ["02:10", "How"]], "tags": ["study"]}

    def test_good_passes(self):
        self.assertEqual(self.run_lint(self.good(), "--duration", "240"), 0)

    def test_long_title_fails(self):
        pkg = self.good()
        pkg["titles"] = ["x" * 75]
        self.assertEqual(self.run_lint(pkg), 1)

    def test_chapter_rules(self):
        pkg = self.good()
        pkg["chapters"] = [["00:05", "A"], ["00:10", "B"], ["00:30", "C"]]
        self.assertEqual(self.run_lint(pkg), 1)

    def test_clickbait_fails(self):
        pkg = self.good()
        pkg["titles"] = ["You Won't Believe How Memory Works"]
        self.assertEqual(self.run_lint(pkg), 1)

    def test_wordy_thumbnail_fails(self):
        pkg = self.good()
        pkg["thumbnails"][0]["text"] = "this is far too many words here"
        self.assertEqual(self.run_lint(pkg), 1)


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg missing")
class AssembleAndQC(unittest.TestCase):
    def test_pipeline_on_synthetic_media(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            ff = ["ffmpeg", "-y", "-loglevel", "error"]
            subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30,rotate=2*t", "-t", "3",
                                 "-pix_fmt", "yuv420p", str(td / "a.mp4")], check=True)
            subprocess.run(ff + ["-f", "lavfi", "-i", "sine=f=180:sample_rate=48000", "-t", "3",
                                 "-ac", "1", str(td / "n.wav")], check=True)
            (td / "c.srt").write_text("1\n00:00:00,200 --> 00:00:02,500\nA test caption.\n")
            out = td / "final.mp4"
            r = subprocess.run([sys.executable, str(SCRIPTS / "assemble.py"), "--scenes", str(td / "a.mp4"),
                                "--narration", str(td / "n.wav"), "--captions", str(td / "c.srt"), "--out", str(out)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(out.with_suffix(".srt").exists())
            code = qc.main([str(out), "--captions", str(td / "c.srt"), "--json", str(td / "qc.json"),
                            "--sheet", str(td / "sheet.jpg"), "--min-duration", "2"])
            report = json.loads((td / "qc.json").read_text())
            self.assertEqual(code, 0, report)
            self.assertEqual(report["errors"], [], report)
            self.assertTrue(any(c.startswith("Loudness") for c in report["checks"]), report)
            self.assertTrue(any(c.startswith("Captions") for c in report["checks"]), report)


if __name__ == "__main__":
    unittest.main()
