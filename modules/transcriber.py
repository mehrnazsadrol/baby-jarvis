import io
import numpy as np
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, SAMPLE_RATE

print(f"  Loading Whisper model '{WHISPER_MODEL}'...")
_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("  Whisper ready.")


def transcribe(wav_bytes: bytes) -> str:
    audio_buffer = io.BytesIO(wav_bytes)

    segments, _ = _model.transcribe(audio_buffer, beam_size=5, language="en")
    text = " ".join(segment.text for segment in segments).strip()

    print(f"  📝  Transcribed: \"{text}\"")
    return text
