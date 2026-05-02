"""
transcriber.py — Transcribes WAV bytes to text using faster-whisper (local).
"""

import io
import numpy as np
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, SAMPLE_RATE

# Load once at import time
print(f"  Loading Whisper model '{WHISPER_MODEL}'...")
_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("  Whisper ready.")


def transcribe(wav_bytes: bytes) -> str:
    """
    Transcribe WAV bytes to a string.
    Returns the transcription text, stripped of leading/trailing whitespace.
    """
    # faster-whisper can accept a file-like object
    audio_buffer = io.BytesIO(wav_bytes)

    segments, _ = _model.transcribe(audio_buffer, beam_size=5, language="en")
    text = " ".join(segment.text for segment in segments).strip()

    print(f"  📝  Transcribed: \"{text}\"")
    return text
