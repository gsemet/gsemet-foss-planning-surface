"""Every `file:line` "quoted start" of the foreman, chief-of-staff and griller inventories, against
the cards now."""

import re
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
EV = Path(__file__).resolve().parents[2] / "evidence"
PAIR = re.compile(r'`([\w./-]+\.md):(\d+)` "(.*?)"(?=;| \|\s*$)')


def norm(text: str) -> str:
    return " ".join(text.replace("\\|", "|").split())


for name in ("foreman", "chief-of-staff", "griller"):
    path = EV / f"cards-inventory-{name}.md"
    seen, bad = 0, {}
    for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        for rel, n, quote in PAIR.findall(line):
            seen += 1
            card = CN / rel
            if not card.exists():
                bad.setdefault((rel, n, quote, "no file"), []).append(i)
                continue
            lines = card.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
            now = lines[int(n) - 1] if int(n) <= len(lines) else ""
            if not norm(now).startswith(norm(quote.rstrip("…"))):
                bad.setdefault((rel, n, quote, norm(now)), []).append(i)
    print(f"{path.name}: {seen} quotes, {sum(map(len, bad.values()))} stale")
    for (rel, n, quote, now), at in bad.items():
        print(f"  {rel}:{n} at lines {at}\n    quoted: {quote}\n    now:    {now[:160]}")
