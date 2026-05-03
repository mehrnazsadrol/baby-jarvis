import ollama
from config import OLLAMA_MODEL, OLLAMA_HOST, SYSTEM_PROMPT


def generate_code(prompt: str) -> str:
    print(f"\n  🤖  Generating code with {OLLAMA_MODEL}...\n")
    print("  " + "─" * 60)

    client = ollama.Client(host=OLLAMA_HOST)
    full_response = []

    stream = client.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_response.append(token)

    print("\n  " + "─" * 60)

    return "".join(full_response).strip()
