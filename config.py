# voice-to-code configuration

# Wake word (phrase openwakeword will listen for)
WAKE_WORD = "hey_jarvis"  # openwakeword built-in model; see docs to add custom phrases

# Silence detection: stop recording after this many seconds of silence
SILENCE_DURATION_SEC = 1.5

# Max recording duration in seconds (safety cap)
MAX_RECORD_SEC = 30

# Whisper model size: "tiny", "base", "small", "medium", "large"
WHISPER_MODEL = "base"

# Ollama model to use for code generation
OLLAMA_MODEL = "deepseek-coder:6.7b"

# Ollama host (default local)
OLLAMA_HOST = "http://localhost:11434"

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1

# Wake word detection sensitivity (0.0 - 1.0)
WAKE_WORD_THRESHOLD = 0.5

# System prompt for code generation
SYSTEM_PROMPT = (
    "You are an expert programmer. The user will describe what they want in plain English. "
    "Respond with ONLY the raw code — no markdown, no code fences, no explanation. "
    "Use the most appropriate programming language for the task described. "
    "If a language is specified, use that language."
)
