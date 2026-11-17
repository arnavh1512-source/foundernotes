"""Private environment-backed ElevenLabs SDK client for FounderNotes."""
import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs


def create_client():
    load_dotenv(Path(__file__).resolve().parent / '.env.local', override=False)
    if not os.environ.get('ELEVENLABS_API_KEY'):
        raise ValueError('Configure ELEVENLABS_API_KEY privately before generation')
    return ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
