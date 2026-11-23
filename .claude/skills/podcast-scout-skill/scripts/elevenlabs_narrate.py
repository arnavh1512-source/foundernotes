#!/usr/bin/env python3
"""Opt-in ElevenLabs character dialogue -> measured FounderNotes narration.

Default is a no-network plan. --generate explicitly requests metered synthesis.
Load ELEVENLABS_API_KEY from environment or the private project .env.local.
No voice cloning, narrator replacement, automatic fallback or publication.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import wave

from voicestudio_narrate import validate_episode, valid_wav, attach_metadata

try:  # only real SDK/API transport failures are reported as "SDK failure"; bugs stay visible
    from elevenlabs.core.api_error import ApiError
    import httpx
    SDK_ERRORS=(ApiError,httpx.HTTPError)
except ImportError:  # SDK absent: create_client() raises ImportError, reported separately
    SDK_ERRORS=()

REPO=Path(__file__).resolve().parents[4]


def load_script(path):
    source=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(source,dict) or not isinstance(source.get('speakers'),dict):
        raise ValueError('Script must define speakers and segments')
    for role,profile in source['speakers'].items():
        if not isinstance(profile,dict) or not isinstance(profile.get('voice_id'),str) or not profile['voice_id'].strip():
            raise ValueError('Each character needs a verified ElevenLabs voice_id')
        profile['profile_id']=profile['voice_id']
    return validate_episode(source)


def create_client():
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from elevenlabs_client import create_client as configured_client
    return configured_client()


def synthesize_segment(client,text,voice_id,model_id,output):
    audio=bytearray()
    for chunk in client.text_to_speech.convert(text=text,voice_id=voice_id,model_id=model_id,output_format='pcm_24000'):
        if chunk:audio.extend(chunk)
    if not audio or len(audio)%2:
        raise ValueError('ElevenLabs returned empty or incomplete 16-bit PCM')
    output=Path(output)
    temporary=output.with_suffix('.partial.wav')
    with wave.open(str(temporary),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(24000);wav.writeframes(audio)
    valid_wav(temporary.read_bytes())
    temporary.replace(output)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('script',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--model',default='eleven_v4')
    p.add_argument('--generate',action='store_true',help='Explicitly request metered ElevenLabs speech')
    p.add_argument('--force',action='store_true',help='Regenerate takes even if request/audio hashes match')
    a=p.parse_args(argv)
    try:
        source=load_script(a.script)
        if not a.model.strip():raise ValueError('model must be nonempty')
        if not a.generate:
            print(json.dumps({'status':'plan-only','engine':'elevenlabs','model':a.model,
                              'segments':len(source['segments']),'characters':sum(len(s['text']) for s in source['segments']),
                              'note':'No API request or audio generation. Voices and model require account access; --generate consumes credits.'}))
            return 0
        client=create_client()
        raw=a.out.resolve()/'elevenlabs-raw';raw.mkdir(parents=True,exist_ok=True)
        for segment in source['segments']:
            request={'text':segment['text'],'voice_id':source['speakers'][segment['speaker']]['voice_id'],
                     'model':a.model,'output_format':'pcm_24000'}
            key=hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
            wav=raw/(segment['id']+'.wav');stamp=raw/(segment['id']+'.json')
            if not a.force and wav.is_file() and stamp.is_file():
                cached=json.loads(stamp.read_text(encoding='utf-8'))
                if not isinstance(cached,dict):
                    raise ValueError('Cached take stamp is not a JSON object; inspect and regenerate with --force')
                if cached.get('request_sha256')==key:
                    valid_wav(wav.read_bytes())
                    if hashlib.sha256(wav.read_bytes()).hexdigest()!=cached.get('audio_sha256'):
                        raise ValueError('Cached audio changed; inspect and explicitly regenerate with --force')
                    continue
            synthesize_segment(client,request['text'],request['voice_id'],a.model,wav)
            stamp.write_text(json.dumps({'request_sha256':key,'audio_sha256':hashlib.sha256(wav.read_bytes()).hexdigest()}),encoding='utf-8')
        clean={'voice':{'engine':'files','speed':1.0,'chain':'none'},'lead':source.get('lead',.3),'tail':source.get('tail',.8),
               'segments':[{k:v for k,v in seg.items() if k in {'id','text','display','pause_after','scene_id'}} for seg in source['segments']]}
        native_input=a.out.resolve()/'elevenlabs-files-input.json';native_input.write_text(json.dumps(clean,indent=2),encoding='utf-8')
        subprocess.run([sys.executable,str(Path(__file__).with_name('narrate.py')),str(native_input),'--out',str(a.out.resolve()),'--engine','files','--files-dir',str(raw)],check=True)
        timing_path=a.out.resolve()/'timings.json'
        timings=attach_metadata(json.loads(timing_path.read_text(encoding='utf-8')),source,engine='elevenlabs')
        timings['elevenlabs_model']=a.model
        timing_path.write_text(json.dumps(timings,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':'generated-not-approved','out':str(a.out.resolve()),'voice_source':'elevenlabs'}))
        return 0
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print('elevenlabs_narrate: '+str(exc),file=sys.stderr);return 2
    except ImportError as exc:
        print('elevenlabs_narrate: ElevenLabs SDK unavailable ('+str(exc)+'); install requirements.txt',file=sys.stderr);return 2
    except SDK_ERRORS as exc:
        # SDK error bodies may include request details; report only status/type.
        print('elevenlabs_narrate: SDK failure '+type(exc).__name__+' status='+str(getattr(exc,'status_code',None)),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
