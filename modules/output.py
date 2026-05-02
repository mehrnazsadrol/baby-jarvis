"""
output.py — Copies generated code to the clipboard and shows a terminal preview.
"""

import pyperclip


def copy_to_clipboard(code: str):
    """Copy code to clipboard and print a confirmation with preview."""
    pyperclip.copy(code)

    preview_lines = code.splitlines()[:5]
    preview = "\n    ".join(preview_lines)
    if len(code.splitlines()) > 5:
        preview += f"\n    ... ({len(code.splitlines())} lines total)"

    print("\n  📋  Copied to clipboard!")
    print(f"  Preview:\n    {preview}\n")
