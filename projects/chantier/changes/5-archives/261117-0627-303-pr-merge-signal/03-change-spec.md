# Change Specification: the board signals a merge it sees

## Goal

The user's words (2026-11-15, batch-18): "a 'monitor PR' that refreshes by itself so that I know
which PR is merged." The CR `pr-monitor` gives the user a read-only PRs page on the web board.
This CR, split from it on 2026-11-16 (Q11), closes the loop: when that page's forge read finds a PR
merged that the record does not hold yet, the board leaves one line in a local file, and
`chantier status` prints it for the Chief of Staff, who records the merge (`order merged`) at its
next `status`. The board itself records nothing.

**Its grill is `pr-monitor`'s:** `projects/chantier/changes/2-backlog/P1/pr-monitor/02-answers.md`,
answers Q4, Q5, Q10, Q11 and Q13 (this CR's folder holds only `intake/request.md`).

**It comes after `pr-monitor`:** it builds on that CR's route `GET /api/projects/<id>/prs`
(`board/prs.py`), its forge read and its rows (`state`, `merged_into`, `merged_at`). It starts only
once `pr-monitor` is merged, or stacked on it in the same batch.

## Decisions carried from pr-monitor's 02-answers.md

| Answer | Decision | Where it lands |
| --- | --- | --- |
| Q4 | A merge the view sees is signalled, not recorded. The view changes nothing in the batch. It leaves a line the Chief of Staff reads at its next heartbeat, and the Chief of Staff still records the merge (`order merged`). Today the board never edits a batch and never messages an agent (AGENTS.md): this signal is a second named exception for the board, said in AGENTS.md with the first (`pr-monitor`'s forge read). | 1, 2, 4 |
| Q5 | In Foreman mode too, the Chief of Staff sees the line and records the merge at its own next `status`. The Foreman does nothing more with it and sends no extra message. | 2, 3 |
| Q10 | Q5 stays. When nothing runs (no heartbeat, the batch-18 case), the PRs page's row says "merged on the forge, not recorded yet: tell the Chief of Staff", and the docs say so. The row text is already drawn by `pr-monitor`'s page and does not change here; this CR adds the docs' side: the signal is read only when a `status` runs, and with nothing running the user tells the Chief of Staff, as the row says. | 4 |
| Q11 | Two CRs. This one holds the merge signal: `board-seen.jsonl`, the `status` line, the two cards, the second AGENTS.md exception, Q4, Q5, Q10. | Whole spec |
| Q13 | In a stacked batch, a PR merged into the PR under it (another CR's branch) is signalled, with its branch in the line. The Chief of Staff does not record it as merged: it tells the user where it went and waits until the PR under it lands. | 1, 2, 3 |

No other decision is made here.

## What changes

### 1. The signal file (board server, `skills/chantier/scripts/cli/src/chantier/board/`)

- In `pr-monitor`'s route (`board/prs.py`), after a forge read: for each row whose forge state is
  `merged` and whose CR the record does not show merged (`crs[].state != "merged"`), the server
  appends one line, once per batch and CR, to a new local file at the planning folder's root,
  `board-seen.jsonl`:
  `{"t": <now>, "kind": "merged", "batch": <batch id>, "cr": <cr>, "pr": <link>, "into": <the branch it was merged into>, "merged_at": <the forge's time>}`.
  `into` is the row's `merged_into` branch, carried as it is, with `into_cr`: the CR whose branch it is, or null when it is no CR's branch (the default branch). A merge into another CR's branch is signalled too (Q13).
- It is written under the lifecycle lock (`changes_lock`), as `board/journal.py`'s `_append`
  does, in UTF-8. Before writing, the server reads the file for that batch and CR: a later read
  that sees the same merge writes nothing more. A cached read (less than 10 s old, `pr-monitor`'s
  rule) writes nothing. A PR closed without a merge writes no line: only a merge is signalled.
- The file is local and never published: add `board-seen.jsonl` to `IGNORED` in `core/files.py`
  and to `SINGLE` in `board/fingerprint.py`, as `board-journal.jsonl` is. It is not the board's
  journal: it does not count in the "Written by the board" tile, and the rescan does not clear it.
- The board never edits `batch.json`, `events.jsonl` or a STATUS file, never runs `order`, and
  never sends a message to a session. The line is only a file that `status` reads.
- `pr-monitor`'s read-only rule for the route (nothing written in the planning folder) becomes
  "nothing written apart from `board-seen.jsonl`"; its test is changed to match.

### 2. Where the Chief of Staff reads it (`commands/batch_status.py`)

- `chantier status`, in every form (the Chief of Staff's own `status` and `status --refresh`, and
  the Foreman's heartbeat `status --refresh --batch <batch> --epoch <n>`), prints one line for each
  entry of `board-seen.jsonl` for the current batch whose CR the record does not yet show merged,
  next to the order lines (a helper beside `_order_lines` and `_autosync_lines`):
  `board saw merged: <cr> <pr link> into <branch> at <merged_at>; for the Chief of Staff: order merged <cr>`.
  For a merge into another CR's branch (`into_cr` set, Q13) the tail differs:
  `board saw merged: <cr> <pr link> into <into_cr>'s branch at <merged_at>; for the Chief of Staff: not landed, tell the user, record nothing until <into_cr> lands`.
- Once the merge is recorded the line no longer prints, so nothing has to clear the file. A CR
  cancelled since prints no line either. The batch's `close` leaves the file alone; entries for
  another batch never print. An unreadable line of the file is skipped and named once in the
  output (`board-seen.jsonl: line <n> unreadable`), never guessed.
- `status` writes nothing for this: it reads the file.

### 3. Cards (`skills/chantier/references/`)

- `chief-of-staff.md`, the "While it runs" row "add, drop, reorder, change a CR; \"I merged #42\";
  …" (line 30): add "a `board saw merged` line in `status`" next to "I merged #42". And in the
  bullet about a merge the user makes before its `ready-to-merge` line ("record it as any merge"):
  a `board saw merged: <cr> …` line in `status` is a merge the user made; record it like any merge,
  at the `status` that shows it: `order merged <cr>`, then, in Foreman mode, send its line to the
  Foreman as for any order. A line that says `into <other cr>'s branch` (Q13) is not a merge to record: do not run `order merged`; tell the user where the PR went (into `<other cr>`'s PR, not the default branch) and wait until the PR under it lands; the line keeps printing until the CR is recorded merged.
- `foreman.md`, beside the heartbeat bullet (line 617, "Heartbeat: the wake that runs `chantier
  status --refresh --batch <batch> --epoch <n>`"): a `board saw merged` line in `status` is the
  Chief of Staff's; do nothing with it, send no message about it, and it is not an undone order
  for ending the heartbeat (Q5).
- The two host files (`agents/` and `com.github.copilot/agents/`) do not change: no role's body
  changes.

### 4. AGENTS.md, CONTRIBUTING.md and the docs

- `AGENTS.md`, the board's bullet, after `pr-monitor`'s exception for its PRs page: the second
  named exception, in the same sentence family. Proposed wording:

  > and a second, from the same page: when its forge read finds a PR merged that the record does
  > not hold, it appends one line to `board-seen.jsonl` (planning folder, never published), which
  > `status` prints for the Chief of Staff to record at its next `status`; the board itself records
  > nothing and messages no agent;

  The bullet's list of what chantier writes ("chantier writes only in the planning folder …") is
  unchanged: the file is in the planning folder.
- `CONTRIBUTING.md`, the same board paragraph (lines 93-98): the same exception, in the same
  words.
- `docs/web-board.md`, `pr-monitor`'s "### PRs" section: the signal (the board leaves a line;
  `status` prints it; the Chief of Staff records it at its next `status`, in direct and Foreman
  mode alike), and Q10: the signal is read only when a `status` runs; when nothing runs (no
  heartbeat), the row's "merged on the forge, not recorded yet: tell the Chief of Staff" means just
  that: tell the Chief of Staff, who records it. And Q13: a PR merged into another CR's PR is
  signalled with its branch, and the Chief of Staff records nothing until the PR under it lands. The intro line keeps "It never touches a batch."
  (the signal file is not the batch's).
- No picture (as `pr-monitor`).

## Out of scope

- The PRs page, its route, its forge read and its row texts: `pr-monitor`'s, unchanged here
  (Q10's row text included).
- Recording a merge from the board, or any write to `batch.json`, `events.jsonl` or a STATUS file:
  only the Chief of Staff records, with `order merged` (Q4).
- The Foreman acting on the line or relaying it (Q5).
- A message from the board to any session; a notification outside `status`.
- Clearing or rotating `board-seen.jsonl`.
- The CR board pane (`hooks/register.tsx`, `STATUS.json`): unchanged; `just mod` not required.

## Evidence

- **Tests** (`skills/chantier/scripts/cli/tests/test_board.py` and the `status` tests, in-process,
  parametrized, no network; `gh` stubbed as in `pr-monitor`'s tests):
  - A read that finds one PR merged on the forge and not in the record: exactly one
    `board-seen.jsonl` line with its fields (`into` included); a second read, and a cached read,
    write none more. A PR merged into another CR's branch: one line, with `into` and `into_cr` (Q13).
  - A PR closed without a merge: no line.
  - `status` prints `board saw merged: <cr> … for the Chief of Staff: order merged <cr>` for an
    unrecorded merge, parametrized over the direct form and the `--refresh --batch <batch> --epoch
    <n>` form, and stops printing it after `order merged <cr>`; an entry of another batch never
    prints; a cancelled CR's entry never prints; an unreadable line is named, not guessed; an entry with `into_cr` prints the `not landed, tell the user, record nothing until <into_cr> lands` tail, never `order merged` (Q13).
  - `board-seen.jsonl` is in `IGNORED` and in the fingerprint; the rescan leaves it.
  - The route writes nothing in the planning folder but `board-seen.jsonl`.
  - `just test` stays within its budget (AGENTS.md: at most 30 s above 18.5 s).
- **Scenario** (`scenario/run_scenario.py`, unit `surface-board`, extending `pr-monitor`'s steps):
  merge one PR in the fake forge without `order merged`; `GET …/prs`; check `board-seen.jsonl`
  holds one line and `status` prints the `board saw merged` line; run the Foreman's heartbeat form
  of `status` and check it prints the line and the batch's orders are unchanged; `order merged
  <cr>`; `status` no longer prints it. Name the steps in `scenario/README.md` under
  `surface-board`.
- **The cards:** the Chief of Staff's and the Foreman's lines checked by reading, as any card
  change.
- `just check` passes on Linux, macOS and Windows. The PR passes `just scenario (ubuntu-latest)`
  (a CLI, cards and scenario change), and the local Windows run as AGENTS.md says for the CR on top
  of the stack.

## Open questions (for the user)

None: the first run's question is answered in pr-monitor's `02-answers.md` (Q13).
