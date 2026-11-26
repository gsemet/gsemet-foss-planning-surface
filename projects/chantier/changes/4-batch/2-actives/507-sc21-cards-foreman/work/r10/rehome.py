"""Round 10: set the `new home` (and `check`) cell of rows whose home did not hold their rule.

Run: python -I rehome.py <evidence folder> [--apply]
Without --apply it prints each change and writes nothing. A second run changes nothing.
The main 8-column rows are set first; then the end-list rows of the same ids, in the tables
whose header has a home column, have the old home replaced by the new one.
"""

import pathlib
import re
import sys

DROPPED = "none (dropped)"
PROOF = "none (dated proof: `docs/proofs`, child 24)"


def topic(name):
    return (f"topic {name}", f"help {name}")


# id -> (new home cell, new check cell or None to keep it)
MOVES = {
    "C-1376": ("topic release-chief-after; the rule it applies: card chief-of-staff.md:15", "help release-chief-after"),
    "C-495": ("card chief-of-staff.md:39", "grep -c -F 'Progress and Completion reports keep' chief-of-staff.md"),
    "H-089": ("topic batch-plan-show, board; card chief-of-staff.md:26 (the writer stages the surface)", None),
    "H-186": ("topic batch-pause, retro, retro-lines", "help retro"),
    "H-187": topic("retro"),
    "C-024": topic("pr-template-own"),
    "H-282": topic("long-gate"),
    "H-711": topic("status-notes-more"),
    "C-1031": topic("grill-series"),
    "C-1032": topic("grill-series"),
    "C-1033": topic("grill-series"),
    "C-793": topic("stack-changes-chief"),
    "C-797": topic("stack-changes-chief"),
    "C-1152": topic("grill-backlog"),
    "H-1449": topic("host-allow-add"),
    "C-943": topic("direct-mode"),
    "C-1286": topic("ticket-summary"),
    "C-1269": topic("ticket-summary"),
    "C-1281": topic("ticket-summary"),
    "C-1285": topic("ticket-summary"),
    "C-248": topic("forge-permissions-say"),
    "C-560": topic("chain-conflict"),
    "H-1350": topic("options"),
    "C-917": topic("direct-mode"),
    "FM-055": topic("lease-steering"),
    "C-1308": topic("ticket-summary-post"),
    "C-468": topic("demo"),
    "G-023": ("card griller-skill.md:20", "grep -c -F 'give its link from' griller-skill.md"),
    "C-1496": topic("first-turn"),
    "C-1485": topic("first-turn"),
    "C-693": topic("merge-words"),
    "C-698": ("topic merge-words; the rule it applies: floor 1", "help merge-words"),
    "C-699": topic("merge-words"),
    "C-750": topic("merge-stack-ready"),
    "C-761": topic("merge-stack-ready"),
    "C-739": topic("merge-stack-ready"),
    "C-159": ("card chief-of-staff.md:41", "grep -c -F 'merge-series-stack' chief-of-staff.md"),
    "H-143": topic("stack-run"),
    "H-149": ("topic stack-run; no rule: a fact", "help stack-run"),
    "H-164": topic("stack-changes-chief"),
    "H-167": topic("hold"),
    "C-1506": topic("reload"),
    "C-1061": topic("grill-series"),
    "FM-099": ("topic ask-lines; the rule it applies: card foreman.md:15", "help ask-lines"),
    "FM-100": ("topic ask-lines; the rule it applies: card foreman.md:15", "help ask-lines"),
    "FM-101": ("card foreman.md:38", "grep -c -F 'Name CRs by number and slug' foreman.md"),
    "FM-B002": ("dropped (specification B1b: `judge` carries no icon, the rule disappears)", DROPPED),
    "C-670": topic("watcher-events"),
    "C-1272": topic("ticket-summary"),
    "C-628": topic("watcher-events"),
    "H-898": ("card chief-of-staff.md:14; topic sync-offer", None),
    "H-905": ("card chief-of-staff.md:14; topic sync-offer", None),
    "FM-568": ("card chief-of-staff.md:10; topic refused-push-chief", None),
    "H-1138": ("card chief-of-staff.md:13; topic host-allow-broad", None),
    "H-1443": ("card chief-of-staff.md:13; topic allow-rules", None),
    "H-774": ("card chief-of-staff.md:13; card init.md:3", None),
    "H-779": ("card chief-of-staff.md:13; card init.md:9", None),
    "H-808": ("card chief-of-staff.md:13; card init.md:32", None),
    "H-832": ("card chief-of-staff.md:13; card init.md:32", None),
    "H-833": ("card chief-of-staff.md:13; topic init-tools", None),
    "H-839": ("card chief-of-staff.md:13; topic init-tools", None),
    "C-970": ("card chief-of-staff.md:16; topic direct-mode", None),
    "H-958": ("card chief-of-staff.md:14; host row stop-session", None),
    "H-1697": ("card chief-of-staff.md:14; host row stop-session", None),
    "H-1421": ("card chief-of-staff.md:13; floor 7; topic host-remote", None),
    "C-210": ("card chief-of-staff.md:24; topic ticket-summary-post", None),
    "H-1545": topic("session-start"),
    "H-1548": topic("session-start"),
    "C-1522": topic("board"),
    "C-1202": topic("grill-restate"),
    "G-029": ("card griller-skill.md:29", "grep -c -F 'send once the specification is final' griller-skill.md"),
    "H-106": topic("grill-backlog"),
    "C-1173": topic("grill-outside-pr"),
    "G-036": ("card griller-skill.md:25", "grep -c -F 'commit, pull and push nothing' griller-skill.md"),
    "H-258": ("card concepts.md:71; refusal handback ready, gate, take, ship", None),
    "H-478": ("card cr-driver.md:17; card pr-template.md:131", None),
    "H-397": ("card concepts.md:79", "grep -c -F 'where they are silent' concepts.md"),
    "H-1546": ("card concepts.md:75; floor 1, 6", None),
    "H-1737": ("floor 3; host row model-ran-on", None),
    "H-1746": ("floor 3; host row stop-driver", None),
    "H-1770": ("floor 3; host row run-watcher", None),
    "FM-004": ("card foreman.md:10; topic wakes", None),
    "FM-066": ("card foreman.md:13; topic lease-steering", None),
    "FM-082": ("card foreman.md:29; topic project-rules", None),
    "FM-139": ("card foreman.md:8; topic session-shell", None),
    "FM-154": ("`brief foreman` (it prints the host rows)", "brief foreman builds"),
    "FM-158": topic("wakes-forge"),
    "FM-133": (
        '`status --stop-heartbeat` (it prints "heartbeat stopped recorded for <batch>; the next '
        '`status --refresh --epoch <n>` clears it")',
        "status --stop-heartbeat prints",
    ),
    "FM-B053": ("card foreman.md:24 (the allow line dropped, specification B6)", None),
    "H-379": ("card concepts.md:140", None),
    "H-380": ("card concepts.md:141", None),
    "H-381": ("card concepts.md:142", None),
    "H-382": ("card concepts.md:143", None),
    "H-383": ("card concepts.md:144", None),
    "H-384": ("card concepts.md:138", "grep -c -F 'a failed restack escalates the stack' concepts.md"),
    "H-375": ("card concepts.md:138", "grep -c -F 'escalate. Drivers never do' concepts.md"),
    "H-376": ("card concepts.md:138", "grep -c -F 'Drivers never do (a failed restack' concepts.md"),
    "H-377": ("card concepts.md:138", "grep -c -F 'nor do the judging agents' concepts.md"),
    "H-385": ("card concepts.md:145", None),
    "H-388": ("card concepts.md:146", None),
    "H-389": ("card concepts.md:146", None),
    "H-390": ("card concepts.md:146", None),
    "H-392": ("card concepts.md:146", None),
    "H-393": ("card concepts.md:146", None),
    "H-394": ("card concepts.md:147", None),
    "H-395": ("card concepts.md:147", None),
}
for key in (
    "C-1080 C-1081 C-1083 C-1085 C-1086 C-1088 C-1089 C-1091 C-1092 C-1093 C-1094 C-1096 C-1098 "
    "C-1099 C-1100 C-1102 C-1103 C-1104 C-1107 C-1108"
).split():
    MOVES[key] = ("topic grill-example; no rule: a worked example", "help grill-example")
