# Baby Jarvis

A fully local voice-to-code agent. Say "hey jarvis", speak a natural-language code request, and the generated code is copied to your clipboard — no cloud APIs, no API keys.

**Pipeline:** wake word → record → Whisper (transcribe) → Ollama (generate) → clipboard

---

## Requirements

- Python 3.13
- [Ollama](https://ollama.com) installed and running locally

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/baby-jarvis.git
cd baby-jarvis
```

### 2. Install Ollama

Download and install from [ollama.com](https://ollama.com), then start the server:

```bash
ollama serve
```

In a separate terminal, pull the code generation model:

```bash
ollama pull deepseek-coder:6.7b
```

### 3. Create a virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Download wake word models

```bash
python3 -c "from openwakeword.utils import download_models; download_models()"
```

---

## Usage

```bash
source .venv/bin/activate
python3 main.py
```

Say **"hey jarvis"**, wait for the beep, then speak your request. The generated code is copied to your clipboard.

---

## Configuration

All settings are in `config.py`:

| Key | Default | Description |
|---|---|---|
| `WAKE_WORD` | `hey_jarvis` | Wake word model name |
| `WHISPER_MODEL` | `base` | Whisper model size (`tiny`/`base`/`small`/`medium`/`large`) |
| `OLLAMA_MODEL` | `deepseek-coder:6.7b` | Any model available in local Ollama |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server address |
| `SILENCE_DURATION_SEC` | `1.5` | Seconds of silence before stopping recording |
| `WAKE_WORD_THRESHOLD` | `0.5` | Detection sensitivity (0.0–1.0) |

---

## Platform notes

- **macOS**: grant microphone access to your terminal when prompted.
- **Linux**: install `xclip` for clipboard support — `sudo apt install xclip`.
