#!/usr/bin/env python3
"""Orchestrator helper: update one task row of STATE.md and append to journal.md.

Usage:
  state.py show Txx
  state.py set Txx <column>=<value> [<column>=<value> ...] [--log "<step> · <outcome> · <details>"]
  state.py log Txx "<step> · <outcome> · <details>"
  state.py duration Txx [<note>]

Columns: status, round, base, commit, duration, gates, notes. Values must not contain "|".

Duration is the wall-clock time from the task's first "pre-flight" journal line to its commit.
`set Txx status=done` fills it automatically (end = now) unless the cell already has a value or
the same call sets `duration=`. `duration Txx` recomputes it from the journal (end = the first
line after the pre-flight that records a commit SHA) and appends the optional note, for example
"incl. 1 h 50 min screen lock".
"""
import datetime
import pathlib
import re
import sys

PLAN = pathlib.Path(__file__).resolve().parent.parent
STATE = PLAN / "STATE.md"
JOURNAL = PLAN / "journal.md"
COLUMNS = {"status": 3, "round": 4, "base": 5, "commit": 6, "duration": 7, "gates": 8, "notes": 9}
STATUSES = {"todo", "implementing", "gating", "reviewing", "changes-requested", "done", "blocked"}
STAMP = "%Y-%m-%d %H:%M"
COMMIT_LINE = re.compile(r"\bcommit(?: ·)? [0-9a-f]{7}\b")


def find_row(lines, task):
    for index, line in enumerate(lines):
        if line.startswith(f"| [{task}]("):
            return index
    sys.exit(f"no row for {task} in STATE.md")


def log(task, text):
    stamp = datetime.datetime.now().strftime(STAMP)
    with JOURNAL.open("a", encoding="utf-8") as journal:
        journal.write(f"{stamp} · {task} · {text}\n")


def journal_entries(task):
    """Yield (datetime, text) for the journal lines of one task, in order."""
    for line in JOURNAL.read_text(encoding="utf-8").splitlines():
        parts = line.split(" · ", 2)
        if len(parts) == 3 and parts[1] == task:
            try:
                yield datetime.datetime.strptime(parts[0], STAMP), parts[2]
            except ValueError:
                continue


def preflight_time(task):
    for when, text in journal_entries(task):
        if text.startswith("pre-flight"):
            return when
    sys.exit(f"no pre-flight line for {task} in journal.md")


def commit_time(task):
    start = preflight_time(task)
    for when, text in journal_entries(task):
        if when >= start and COMMIT_LINE.search(text):
            return when
    sys.exit(f"no commit line for {task} in journal.md")


def format_duration(start, end):
    minutes = max(0, round((end - start).total_seconds() / 60))
    hours, minutes = divmod(minutes, 60)
    return f"{hours} h {minutes:02d} min" if hours else f"{minutes} min"


def write_cells(lines, index, cells):
    lines[index] = "| " + " | ".join(cells) + " |"
    STATE.write_text("\n".join(lines), encoding="utf-8")
    print(lines[index])


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    command, task = argv[1], argv[2]
    lines = STATE.read_text(encoding="utf-8").split("\n")
    index = find_row(lines, task)
    if command == "show":
        print(lines[index])
        return
    if command == "log":
        log(task, argv[3])
        return
    cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
    if command == "duration":
        value = format_duration(preflight_time(task), commit_time(task))
        note = argv[3] if len(argv) > 3 else ""
        if "|" in note:
            sys.exit(f"bad note: {note}")
        cells[COLUMNS["duration"]] = f"{value} ({note})" if note else value
        write_cells(lines, index, cells)
        return
    if command != "set":
        sys.exit(__doc__)
    message = None
    assigned = set()
    rest = argv[3:]
    while rest:
        item = rest.pop(0)
        if item == "--log":
            message = rest.pop(0)
            continue
        name, _, value = item.partition("=")
        if name not in COLUMNS or "|" in value:
            sys.exit(f"bad assignment: {item}")
        if name == "status" and value not in STATUSES:
            sys.exit(f"bad status: {value}")
        cells[COLUMNS[name]] = value
        assigned.add(name)
    if cells[COLUMNS["status"]] == "done" and "duration" not in assigned \
            and not cells[COLUMNS["duration"]]:
        cells[COLUMNS["duration"]] = format_duration(preflight_time(task), datetime.datetime.now())
    write_cells(lines, index, cells)
    if message:
        log(task, message)


if __name__ == "__main__":
    main(sys.argv)
