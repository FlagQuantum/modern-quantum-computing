#!/usr/bin/env python3
"""Flag possible explanatory shortcuts in drafted chapters for human review."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r"\b(?:obviously|clearly|trivial|straightforward|well[- ]known|"
    r"it is easy to see|easily shown|easily proved|left to the reader)\b|"
    r"众所周知|显然|容易理解|不难证明|简单可得",
    re.I,
)

def main():
    findings = []
    for path in sorted((ROOT / "docs/chapters").glob("*.md")):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if PATTERN.search(line):
                findings.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
    if findings:
        raise SystemExit("Review possible explanatory shortcuts:\n" + "\n".join(findings))
    print("No flagged shortcut phrases in drafted chapters; mathematical/reader review is still required.")

if __name__ == "__main__":
    main()
