"""
main.py — Voice-to-Code Agent entry point.

Flow:
  [always listening] → wake word "hey jarvis" → 🔔 beep
  → record until silence → transcribe (Whisper) → generate code (Ollama)
  → copy to clipboard ✓ → back to listening
"""

import sys
import threading
from modules.wake_word import WakeWordDetector
from modules.recorder import record_until_silence
from modules.transcriber import transcribe
from modules.code_gen import generate_code
from modules.output import copy_to_clipboard
from config import WAKE_WORD

# Prevent overlapping triggers
_processing = threading.Lock()


def on_wake_word():
    """Called by WakeWordDetector when the wake phrase is heard."""
    if not _processing.acquire(blocking=False):
        return  # already processing, ignore

    try:
        print("\n" + "═" * 64)
        print(f"  👂  Wake word detected! Listening for your request...")

        wav_bytes = record_until_silence()
        text = transcribe(wav_bytes)

        if not text:
            print("  ⚠️  Nothing transcribed. Try again.")
            return

        code = generate_code(text)

        if not code:
            print("  ⚠️  No code generated. Try rephrasing.")
            return

        copy_to_clipboard(code)
        print("  🟢  Ready — say the wake word to go again.")
        print("═" * 64 + "\n")

    except Exception as e:
        print(f"  ❌  Error: {e}")
    finally:
        _processing.release()


def main():
    print("\n" + "═" * 64)
    print("  🎤  Voice-to-Code Agent")
    print(f"  Wake word : \"{WAKE_WORD.replace('_', ' ')}\"")
    print("  Output    : clipboard")
    print("  Press Ctrl+C to quit.")
    print("═" * 64 + "\n")

    detector = WakeWordDetector(on_detected=on_wake_word)
    detector.start()
    print("  👂  Listening for wake word...\n")

    try:
        threading.Event().wait()  # block main thread forever
    except KeyboardInterrupt:
        print("\n  Shutting down. Goodbye!")
        detector.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
