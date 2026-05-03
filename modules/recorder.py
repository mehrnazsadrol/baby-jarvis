import io
import numpy as np
import sounddevice as sd
import webrtcvad
import wave
from config import SAMPLE_RATE, CHANNELS, SILENCE_DURATION_SEC, MAX_RECORD_SEC


def record_until_silence() -> bytes:
    vad = webrtcvad.Vad(2)

    frame_duration_ms = 30 
    frame_samples = int(SAMPLE_RATE * frame_duration_ms / 1000)

    recorded_frames = []
    silence_frames = 0
    silence_limit = int(SILENCE_DURATION_SEC * 1000 / frame_duration_ms)
    max_frames = int(MAX_RECORD_SEC * 1000 / frame_duration_ms)

    print("  🎙  Recording... (speak now)")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16") as stream:
        while len(recorded_frames) < max_frames:
            audio_chunk, _ = stream.read(frame_samples)
            pcm = audio_chunk.tobytes()
            recorded_frames.append(pcm)

            is_speech = vad.is_speech(pcm, SAMPLE_RATE)
            if not is_speech:
                silence_frames += 1
            else:
                silence_frames = 0

            if silence_frames >= silence_limit and len(recorded_frames) > silence_limit:
                break

    print("  ✅  Recording complete.")

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(recorded_frames))
    wav_buffer.seek(0)
    return wav_buffer.read()
