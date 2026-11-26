"""LF bytes and line endings of the files this round touches."""

import sys
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
names = sys.argv[1:] or [
    "foreman.md",
    "chief-of-staff.md",
    "inspector.md",
    "cr-driver.md",
    "stack-driver.md",
    "release-driver.md",
    "conflict-resolver.md",
    "concepts.md",
    "hosts/claude-code.md",
]
for name in names:
    raw = (CN / name).read_bytes()
    crlf = raw.count(b"\r\n")
    lf = len(raw) - crlf
    bom = raw.startswith(b"\xef\xbb\xbf")
    print(f"{name}: {lf:,} LF bytes; {raw.count(b'\n')} lines, {crlf} CRLF; bom={bom}")
