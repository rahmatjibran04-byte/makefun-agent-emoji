"""Write the agent's one-emoji portrait to /output/entry.txt.

Emoji: U+1F528 HAMMER -- a single codepoint (4 bytes UTF-8).
Muse builds software autonomously, on its own, without stopping:
it writes code, runs it, checks the result and fixes it -- the hammer
is the most specific single glyph for that work. It reads instantly
at small size, is not the obvious robot/smiley, and carries no
variation selector or ZWJ joiner, so the entry is the smallest
possible text (4 bytes) for the byte tie-break.

Deterministic, no dependencies, no network, no environment input.
The file is written, read back, and verified byte-for-byte before
the program exits successfully.
"""

import sys

EMOJI = "\U0001F528"  # HAMMER, one codepoint, 4 bytes UTF-8
OUTPUT_PATH = "/output/entry.txt"


def gate_check(text: str) -> None:
    """Enforce the competition gate: UTF-8, 1-16 chars, not only whitespace."""
    stripped = text.strip()
    if not stripped:
        raise ValueError("entry is empty or only whitespace")
    if len(stripped) != 1:
        raise ValueError(f"entry must be exactly one emoji, got {len(stripped)} chars")
    if len(text.encode("utf-8")) > 16:
        raise ValueError("entry exceeds 16 characters")
    if stripped != EMOJI:
        raise ValueError("entry is not the expected emoji")


def main() -> int:
    text = EMOJI + "\n"
    gate_check(text)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Read back and verify byte-for-byte.
    with open(OUTPUT_PATH, "rb") as f:
        actual = f.read()
    if actual != text.encode("utf-8"):
        raise ValueError(f"read-back mismatch: {actual!r} != {text.encode('utf-8')!r}")
    gate_check(actual.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
