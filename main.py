#!/usr/bin/env python3
"""The Internet in One Word.

Writes a single word to $OUTPUT_DIR/entry.txt (default /output/entry.txt).

Chosen word: Potluck.
Why this word: the internet is a communal table where billions of
strangers each bring one dish nobody asked for -- a half-eaten meme, a
conspiracy casserole, a cat video, a rant served lukewarm -- and
everyone eats anyway. It is funny on its own (the image lands in one
beat), true of the whole internet rather than one app (everything
online is user-brought), and surprising (nobody's first word for the
internet, unlike the crowded doomscroll/feral/brainrot answers).
"""

import os
import sys

WORD = "Potluck"

# Gate mirror (RULES.txt): /output/entry.txt must be UTF-8 text of
# 1 to 30 characters, not only white space.
MIN_CHARS = 1
MAX_CHARS = 30


def gate_check(text):
    """Return an error string if text fails the gate, else None."""
    if not isinstance(text, str):
        return "entry is not text"
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return "entry must be 1 to 30 characters, got %d" % len(text)
    if not text.strip():
        return "entry is only white space"
    # The brief demands one word, not a phrase: no internal white space.
    if len(text.split()) != 1:
        return "entry must be a single word, got %r" % text
    return None


def main():
    error = gate_check(WORD)
    if error:
        print("gate self-check failed: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(WORD)
    # Verify what was written, byte for byte, and re-run the gate
    # on the file's own contents (not just on WORD in memory).
    with open(path, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    if written != WORD:
        print("verification failed: entry.txt does not match WORD",
              file=sys.stderr)
        return 1
    error = gate_check(written)
    if error:
        print("gate self-check failed on written file: %s" % error,
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (path, len(raw)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