for key in ("FM-222", "FM-223"):
    MOVES[key] = ("card foreman.md:21; topic stack-asks", None)
for key in "H-1055 H-1182 H-1249 H-1264 H-1304 H-1336 H-1368 H-1376 H-1381".split():
    MOVES[key] = ("proof file", PROOF)

# id -> topics or cards appended to the home cell
APPEND = {}


def add(suffix, ids):
    for key in ids.split():
        APPEND.setdefault(key, []).append(suffix)


add("topic main-checkout", "FM-286 FM-300 FM-302 FM-306 FM-308 FM-309 FM-310")
add("topic merge-under-grant", "FM-317 FM-322 FM-330 FM-B033 FM-B035")
add("topic merge-github", "FM-328 FM-329")
add("topic conflict-check", "FM-485")
add("topic refused-push-steering", "FM-526 FM-529 FM-542 FM-546 FM-547")
add("topic refused-push-judgement", "FM-535")
add("topic refused-push-gate", "FM-541 FM-558")
add("topic refused-push-run", "FM-566")
add("topic refused-rebase", "FM-582 FM-583 FM-584 FM-585")
add("topic refused-rebase-run", "FM-589")
add("topic ask-lines", "FM-B006")
add("topic long-gate", "FM-071 FM-B010 FM-B023 FM-B024")
add("topic local-gate", "FM-B011 FM-B014 FM-B015 FM-B019 FM-B029 FM-B030")
add("topic long-gate-waiver", "FM-B025 FM-B026 FM-B027 FM-B028 FM-B031")
add("topic orders", "FM-B043 FM-B045")
add("topic take-back", "FM-B046")
add("topic drop", "FM-B056")
add("topic cleanup", "FM-B058")
add("card concepts.md:105", "FM-062 FM-063 FM-064")
add("card concepts.md:7", "H-029")
add("topic host-turn-end", "H-1032")
add("topic host-remote", "H-1426")
add("topic host-auto-fix", "H-992")
add("card concepts.md:136", "H-373")
add("card concepts.md:81", "H-402 H-301 H-1541")
add("topic config", "H-402")
add("card init.md:32", "H-821")
add("topic host-refused", "H-1174")
add("card concepts.md:146", "H-391")
add("topic watcher-board", "H-110")
add("topic verifier-delta-matrix", "H-407")
add("topic release-evidence", "H-622 H-590")
add("topic host-sessions-more", "H-976 H-1714")
add("floor 10", "H-866")
add("topic worker-shell; topic session-shell", "H-1536")
add("topic griller-worktree", "G-040")
add("topic recovery", "H-119 H-120")


