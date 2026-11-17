"""track.py <Txx> <status> <round> <commit|-> "<text>": update PLAN.md row, STATE.md S7 line, journal."""
import datetime, pathlib, re, sys

D = pathlib.Path(__file__).resolve().parent.parent
task, status, rnd, commit, text = sys.argv[1:6]
plan = D / "PLAN.md"
lines = plan.read_text().split("\n")
for i, line in enumerate(lines):
    if line.startswith(f"| {task} |"):
        cells = line.split("|")
        # | ID | Title | Backlog | Ph | Size | Depends | Gate | Commit type | Status | Round | Commit |
        cells[9] = f" {status} "
        cells[10] = f" {rnd} "
        if commit != "-":
            cells[11] = f" `{commit}` "
        lines[i] = "|".join(cells)
        print(lines[i])
        break
else:
    sys.exit(f"row {task} not found")
plan.write_text("\n".join(lines))
state = D / "STATE.md"
s = state.read_text()
s = re.sub(r"(\| S7 \| Implementation, task by task \(see PLAN.md task table\)) — current: [^|]*\|",
           rf"\1 — current: {task} {status} r{rnd} |", s)
state.write_text(s)
with (D / "journal.md").open("a") as f:
    f.write(f"- {datetime.date.today()} {task} r{rnd} {status}: {text}\n")
