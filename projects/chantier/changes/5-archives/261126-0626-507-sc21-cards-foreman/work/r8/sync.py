"""Round 8: after rehome.py, the FM-102 and FM-155 suffixes, the host-and-shared home tables, the
closing quotes and the counts (run once)."""
import re
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
EV = CR / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"


def load(name):
    raw = (EV / name).read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.split(nl), nl


def save(name, lines, nl):
    (EV / name).write_bytes(nl.join(lines).encode("utf-8"))


def once(lines, old, new):
    at = [i for i, x in enumerate(lines) if old in x]
    assert len(at) == 1 and lines[at[0]].count(old) == 1, (old, at)
    lines[at[0]] = lines[at[0]].replace(old, new)


# Foreman
f, nl = load("cards-inventory-foreman.md")
once(f, "| e | topic ready-asks | help ready-asks |", "| e | topic ready-asks; the rule it applies: card foreman.md:15 | help ready-asks |")
at = next(i for i, x in enumerate(f) if x.startswith("| FM-155 | foreman.md"))
f[at] = "| FM-155 | foreman.md:383 | topic wakes; no rule: how the Foreman keeps a turn short |"
at = next(i for i, x in enumerate(f) if x.startswith("| FM-155 | foreman |"))
assert "| e | topic wakes | help wakes |" in f[at]
f[at] = f[at].replace("| e | topic wakes | help wakes |", "| e | topic wakes; no rule: how the Foreman keeps a turn short | help wakes |")
at = next(i for i, x in enumerate(f) if x.startswith("| FM-105 | foreman.md") )
f.insert(at, "| FM-102 | foreman.md:290-293 | topic ready-asks; the rule it applies: card foreman.md:15 |")
once(f, "65 rows (kind e) say never", "66 rows (kind e) say never") if any("65 rows (kind e)" in x for x in f) else None
once(f, "63 name, after", "62 name, after")
once(f, "2 hold no rule of their own", "3 hold no rule of their own")
once(f, "1 are held by no card, floor or refusal", "1 is held by no card, floor or refusal")
save("cards-inventory-foreman.md", f, nl)

# Chief of Staff
c, nl = load("cards-inventory-chief-of-staff.md")
once(c, "337 rows (kind e) say never", "333 rows (kind e) say never")
once(c, "236 name, after", "235 name, after")
once(c, "98 hold no rule of their own", "96 hold no rule of their own")
once(c, "3 are held by no card, floor or refusal (`gap:`: C-006, C-304, C-885)", "2 are held by no card, floor or refusal (`gap:`: C-304, and C-885 for the user's word on another session's Driver)")
once(c, "337 protecting-looking rows carried by a topic.", "333 protecting-looking rows carried by a topic.")
once(c, "grep -c 'Take the seat or act as' chief-of-staff.md", "grep -c 'Take the seat, or act as' chief-of-staff.md")
save("cards-inventory-chief-of-staff.md", c, nl)

# Host and shared: the two home tables without a check column, then the kind a quotes
h, nl = load("cards-inventory-host-and-shared.md")
homes = {}
section = None
for i, line in enumerate(h):
    if line.startswith("## "):
        section = line
    parts = re.split(SEP, line)
    rid = parts[1].strip() if len(parts) > 3 else ""
    if not re.fullmatch(r"H-\d+", rid):
        continue
    if len(parts) == 10:
        homes[rid] = parts[7].strip()
    elif section.startswith(("## Protecting-looking rows not", "## Inferable rows")):
        old = parts[3].strip()
        if old != homes[rid]:
            print(section, rid, old, "->", homes[rid])
            parts[3] = f" {homes[rid]} "
            h[i] = "|".join(parts)
    elif section.startswith("## Protecting rows and"):
        home = homes[rid]
        found = re.match(r"card ([\w./-]+\.md):(\d+)", home)
        quote = parts[4].strip()
        parts[3] = f" {home} "
        if found and rid in ("H-057", "H-059"):
            lines = (CN / found.group(1)).read_text(encoding="utf-8").split("\n")
            parts[4] = " " + lines[int(found.group(2)) - 1].strip().replace("|", chr(92) + "|") + " "
            print(rid, parts[4])
        h[i] = "|".join(parts)
save("cards-inventory-host-and-shared.md", h, nl)
