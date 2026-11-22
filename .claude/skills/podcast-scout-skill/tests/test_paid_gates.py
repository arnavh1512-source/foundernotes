"""collage-director paid stages: a bare run is a plan only; --generate and --max-jobs gate real spend. No network."""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "collage-director" / "scripts"))
import aroll_clips  # noqa: E402
import asr_beats  # noqa: E402
import audio  # noqa: E402
import clips  # noqa: E402
import croll_keyframes  # noqa: E402
import keyframes  # noqa: E402
import provider  # noqa: E402
import style_bakeoff  # noqa: E402


class FakeProvider:
    def __init__(self, status="completed"):
        self.calls, self.status = [], status

    def _job(self, name, *args, **kwargs):
        self.calls.append((name, args, kwargs))
        return f"job{len(self.calls)}"

    def submit_image(self, *a, **k): return self._job("submit_image", *a, **k)
    def submit_video(self, *a, **k): return self._job("submit_video", *a, **k)
    def submit_audio(self, *a, **k): return self._job("submit_audio", *a, **k)

    def upload(self, path):
        self.calls.append(("upload", (path,), {}))
        return f"https://cdn.example/{os.path.basename(path)}"

    def download(self, url, dest):
        self.calls.append(("download", (url, dest), {}))

    def get_status(self, job_id):
        return {"status": self.status, "output": f"https://cdn.example/{job_id}.out", "error": "boom"}

    def names(self):
        return [c[0] for c in self.calls]


def beats_doc(n=2):
    return {"mode": "aroll", "source_video": "src.mp4", "anchor_photo": "photo.jpg",
            "beats": [{"id": i, "start": 0, "end": 2, "narration": f"line {i}",
                       "shots": [{"id": "a", "scene": "a paper goat", "keyframe_path": "kf.jpg"}]}
                      for i in range(1, n + 1)]}


class PaidStageTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.write(beats_doc())
        self.fake = FakeProvider()
        for module in (keyframes, clips, style_bakeoff, croll_keyframes, aroll_clips, audio, asr_beats):
            p = patch.object(module, "get_provider", lambda *a, **k: self.fake)
            p.start()
            self.addCleanup(p.stop)
        sleep = patch.object(provider.time, "sleep")
        sleep.start()
        self.addCleanup(sleep.stop)

    def write(self, doc):
        (self.dir / "beats.json").write_text(json.dumps(doc), encoding="utf-8")

    def quiet(self, fn, *args, **kwargs):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            fn(*args, **kwargs)
        return out.getvalue()

    def test_bare_run_is_plan_only_for_every_stage(self):
        before = (self.dir / "beats.json").read_bytes()
        with patch.object(aroll_clips.subprocess, "run", side_effect=AssertionError("ffmpeg in a dry run")):
            for run in (keyframes.run, clips.run, style_bakeoff.run, croll_keyframes.run, aroll_clips.run, audio.run):
                out = self.quiet(run, str(self.dir))
                self.assertIn("dry run", out, run.__module__)
        self.assertEqual(self.fake.calls, [])  # no upload, no submit
        self.assertEqual((self.dir / "beats.json").read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()), ["beats.json"])

    def test_plan_over_max_jobs_refuses_a_real_run(self):
        with self.assertRaisesRegex(SystemExit, "max-jobs"):
            self.quiet(keyframes.run, str(self.dir), generate=True, max_jobs=1)
        self.assertEqual(self.fake.calls, [])

    def test_generate_submits_and_uploads_lazily_once(self):
        self.quiet(clips.run, str(self.dir), generate=True)
        self.assertEqual(self.fake.names().count("upload"), 2)
        submits = [c for c in self.fake.calls if c[0] == "submit_video"]
        self.assertEqual(len(submits), 2)
        self.assertEqual(submits[0][2]["image_url"], "https://cdn.example/kf.jpg")
        doc = json.loads((self.dir / "beats.json").read_text(encoding="utf-8"))
        self.assertTrue(all(b["shots"][0]["clip_url"] for b in doc["beats"]))

    def test_audio_reuses_existing_narration(self):
        doc = beats_doc()
        existing = self.dir / "narr_1.mp3"
        existing.write_bytes(b"ID3")
        doc["beats"][0]["audio_path"] = str(existing)
        self.write(doc)
        with patch.object(audio, "probe_dur", return_value=1.0):
            self.quiet(audio.run, str(self.dir), generate=True)
        texts = [c[2].get("text") for c in self.fake.calls if c[0] == "submit_audio"]
        self.assertEqual(texts, ["line 2", None])  # beat 2 narration + bgm only

    def test_clone_upload_needs_its_own_flag(self):
        ref = self.dir / "owner.wav"
        ref.write_bytes(b"RIFF")
        doc = beats_doc()
        doc["voice"] = {"clone_ref": str(ref), "clone_ref_is_owner_own_voice": True}
        self.write(doc)
        with self.assertRaisesRegex(SystemExit, "--allow-clone-upload"):
            self.quiet(audio.run, str(self.dir), generate=True)
        self.assertEqual(self.fake.calls, [])
        self.quiet(audio.run, str(self.dir), allow_clone_upload=True)  # dry run with the flag: allowed, nothing sent
        self.assertEqual(self.fake.calls, [])


class AsrTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir, True)

    def run_asr(self, fake, **kwargs):
        with patch.object(asr_beats, "get_provider", lambda *a, **k: fake), \
                patch.object(asr_beats, "extract_audio") as extract, \
                patch.object(asr_beats.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            try:
                asr_beats.run(str(self.dir), "talk.mp4", **kwargs)
            finally:
                self.extracted = extract.called

    def test_bare_run_is_plan_only(self):
        fake = FakeProvider()
        self.run_asr(fake)
        self.assertEqual(fake.calls, [])
        self.assertFalse(self.extracted)

    def test_stuck_job_hits_deadline_instead_of_hanging(self):
        with self.assertRaisesRegex(SystemExit, "still not done"):
            self.run_asr(FakeProvider(status="pending"), generate=True, deadline_s=0)
        self.assertFalse((self.dir / "beats.json").exists())

    def test_failed_asr_exits_without_dummy_beats(self):
        with self.assertRaisesRegex(SystemExit, "ASR failed"):
            self.run_asr(FakeProvider(status="failed"), generate=True)
        self.assertFalse((self.dir / "beats.json").exists())


if __name__ == "__main__":
    unittest.main()
