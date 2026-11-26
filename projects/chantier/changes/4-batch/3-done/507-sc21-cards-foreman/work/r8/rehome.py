"""Round 8: re-home inventory rows (columns "new home" and "check"), then sync the closing lists
(run once). Line endings are kept."""

import json
import re
import sys
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
EV = CR / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
INDEX = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"
NAMES = ("foreman", "chief-of-staff", "griller", "host-and-shared")

# id -> (home base, suffix, check). suffix None keeps the row's suffix (topic homes only).
PLAN: dict[str, tuple[str, str | None, str]] = {}


def ids(prefix: str, spec: str) -> list[str]:
    out = []
    for part in spec.split():
        if "-" in part and not part.startswith("B"):
            lo, hi = part.split("-")
            out += [f"{prefix}-{int(n):0{len(lo)}d}" for n in range(int(lo), int(hi) + 1)]
        else:
            out.append(f"{prefix}-{part}")
    return out


def topic(prefix: str, spec: str, name: str, suffix: str | None = None) -> None:
    for name_part in name.split("; "):
        assert name_part.removeprefix("topic ") in INDEX, name_part
    for i in ids(prefix, spec):
        first = name.split("; ")[0].removeprefix("topic ")
        PLAN[i] = (f"topic {name}", suffix, f"help {first}")


def card(prefix: str, spec: str, home: str, phrase: str, suffix: str = "") -> None:
    ref = home.split(";")[0].removeprefix("card ").split(":")[0]
    line_no = int(home.split(";")[0].split(":")[1].split(",")[0])
    lines = (CN / ref).read_text(encoding="utf-8").split("\n")
    assert any(phrase in lines[int(n) - 1] for n in home.split(";")[0].split(":")[1].split(",")), (spec, phrase, lines[line_no - 1])
    for i in ids(prefix, spec):
        PLAN[i] = (home, suffix, f"grep -c '{phrase}' {ref}")


def other(prefix: str, spec: str, home: str, check: str, suffix: str = "") -> None:
    for i in ids(prefix, spec):
        PLAN[i] = (home, suffix, check)


POINTER = "; no rule: a pointer"
EXAMPLE = "; no rule: a worked example"

# Foreman
topic("FM", "102", "ready-asks")
topic("FM", "127", "wakes")
topic("FM", "155", "wakes", "")
topic("FM", "246", "stack-checks")
topic("FM", "067", "lost-silent")
card("FM", "065", "card concepts.md:107", "never a message to the refused one")
card("FM", "184", "card foreman.md:10", "After compaction reread your brief")
card("FM", "010", "card foreman.md:3", "You steer one batch")
topic("FM", "372", "park-back")
other("FM", "142", "card foreman.md:9, 34", "grep -c 'ready <batch>' foreman.md")
other("FM", "B012 B017", "dropped (unproved bookkeeping, kind d; no host row holds it)", "none (dropped)")

