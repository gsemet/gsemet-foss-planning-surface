"""Round 8: refresh the stale card quotes and grep phrases of the inventories."""
import re
from pathlib import Path

EV = Path(__file__).resolve().parents[2] / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
PAIR = re.compile(r'`([\w./-]+\.md):(\d+)` "(.*?)"(?=;| \|\s*$)')
GREPS = (
    ("'Widen a grant, or approve", "'Widen a grant or approve"),
    ("'Your only git'", "'Only git'"),
    ("'branch protection unread'", "'no branch protection read'"),
)


def norm(text):
    return " ".join(text.replace(chr(92) + "|", "|").split())


for name in ("foreman", "chief-of-staff", "griller", "host-and-shared"):
    path = EV / f"cards-inventory-{name}.md"
    raw = path.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    out = []
    for line in raw.split(nl):
        for old, new in GREPS:
            if old in line:
                line = line.replace(old, new)
                print(name, line.split("|")[1].strip(), old, "->", new)

        def fresh(m):
            now = (CN / m.group(1)).read_text(encoding="utf-8").split("\n")[int(m.group(2)) - 1].strip()
            quote = m.group(3)
            if norm(now).startswith(norm(quote.rstrip("…"))):
                return m.group(0)
            if quote.endswith("…") or len(now) > 70:
                now = now[:70].rstrip() + "…" if len(now) > 70 else now
            now = now.replace("|", chr(92) + "|")
            print(name, f"{m.group(1)}:{m.group(2)} quote ->", now)
            return f'`{m.group(1)}:{m.group(2)}` "{now}"'

        if name != "host-and-shared":
            line = PAIR.sub(fresh, line)
        out.append(line)
    path.write_bytes(nl.join(out).encode("utf-8"))
