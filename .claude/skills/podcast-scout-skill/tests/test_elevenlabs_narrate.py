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

    @unittest.skipUnless(importlib.util.find_spec('elevenlabs') and importlib.util.find_spec('dotenv'),
                         'elevenlabs/python-dotenv not installed (CI installs requirements.txt)')
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

    def run_main(self,args):
        from contextlib import redirect_stderr
        import io
        err=io.StringIO()
        with redirect_stderr(err):code=app.main(args)
        return code,err.getvalue()

    def test_shared_validator_errors_are_labelled_elevenlabs(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'script.json'
            path.write_text(json.dumps({'speakers':{'youth':{'voice_id':'one'}},'segments':[{'id':'s1','speaker':'youth','text':'Hi','pause_after':-1}]}),encoding='utf-8')
            code,err=self.run_main([str(path),'--out',str(Path(td)/'audio')])
        self.assertEqual(code,2)
        self.assertTrue(err.startswith('elevenlabs_narrate: segment s1 pause_after'),err)
        self.assertNotIn('voicestudio',err)

    def test_only_sdk_errors_are_reported_as_sdk_failure(self):
        from unittest.mock import patch
        class FakeApiError(Exception):
            status_code=401
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'script.json'
            path.write_text(json.dumps({'speakers':{'youth':{'voice_id':'one'}},'segments':[{'id':'s1','speaker':'youth','text':'Hello'}]}),encoding='utf-8')
            args=[str(path),'--out',str(Path(td)/'audio'),'--generate']
            with patch.object(app,'create_client',side_effect=ModuleNotFoundError("No module named 'elevenlabs'")):
                code,err=self.run_main(args)
            self.assertEqual(code,2);self.assertIn('SDK unavailable',err);self.assertNotIn('SDK failure',err)
            with patch.object(app,'create_client',return_value=object()), \
                 patch.object(app,'synthesize_segment',side_effect=KeyError('bug')):
                with self.assertRaises(KeyError):app.main(args)
            with patch.object(app,'SDK_ERRORS',(FakeApiError,)), patch.object(app,'create_client',return_value=object()), \
                 patch.object(app,'synthesize_segment',side_effect=FakeApiError('secret body')):
                code,err=self.run_main(args)
            self.assertEqual(code,2);self.assertIn('SDK failure FakeApiError status=401',err);self.assertNotIn('secret',err)

if __name__=='__main__':unittest.main()
