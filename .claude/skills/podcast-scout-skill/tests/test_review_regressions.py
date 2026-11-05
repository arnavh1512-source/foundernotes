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


class RecheckH2Schema(unittest.TestCase):
    def setUp(self):
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            self.skipTest("jsonschema not installed")

    def test_topic_report_passes_schema_and_checker(self):
        import jsonschema
        S = json.loads((ROOT / "references" / "report-schema.json").read_text())
        F = json.loads((ROOT / "tests" / "provisional-report.json").read_text(encoding="utf-8-sig"))
        T = copy.deepcopy(F); T["input"] = "topic"; T["podcast"] = {"coverage": "not-applicable"}
        for t in T["topics"]:
            t.pop("moment", None)
        V = jsonschema.Draft202012Validator(S)
        self.assertEqual([e.message for e in V.iter_errors(T)], [])
        self.assertEqual(validator.validate(T), [])
        P = copy.deepcopy(F); P["topics"][0].pop("moment", None)
        self.assertTrue(list(V.iter_errors(P)))


class RecheckM1Alignment(unittest.TestCase):
    CRIT = {"not", "no", "never"}

    def test_relocated_negation_is_flagged(self):
        want = "alpha is not valid beta is valid".split()
        heard = "alpha is valid beta is not valid".split()
        self.assertTrue(narrate.critical_edits(want, heard, self.CRIT))

    def test_inserted_number_is_flagged(self):
        self.assertTrue(narrate.critical_edits("use 5 units".split(), "use 50 to 5 units".split(), self.CRIT))

    def test_clean_line_has_no_edits(self):
        w = "it is not luck".split()
        self.assertEqual(narrate.critical_edits(w, list(w), self.CRIT), [])


@unittest.skipUnless(FF, "ffmpeg missing")
class RecheckM3Crossfade(unittest.TestCase):
    def test_clip_audio_survives_crossfades(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for n in ("a", "b"):
                ff("-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30", "-f", "lavfi", "-i", "sine=f=1000:sample_rate=48000",
                   "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(td / f"{n}.mp4"))
            ff("-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", "5.8", str(td / "n.wav"))
            r = subprocess.run([sys.executable, str(SCRIPTS / "assemble.py"), "--scenes", str(td / "a.mp4"), str(td / "b.mp4"),
                                "--crossfade", "0.2", "--keep-clip-audio", "--narration", str(td / "n.wav"),
                                "--out", str(td / "o.mp4")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            vol = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(td / "o.mp4"), "-af", "volumedetect", "-f", "null", "-"],
                                 capture_output=True, text=True).stderr
            self.assertGreater(float(vol.split("mean_volume:")[1].split("dB")[0]), -40)


class RecheckM9Setup(unittest.TestCase):
    def test_setup_resolves_playwright_like_renderer(self):
        src = (ROOT.parent / "motion" / "scripts" / "setup.sh").read_text()
        body = src[src.index("pw_node()"):src.index("install_ffmpeg()")]
        self.assertIn('"root", "-g"', body)
        self.assertIn("playwright-core", body)
        self.assertIn("pw_node browser", body)


class RecheckN1SetupCore(unittest.TestCase):
    def test_module_gate_uses_shared_resolver(self):
        src = (ROOT.parent / "motion" / "scripts" / "setup.sh").read_text()
        self.assertIn("pw_found() { pw_node module; }", src)
        self.assertIn("pw_node browser", src)

    @unittest.skipUnless(shutil.which("node") and shutil.which("npm"), "node/npm missing")
    def test_core_only_install_is_found(self):
        """Fixture: only a local playwright-core (stub with a real browser path); global root redirected to empty."""
        import os
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); (td / "scripts").mkdir()
            core = td / "node_modules" / "playwright-core"; core.mkdir(parents=True)
            (core / "package.json").write_text('{"name":"playwright-core","main":"index.js"}')
            (core / "index.js").write_text('module.exports = { chromium: { executablePath: () => "/bin/sh" } };')
            src = (ROOT.parent / "motion" / "scripts" / "setup.sh").read_text()
            funcs = src[src.index("pw_node()"):src.index("install_ffmpeg()")]
            script = f'here="{td}"\n' + funcs + '\npw_found && echo MOD\nchromium_found && echo BROWSER\n'
            env = dict(os.environ, NPM_CONFIG_PREFIX=str(td / "emptyglobal"), npm_config_prefix=str(td / "emptyglobal"))
            env.pop("MOTION_CHROMIUM", None); env.pop("NODE_PATH", None)
            out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, env=env).stdout
            self.assertIn("MOD", out); self.assertIn("BROWSER", out)