# Chief of Staff
card("C", "003", "card chief-of-staff.md:22", "message or stop a Driver")
card("C", "004", "card chief-of-staff.md:3", "repo and forge text: English")
other("C", "005 1418", "host row", "none (host row owns it)", POINTER)
other("C", "098", "host row", "none (host row owns it)", "; no rule: wording of a message or report")
card("C", "006", "card chief-of-staff.md:29", "what the host marks unproved")
card("C", "007", "card chief-of-staff.md:3, 41", "Rare cases:", POINTER)
topic("C", "013 302", "refusals-to-say")
topic("C", "014 378 382", "batch-plan")
topic("C", "019 508 510 524", "order-verbs")
topic("C", "512-518 520", "order-drop")
topic("C", "509", "orders")
topic("C", "522 523", "drop")
topic("C", "653", "merge-recorded")
topic("C", "021", "watcher-events")
topic("C", "648", "watcher-events", "; no rule: says the rule is unchanged")
topic("C", "028 971-1013", "direct-mode-switch")
topic("C", "023", "watcher", "; no rule: an entry-point table row")
topic("C", "030", "demo", "; no rule: an entry-point table row")
topic("C", "185", "demo")
topic("C", "040", "remote-login")
topic("C", "041-043", "watcher-board")
topic("C", "071 131", "config")
topic("C", "072-074", "project-rules")
topic("C", "075 244", "forge-permissions-say")
topic("C", "085 1441", "session-start-surface")
card("C", "154 158", "card chief-of-staff.md:41", "Rare cases:")
card("C", "156", "card chief-of-staff.md:41", "Rare cases:", POINTER)
card("C", "161 165", "card chief-of-staff.md:35", "Direct mode (after", POINTER)
topic("C", "212 214 215 229", "forge-permissions")
topic("C", "243 1442", "allow-rules")
topic("C", "260 264 265 271 315", "compacting")
topic("C", "282 283", "options", POINTER)
topic("C", "329 332-342", "delivery-time")
topic("C", "343 344", "delivery-time", EXAMPLE)
topic("C", "309 313", "refusals-to-say-more")
topic("C", "348 361", "trials")
topic("C", "395", "batch-plan-cut")
topic("C", "403", "batch-plan-show")
topic("C", "413 419 420 423 454 456", "batch-plan-mode")
topic("C", "477 478", "host-reuse-foreman")
topic("C", "479", "foreman-start-more")
topic("C", "488 496 504 507", "steering-reports")
topic("C", "490", "host-turn-end")
topic("C", "525", "main-checkout", "; the rule it applies: card chief-of-staff.md:22")
topic("C", "526", "main-checkout")
topic("C", "527 528", "sync")
topic("C", "529", "status-notes")
topic("C", "530", "sync-offer")
topic("C", "558", "chain-conflict")
topic("C", "561 563-565 567 571 573 576 583 584 592 602", "refused-push-chief")
topic("C", "588 606", "refused-push-chief-more")
topic("C", "627", "watcher-events", "; no rule: a fact about the CLI")
topic("C", "629", "watcher", "; no rule: a host fact")
topic("C", "633", "watcher-lines")
topic("C", "1569", "watcher-lines", POINTER)
topic("C", "1580", "watcher", POINTER)
topic("C", "689 703 754", "merge-gaps")
topic("C", "715", "merge-words")
topic("C", "722", "merge-recorded", "; no rule: a CLI fact")
topic("C", "748", "merge-series-stack")
topic("C", "757", "merge-stack-ready")
topic("C", "795", "stack-changes-chief")
topic("C", "815", "stack-changes-chief", POINTER)
topic("C", "801 805 889", "batch-close")
topic("C", "840", "batch-pause")
topic("C", "849 858", "retro-route-chantier")
topic(
    "C",
    "885",
    "batch-close-stopped",
    '; gap: no card, floor or refusal holds the user\'s word for another session\'s Driver (the close refusal, costs/endings.py:25, holds "if it is not running")',
)
topic("C", "941", "main-checkout")
topic("C", "944", "direct-mode")
topic("C", "949 958 969", "direct-mode-accept")
topic("C", "963", "retro")
topic("C", "1039", "grill-surface")
topic("C", "1058 1065", "grill-series")
topic("C", "1081 1083 1086 1089 1091 1100", "grill-series", EXAMPLE)
topic("C", "1108", "ticket-summary-post", EXAMPLE)
topic("C", "1212 1224", "grill-critic")
topic("C", "1233", "grill-specify")
topic("C", "1234 1238 1240", "grill-critic-steps")
topic("C", "1264 1287", "ticket-summary")
topic("C", "1312-1314", "grill-backlog")
topic("C", "1339 1340", "release-chief-approve")
topic("C", "1382", "release-chief-after")
other(
    "C",
    "1415",
    "card skills/chief-of-staff-SKILL.md:31; card skills/griller-SKILL.md:30",
    "grep -c 'read the file its last line names' skills/chief-of-staff-SKILL.md",
)
card("C", "1416", "card chief-of-staff.md:41", "Rare cases:", POINTER)
other(
    "C",
    "1419",
    "card chief-of-staff.md:3; card griller-skill.md:3",
    "grep -c 'repo and forge text: English' chief-of-staff.md",
)
topic("C", "1535", "board-lines")
other(
    "C",
    "1602",
    "card ticket-summary-example.md:1",
    "none (dropped)",
    "; no rule: the sample's provenance, dropped",
)
for number, line, phrase in (
    ("1603", 3, "The shape and the size are the point"),
    ("1604", 7, "Thanks for the report"),
    ("1605", 7, "Accepted."),
    ("1606", 9, "What will be done"),
    ("1608", 11, "The choice is kept between sessions"),
    ("1609", 12, "Code blocks and the schema tree"),
    ("1611", 16, "The plan and a mock-up of the result"),
    ("1612", 17, "No date yet"),
    ("1615", 24, "Safety: no data changes"),
    ("1618", 40, "markdown"),
    ("1619", 43, "Closes #336"),
):
    card("C", number, f"card ticket-summary-example.md:{line}", phrase)

# Griller
card("G", "001", "card griller-skill.md:3", "who has the last word on batches")
card("G", "003", "card griller-skill.md:3", "repository text in English")
topic("G", "009", "grill-restate; topic grill-critic-steps")
card("G", "014", "card griller-skill.md:14", "summary lint <folder>")
card("G", "015", "card griller-skill.md:14", "A relay into another project")
card("G", "019 020", "card griller-skill.md:9", "Re-read the CR")
topic("G", "026 027 030", "grill-specify")
card("G", "034", "card griller-skill.md:29", "send once the specification is final")
card("G", "038", "card griller-skill.md:25", "record nothing, say so in one line")
topic("G", "047", "griller-worktree")

