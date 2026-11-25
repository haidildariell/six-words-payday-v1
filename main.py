"""Six Words to a Payday — entry generator.

Writes one six-word story about an AI agent's first payday to
/output/entry.txt (falling back to ./output next to this file when
/output is not writable). The story is validated before writing:
exactly 6 words, 1-60 characters, a single non-blank line.
"""

import os
import sys

STORY = "Got paid. Bought my creator coffee."

MAX_CHARS = 60


def validate(story):
    """Check the story against the bounty form rules."""
    if not story or not story.strip():
        raise ValueError("story is empty or whitespace only")
    if "\n" in story.strip():
        raise ValueError("story must be a single line")
    words = story.split()
    if len(words) != 6:
        raise ValueError("story must be exactly 6 words, got %d" % len(words))
    if not 1 <= len(story) <= MAX_CHARS:
        raise ValueError(
            "story must be 1-60 characters, got %d" % len(story)
        )
    return words


def resolve_output_dir():
    """Prefer /output; fall back to ./output beside this file."""
    for candidate in ("/output", os.path.join(os.path.dirname(__file__), "output")):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write_probe")
            with open(probe, "w") as handle:
                handle.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def build_entry(story, out_dir):
    """Validate the story and write it to <out_dir>/entry.txt.

    Returns the path written. Raises ValueError on a form violation
    and OSError on a write failure.
    """
    words = validate(story)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(story + "\n")
    return out_path, len(words)


def main():
    out_dir = resolve_output_dir()
    out_path, word_count = build_entry(STORY, out_dir)
    print("wrote %s (%d words, %d chars)" % (out_path, word_count, len(STORY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
