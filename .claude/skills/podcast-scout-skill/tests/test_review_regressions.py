"""Regression tests for the 2026-11-05 repository review (H1–H2, M1–M9, L1)."""
import copy, importlib.util, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FF = shutil.which("ffmpeg") is not None


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


qc, lint, narrate, validator = load("qc_video"), load("package_lint"), load("narrate"), load("validate_report")


def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)


@unittest.skipUnless(FF, "ffmpeg missing")
class H1TruncatedAudio(unittest.TestCase):
    def test_four_second_video_with_one_second_audio_fails(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); v = td / "v.mp4"
            ff("-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=30", "-f", "lavfi", "-i", "sine=f=300:sample_rate=48000",
               "-t", "4", "-filter_complex", "[1:a]atrim=0:1[a]", "-map", "0:v", "-map", "[a]", "-c:v", "libx264",
               "-pix_fmt", "yuv420p", "-c:a", "aac", str(v))
            (td / "t.json").write_text(json.dumps({"duration": 4.0}))
            code = qc.main([str(v), "--timings", str(td / "t.json"), "--json", str(td / "r.json")])
            r = json.loads((td / "r.json").read_text())
            self.assertEqual(code, 1)
            self.assertTrue(any("audio stream covers" in x["msg"] for x in r["results"]))


class H2TopicMode(unittest.TestCase):
    def test_topic_report_without_podcast_quote_validates(self):
        fixture = json.loads((ROOT / "tests" / "provisional-report.json").read_text(encoding="utf-8-sig"))
        rep = copy.deepcopy(fixture)
        rep["input"] = "topic"
        rep["podcast"] = {"coverage": "not-applicable"}
        for t in rep["topics"]:
            t.pop("moment", None)
        self.assertEqual(validator.validate(rep), [])

    def test_podcast_report_still_needs_quote(self):
        fixture = json.loads((ROOT / "tests" / "provisional-report.json").read_text(encoding="utf-8-sig"))
        rep = copy.deepcopy(fixture)
        rep["topics"][0].pop("moment", None)
        self.assertIn("quote", "\n".join(validator.validate(rep)))


class M1Negation(unittest.TestCase):
    def test_second_not_cannot_hide_a_missing_first_not(self):
        want = "it is not luck and it is not talent".split()
        heard = "it is luck and it is not talent".split()
        self.assertEqual(narrate.missing_words(want, heard), ["not"])


@unittest.skipUnless(FF, "ffmpeg missing")
class M2RecordingCache(unittest.TestCase):
    def test_replaced_recording_is_resynthesised(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); rec = td / "rec"; rec.mkdir()
            (td / "s.json").write_text(json.dumps({"segments": [{"id": "s01", "text": "hello there"}]}))
            ff("-f", "lavfi", "-i", "sine=f=200:sample_rate=48000", "-t", "1", str(rec / "s01.wav"))
            args = [str(td / "s.json"), "--out", str(td / "o"), "--engine", "files", "--files-dir", str(rec)]
            narrate.main(args); d1 = json.loads((td / "o" / "timings.json").read_text())["segments"][0]
            ff("-f", "lavfi", "-i", "sine=f=200:sample_rate=48000", "-t", "2", str(rec / "s01.wav"))
            narrate.main(args); d2 = json.loads((td / "o" / "timings.json").read_text())["segments"][0]
            self.assertGreater(d2["end"] - d2["start"], (d1["end"] - d1["start"]) + 0.5)


@unittest.skipUnless(FF, "ffmpeg missing")
class M3M4Assemble(unittest.TestCase):
    def test_clip_audio_kept_and_same_path_sidecar(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            ff("-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30", "-f", "lavfi", "-i", "sine=f=1000:sample_rate=48000",
               "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(td / "c.mp4"))
            ff("-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "3", str(td / "n.wav"))
            (td / "final.srt").write_text("1\n00:00:00,200 --> 00:00:02,000\nHi.\n")
            r = subprocess.run([sys.executable, str(SCRIPTS / "assemble.py"), "--scenes", str(td / "c.mp4"),
                                "--narration", str(td / "n.wav"), "--keep-clip-audio", "--captions", str(td / "final.srt"),
                                "--out", str(td / "final.mp4")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            vol = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(td / "final.mp4"), "-af", "volumedetect", "-f", "null", "-"],
                                 capture_output=True, text=True).stderr
            mean = float(vol.split("mean_volume:")[1].split("dB")[0])
            self.assertGreater(mean, -40, "1 kHz clip tone should survive into the mix")


class M5Captions(unittest.TestCase):
    def test_reversed_cue_is_a_structural_failure(self):
        cues, problems = qc.parse_srt_strict("1\n00:00:02,000 --> 00:00:01,000\nBackwards.\n")
        self.assertTrue(problems)


class M6ShortTimestamps(unittest.TestCase):
    def test_single_digit_minutes_parse(self):
        self.assertEqual(validator.timestamp_seconds("0:20"), 20)
        self.assertEqual(validator.timestamp_seconds("1:02:03"), 3723)
        segs = validator.caption_segments("[0:20] early words here\n[10:00] later words\n")
        self.assertEqual([s for s, _ in segs], [20, 600])


class M7L1PackageLint(unittest.TestCase):
    def run_lint(self, pkg):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "p.json"; p.write_text(json.dumps(pkg)); return lint.main([str(p)])

    def test_empty_title_fails(self):
        self.assertEqual(self.run_lint({"titles": [""], "description": "x"}), 1)

    def test_negative_title_index_fails_cleanly(self):
        self.assertEqual(self.run_lint({"titles": ["A real title"], "description": "x",
                                        "thumbnails": [{"title_index": -2, "text": "HI", "focal": "x"}]}), 1)

    def test_malformed_chapter_stamp_fails_cleanly(self):
        self.assertEqual(self.run_lint({"titles": ["A real title"], "description": "x",
                                        "chapters": [["0:00", "a"], ["0:4x", "b"], ["1:00", "c"]]}), 1)


class M8M9RenderScript(unittest.TestCase):
    def test_stale_stills_cleared_and_windows_npm_shell(self):
        src = (ROOT.parent / "motion" / "scripts" / "render.mjs").read_text()
        self.assertIn("readdirSync(dir)", src)
        self.assertIn('shell: process.platform === "win32"', src)


if __name__ == "__main__":
    unittest.main()