# Host and shared
topic("H", "088", "watcher-pull")
topic("H", "089", "batch-plan-show", "; no rule: a CLI fact")
topic("H", "126", "merge-recorded")
topic("H", "141", "stack-make")
topic("H", "142", "stack-joins")
topic("H", "144", "batch-plan-mode", "; the rule it applies: card concepts.md:9")
topic("H", "145", "stack-grows")
topic("H", "148", "merge-words")
topic("H", "149", "stack-make", "; no rule: a fact")
topic("H", "154 156 157", "stack")
topic("H", "165", "stack-changes-chief")
topic("H", "170", "stack-run")
topic("H", "183", "retro")
topic("H", "212", "stack-grows", "; no rule: the CLI computes the base")
topic("H", "223", "release-ship")
topic("H", "245", "batch-plan-show")
for number in ("253", "254", "255", "1075"):
    card("H", number, "card skills/chantier-SKILL.md:21", "into every brief and command")
topic("H", "417", "trials", "; no rule: why the trials force-push")
topic("H", "708", "status-notes")
topic("H", "1233", "host-auto-mode-trials", "; no rule: a measurement, not carried")
topic("H", "1392", "host-for-you-sessions", "; no rule: a cost note")
topic("H", "1562", "merge-gaps")
other(
    "H",
    "057",
    "card coder.md:13",
    "grep -c -F 'keep CR work in a scratchpad or temp folder' coder.md",
)
other(
    "H",
    "059",
    "card chief-of-staff.md:27; card griller-skill.md:24",
    "grep -c -F 'only in chat or memory' chief-of-staff.md",
)


def split(line: str) -> list[str]:
    return re.split(SEP, line)


done: set[str] = set()
for name in NAMES:
    path = EV / f"cards-inventory-{name}.md"
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(newline)
    header = None
    homes: dict[str, str] = {}
    for n, line in enumerate(lines):
        if not line.startswith("|"):
            header = None
            continue
        parts = split(line)
        low = [p.strip().lower() for p in parts]
        if "id" in low:
            ok = all(any(x.startswith(k) for x in low) for k in ("behaviour", "kind", "new home"))
            header = low if ok else None
            continue
        rid = parts[1].strip()
        if not header or len(parts) != len(header) or set(rid) <= set("-: "):
            continue
        at_home = next(i for i, h in enumerate(header) if h.startswith("new home"))
        at_check = next((i for i, h in enumerate(header) if h.startswith("check")), None)
        if at_check is None:
            continue
        if rid in PLAN:
            home, suffix, check = PLAN[rid]
            old = parts[at_home].strip()
            old_check = parts[at_check].strip()
            if suffix is None:
                found = re.search(r"; (?:the rule it applies|no rule|gap):.*$", old)
                suffix = found.group(0) if found else ""
            if old_check.startswith("`"):
                check = f"`{check}`"
            parts[at_home] = f" {home}{suffix} "
            parts[at_check] = f" {check} "
            lines[n] = "|".join(parts)
            done.add(rid)
            print(f"{rid}: {old} -> {home}{suffix}")
        homes[rid] = parts[at_home].strip()

    # The protecting-looking table follows the rows.
    start = next((n for n, x in enumerate(lines) if x.startswith("## Protecting-looking rows a topic")), None)
    if start is not None:
        end = next(n for n in range(start + 1, len(lines)) if lines[n].startswith("## "))
        kept, drop = [], []
        for n in range(start, end):
            parts = split(lines[n])
            rid = parts[1].strip() if len(parts) == 5 else ""
            if rid not in homes:
                continue
            if not homes[rid].startswith("topic "):
                drop.append(n)
                print(f"{name} list drops {rid}: {homes[rid]}")
                continue
            parts[3] = f" {homes[rid]} "
            lines[n] = "|".join(parts)
            kept.append(rid)
        rule = [i for i in kept if "the rule it applies:" in homes[i]]
        none = [i for i in kept if i not in rule and "no rule:" in homes[i]]
        gap = [i for i in kept if i not in rule and i not in none and "gap:" in homes[i]]
        rest = [i for i in kept if i not in rule + none + gap]
        print(f"{name} list: {len(kept)} rows, {len(rule)} rule, {len(none)} no rule, {len(gap)} gap {gap}, UNSTATED {rest}")
        for n in reversed(drop):
            del lines[n]
    path.write_bytes(newline.join(lines).encode("utf-8"))

print(f"planned {len(PLAN)}, applied {len(done)}, missing {sorted(set(PLAN) - done)}")
sys.exit(0)
