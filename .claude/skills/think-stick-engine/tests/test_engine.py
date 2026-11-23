"""Regression tests for the Think! stick engine helpers (numpy only)."""
import json, os, shutil, subprocess, sys, tempfile, unittest, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.dirname(HERE)

def write_wav(path, y, sr=48000):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(y, -1, 1) * 32767).astype('<i2').tobytes())

def read_wav(path):
    with wave.open(path) as w: return np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32) / 32768, w.getframerate()

class SfxBank(unittest.TestCase):
    def test_cc0_samples_rendered_at_cue_times(self):
        d = tempfile.mkdtemp(); film = os.path.join(d, 'film'); os.makedirs(film)
        shutil.copy(os.path.join(SKILL, 'engine', 'sfx.py'), film)
        open(os.path.join(film, 'timing.js'), 'w').write('window.SEG={"a":[0,3]}; window.DUR=3.0;')
        cues = [[.1, 'thunk'], [.4, 'whoosh'], [.7, 'pop'], [.9, 'ding']]
        open(os.path.join(film, 'shots.js'), 'w').write('window.SHOTS2=' + json.dumps([{'seg': 'a', 'a': 0, 'b': 1, 'n': 'x', 'sfx': cues}]) + ';')
        env = dict(os.environ, THINK_SFX=os.path.join(SKILL, 'assets', 'sfx'))
        out = subprocess.run([sys.executable, 'sfx.py', 'out.wav'], cwd=film, env=env, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr); self.assertIn('4 cues', out.stdout)
        y, sr = read_wav(os.path.join(film, 'out.wav')); self.assertAlmostEqual(len(y) / sr, 3.0, places=2)
        self.assertLess(np.abs(y[:int(.25 * sr)]).max(), 1e-3)             # silence before the first cue (0.3 s)
        self.assertGreater(np.abs(y[int(.3 * sr):int(.6 * sr)]).max(), .05)  # thunk lands at 0.3 s

class StressedBeats(unittest.TestCase):
    def test_peaks_found_on_bursts_with_spacing(self):
        d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, 'mix')); os.makedirs(os.path.join(d, 'film'))
        sr = 48000; t = np.arange(int(sr * 6)) / sr; y = .02 * np.sin(2 * np.pi * 180 * t)
        for c in (1.0, 2.5, 4.2): y += .6 * np.exp(-((t - c) / .08) ** 2) * np.sin(2 * np.pi * 220 * t)
        write_wav(os.path.join(d, 'mix', 'narration.wav'), y, sr)
        open(os.path.join(d, 'film', 'turns.js'), 'w').write('window.SPEAK=' + json.dumps([[0.5, 5.5, 'youth']]) + ';')
        out = subprocess.run([sys.executable, os.path.join(SKILL, 'tools', 'emph.py')], cwd=d, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        js = open(os.path.join(d, 'film', 'turns.js')).read(); E = json.loads(js.split('window.EMPH=')[1].rstrip(';'))
        beats = E['0.500']; self.assertEqual(len(beats), 3)
        for got, want in zip(beats, (1.0, 2.5, 4.2)): self.assertAlmostEqual(got, want, delta=.08)

if __name__ == '__main__':
    unittest.main()