def cells(line):
    return re.split(r"(?<!\\)\|", line)


def tables(lines):
    """Yield (line index, header cells, row parts) for every table data row."""
    header = None
    for index, raw in enumerate(lines):
        line = raw.rstrip("\r")
        if not line.startswith("|"):
            header = None
            continue
        after = lines[index + 1].rstrip("\r") if index + 1 < len(lines) else ""
        if re.match(r"^\|[-: |]+\|\s*$", after):
            header = [c.strip().lower() for c in cells(line)]
            continue
        if header is None or re.match(r"^\|[-: |]+\|\s*$", line):
            continue
        yield index, header, cells(line)


def new_home(key, old):
    home = MOVES[key][0] if key in MOVES else old
    for suffix in APPEND.get(key, []):
        if suffix not in home:
            home = f"{home}; {suffix}"
    return home


def main():
    folder = pathlib.Path(sys.argv[1])
    apply = "--apply" in sys.argv
    wanted = set(MOVES) | set(APPEND)
    files = {}
    for path in sorted(folder.glob("cards-inventory-*.md")):
        files[path] = path.read_bytes().decode("utf-8").split("\n")
    changes = {}
    seen = {}
    old_homes = {}
    for path, lines in files.items():
        for index, header, parts in tables(lines):
            key = parts[1].strip() if len(parts) > 1 else ""
            if key not in wanted or "behaviour" not in header or "check" not in header:
                continue
            seen[key] = seen.get(key, 0) + 1
            home_at = header.index("new home")
            check_at = header.index("check")
            old = parts[home_at].strip()
            old_check = parts[check_at].strip()
            home = new_home(key, old)
            check = old_check
            if key in MOVES and MOVES[key][1] is not None:
                value = MOVES[key][1]
                quote = old_check.startswith("`") and value.startswith(("help ", "grep "))
                check = f"`{value}`" if quote else value
                if check.strip("`") == old_check.strip("`"):
                    check = old_check
            old_homes[key] = (old, home)
            if home == old and check == old_check:
                continue
            parts[home_at] = f" {home} "
            parts[check_at] = f" {check} "
            ending = "\r" if lines[index].endswith("\r") else ""
            lines[index] = "|".join(parts).rstrip("\r") + ending
            changes[path] = True
            print(f"{path.name}:{index + 1} {key}: {old} [{old_check}] -> {home} [{check}]")
    for path, lines in files.items():
        for index, header, parts in tables(lines):
            key = parts[1].strip() if len(parts) > 1 else ""
            if key not in wanted or "behaviour" in header and "check" in header:
                continue
            if key not in old_homes:
                continue
            columns = [i for i, name in enumerate(header) if "home" in name and name != "the home line"]
            if not columns:
                continue
            at = columns[0]
            old, home = old_homes[key]
            if old == home:
                continue
            cell = parts[at].strip()
            if home in cell:
                continue
            bare = old.strip("`")
            if bare and bare in cell:
                cell = cell.replace(bare, home, 1)
                parts[at] = f" {cell} "
                ending = "\r" if lines[index].endswith("\r") else ""
                lines[index] = "|".join(parts).rstrip("\r") + ending
                changes[path] = True
                print(f"  end {path.name}:{index + 1} {key}: {cell[:200]}")
            else:
                print(f"  MANUAL {path.name}:{index + 1} {key} [{header[at]}]: {cell[:200]} || {old} -> {home}")
    if apply:
        for path in changes:
            path.write_bytes("\n".join(files[path]).encode("utf-8"))
    for key in sorted(wanted):
        if seen.get(key) != 1:
            print("main row count", key, seen.get(key, 0))


if __name__ == "__main__":
    main()
