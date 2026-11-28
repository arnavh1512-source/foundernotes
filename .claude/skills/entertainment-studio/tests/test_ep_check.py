"""Entertainment checks: every link from script to export must hold, and only Entertainment IP workspaces use them."""
import hashlib, json, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ep_build  # noqa: E402
from ep_check import check  # noqa: E402

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def workspace(td, temporary=True):
    ws = Path(td)
    for d in ("script", "assets", "scenes", "takes/clips", "export"):
        (ws / d).mkdir(parents=True, exist_ok=True)
    (ws / "script/ep.r1.md").write_text("A03-L01 The spoon slips.\n")
    (ws / "assets/HL-PROP-SPOON.v1.json").write_text('{"length": 170}')
    (ws / "scenes/_common.js").write_text("// helpers\n")
    (ws / "scenes/s01.js").write_text("S.s01=()=>{};\n")
    (ws / "scenes/s02.js").write_text("S.s02=()=>{};\n")
    uses = [{"asset": "HL-PROP-SPOON", "v": 1}]
    m = {"profile": "entertainment-ip", "series": "Half Landing", "series_slug": "half-landing", "episode": "A03",
         "script": {"path": "script/ep.r1.md", "revision": "r1", "sha256": sha(ws / "script/ep.r1.md")},
         "assets": [{"id": "HL-PROP-SPOON", "kind": "prop", "versions": [{"v": 1, "file": "assets/HL-PROP-SPOON.v1.json", "sha256": sha(ws / "assets/HL-PROP-SPOON.v1.json")}]}],
         "shots": [{"id": "S01", "scene": "s01", "dur": 1.0, "uses": uses}, {"id": "S02", "scene": "s02", "dur": 0.8, "uses": uses}],
         "audio_cues": [{"id": "C01", "shot": "S01", "t": 0.5, "kind": "thunk", "temporary": temporary, "note": "no approved sound yet" if temporary else ""}],
         "variants": [{"id": "short", "overrides": {"S02": {"dur": 0.4}}}, {"id": "long", "overrides": {"S02": {"dur": 1.2}}}]}
    m["takes"] = []
    for v in m["variants"]:
        rows = []
        for s in ep_build.resolve(m, v["id"]):
            key = ep_build.render_key(ws, m, s)
            clip = ws / f"takes/clips/{s['id']}-{key}.mp4"
            clip.write_bytes(key.encode())
            rows.append({"id": s["id"], "render_key": key, "clip": str(clip.relative_to(ws)), "clip_sha256": sha(clip)})
        take = ws / f"takes/{v['id']}.mp4"
        take.write_bytes(v["id"].encode())
        m["takes"].append({"id": f"T-{v['id']}", "variant": v["id"], "file": str(take.relative_to(ws)), "sha256": sha(take), "shots": rows})
    m["selected"] = {"take": "T-long", "reason": "the long hold lets the relief land before the reveal reverses it",
                     "notes": [{"take": "T-long", "t": 4.6, "observation": "relief reads"}]}
    out = ws / f"export/half-landing-a03-animatic{'_TEMP-AUDIO' if temporary else ''}.mp4"
    out.write_bytes(b"long")
    m["export"] = {"file": str(out.relative_to(ws)), "from_take": "T-long", "sha256": sha(out)}
    (ws / "workspace.json").write_text(json.dumps(m))
    return ws, m


def save(ws, m):
    (ws / "workspace.json").write_text(json.dumps(m))


