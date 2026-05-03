import subprocess
import threading
import numpy as np
import sounddevice as sd
from openwakeword.model import Model
from config import SAMPLE_RATE, WAKE_WORD, WAKE_WORD_THRESHOLD


def _say_listening():
    subprocess.run(["say", "I'm listening"], check=False)


class WakeWordDetector:
    def __init__(self, on_detected):
        self.on_detected = on_detected
        self.running = False
        self._thread = None
        self.model = Model(wakeword_models=[WAKE_WORD], inference_framework="onnx")

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False

    def _listen_loop(self):
        chunk = 1280

        while self.running:
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="int16") as stream:
                while self.running:
                    audio, _ = stream.read(chunk)
                    pcm = audio[:, 0]
                    predictions = self.model.predict(pcm)

                    score = predictions.get(WAKE_WORD, 0.0)
                    if score >= WAKE_WORD_THRESHOLD:
                        _say_listening()
                        self.model.reset()
                        break

            if self.running:
                self.on_detected()
