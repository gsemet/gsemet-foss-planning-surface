# Change Specification: CR board

A read-only pane beside the chat in Claude Code that shows where every change request stands. It
has two parts: the CLI extends `3-requests/STATUS.json` into a full index, and a mod in the
plugin draws it. On Claude only; Copilot is untouched.

## Part 1: the index, in the CLI

In `skills/chantier/scripts/cli/src/chantier/status.py`, `dashboard_view` keeps what it writes
and adds fields. No field changes meaning, so `SCHEMA` stays 2. `dashboard_markdown` does not
change. `write_dashboard` already runs on `file`, `triage`, `abandon`, `close` and at each batch
save: no new call is needed, and the CLI gets no new command.

- `landed` and `trashed`: the last 50 CRs of `4-archives/` and `5-trash/`, newest first by the
  folder's `YYMMDD-HHMM` prefix. Each entry: `cr`, `title`, `state`, `batch`, `pr`, `cost_usd`,
  `when` (the prefix as a timestamp) and `path` (the folder, relative to `3-requests/`). The
  values come from the folder's `STATUS.json`; a folder without one, such as an item abandoned
  from the inbox, gives its `title` from `_title` and `null` for the rest.
- `landed_total` and `trashed_total`: the number of folders in each stage.
- Each entry of `batches` gains `heartbeat` and `orders_pending`, the batch's own values.
- Each CR row (`_row`) gains `blocked` (the reason, or `null`) and `silent_minutes`. `status`
  and `specification` keep their meaning; the row also gains `folder`, the CR's folder relative
  to `3-requests/`.

The index stays fast: it reads at most 100 `STATUS.json` files, and never the forge.

## Part 2: the mod, in the plugin

`hooks/hooks.json` at the plugin's root names `./register.tsx`; `hooks/register.tsx` is the
module, with `types/index.d.ts` as its contract if it keeps values in `$.state`, named in
`.claude-plugin/plugin.json`. Check first that Copilot ignores this folder; if it does not,
stop and report it.

### Opening and closing

- When the chantier skill's prompt expands (`skill.prompt`, in the session that loads it), the
  pane opens. It never closes this way, and the prompt is not changed. The Foreman reads its
  cards without loading the skill, so its session opens no pane.
- `/chantier-board`, a command the mod registers, closes the pane if it is open and opens it
  otherwise. `/chantier` stays the Chief of Staff's.
- The pane's id is `cr-board`, its title "CR board".

### Finding the files

From the session's folder, run `git rev-parse --path-format=absolute --git-common-dir`; the main
checkout is that folder's parent, so a session in a worktree finds it. Outside a git repository,
use the session's folder. The index is `.agents/changes/3-requests/STATUS.json` there.

### Reading

- While the pane is open, a timer checks the shown files every 15 seconds with `$.fs.stat`, and
  reads one again only if its modification time changed. On close the timer stops: a closed pane
  runs nothing. The first check runs at opening.
- With no index, the pane says so in one line: `No chantier status here: <path> not found.`
- A file that does not parse keeps the last view, with one line saying so. A schema other than
  2 is said in one line and nothing else is drawn: no guess.
- The mod writes nothing. It runs no process but the `git rev-parse` above.

### The board

One column, for narrow panes and for the phone.

- **Header:** live CRs, how many wait for the user, the time since the last read.
- **One section per open batch**, in the index's order, open by default. Its title line has the
  batch's name, spent and budget as `$5.07 / $20` and a text gauge. In it:
  - **Waiting for you**, first: the blocked CRs with
    their reason, the CRs ready to merge, the batch's unread asks as a count, and "Foreman silent
    for N min" when the batch is live and `heartbeat` is older than 20 minutes. Empty, one line
    says nothing waits.
  - **In progress:** the other live CRs.
  - A CR's row: severity icon, CR id, `label` (round and step), title, PR as a link, cost, branch
    and silent time.
- **Backlog**, folded: a line per priority (inbox, P1 to P4) with its count, each folded in turn;
  a row is the title and its file count.
- **Landed** and **Trashed**, folded: `Landed (50 of 131)`; a row is CR id, title, state, PR and
  cost.

No Markdown table, and no search field. A landed batch still listed shows folded, with its cost.

### The CR sheet

Pressing a CR opens its sheet, from its own `STATUS.json` (`folder` in the row, or `path`):

- a way back, the id, title, label and cost;
- `steps` as one line of text, with notes dropped and each repeated name kept once, in order;
- `now`, `next`, the blocked reason, the PR link;
- `documents`, each pressable.

An inbox or backlog item has no `STATUS.json`: its sheet lists the folder's Markdown files.

### Documents

Pressing a document shows it in the pane as Markdown, with a way back to the sheet. Paths resolve
from the folder of the `STATUS.json` that names them; a path that leaves the main checkout is
drawn as plain text. A folder (`evidence`) lists its files. A file not in UTF-8, or over 200 KB,
says so in one line. An `https:` link stays a link. A relative link inside a shown document opens
in the pane by the same rule.

### Surfaces

The same tree on `desktop`, `mobile`, `terminal` and `vscode`, with the elements they all share:
no `Svg`, no `Input`.

## What this does not do

No action on a CR, no order, no merge. No status line, no toast, no watch while the pane is
closed. No file generated by the mod. Nothing on Copilot.

## Documentation

`README.md` says what the board is and names `/chantier-board`. `CONTRIBUTING.md` lists the mod
as part of the plugin and how to test it. The cards do not change: no role uses the board.

## Done when

- `just check` and `just scenario` pass; the scenario checks `landed`, `trashed`, the totals, the
  limit of 50 and the new row fields.
- `claude plugin validate` and `claude plugin test` pass, and the mod type-checks. On Claude
  Desktop `claude` is not on the `PATH`: run the session's own binary, the process `CLAUDE_PID`
  names (`(Get-Process -Id $env:CLAUDE_PID).Path` on Windows). The mod's tests cover
  opening from the skill, the toggle, the worktree path, an unchanged file not being read again,
  no timer after close, a missing index, a bad file, and a path leaving the checkout.
- Run on this repository in the desktop app, the board shows the real state; a `$CHANTIER file`
  appears within 15 seconds; the sheet and a document open and go back.