class EpCheck(unittest.TestCase):
    def test_linked_workspace_passes(self):
        with tempfile.TemporaryDirectory() as td:
            ws, _ = workspace(td)
            self.assertEqual(check(ws), [])

    def test_think_workspaces_are_not_entertainment(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["profile"] = "think"; save(ws, m)
            self.assertIn("Think!", check(ws)[0])

    def test_edited_script_or_asset_breaks_the_pin(self):
        with tempfile.TemporaryDirectory() as td:
            ws, _ = workspace(td)
            (ws / "assets/HL-PROP-SPOON.v1.json").write_text('{"length": 200}')
            self.assertTrue(any("make a new version" in e for e in check(ws)))

    def test_malformed_asset_id_and_unregistered_version(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["assets"][0]["id"] = "spoon"; save(ws, m)
            errs = check(ws)
            self.assertTrue(any("stable" in e for e in errs))
            self.assertTrue(any("not a registered asset version" in e for e in errs))

    def test_variants_may_only_change_timing(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["variants"][0]["overrides"]["S02"]["scene"] = "s01"; save(ws, m)
            self.assertTrue(any("only change timing" in e for e in check(ws)))

    def test_temporary_sound_needs_a_note_and_a_labelled_export(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["audio_cues"][0]["note"] = ""; save(ws, m)
            self.assertTrue(any("no note" in e for e in check(ws)))
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["export"]["file"] = "export/half-landing-a03-animatic.mp4"; (ws / m["export"]["file"]).write_bytes(b"long"); save(ws, m)
            self.assertTrue(any("TEMP-AUDIO" in e for e in check(ws)))

    def test_revised_shot_marks_only_that_shot_stale(self):
        with tempfile.TemporaryDirectory() as td:
            ws, _ = workspace(td)
            (ws / "scenes/s01.js").write_text("S.s01=()=>{ /* revised */ };\n")
            errs = check(ws)
            self.assertTrue(errs)
            self.assertTrue(all(" S01:" in e for e in errs), errs)

    def test_export_must_be_the_selected_take(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["export"]["from_take"] = "T-short"; save(ws, m)
            self.assertTrue(any("not the selected take" in e for e in check(ws)))

    def test_selection_needs_a_reason_and_timestamped_notes(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["selected"]["reason"] = "better"; m["selected"]["notes"] = []; save(ws, m)
            errs = check(ws)
            self.assertTrue(any("reason" in e for e in errs))
            self.assertTrue(any("timestamps" in e for e in errs))



class CueFiles(unittest.TestCase):
    def test_episode_foley_comes_before_the_shared_bank(self):
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td); (ws / "sound").mkdir()
            (ws / "sound/thunk-own.wav").write_bytes(b"x")
            self.assertEqual(ep_build.cue_file(ws, {"kind": "thunk"}).name, "thunk-own.wav")
            self.assertTrue(ep_build.cue_file(ws, {"kind": "whoosh"}).is_relative_to(ep_build.SFX))
            with self.assertRaises(SystemExit):
                ep_build.cue_file(ws, {"id": "C9", "kind": "nosuchsound"})

    def test_a_cue_can_stop_on_an_action(self):
        self.assertNotIn("atrim", ep_build.cue_filter(0, {"kind": "creak"}, 500))
        f = ep_build.cue_filter(2, {"kind": "creak", "dur": 0.5, "gain": 0.6}, 6750)
        self.assertTrue(f.startswith("[2]atrim=0:0.5,afade=t=out:st=0.470"))
        self.assertIn("adelay=6750|6750,volume=0.6[a2]", f)

    def test_cue_length_must_be_positive(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            m["audio_cues"][0]["dur"] = 0; save(ws, m)
            self.assertTrue(any("dur must be" in e for e in check(ws)))


class VerticalPages(unittest.TestCase):
    def test_vertical_reel_page_and_key(self):
        with tempfile.TemporaryDirectory() as td:
            ws, m = workspace(td)
            shot = m["shots"][0]
            land = ep_build.render_key(ws, m, shot)
            html = ep_build.shot_page(ws, m, shot, "k1").read_text()
            self.assertIn('width="1920" height="1080"', html)
            m.update(format="vertical", overlay_tag=False)
            self.assertNotEqual(ep_build.render_key(ws, m, shot), land)   # a vertical render never reuses a landscape clip
            html = ep_build.shot_page(ws, m, shot, "k2").read_text()
            self.assertIn('width="1080" height="1920"', html)
            self.assertIn("const W=1080,H=1920", html)
            self.assertNotIn("logo.png", html)
            self.assertIn('"tag": ""', (ws / "film/shot_k2.js").read_text())


class ReviewMeasures(unittest.TestCase):
    def test_onsets_and_matching(self):
        import numpy as np, ep_review
        sr = 16000; a = np.zeros(sr * 2)
        for t in (0.5, 1.2):
            i = int(t * sr); a[i:i + 1600] = 0.5 * np.sin(np.arange(1600) * 0.3)
        found = ep_review.onsets(a, sr)
        self.assertEqual(found, [0.5, 1.2])
        rows = ep_review.match([("C1", 0.5), ("C2", 1.23), ("C3", 1.9)], found)
        self.assertEqual([r["ok"] for r in rows], [True, True, False])

    def test_phone_low_share(self):
        import numpy as np, wave, ep_review
        with tempfile.TemporaryDirectory() as td:
            for name, hz in (("sub", 45), ("mid", 900)):
                sr = 16000; a = (0.5 * np.sin(2 * np.pi * hz * np.arange(sr) / sr) * 32767).astype(np.int16)
                w = wave.open(f"{td}/{name}.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(a.tobytes()); w.close()
            self.assertGreater(ep_review.low_share(f"{td}/sub.wav"), 95)
            self.assertLess(ep_review.low_share(f"{td}/mid.wav"), 5)

    def test_loop_seam(self):
        from PIL import Image
        import ep_review
        a = Image.new("RGB", (100, 200), "white"); b = a.copy(); c = Image.new("RGB", (100, 200), "black")
        self.assertEqual(ep_review.seam(a, b), 0.0)
        self.assertEqual(ep_review.seam(a, c), 100.0)

if __name__ == "__main__":
    unittest.main()


class RefCompare(unittest.TestCase):
    def test_time_pairs(self):
        import ref_compare
        self.assertEqual(ref_compare.pairs(["1.3", "22.5:22.0"]), [(1.3, 1.3), (22.5, 22.0)])
