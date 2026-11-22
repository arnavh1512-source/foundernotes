"""assemble.py on tiny real clips: crossfade timing, awkward paths, sidecar suffix, pass-through and end hold."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
HAS_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
FRAME = 1 / 30
X264 = ("-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p")
X264_TB90K = X264 + ("-video_track_timescale", "90000")   # conformant, but another muxer's timebase


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def clip(path, seconds, size="1920x1080", codec=X264):
    ff("-f", "lavfi", "-i", f"testsrc2=s={size}:r=30", "-t", str(seconds), *codec, str(path))


def voice(path, seconds):
    ff("-f", "lavfi", "-i", "sine=f=220:sample_rate=48000", "-t", str(seconds), str(path))


def video_stream(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,duration", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)["streams"][0]


def decoded_md5(path):
    return subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v", "-f", "md5", "-"],
                          check=True, capture_output=True, text=True).stdout.strip()


def assemble(*args, env=None):
    return subprocess.run([sys.executable, str(SCRIPTS / "assemble.py"), *map(str, args)],
                          capture_output=True, text=True, env=env)


@unittest.skipUnless(HAS_FF, "FFmpeg/ffprobe unavailable")
class AssembleTests(unittest.TestCase):
    def test_crossfade_keeps_every_scene_on_its_original_clock(self):
        with tempfile.TemporaryDirectory() as temp:
            td = Path(temp)
            clip(td / "a.mp4", 1, codec=X264_TB90K)
            clip(td / "b.mp4", 1, "320x180", ("-c:v", "mpeg4"))   # non-conformant: gets normalised
            clip(td / "c.mp4", 1)
            voice(td / "n.wav", 1)    # shorter than the picture, so no end hold can hide a short picture
            r = assemble("--scenes", td / "a.mp4", td / "b.mp4", td / "c.mp4", "--crossfade", "0.3",
                         "--narration", td / "n.wav", "--no-burn", "--out", td / "o.mp4")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertAlmostEqual(float(video_stream(td / "o.mp4")["duration"]), 3.0, delta=FRAME + 1e-3)

    def test_quote_and_space_in_paths_and_ass_sidecar(self):
        with tempfile.TemporaryDirectory() as temp:
            td = Path(temp) / "O'Brien clips"
            (td / "fonts").mkdir(parents=True)
            clip(td / "a.mp4", 1, "640x360")
            clip(td / "b.mp4", 1, "640x360")
            voice(td / "n.wav", 2)
            captions = td / "cap's.ass"
            captions.write_text(
                "[Script Info]\nScriptType: v4.00+\nPlayResX: 384\nPlayResY: 288\n\n[V4+ Styles]\n"
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
                "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
                "MarginL, MarginR, MarginV, Encoding\n"
                "Style: Default,DejaVu Sans,13,&H0047B8E8,&H00D2E8F3,&H5022180E,&H5022180E,1,0,0,0,100,100,0,0,3,6,0,2,40,40,22,1\n"
                "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
                "Dialogue: 0,0:00:00.20,0:00:01.50,Default,,0,0,0,,{\\k50}It's {\\k50}fine\n", encoding="utf-8")
            env = dict(os.environ, TMP=str(td), TEMP=str(td), TMPDIR=str(td))   # the concat list lives in here too
            out = td / "final.mp4"
            r = assemble("--scenes", td / "a.mp4", td / "b.mp4", "--narration", td / "n.wav", "--captions", captions,
                         "--sub-karaoke", "--sub-fonts-dir", td / "fonts", "--out", out, env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(out.with_suffix(".ass").is_file())
            self.assertFalse(out.with_suffix(".srt").exists())

    def test_conformant_clip_is_not_reencoded_and_end_hold_matches_narration(self):
        with tempfile.TemporaryDirectory() as temp:
            td = Path(temp)
            clip(td / "a.mp4", 1, codec=X264_TB90K)
            clip(td / "small.mp4", 1, "640x360")
            voice(td / "short.wav", 0.5)
            voice(td / "long.wav", 2.5)
            r = assemble("--scenes", td / "a.mp4", "--narration", td / "short.wav", "--no-burn", "--out", td / "copy.mp4")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(decoded_md5(td / "copy.mp4"), decoded_md5(td / "a.mp4"))   # bit-exact pictures
            # copied + normalised clips concatenated, then held in the final encode
            r = assemble("--scenes", td / "small.mp4", td / "a.mp4", "--narration", td / "long.wav", "--no-burn",
                         "--out", td / "held.mp4")
            self.assertEqual(r.returncode, 0, r.stderr)
            held = video_stream(td / "held.mp4")
            self.assertAlmostEqual(float(held["duration"]), 2.6, delta=FRAME + 1e-3)   # narration + 0.1 s, as before
            self.assertEqual((held["width"], held["height"], held["r_frame_rate"]), (1920, 1080, "30/1"))


if __name__ == "__main__":
    unittest.main()
