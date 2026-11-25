"""Round 7: apply the judged fixes to cards-inventory-host-and-shared.md (read row by row)."""

import re
import shutil
import sys
from pathlib import Path

import inv

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
PATH = inv.EV / "cards-inventory-host-and-shared.md"
BEFORE = Path(__file__).parent / "before" / PATH.name

raw = PATH.read_bytes()
crlf = b"\r\n" in raw
assert not raw.startswith(b"\xef\xbb\xbf")
text = raw.decode("utf-8").replace("\r\n", "\n")
assert "nor ask anyone to' " not in text, "already applied"
if "--dry" not in sys.argv:
    BEFORE.parent.mkdir(exist_ok=True)
    if not BEFORE.exists():
        shutil.copy2(PATH, BEFORE)
lines = text.split("\n")


def lines_of(rel):
    return (CN / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def cell(value, cut):
    value = " ".join(value.split())
    if len(value) > cut:
        value = value[:cut].rsplit(" ", 1)[0] + " ..."
    return value.replace("|", "\\|")


def grep(phrase, card):
    assert phrase in (CN / card).read_text(encoding="utf-8"), (phrase, card)
    return f"`grep -c -F '{phrase}' {card}`"


# --- rule rows: id -> {column index: new value}. Columns: 1 role, 6 new home, 7 check.
ROLE, HOME, CHECK = 1, 6, 7
FIX: dict[str, dict[int, str]] = {}


def fix(ids, **kw):
    for i in ids.split():
        slot = FIX.setdefault(f"H-{i}", {})
        for key, value in kw.items():
            slot[{"role": ROLE, "home": HOME, "check": CHECK}[key]] = value


fix("057", home="card coder.md:13; gap: large binaries (coder.md is over its budget)")
fix(
    "059",
    role="chief-of-staff, griller",
    home="card chief-of-staff.md:27; card griller-skill.md:24 (memory); gap: the host's settings",
    check=grep("only in chat, memory", "chief-of-staff.md"),
)
fix("067", check=grep("set a priority, label or group but on", "chief-of-staff.md"))
fix("299 976 1359 1677 1714 1774", home="floor 3, 9",
    check="floor.md:7, floor.md:13 (every brief carries them)")
fix("333", home="card demo-explorer.md:10, 11")
fix("391", home='floor 7; refusal round, "<cr>: round limit <n> reached; hand back blocked…" (rails.py:313)')
fix("860", check=grep("notes and green CI are not proof", "review-step.md"))
fix("706 898 899 905 906 907 908 958 1697",
    check=grep("Stopping a Foreman or a process", "chief-of-staff.md"))
fix("1004", home="card chief-of-staff.md:13 (the PR monitor is an app setting)")
fix("1057", check=grep("never on silence alone", "foreman.md"))
fix("1360", home="card chief-of-staff.md:31 (the Foreman's worktree override is dropped per sc21-Q1, "
    "default, to confirm by the owner)")
fix("1421", home="card chief-of-staff.md:13; floor 7")
fix("1546", home="floor 1, 6", check="floor.md:5, floor.md:10 (every brief carries them)")
fix("1577", check=grep("nor ask anyone to", "skills/chantier-SKILL.md"))
fix("1599", check=grep("nor ask anyone to", "skills/chief-of-staff-SKILL.md"))
fix("1621", check=grep("nor ask anyone to", "skills/griller-SKILL.md"))
fix("1641", check=grep("nor ask anyone to", "skills/status-SKILL.md"))
fix("1607", home="card skills/chief-of-staff-SKILL.md:33",
    check=grep("no flag added", "skills/chief-of-staff-SKILL.md"))

done = set()
a_rows = {}
rules = {}
for n, line in enumerate(lines):
    if not re.match(r"\| H-\d+ \|", line):
        continue
    c = inv.cells(line)
    if len(c) != 8:
        continue
    ident = c[0]
    assert ident not in rules, ident
    if ident in FIX:
        for k, v in FIX[ident].items():
            assert "|" not in v, (ident, v)
            c[k] = v
        lines[n] = "| " + " | ".join(c) + " |"
        done.add(ident)
    rules[ident] = c
    if c[5] == "a":
        a_rows[ident] = c
assert done == set(FIX), set(FIX) - done
print("rule rows", len(rules), "changed", len(done), "kind a", len(a_rows))


# --- sections
def section(title):
    start = lines.index(title)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


# protecting table: homes and quotes from the working tree
floor = lines_of("floor.md")


def quote_of(home):
    m = re.match(r"card ([\w./-]+\.md):(\d+(?:, \d+)*)", home)
    if m:
        got = lines_of(m[1])
        parts = [got[int(k) - 1] for k in m[2].split(", ")]
    elif home.startswith("floor 1-10"):
        parts = [floor[2]]
    elif home.startswith("floor "):
        nums = re.match(r"floor (\d+(?:, \d+)*)", home)[1]
        parts = [floor[int(k) + 3] for k in nums.split(", ")]
    else:
        assert home.startswith("refusal "), home
        return ""
    assert all(p.strip() and not p.startswith("#") for p in parts), (home, parts)
    return " / ".join(parts)


start, end = section("## Protecting rows and their homes")
seen = []
moved = 0
for n in range(start, end):
    if lines[n].startswith("| H-"):
        c = inv.cells(lines[n])
        rule = rules[c[0]]
        home = rule[HOME]
        new = f"| {c[0]} | {c[1]} | {home} | {cell(quote_of(home).replace(chr(92) + '|', '|'), 200)} |"
        moved += new != lines[n]
        lines[n] = new
        seen.append(c[0])
assert seen == list(a_rows), set(seen) ^ set(a_rows)
print("protecting rows", len(seen), "changed", moved)

# the not-a list
ADD = "105 121 131 224 242 244 514 540 697 699 1022 1178 1199 1208 1209 1328 1436 1610".split()
start, end = section("## Protecting-looking rows not classified a")
listed = {}
for n in range(start, end):
    if lines[n].startswith("| H-"):
        c = inv.cells(lines[n])
        listed[c[0]] = lines[n]
ids = set(listed) | {f"H-{i}" for i in ADD}
assert len(ids) == len(listed) + len(ADD), "an added row was listed already"
table = []
for ident in sorted(ids, key=lambda x: int(x[2:])):
    rule = rules[ident]
    assert rule[5] != "a", ident
    behaviour = rule[3].replace(chr(92) + "|", "|")
    table.append(f"| {ident} | {rule[5]} | {rule[HOME]} | {cell(behaviour, 150)} |")
body = [
    "## Protecting-looking rows not classified a",
    "",
    f"{len(table)} rows of kind b to f hold \"never\", \"only on\", \"only after\", \"must not\", "
    "\"the user's word\", \"without the user\" or the like; each is listed so a reader can contest "
    "its kind.",
    "",
    "| id | kind | new home | behaviour |",
    "| --- | --- | --- | --- |",
    *table,
    "",
]
lines[start:end] = body
print("not-a rows", len(listed), "->", len(table))

# sibling-card edits
OLD_HEAD = ("Every changed line, against the worktree's base `bf4e4c42` (`git diff HEAD`), of the "
            "files under `skills/chantier/cards-next/` that existed there: this CR's first two parts "
            "and the other card children's.")
NEW_HEAD = ("Every changed line, against this CR's first two parts as rebased, `fe7fbf0f` "
            "(`git diff fe7fbf0f`, uncommitted changes included), of the files under "
            "`skills/chantier/cards-next/` that existed there: this CR's first two parts and the other "
            "card children's.")
start, end = section("## Sibling-card edits")
block = "\n".join(lines[start:end])
assert block.count(OLD_HEAD) == 1
block = block.replace(OLD_HEAD, NEW_HEAD)
rows = {}
head_lines, order = [], []
for line in block.split("\n"):
    if line.startswith("| ") and not line.startswith("| file:line") and not line.startswith("| ---"):
        key = inv.cells(line)[0]
        rows[key] = line
        order.append(key)


def put(key, what, why, after=None):
    new = f"| {key} | {what} | {why} |"
    if key in rows:
        rows[key] = new
        return
    assert after in order, after
    order.insert(order.index(after) + 1, key)
    rows[key] = new


first = order[0]
order.insert(0, "chief-of-staff.md:3")
rows["chief-of-staff.md:3"] = (
    "| chief-of-staff.md:3 | the opening: \"repository and forge text: English\" | trim |")
put("chief-of-staff.md:10",
    "the push rail: never the default \"or a protected\" branch; \"A host refusing your own run\"",
    "kind a (H-422); trim")
put("chief-of-staff.md:14",
    "stopping a Foreman or a process the session did not start, its own board and watcher too, only on "
    "the user's yes; never by name, pattern or PID (floor 10)",
    "kind a (sync-checkout, H-958)")
put("chief-of-staff.md:24", "never post a text naming a CR, batch, role or cost on an issue",
    "kind a (H-044)", after="chief-of-staff.md:23")
put("chief-of-staff.md:26",
    "`abandon` and `restore` only on the user's word, with priority, labels and groups", "review",
    after="chief-of-staff.md:24")
put("chief-of-staff.md:39",
    "the report line is shorter; \"by number and slug together\" is now \"name CRs by number and "
    "slug\"", "trim")

FOREMAN = [
    ("3, 6, 7, 8, 9, 10", "the opening and the Start lines are shorter", "trim"),
    ("13", "`gate --first` only for a critical-path CR or the user's next merge, not on a Driver's say; "
     "\"fill free slots\"", "kind a (FM-071); trim"),
    ("14", "never switch the mode", "kind a (FM-485)"),
    ("15", "an image note goes in the ask's one added sentence", "kind a (FM-B006)"),
    ("16", "stop stray background tasks by id; none outlives the heartbeat; a refusal rules over `next`",
     "kind a (FM-131, FM-160)"),
    ("17", "the retro line is shorter", "trim"),
    ("20", "a granted merge takes the judged head only, with no open PR below, reread before a retry",
     "kind a (the release grant)"),
    ("21", "never drop a hand-back; a local run is owed at that head and a waiver must name it; "
     "`deliver by` points at `help local-gate`", "kind a (the long gate)"),
    ("22", "the fast-forward is `--no-overwrite-ignore`, of a clean main checkout; the checks of a "
     "Driver's refused push or rebase; no comment on a dropped CR's PR, its branch kept; \"Stop no sync "
     "holder\"", "kind a (H-428, FM-B064, FM-B065)"),
    ("24", "the chat line is shorter", "trim"),
    ("25", "a Driver is replaced only by `help lost-restart`, never on silence alone",
     "kind a (H-1057); trim"),
    ("26", "the exit 3 line is shorter", "trim"),
    ("27", "never 8: CR work in a scratchpad or temp folder, a secret or personal data in a CR folder",
     "kind a (concepts)"),
    ("29", "a fact with no source is said unknown", "kind a (FM-083); trim"),
    ("31", "the end line is shorter", "trim"),
    ("38", "Rare cases: only `refused-push` and `session-shell` are named, and `help --for foreman` "
     "lists the topics; the other topic names are cut", "pointer; trim"),
]
at = next(i for i, k in enumerate(order) if k.startswith("foreman.md:"))
order = [k for k in order if not k.startswith("foreman.md:")]
for offset, (nums, what, why) in enumerate(FOREMAN):
    key = f"foreman.md:{nums}"
    order.insert(at + offset, key)
    rows[key] = f"| {key} | {what} | {why} |"

pre = block.split("\n")
top = pre[: next(i for i, line in enumerate(pre) if line.startswith("| ---")) + 1]
lines[start:end] = top + [rows[k] for k in order] + [""]
print("sibling rows", len(order))

# behaviour on purpose / known gaps
OLD_LINKS = ("- The role cards, `floor.md`, the forge files, the host JSON files and `review-step.md` "
             "hold no markdown link.")
NEW_LINKS = ("- `floor.md`, the host JSON files and `review-step.md` hold no markdown link, nor does a "
             "role card but `chief-of-staff.md` (its `init` link).")
full = "\n".join(lines)
assert full.count(OLD_LINKS) == 1
full = full.replace(OLD_LINKS, NEW_LINKS)
OLD_STOP = "- The Foreman's card says only \"Stop no sync holder\""
assert full.count(OLD_STOP) == 1
full = full.replace(
    OLD_STOP,
    "- H-057: no card says large binaries are kept out of a CR folder (`coder.md` is over its budget). "
    "H-059: no card, floor or refusal says CR work never goes into the host's settings.\n" + OLD_STOP,
)
full = full.replace("\n## Counts\n", "\n\n## Counts\n").replace("\n\n\n## Counts\n", "\n\n## Counts\n")

homes = {}
for c in rules.values():
    h = c[HOME]
    for k in ("card", "topic", "host row", "inferable", "floor", "proof file", "incidents file",
              "refusal", "facts"):
        if h.startswith(k):
            homes[k] = homes.get(k, 0) + 1
            break
    else:
        raise AssertionError((c[0], h))
count_line = "Homes: " + ", ".join(
    f"{k} {v}" for k, v in sorted(homes.items(), key=lambda kv: -kv[1])) + "."
old_count = re.search(r"^Homes: .*$", full, re.M)[0]
print("old", old_count)
print("new", count_line)
if "--dry" not in sys.argv:
    out = full.replace("\n", "\r\n") if crlf else full
    PATH.write_bytes(out.encode("utf-8"))
    print("written")
else:
    Path(__file__).parent.joinpath("host.dry.md").write_bytes(full.encode("utf-8"))
