#!/usr/bin/env python3
"""One Line, Big Laugh — make.fun entry.

Writes one funny line to /output/entry.txt. The line is the whole
entry: a bank phones to praise the reader for saving money, then
charges a fee for the phone call itself — the congratulation was
the sales pitch for the charge.

Deterministic by design: standard library only, no network, no
randomness, no clock reads. Every run writes byte-identical output.
"""

import os
import sys

# The joke in two clauses, joined with a single space. The setup
# sounds like good news (the bank noticed the saving); the punchline
# turns it (the call that delivered the praise is itself billable).
# Neither clause is funny alone — the turn is the joke.
_CLAUSES = (
    "My bank called to congratulate me on saving money,",
    "then charged me a fee for the phone call.",
)

# Competition ceiling for the single line (kit RULES.txt gate: 1-200).
MAX_LINE_CHARS = 200


def build_line() -> str:
    """Assemble the one-line laugh from its clauses.

    The result must be exactly one line: a stray newline would
    silently break the entry format, so fail loudly instead of
    writing a malformed file.
    """
    line = " ".join(_CLAUSES)
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    if not line.strip():
        raise ValueError("line must not be only white space")
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
