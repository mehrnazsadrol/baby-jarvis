# Voice-to-Code Agent — Project Context

## What this project does
A fully local voice-to-code agent. The user says a wake word ("hey jarvis"), speaks
a natural-language code request, and the agent transcribes it (Whisper), generates
code (Ollama), and copies the result to the clipboard.

## Architecture decisions (already decided — do not change without reason)
| Decision | Choice | Reason |
|---|---|---|
| Wake word | openwakeword | Fully local, open source, no API key |
| Audio recording | sounddevice + numpy | Lightweight, cross-platform |
| Silence detection | webrtcvad | Stops recording when user stops talking |
| Speech-to-text | faster-whisper (base model) | Local Whisper, lower memory than openai-whisper |
| Code generation | Ollama (deepseek-coder:6.7b) | Fully offline LLM, good code quality |
| Output | pyperclip (clipboard) | User can paste code anywhere |

## Project structure
```
voice-to-code/
├── main.py              # Entry point / main loop
├── config.py            # All settings (wake word, model, timeouts, etc.)
├── modules/
│   ├── wake_word.py     # openwakeword continuous listener + beep on detection
│   ├── recorder.py      # sounddevice recording + webrtcvad silence detection
│   ├── transcriber.py   # faster-whisper transcription (loads model once)
│   ├── code_gen.py      # Ollama streaming code generation
│   └── output.py        # pyperclip clipboard copy + terminal preview
└── requirements.txt
```

## Status: scaffold complete, implementation pending

All files are created with full logic. The next steps are:

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Pull the Ollama model
```bash
ollama pull deepseek-coder:6.7b
```

### 3. Test each module in isolation before running main.py
- Test recorder: run `python -c "from modules.recorder import record_until_silence; record_until_silence()"`
- Test transcriber: pass a WAV file through transcriber.py
- Test code_gen: call generate_code("write a hello world in Python")
- Test wake word: confirm openwakeword loads the hey_jarvis model

### 4. Known issues to resolve
- `openwakeword` requires the `hey_jarvis` ONNX model to be available locally.
  If it fails to load, replace WAKE_WORD in config.py with another built-in model
  (see: https://github.com/dscripka/openWakeWord#pre-trained-models)
- `webrtcvad` needs 16kHz int16 mono audio — recorder.py is already configured for this.
- On macOS, `pyperclip` may require `pbcopy` (built-in) — should work out of the box.
- On Linux, install `xclip` or `xsel` for pyperclip: `sudo apt install xclip`

### 5. Enhancements to consider (not yet implemented)
- [ ] Add language detection / multi-language support in transcriber.py
- [ ] Support custom wake word training via openwakeword
- [ ] Add a config flag to also save generated code to a timestamped .py file
- [ ] Stream Whisper output for faster perceived response time
- [ ] Add a GUI tray icon showing agent status (listening / recording / generating)

## Config reference (config.py)
| Key | Default | Description |
|---|---|---|
| WAKE_WORD | hey_jarvis | openwakeword model name |
| SILENCE_DURATION_SEC | 1.5 | Seconds of silence before stopping recording |
| MAX_RECORD_SEC | 30 | Hard cap on recording length |
| WHISPER_MODEL | base | tiny/base/small/medium/large |
| OLLAMA_MODEL | deepseek-coder:6.7b | Any model available in local Ollama |
| OLLAMA_HOST | http://localhost:11434 | Ollama server address |
| WAKE_WORD_THRESHOLD | 0.5 | Detection confidence (0.0–1.0) |

## How to run
```bash
cd voice-to-code
python main.py
```
Then say: **"hey jarvis"** → wait for beep → speak your request.
