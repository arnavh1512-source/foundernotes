"""Offline API fixtures, not synthesized speech or a voice-quality approval."""
import copy
import importlib.util
import io
import math
import struct
import json
from pathlib import Path
import shutil
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import tempfile
import unittest
from urllib.parse import parse_qs
import wave

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
spec = importlib.util.spec_from_file_location('voicestudio_narrate', SCRIPTS / 'voicestudio_narrate.py')
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)


def wav_fixture():
    stream = io.BytesIO()
    with wave.open(stream, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
        w.writeframes(b''.join(struct.pack('<h', int(6000 * math.sin(2*math.pi*330*i/24000))) for i in range(4800)))
    return stream.getvalue()


def episode():
    return {'speakers': {'youth': {'profile_id': 'test-youth'}, 'philosopher': {'profile_id': 'test-philosopher'}},
            'lead': .1, 'tail': .1, 'segments': [
                {'id':'s1','speaker':'youth','scene_id':'hook','text':'A test line.','pause_after':.1},
                {'id':'s2','speaker':'philosopher','scene_id':'study','text':'Another test line.'}]}


class VoiceStudioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.script = self.root / 'script.json'
        self.script.write_text(json.dumps(episode()))

    def server(self, redirect=False):
        received = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_POST(self):
                received.append(parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode()))
                if redirect:
                    self.send_response(302); self.send_header('Location', '/other'); self.end_headers(); return
                data = wav_fixture()
                self.send_response(200); self.send_header('Content-Type','audio/wav'); self.end_headers(); self.wfile.write(data)
            def do_GET(self):
                received.append({'unexpected_get':self.path})
                self.send_response(200); self.end_headers(); self.wfile.write(wav_fixture())
        server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        return 'http://127.0.0.1:' + str(server.server_port), received

    def test_non_loopback_urls_are_rejected(self):
        for value in ['https://localhost:3900','http://example.org','http://127.0.0.1@evil.invalid','http://localhost/path']:
            with self.subTest(url=value), self.assertRaises(SystemExit): voice.local_url(value)

    def test_invalid_audio_is_rejected(self):
        for value in [b'garbage', b'RIFF1234WAVE']:
            with self.assertRaises(SystemExit): voice.valid_wav(value)

    def test_metadata_matches_ids_not_position_and_rejects_missing_segments(self):
        timing = {'segments':[{'id':'s2'}, {'id':'s1'}]}
        voice.attach_metadata(timing, episode())
        self.assertEqual([s['speaker'] for s in timing['segments']], ['philosopher','youth'])
        with self.assertRaises(SystemExit): voice.attach_metadata({'segments':[{'id':'s1'}]},episode())

    def test_invalid_pause_is_rejected_before_synthesis(self):
        source=episode(); source['segments'][0]['pause_after']=-1
        self.script.write_text(json.dumps(source))
        with self.assertRaises(SystemExit): voice.load_episode(self.script)

    def test_redirect_is_not_followed(self):
        origin, calls = self.server(True)
        with self.assertRaisesRegex(SystemExit, 'HTTP 302'):
            voice.synthesize(origin, {'text':'test'},10)
        self.assertEqual(len(calls),1)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'FFmpeg required')
    def test_real_assembly_preserves_cast_scenes_and_reuses_valid_cache(self):
        origin, calls = self.server()
        args=[str(self.script),'--out',str(self.root / 'audio'),'--url',origin]
        self.assertEqual(voice.main(args),0)
        self.assertEqual(len(calls),2)
        self.assertEqual(calls[0]['profile_id'],['test-youth'])
        self.assertEqual(calls[0]['speed'],['1.0'])
        timings=json.loads((self.root/'audio/timings.json').read_text())
        self.assertEqual([s['speaker'] for s in timings['segments']],['youth','philosopher'])
        self.assertEqual([s['scene_id'] for s in timings['segments']],['hook','study'])
        self.assertTrue((self.root/'audio/captions.srt').is_file())
        with wave.open(str(self.root/'audio/narration.wav')) as w:
            self.assertEqual(w.getframerate(),48000)
            self.assertAlmostEqual(w.getnframes()/w.getframerate(),timings['duration'],places=2)
        kit=SCRIPTS.parents[1]/'painted-character-motion/scripts/build_from_timings.py'
        spec=importlib.util.spec_from_file_location('painted_builder',kit)
        builder=importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)
        shots,total=builder.build(self.root/'audio/timings.json',self.root/'visual',builder.DEFAULT_SCENES)
        self.assertEqual([s['id'] for s in shots],['gate','study'])
        self.assertEqual(total,timings['duration'])
        voice.main(args)
        self.assertEqual(len(calls),2)
        (self.root/'audio/voicestudio-raw/s1.wav').write_bytes(b'corrupt')
        with self.assertRaises(SystemExit): voice.main(args)

if __name__ == '__main__': unittest.main()
