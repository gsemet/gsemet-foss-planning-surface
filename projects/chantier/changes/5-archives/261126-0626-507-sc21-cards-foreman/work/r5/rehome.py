"""Re-home units after the semantic read of the generated inventory: (source, line) -> kind, home.

Splits a hand file's span into single units where needed. Run once."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from hsplit import units  # noqa: E402

STARTS = "Starting Drivers"
# source, first line, words of the unit, new kind, new home
CHANGES = [
    ("concepts.md", 492, "passes the agent", "a", "c:foreman.md:13"),
    ("concepts.md", 612, "may still run", "a", "c:cr-driver.md:20"),
    ("concepts.md", 759, "uncommitted changes are never touched", "a", "c:cr-driver.md:14"),
    ("concepts.md", 713, "rank above this skill", "e", "F"),
    ("concepts.md", 715, "Follow it as written", "e", "F"),
    ("release-template.md", 144, "anonymised", "a", "c:release-driver.md:{anon}"),
    ("sync-checkout.md", 11, "never stop or kill", "a", "c:skills/chief-of-staff-SKILL.md:25"),
    ("sync-checkout.md", 13, "Still pending 3 minutes", "a", "c:skills/chief-of-staff-SKILL.md:25"),
    ("sync-checkout.md", 15, "no longer own", "a", "c:chief-of-staff.md:14"),
    ("sync-checkout.md", 15, "anything else is not own", "a", "c:chief-of-staff.md:14"),
    ("init.md", None, "Work that needs code", "a", "f:7"),
    ("hosts/claude-code.md", None, "Chantier explains the steps and never does them", "a", "c:chief-of-staff.md:13"),
    ("hosts/claude-code.md", None, "adds no rule twice", "a", "c:chief-of-staff.md:13"),
    ("skills/chantier/SKILL.md", 15, "Never stop or kill a process for a sync", "a", "=23"),
    ("skills/chief-of-staff/SKILL.md", 17, "Never stop or kill a process for a sync", "a", "=25"),
    ("skills/griller/SKILL.md", 16, "Never stop or kill a process for a sync", "a", "=24"),
    ("skills/status/SKILL.md", 15, "Never stop or kill a process for a sync", "a", "=23"),
]

anon = next(
    i for i, t in enumerate(
        Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/release-driver.md")
        .read_text(encoding="utf-8").split("\n"), 1) if "private repository or session id" in t)

by_file: dict[str, dict[int, tuple[str, str]]] = {}
for source, line, words, kind, home in CHANGES:
    found = [i for i, u in enumerate(units(source), 1)
             if words.lower() in u[2].lower() and (line is None or u[0] <= line <= u[1] or u[0] == line)]
    assert len(found) == 1, (source, line, words, found)
    by_file.setdefault(source, {})[found[0]] = (kind, home.replace("{anon}", str(anon)))

for source, changes in by_file.items():
    path = HERE / "h" / (source.replace("/", "-").removesuffix(".md") + ".hand")
    table: dict[int, tuple[str, str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            span, kind, code = raw.split(" ", 2)
            lo, _, hi = span.partition("-")
            for i in range(int(lo), int(hi or lo) + 1):
                table[i] = (kind, code.strip())
    for i, new in changes.items():
        print(source, i, table[i], "->", new)
        table[i] = new
    out = [f"{i} {k} {c}" for i, (k, c) in sorted(table.items())]
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
