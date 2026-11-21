# A batch CR's card shows its batch folder, not its old 3-ready chip

Short name: `chip`. A bug fix in the surface server's batch rows and the web client's batch views.

## Goal

A CR in the batch (`4-batch/`) shows, on its card, the batch folder it is really in (`1-pending`,
`2-actives` or `3-done`) in the place where it showed its old priority chip, never `3-ready` nor
any other backlog bucket (chip-Q1 as changed by answer 3). The backlog views (Triage, the Kanban's
backlog columns, Home's backlog) keep their priority chips as today.

## Why it shows 3-ready today

Every path below is under `skills/chantier/scripts/cli/src/chantier/` (`clients/web/` for the
`js/`, `css/` and `DESIGN.md` paths).

- `board/crs.py:_row` sends, for each CR of the batch, `"priority": priority_of(events, c)`.
- `board/times.py:priority_of` reads the CR's `add` event's `origin` (the folder the CR came
  from): `inbox`, `P1`...`P4` or `3-ready`. For a CR that joined from `3-ready` it says `3-ready`
  for its whole life in the batch.
- Four batch views pass it to the one card, `card({ priority: c.priority, ... })`, and
  `js/ui/card.js:topRow` draws it with `js/ui/parts.js:priorityChip`, first in the top row:
  - `js/views/batch-graph.js:68` (`node`, the Batch graph's node of a CR; `recordedNode` above it
    draws no chip and stays so);
  - `js/views/batch-gantt.js:64` (`label`, the Gantt's label cell);
  - `js/views/batch-timecards.js:55` (`timecard`, the Batch time card);
  - `js/views/batch-pr-card.js:76` (`prCard`, the PRs page's card, used by `js/views/batch-prs.js`).
- No other view reads a batch row's `priority`. `js/views/kanban-cards.js:53` (the Kanban's card
  of a batch CR) draws no priority chip today. The batches' history (`board/state.py:_history`)
  is the raw records and draws no card.

## What changes

### Server: `board/crs.py`, `board/times.py`

- `_row` drops the key `priority` and gains the key `stage`: the CR's batch folder, read from the
  row's own `folder` (`repo.rel(folder)`, relative to the planning folder, for example
  `4-batch/2-actives/425-factory-redefine`): its second part when the first is `4-batch` and the
  second is one of `lifecycle/stages.py:STATE_FOLDERS` (`1-pending`, `2-actives`, `3-done`);
  `None` otherwise (no folder found, or a folder outside `4-batch/`: a cancelled CR moved out to
  `1-inbox` or `2-backlog/P<n>`, or any other place).
- It is read from the folder on disk, never from the CR's state or its events, so it says what the
  user sees in the planning folder.
- `board/times.py:priority_of` (and `PRIORITY_AFTER`, which only it uses) is removed, with its
  import in `crs.py`: nothing reads it then. `tests/test_board_times.py:test_priority_of` goes with
  it, and that file's docstring drops "and priority chip".

### Web client (read `clients/web/DESIGN.md` first and keep it true)

- The four batch views above pass `priority: c.stage` in place of `priority: c.priority`: the
  stage chip takes the priority chip's place, first in the top row, through the same `card.js`
  and `priorityChip` (no new builder, no change to `card.js`'s code). A row with `stage: null`
  draws no chip, as `topRow` already does for an empty `priority`.
- `css/components/chip.css` gains the three classes `priorityChip` writes for them
  (`.tag.pri-1-pending`, `.tag.pri-2-actives`, `.tag.pri-3-done`): one neutral look, the grey of a
  plain chip from existing tokens (the `--chip` fill and its `--edge`, the ordinary ink), so a
  stage never reads as a priority. No new token: DESIGN.md's token table is unchanged.
- The chip's text is the folder's name as it is (`1-pending`, `2-actives`, `3-done`): data shown as
  it is (DESIGN.md "Words"), no i18n key.
- Comments follow: `js/ui/parts.js` (the priority chip's `bucket` may also be a batch folder),
  `js/ui/card.js` line 7 (`priority`: a bucket or a batch folder), `js/views/batch-gantt.js:59`
  ("its priority chip" becomes "its batch folder chip").
- `DESIGN.md`, rule "One card, one column, one chip": after "on every card that has a priority
  (inbox, P1 to P4, 3-ready)", one sentence: a card of a CR in the batch shows in that place its
  batch folder (`1-pending`, `2-actives`, `3-done`) in a neutral grey chip, never a priority.

## Decisions carried

- chip-Q1, answer 3 (replacing answer 1's "no chip"): a batch CR's card shows its real folder in
  the batch in place of the old priority chip, never `3-ready`.
- chip-Q1's restatement, as far as answer 3 leaves it: this holds in every board view that draws
  the CR as a batch CR with that chip (the batch graph first); the backlog views keep their chips.
- chip-Q2: destination batch-30, at once.

## Out of scope

- The Kanban's card of a batch CR (`js/views/kanban-cards.js`): it has no priority chip today, so
  there is nothing to replace; its column already names its state. See the open question.
- Any colour per stage, any new token, any change to the state badges, the backlog's chips, the
  `add` event's `origin` or the record.
- CR-427's Triage "running batch" half, beyond the note below.

## Overlap with batch-30

- **CR-427 `board-running-batch-lane`** (in `1-pending`):
  - its top half draws the batch's pending CRs (`state.data.batch.crs`, state `queued`) as item
    cards with `js/ui/card.js`. Those are batch CRs: they must show `1-pending` through
    `priority: c.stage`, never `c.priority`, which this CR removes. Whichever of the two lands
    second carries it (CR-427's Driver, if this CR is merged first; this CR's, otherwise).
  - both edit the same DESIGN.md rule, "One card, one column, one chip" (CR-427 adds a lane
    sentence after the column's): a textual conflict on rebase only, not a dependency; no
    `depends.json`.
- **CR-429 `board-fingerprint-cache`**: no overlap. It changes how and when the server reads the
  planning folder (a file watch, `board/fingerprint.py`, `board/api/`), not the rows' fields;
  `board/crs.py` and the web client are not in it.

## Evidence

- Server, in-process (`tests/test_board_waits.py`'s pattern: `forge_world.World`, `write_batch`,
  `cr_rows`): one parametrized test in an existing board test file, with an `add` event whose
  `origin` is `3-ready/<slug>` and a CR whose `path` is a folder in each of `4-batch/1-pending`,
  `4-batch/2-actives`, `4-batch/3-done`, one in `2-backlog/P2` (a cancelled CR moved out) and one
  with no folder on disk: `stage` is `1-pending`, `2-actives`, `3-done`, `None`, `None`, and no
  row has the key `priority`.
- Web client, from the shipped files (read from the repository at the head under test, as
  `tests/test_board_design.py` reads them, no prepared copy): no file under `clients/web/js/`
  holds `c.priority`; each of the four batch views holds `priority: c.stage`;
  `css/components/chip.css` holds a rule for each of `.tag.pri-1-pending`, `.tag.pri-2-actives`
  and `.tag.pri-3-done`. The existing design tests (one card, components, tokens) keep passing.
- `just check` passes; `just eval-dry-run` in the worktree (a change under the CLI's `src/`); the
  pipeline's `just scenario (ubuntu-latest)` green at the PR's head (a CLI change).
- By hand, on a running board with batch-30: the batch graph, the Gantt, the time cards and the
  PRs page show `2-actives` on an active CR's card and `1-pending` on a pending one's, never
  `3-ready`; Triage and the Kanban's backlog columns still show their priority chips.

## Open questions

1. The Kanban's card of a batch CR (`js/views/kanban-cards.js:53`) has no chip today. Should it
   also show its batch folder chip, for one look across views, or stay as it is (its column
   already says its state)? This spec leaves it as it is.
