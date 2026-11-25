"""Round 8: refresh the stale citations cite_check.py found (run once)."""
import re
from pathlib import Path

EV = Path(__file__).resolve().parents[2] / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"
QUOTES = "H-048 H-049 H-122 H-175 H-191 H-333 H-428 H-993 H-999 H-1288 H-1360".split()
SWAPS = {
    "FM-008": (("card foreman.md:9", "card foreman.md:10"), ("grep -c 'batch' foreman.md", "grep -c 'After compaction reread your brief' foreman.md")),
    "H-892": (("sync-checkout.md:17", "sync-checkout.md:18"),),
    "H-910": (("sync-checkout.md:18", "sync-checkout.md:19"),),
    "H-914": (("sync-checkout.md:18", "sync-checkout.md:19"),),
    "C-1161": (("topic grill-backlog-p2", "topic grill-backlog"),),
}
done = []
for name in ("foreman", "chief-of-staff", "host-and-shared"):
    path = EV / f"cards-inventory-{name}.md"
    raw = path.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    section = ""
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line
        parts = re.split(SEP, line)
        rid = parts[1].strip() if len(parts) > 3 else ""
        if rid in SWAPS:
            for old, new in SWAPS[rid]:
                if old in line:
                    line = line.replace(old, new)
                    done.append((rid, old))
            lines[i] = line
            parts = re.split(SEP, line)
        if rid in QUOTES and section.startswith("## Protecting rows and") and len(parts) == 6:
            found = re.match(r"card ([\w./-]+\.md):([\d, ]+)", parts[3].strip())
            card = (CN / found.group(1)).read_text(encoding="utf-8").split("\n")
            now = " / ".join(card[int(n) - 1].strip() for n in found.group(2).split(",") if n.strip())
            now = now.replace("|", chr(92) + "|")
            old = parts[4].strip()
            if old.endswith("..."):
                size = len(old) - 3
                now = now[:size].rstrip() + " ..." if len(now) > size else now
            parts[4] = f" {now} "
            lines[i] = "|".join(parts)
            done.append((rid, "quote"))
    path.write_bytes(nl.join(lines).encode("utf-8"))
print(done)
