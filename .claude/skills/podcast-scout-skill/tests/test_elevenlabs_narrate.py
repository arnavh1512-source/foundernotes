import importlib.util
import json
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
import unittest
import wave

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/elevenlabs_narrate.py'
sys.path.insert(0,str(SCRIPT.parent))
spec=importlib.util.spec_from_file_location('elevenlabs_narrate',SCRIPT)
app=importlib.util.module_from_spec(spec)
if SCRIPT.exists(): spec.loader.exec_module(app)

class ElevenTests(unittest.TestCase):
    def test_synthesis_writes_valid_pcm_wav_with_correct_voice(self):
        self.assertTrue(hasattr(app,'synthesize_segment'))
        calls=[]
        def convert(**kwargs): calls.append(kwargs);return iter([b'\0\0'*2400,b'\1\0'*2400])
        client=SimpleNamespace(text_to_speech=SimpleNamespace(convert=convert))
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'line.wav'
            app.synthesize_segment(client,'Hello','voice-one','eleven_v4',output)
            with wave.open(str(output)) as wav:
                self.assertEqual(wav.getframerate(),24000)
                self.assertEqual(wav.getnframes(),4800)
        self.assertEqual(calls[0]['voice_id'],'voice-one')
        self.assertEqual(calls[0]['output_format'],'pcm_24000')

    def test_odd_pcm_payload_is_rejected_without_output(self):
        self.assertTrue(hasattr(app,'synthesize_segment'))
        client=SimpleNamespace(text_to_speech=SimpleNamespace(convert=lambda **kw:iter([b'odd'])))
        with tempfile.TemporaryDirectory() as td:
            output=Path(td)/'line.wav'
            with self.assertRaises(ValueError):app.synthesize_segment(client,'test','one','eleven_v4',output)
            self.assertFalse(output.exists())

    def test_configuration_preserves_two_distinct_characters(self):
        self.assertTrue(hasattr(app,'load_script'))
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'script.json'
            path.write_text(json.dumps({'speakers':{'youth':{'voice_id':'one'},'philosopher':{'voice_id':'two'}},'segments':[{'id':'s1','speaker':'youth','scene_id':'hook','text':'Hello'}]}))
            source=app.load_script(path)
            self.assertEqual(source['speakers']['youth']['profile_id'],'one')
            self.assertEqual(source['speakers']['philosopher']['profile_id'],'two')

    def test_client_sends_key_from_environment_to_sdk(self):
        from unittest.mock import patch, Mock
        fake=Mock()
        sys.path.insert(0,str(SCRIPT.parents[4]))
        with patch('elevenlabs_client.ElevenLabs', fake), patch.dict('os.environ', {'ELEVENLABS_API_KEY':'test-placeholder-not-real'}), patch('elevenlabs_client.load_dotenv'):
            app.create_client()
        fake.assert_called_once_with(api_key='test-placeholder-not-real')

    def test_default_run_never_creates_a_client_or_makes_speech(self):
        self.assertTrue(hasattr(app,'main'))
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'script.json'
            path.write_text(json.dumps({'speakers':{'youth':{'voice_id':'one'}},'segments':[{'id':'s1','speaker':'youth','text':'Hello'}]}))
            with patch.object(app,'create_client',side_effect=AssertionError('Must not call API')):
                self.assertEqual(app.main([str(path),'--out',str(Path(td)/'audio')]),0)
            self.assertFalse((Path(td)/'audio').exists())

if __name__=='__main__':unittest.main()
