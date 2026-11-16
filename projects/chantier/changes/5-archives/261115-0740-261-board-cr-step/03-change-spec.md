# Change Specification: each working CR shows the step it is at, and the board shows the next CR to start

## Goal

The user's request (2026-11-13), from a status map seen on Twitter (zedBSD's work map, its "Phase"
and "owner" columns): on each working CR, show the step it is at and who runs it, such as
"investigator", "coder r3", "inspector", "verifier", "gate scenario", "CI", "rebase", "waits for
the user". Today a CR shows only its round, "r3/6". The user: "étape oui ça a du sens".

The board also shows the next CR to start: the queued CR that starts once a slot frees and its
dependencies are met.

This CR has no `issue:` line.

## Decisions carried from the answers

| Decision (`02-answers.md`, 2026-11-14) | Where |
| --- | --- |
| CS-Q1 (A): the Driver records the CR's step in the record at each step, a small CLI addition; the status, the board and the pane read it | "The record", "The command", "The cards" |
| CS-Q2 (B): the step shows everywhere: the board's Batch view and Kanban cards, `chantier status`, `STATUS.md` and `STATUS.json`, and the CR board pane (`hooks/register.tsx`); so `just mod`, and a pane screenshot from a real session (`AGENTS.md`) | "Where the step shows", "Evidence" |
| CS-Q3 (A): the board also shows the next CR to start | "The next CR to start" |

The request's open point "runs after CR-225 board-read-views" is met: CR-225 is merged
(`5-archives/261114-1354-225-board-read-views/`), and its Batch view and Kanban are on `main`.
This CR has no `depends.json`.

## The words

