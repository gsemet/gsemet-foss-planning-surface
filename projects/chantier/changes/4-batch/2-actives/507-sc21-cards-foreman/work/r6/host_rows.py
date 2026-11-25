"""Round 6: edit rows of the host-and-shared inventory, then rebuild its closing lists and counts.

The closing lists follow work/r5/gen.py (same cells, same cuts, same patterns). Run once; it
stops if a row is not in the state it expects. `--check` rebuilds in memory and reports the
differences without writing.
"""

import collections
import re
import sys
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
CR = Path(__file__).resolve().parents[2]
OUT = CR / "evidence/cards-inventory-host-and-shared.md"
CHECK = "--check" in sys.argv

G = "`grep -c -F '{}' {}`"
EDITS = {
    "H-398": {"home": "topic worker-shell", "check": "`help worker-shell`"},
    "H-403": {"check": G.format("In Foreman mode, message or stop a Driver", "chief-of-staff.md")
              + "; the restart: `concepts.md:121`; fresh workers: `cr-driver.md:5`, `stack-driver.md:5`"},
    "H-404": {"role": "cr-driver", "kind": "a", "home": "card cr-driver.md:5",
              "check": G.format("Each round gets fresh workers", "cr-driver.md") + "; a stack: "
              + G.format("Each move gets fresh workers", "stack-driver.md")},
    "H-405": {"role": "cr-driver", "kind": "a", "home": "card cr-driver.md:5",
              "check": G.format("never wrote the change", "cr-driver.md") + "; a stack: "
              + G.format("never wrote the change", "stack-driver.md") + "; the Verifier: `verifier.md:3`"},
    "H-406": {"role": "chief-of-staff", "kind": "a",
              "check": G.format("In Foreman mode, message or stop a Driver", "chief-of-staff.md")},
    "H-409": {"role": "inspector", "kind": "a", "check": G.format("never fix it there", "inspector.md")},
    "H-416": {"home": "card cr-driver.md:15",
              "check": G.format("publish by any way but", "cr-driver.md")
              + " (`$CHANTIER push` sends one form, `--force-with-lease=<branch>:<expected>`: `commands/push.py`)"},
    "H-419": {"home": "card cr-driver.md:15",
              "check": G.format("publish by any way but", "cr-driver.md")
              + " (`$CHANTIER push` sends one form, `--force-with-lease=<branch>:<expected>`: `commands/push.py`)"},
    "H-421": {"role": "cr-driver", "home": "card cr-driver.md:16",
              "check": G.format("rebase-merges", "cr-driver.md")
              + "; also `stack-driver.md:16`, `release-driver.md:16`, `conflict-resolver.md:11`; rebase only: floor 2"},
    "H-425": {"home": "refusal ship, holds a merge commit",
              "check": "run the command: the CLI refuses (the ban on making one: `conflict-resolver.md:11`, "
              "`stack-driver.md:7`; no card names the forge's button)"},
}
COLS = ["id", "role", "trigger", "behaviour", "source", "kind", "home", "check"]


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def lines_of(rel: str) -> list[str]:
    return (CN / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def cell(text: str, cut: int = 240) -> str:
    text = " ".join(text.split())
    if len(text) > cut:
        text = text[:cut].rsplit(" ", 1)[0] + " ..."
    return text.replace("|", "\\|")


raw = OUT.read_bytes()
assert b"\r\n" not in raw and not raw.startswith(b"\xef\xbb\xbf")
doc = raw.decode("utf-8").split("\n")
start = doc.index("## Protecting rows and their homes")
rows, done = [], set()
for i, line in enumerate(doc[:start]):
    if not re.match(r"\| H-\d+ \|", line):
        continue
    c = cells(line)
    assert len(c) == 8, line[:60]
    r = dict(zip(COLS, c))
    if r["id"] in EDITS:
        r.update(EDITS[r["id"]])
        new = "| " + " | ".join(r[k] for k in COLS) + " |"
        if new != line:
            print("row", r["id"], "->", r["role"], "|", r["kind"], "|", r["home"], "|", r["check"])
        doc[i] = new
        done.add(r["id"])
    r["home"] = r["home"].replace("\\|", "|")
    rows.append(r)
assert done == set(EDITS), set(EDITS) - done
assert len({r["id"] for r in rows}) == len(rows)


def section(title: str) -> tuple[int, int]:
    a = doc.index(title)
    b = next(i for i in range(a + 1, len(doc)) if doc[i].startswith("## "))
    return a, b


def replace(title: str, body: list[str]) -> None:
    a, b = section(title)
    old = doc[a:b]
    new = [title, ""] + body + [""]
    gone = [x for x in old if x not in new]
    came = [x for x in new if x not in old]
    print(f"== {title}: {len(gone)} lines out, {len(came)} lines in")
    for x in gone:
        print("  -", x[:150])
    for x in came:
        print("  +", x[:150])
    doc[a:b] = new


a_rows = [r for r in rows if r["kind"] == "a"]
floor_next = lines_of("floor.md")
body = [f"{len(a_rows)} kind-a rows, each homed in a role card or `SKILL.md` text, the floor or a refusal. "
        "The quoted line is the home's, from the working tree.",
        "", "| id | source | new home | the home line |", "| --- | --- | --- | --- |"]
for r in a_rows:
    home, quote = r["home"], ""
    if home.startswith("card "):
        rel, _, n = home[5:].rpartition(":")
        quote = lines_of(rel)[int(n) - 1]
        assert quote and not quote.startswith("#"), (r["id"], home)
    elif re.fullmatch(r"floor \d+", home):
        quote = floor_next[int(home.split()[1]) + 3]
    elif home.startswith("floor"):
        quote = floor_next[2]
    else:
        assert home.startswith("refusal "), (r["id"], home)
    body.append(f"| {r['id']} | {r['source']} | {home} | {cell(quote, 200)} |")
replace("## Protecting rows and their homes", body)

pat = re.compile(r"(?i)\b(never|only on|only with|must not|no one|only the user|nothing else)\b")
loose = [r for r in rows if r["kind"] != "a" and pat.search(r["behaviour"])]
body = [f"{len(loose)} rows of kind b to f hold \"never\", \"only on\", \"must not\" or the like; "
        "each is listed so a reader can contest its kind.",
        "", "| id | kind | new home | behaviour |", "| --- | --- | --- | --- |"]
body += [f"| {r['id']} | {r['kind']} | {r['home']} | {cell(r['behaviour'].replace(chr(92) + '|', '|'), 150)} |"
         for r in loose]
replace("## Protecting-looking rows not classified a", body)

kinds = collections.Counter(r["kind"] for r in rows)
homes = collections.Counter(
    r["home"].split()[0] if r["home"].split()[0] not in ("host", "proof", "incidents", "next:")
    else " ".join(r["home"].split()[:2]) if r["home"].startswith("host") else r["home"]
    for r in rows)
replace("## Counts", [f"{len(rows)} rows.", "",
                      "Kinds: " + ", ".join(f"{k} {kinds[k]}" for k in "abcdef") + ".", "",
                      "Homes: " + ", ".join(f"{k} {v}" for k, v in homes.most_common()) + "."])

text = re.sub(r"(?i)([A-Z]:[\\/]Users[\\/])(?!<user>)[^\\/<>`\s|]+", r"\1<user>", "\n".join(doc))
if not CHECK:
    OUT.write_text(text, encoding="utf-8", newline="\n")
print(len(rows), "rows;", len(a_rows), "kind a;", "checked only" if CHECK else f"written, {OUT.stat().st_size} bytes")
