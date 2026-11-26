# Evidence 10: no broken relative link

Worktree `batch-31-CR-510`, uncommitted tree (base `88d9ab40`), 2026-11-26. `$W` is the worktree,
`$S` the CR folder's `work/scratch`.

The throwaway script, not committed, is `$S/links.py` (full text below). It reads every tracked or
new file matching `skills/**/*.md`, `agents/**`, `com.github.copilot/agents/**`, `README.md`,
`CONTRIBUTING.md`, `docs/**/*.md` and `evals/**/*.md`, takes each Markdown link, reference
definition and HTML `href`/`src` outside code blocks and code spans, and resolves each relative one
(the file, and the heading for a `#anchor` on a Markdown target). A link with a scheme is not
relative and is not fetched.

## Result at head

`uv run --no-sync --project $W python -I -B $S/links.py $W`, exit 0:

```text
files read: 617
relative links resolved: 311
broken: 0
links into cards-next/: 0
```

## Before round 2's docs fixes

The same script on round 1's tree (616 files, `docs/incidents.md` not yet added) found 279 relative
links, 4 broken, 0 into `cards-next/`:

| File | Broken target |
| --- | --- |
| `CONTRIBUTING.md` | `chief-of-staff-batch-start.md` |
| `docs/release-process.md` | `#visible-evidence` |
| `docs/use-cases.md` | `#a-chief-of-staff-and-grillers-in-remote` |
| `evals/ticket-summary/RUNBOOK.md` | `chief-of-staff-grill.md` |

All four are fixed at head.

## Links rewritten under D5

None. D5 covers a relative link to a removed file in `docs/release-notes/**` and
`evals/results/**`: there is none (no file there changes in this PR, and the run above, which reads
their Markdown files, finds no broken link). The one link of the release notes to a removed card
(`docs/release-notes/2026-11-18-v0.13.0/release-notes.md:34`, `session-start.md`) already points at
the tag `v0.13.0`.

## The script

```python
"""CR-510 evidence 10: every relative link of the docs and cards, resolved in the tree at the cwd.

Usage: python links.py <repository root>
Files: skills/**/*.md, agents/**, com.github.copilot/agents/**, README.md, CONTRIBUTING.md,
docs/**/*.md, evals/**/*.md (tracked or new, not ignored). A link is `[text](target)`,
`[label]: target`, or an HTML href/src. A target with a scheme is not relative. A `#anchor` on a
Markdown target (or on the same file) must match a heading of it, as GitHub builds the anchor.
"""

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

root = Path(sys.argv[1]).resolve()
listed = subprocess.run(
    ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
    check=True, capture_output=True, encoding="utf-8",
).stdout.split("\0")
SCOPE = re.compile(
    r"^(skills/.*\.md|agents/.*\.md|com\.github\.copilot/agents/.*\.md|README\.md"
    r"|CONTRIBUTING\.md|docs/.*\.md|evals/.*\.md)$"
)
files = sorted(f for f in listed if SCOPE.match(f) and (root / f).is_file())
INLINE = re.compile(r"\]\(\s*<?([^()<>\s]+(?:\([^()\s]*\))?[^()<>\s]*)>?(?:\s+\"[^\"]*\")?\s*\)")
REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+\"[^\"]*\")?\s*$", re.M)
HTML = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
FENCE = re.compile(r"^(\s*)(```|~~~).*?^\1\2\s*$", re.M | re.S)
CODE = re.compile(r"(`+)(?:(?!\1).)+?\1", re.S)


def anchors(path: Path) -> set[str]:
    text = FENCE.sub("", path.read_text(encoding="utf-8-sig"))
    seen: dict[str, int] = {}
    out = set(re.findall(r"""<a\s+(?:name|id)=["']([^"']+)["']""", text))
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m[1]).replace("`", "")
        slug = re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        out.add(slug if n == 0 else f"{slug}-{n}")
    return out


broken: list[str] = []
into_staging: list[str] = []
count = 0
for name in files:
    source = root / name
    raw = source.read_text(encoding="utf-8-sig")
    text = CODE.sub("``", FENCE.sub("", raw))
    for target in INLINE.findall(text) + REFDEF.findall(text) + HTML.findall(text):
        if "cards-next" in target:
            into_staging.append(f"{name}: {target}")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:|^//", target):
            continue
        count += 1
        path_part, _, anchor = target.partition("#")
        path_part = unquote(path_part.split("?")[0])
        if not path_part:
            dest = source
        elif path_part.startswith("/"):
            dest = root / path_part.lstrip("/")
        else:
            dest = source.parent / path_part
        if not dest.exists():
            broken.append(f"{name}: {target} (no such file)")
        elif anchor and dest.suffix == ".md" and unquote(anchor) not in anchors(dest):
            broken.append(f"{name}: {target} (no such heading)")

print(f"files read: {len(files)}")
print(f"relative links resolved: {count}")
print(f"broken: {len(broken)}")
for line in broken:
    print(f"  {line}")
print(f"links into cards-next/: {len(into_staging)}")
for line in into_staging:
    print(f"  {line}")
sys.exit(1 if broken or into_staging else 0)
```