- **The step** (the user's word, "étape"): what the CR's Driver is doing now. The existing
  `step` field of `STATUS.json` (`Queued`, `Round`, `CI`, `Notify`…, from `status/words.py`
  `step()`) keeps its meaning and its values; to avoid two fields of one name, the new data is
  named `phase` in the record and in the JSON. Every text the user reads says "Step".
- **Who runs it** is in the step's own word: a worker's role (`investigator`, `coder`,
  `inspector`, `verifier`, `debugger`, `conflict resolver`, a review step's name) or the Driver's
  own work (`gate`, `CI`, `rebase`, `PR`). No separate owner column.

## The record

`skills/chantier/scripts/cli/src/chantier/core/records.py`:

- `CrEntry` gains `phase: str | None = None` (one value of the vocabulary below) and
  `phase_detail: str | None = None` and `phase_at: str | None = None` (the time it was recorded,
  as `core/clock.py` writes times).
- `EventRecord` gains `phase: str | None = None`, so the event of the command below keeps it.

The vocabulary, and the text each value shows (`<n>` is the CR's `round` at the time the text is
drawn, so an inspector after round 3 reads `inspector r3`):

| `phase` | Detail | Shown |
| --- | --- | --- |
| `investigator` | - | `investigator` |
| `coder` | - | `coder r<n>` |
| `inspector` | - | `inspector r<n>` |
| `review` | required: the review step's name, as the Driver's `Team:` gives it | `<name> r<n>` |
| `debugger` | - | `debugger` |
| `conflict-resolver` | - | `conflict resolver` |
| `rebase` | - | `rebase` |
| `gate` | optional: the gate's name, e.g. `scenario` | `gate <detail>`, else `gate` |
| `pr` | - | `PR` (the push, the PR, `ship`, the body) |
| `ci` | - | `CI` |
| `verifier` | - | `verifier` |
| `release` | optional: the procedure's step | `release <detail>`, else `release` |

One function draws the text, in `status/words.py`, `phase_text(c: CrEntry) -> str | None`:

- a `working` CR with a phase: its text from the table;
- a `working` CR with none recorded: `None` (drawn `-`);
- a `blocked` CR that is not `waits_on(c)` (a `waits:` reason): `waits for the user`;
- any other CR: `None`.

Every surface below copies this text; none computes its own.

## The command

`chantier phase <cr> <phase> [detail...]`, declared in `declare/driver.py` beside `note`
(scope `BATCH`: `--batch`), handled in `commands/driver.py`:

- `<phase>` is one of the vocabulary (argparse `choices`): another word is refused, exit 2.
- Refused, exit 2, on a CR that is not `working` (`LIVE`): "`<cr>` is `<status>`: no Driver to
  record a step".
- Refused, exit 2, for `review` with no detail.
- The detail is joined to one line, at most 40 characters (refused past it, exit 2), and kept in
  `phase_detail`; it is cleared when the value takes none.
- It sets `phase`, `phase_detail` and `phase_at`, touches the CR (`b.touch(c)`), logs the event
  `phase` with `phase=` and `note=` (the detail), under `actor="driver"`, inside
  `RenderedBatch` so the STATUS files are rewritten as for `note`.
- It prints `ok` and the `context:` line, as `note` does (`context_line`), so the Driver reads its
  context at each step, as the Driver card asks after `round` and `note`.

The CLI records it without the Driver's call where it already sees the step:

- `round` sets `phase` to `coder` (the round is counted just before the round's coder).
- `take` clears `phase`, `phase_detail` and `phase_at` (a new Driver starts).
- `handback`, `ready` or `blocked`, clears them (the state and its label say the rest; a blocked
  CR shows `waits for the user` by the rule above).

The event `phase` does not enter a CR's Progress list (`status/views.py` `_step_entries` already
skips the kinds it does not name: keep it so) and does not enter the board's Recent activity
(`board/web/js/model/events.js` skips it). `chantier log <cr>` shows it as any event.

The CLI judges nothing about the order of steps; it refuses only the cases above.

## Where the step shows

### `STATUS.json` and `STATUS.md` (`status/views.py`, `status/markdown.py`)

- The CR page's view (`cr_view`) gains `phase` (the text, or `null`) and `phase_at`.
- A batch row and a dashboard row (`_row`) gain `phase` (the text, or `null`).
- The schema stays 3: the fields are added, none changes meaning; a reader of an older file
  finds none and draws `-`.
- `_rows_markdown`: the table becomes `| CR | Subject | Status | Step | Branch | PR | Cost |`, the
  Step cell the text or `-`. It serves the batch's `STATUS.md` and the dashboard's.
- `cr_markdown`: a line `**Step:** <text>` after `**Next:**`, only when the text is not `null`.

### `chantier status` (`commands/batch_status.py`)

`_cr_row` adds ` | step: <text>` after the state, round and PR, before the waits, only when the
text is not `None`. Nothing else in the row moves.

### The web board

Read data (`board/crs.py`, `_row`): `phase` (the text from `phase_text`) and `next_to_start`
(below). The views:

- **Batch view, the graph's node** (`board/web/js/views/batch-graph.js`, `node`): one line under
  the title with the step, only when there is one, in the node's meta style.
- **Kanban, a batch CR's card** (`board/web/js/views/kanban-cards.js`, `crCard`): the step in the
  meta row, before "round r/limit", only when there is one.
- The words go through `model/words.js` and both language files (`i18n/en.js`, `i18n/fr.js`):
  "Step" / "Étape" as the accessible label; the step's own text is the CLI's, in English, as the
  labels are.
- CSS in `css/views/batch.css` and `css/views/kanban.css`, by the tokens, within the targets of
  CR-225 (`just check`'s ESLint, Stylelint and Prettier).

### The CR board pane (`hooks/register.tsx`, `types/index.d.ts`)

- `ChantierRow` gains `phase?: string | null`; the CR sheet's type gains `phase?: string | null`.
- The CR tables (`Crs`) get the columns `CR | Subject | State | Step | PR | Cost`, the Step cell
  `cell(r.phase ?? '-')`. The merged and trashed tables (`Pasts`) keep their five columns: give
  them their own column constant.
- The CR sheet: a line `Step: <text>` under the label line, only when not null.
- `hooks/register.test.tsx` covers a row with a step, one without, and a file with no `phase`
  field (an older `STATUS.json`).
- `AGENTS.md`'s screenshot rule applies (see "Evidence").

## The next CR to start

One function, `next_to_start(d: BatchRecord) -> str | None`, in `status/words.py` beside
`can_start`, from the record only:

- `None` when the batch's budget is spent (`over_budget`): `take` would refuse any CR.
- Else the queued CR of the lowest `order` whose `waits(d, c)` is empty (in a series that list
  holds the predecessor, so it is `take`'s next CR); `None` when every queued CR waits.

It is a reading by order: the Foreman may take another CR that `take` accepts (`foreman.md`, "pick
among the CRs `take` would accept"). The board says "next to start", never "will start".

Shown on the board only (CS-Q3):

- `board/crs.py`: each row's `next_to_start` is true for that CR alone.
- Batch view, the Slots figure (`views/batch.js`): its sub-line becomes "N queued · next: CR-n"
  when there is one ("N queued" as today when there is none).
- Batch view, the node, and Kanban, the card: a tag "next to start" ("prochaine à démarrer") beside
  the state tag, in the queued grey.

`STATUS.json`, `STATUS.md`, `chantier status` and the pane do not show it.

## The cards

- `skills/chantier/references/driver.md`, "Your means": one bullet. `$CHANTIER phase <cr>
  <phase> [detail]` before each step of the vocabulary, as the step starts: `investigator` before
  the investigator, `inspector` before the round's inspector, `review <name>` before each review
  step of `Team:`, `rebase`, `gate <name>` before `gate`, `pr` before the push and the PR, `ci`
  while CI runs, `verifier` before each verifier, `debugger` and `conflict-resolver` before those.
  `round` records `coder` itself; `take` and `handback` clear the step. A step is one call, not
  chained with another command. A step left unrecorded shows the last one: record each.
- `driver.md`, "Release driver": `phase <cr> release <step>` at each step of the procedure.
- The Stack driver and the QA driver record none (no CR of their own is `working` with them).
- `skills/chantier/references/concepts.md`: where it lists what a CR's `STATUS.json` holds or the
  Driver's commands, add `phase` there, in one line.
- No agent file changes (`agents/`, `com.github.copilot/agents/`): the contract lives in the card.
- `status-layout.md` does not change: the report skeleton's columns are fixed, and the State cell
  still copies the label.

## The docs

- `docs/web-board.md` and `docs/boards.md`: one line each, saying a working CR shows its step,
  a blocked one "waits for the user", and the board marks the next CR to start.
- The demo planning folder's batch (`docs/demo/projects/shop-api/changes/4-batch/batch.json`):
  its working CRs get a `phase`, so the screenshots `scripts/docs_screenshots.py` retakes show
  it; the screenshots of the Batch view and the Kanban are retaken with that command.

## Out of scope

- An owner column apart from the step's word.
- The time spent per step, a history of steps, or an alarm on a step held too long (the pane's
  silent mark stays as it is).
- The CLI checking the order of steps, or refusing a stale one.
- The step in the Chief of Staff's or the Foreman's reports (`status-layout.md`: no new column).
- The next CR to start anywhere but the board.
- A step for the stack driver, the QA driver or a QA order.
- A version bump.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them.

- **E1.** `just check` passes on Windows, then in CI on Linux, macOS and Windows (CI unchanged:
  `.github/workflows/ci.yml` runs `just check` as today).
- **E2.** `just mod` passes (the change touches `hooks/` and `types/`); the Driver runs it
  itself, and stops and says so if it cannot (`AGENTS.md`).
- **E3.** `just scenario` passes on both forges, with these checks added where CR-101 runs its
  first round (`scenario/run_scenario.py`, near "`round` counts the round"):
  - after `round`, the CR's `STATUS.json` and its batch row say `phase` `coder r1`;
  - `phase CR-101 inspector` → `inspector r1`; `phase CR-101 gate scenario` → `gate scenario`,
    and `chantier status`'s row holds `step: gate scenario`, the batch's `STATUS.md` a Step cell
    `gate scenario`;
  - `phase` on a queued CR, with an unknown word, and `review` with no detail: each exit 2, the
    record unchanged;
  - the event `phase` is in `events.jsonl` and not in the CR's Progress steps;
  - after `handback ready` the `phase` is `null`; after a `handback blocked question: …` it reads
    `waits for the user`; after a `take` it is `null`;
  - the board's read data names `next_to_start` on the queued CR of the lowest order with
    nothing to wait for, and on none once the budget is spent.
- **E4.** Unit tests stay few (`tests/`): one for `phase_text` over the table's values and the
  blocked and ended cases, one for `next_to_start` (order, waits, budget, series).
- **E5. The pane.** One screenshot of the CR board pane from a real Claude Code session running
  the PR's head, a working CR showing its Step cell, captioned with the head's SHA (seven
  characters), in the PR's Deliverables. Until it is there, Known gaps names it ("no screenshot
  of the pane from a real session") and the ready line quotes it (`AGENTS.md`,
  `CONTRIBUTING.md`).
- **E6. The board.** On a scratch batch made with the CLI (as the scenario does), PC and phone
  screenshots of the Batch view and the Kanban showing: a working CR's step, a blocked CR's
  "waits for the user", the "next to start" tag and the Slots line "N queued · next: CR-n";
  each captioned with the head's SHA7. The browser's console shows no error.

## Open questions for the user

1. **The next CR to start is read by order.** Default: the queued CR of the lowest order with
   nothing to wait for, none when every queued CR waits or the budget is spent. The Foreman may
   take another one `take` accepts (it puts a critical-path CR first, for instance), so the
   board's mark can name a CR the Foreman then passes over. Is a reading by order enough, or must
   the Foreman record its own choice?
2. **A step the Driver forgets to record stays shown.** Default: the board and the pane show the
   last step recorded with no age; the pane's existing silence mark is the only alarm. Show the
   step's age ("since 14:02") as well?
3. **"Waits for the user" on a blocked CR only.** Default: a blocked CR (not a `waits:` one)
   shows "waits for the user"; a CR ready to merge, which also waits for the user's merge, shows
   no step (its label already says "ready to merge"). Show "waits for your merge" there too?
