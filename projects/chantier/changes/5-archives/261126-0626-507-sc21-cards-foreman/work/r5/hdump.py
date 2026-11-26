"""Dump each unit with the best match in the new set, for the hand table (work/r5/h/*.py)."""

import json
import re
from pathlib import Path

import hsplit

HERE = Path(__file__).parent
CN = Path(hsplit.WT) / "skills/chantier/cards-next"
CARDS = (
    "chief-of-staff coder conflict-resolver cr-driver debugger demo-explorer foreman griller "
    "griller-skill inspector investigator qa-driver release-driver retro-critic spec-critic "
    "spec-writer stack-driver verifier floor"
).split()


def tok(t):
    return re.findall(r"[a-z0-9_][a-z0-9_-]{2,}", t.lower())


def idx(text):
    w = tok(text)
    return set(w), set(zip(w, w[1:]))


def score(w, bg, other):
    if not w:
        return 0.0
    s1 = len(w & other[0]) / len(w)
    s2 = len(bg & other[1]) / len(bg) if bg else s1
    return 0.5 * s1 + 0.5 * s2


def blocks(path: Path):
    """(line, text) windows of two lines, so a sentence wrapped differently still matches."""
    lines = path.read_text(encoding="utf-8").split("\n")
    for i in range(len(lines)):
        if lines[i].strip():
            yield i + 1, " ".join(lines[i : i + 3])


NEW = []  # (label, index)
for p in sorted(CN.rglob("*")):
    if p.suffix != ".md":
        continue
    rel = p.relative_to(CN).as_posix()
    for ln, text in blocks(p):
        NEW.append((rel, ln, idx(text)))
for host in ("claude-code", "copilot"):
    rows = json.loads((CN.parent / f"references/hosts/{host}.json").read_text(encoding="utf-8"))["rows"]
    for row in rows:
        NEW.append((f"row {host}", row["capability"], idx(" ".join(row["means"]) + " " + row["name"])))


def best(unit_text, name):
    w, bg = idx(unit_text)
    scored = [(score(w, bg, ix), rel, ln) for rel, ln, ix in NEW]
    same = max((x for x in scored if x[1] == name), default=None)
    top = max(scored, key=lambda x: x[0])
    card = max(
        (x for x in scored if x[1].removesuffix(".md") in CARDS), key=lambda x: x[0], default=None
    )
    return same, top, card


def main():
    out_dir = HERE / "h"
    out_dir.mkdir(exist_ok=True)
    for name in hsplit.SOURCES:
        lines, trig = [], None
        for i, (a, _, text, heading, _) in enumerate(hsplit.units(name), 1):
            if heading != trig:
                lines.append(f"## {heading}")
                trig = heading
            same, top, card = best(text, name)
            if same and same[0] >= 0.85:
                mark, cut = f"=:{same[2]}", 110
            else:
                rel = top[1].removeprefix("topics/")
                mark, cut = f"{rel}:{top[2]} {top[0]:.2f}", 190
                if card and card[0] >= 0.35 and card[1] != top[1]:
                    mark += f" | {card[1]}:{card[2]} {card[0]:.2f}"
            lines.append(f"{i} L{a} [{mark}] {text[:cut]}")
        slug = name.replace("/", "-").removesuffix(".md")
        (out_dir / f"{slug}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(slug, len(lines), len("\n".join(lines)))


if __name__ == "__main__":
    main()
