import pyperclip


def copy_to_clipboard(code: str):
    pyperclip.copy(code)

    preview_lines = code.splitlines()[:5]
    preview = "\n    ".join(preview_lines)
    if len(code.splitlines()) > 5:
        preview += f"\n    ... ({len(code.splitlines())} lines total)"

    print("\n  📋  Copied to clipboard!")
    print(f"  Preview:\n    {preview}\n")
