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


if __name__ == "__main__":
    unittest.main()
