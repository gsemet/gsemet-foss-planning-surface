# Change Specification: `status` prints a trigger line when the first stack is due

## Goal

In batch-24 the first `take stack` was missed: CR-324 and CR-326 were handed back `ready` with a PR,
yet the first stack driver started only at 18:39 and the first ask came at 18:48. The rule exists in
the Foreman's card ("The first take"), but it rested on the Foreman remembering it. From now on,
while the batch's first stack is due, `chantier status` prints one line that says so (`stack: take
stack now: ...`), so the Foreman (or the Chief of Staff in direct mode) sees it on its next wake.

## Decisions carried from `02-answers.md`

- trigger-Q1: the first `take stack` only (the moment the stack can form). The later takes (a CR's
  first PR, a restack after a merge, the final order) stay led by the Foreman's card.
- trigger-Q2, as narrowed by the user's retro-Q1: the line shows in a running stack batch while: no
  stack driver is recorded; no CR of the batch, merged and cancelled ones included, has been placed
  by `stack` (so the line never comes back once a stack was made, even after it fully merged); two
  CRs or more of the stack, release and fix CRs aside, are `ready` with a PR, none of them depending
  on an open CR that is not `ready`. A batch switched to a stack by `order mode` follows the same
  rule (see "What the code has today": leaving a stack clears every CR's mark).
- retro-Q1 (the user): the line is for the batch's very first take only; `stacked` is checked on
  every CR of the batch, merged ones included; later takes stay with the Foreman's card.
- trigger-Q3: one line of the `status` command's output only; not in `STATUS.md`, `STATUS.json`,
  the CR board pane or the web board; nothing recorded.
- trigger-Q4: the words `stack: take stack now: <cr>, <cr> ready with a PR, no stack made yet
  (`take stack --epoch <n>`)`, the CRs in the stack's order.
- trigger-Q5: a reminder, not a rail: it refuses nothing and starts nothing; `take stack` is
  unchanged.
- trigger-Q6: the Foreman's card names the line as the first take's trigger, taken in the same turn.

## What the code has today (read 2026-11-17, `C:\Users\gaeta\Projets\chantier`, main at a65a8d3d)

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless named otherwise.

- `stacks.py`: `chain(d)` (the open CRs of a stack batch, release last, fix CRs out; `[]` outside a
  stack), `FORMING = 2`, and `stack_forms(d)`, "two CRs or more of the stack, the release and a
  fix CR aside, are handed back `ready` with a PR". `stack_forms` has no caller today, and it does
  not check the dependency condition of the card. `_open_after(d, c)` gives a CR's dependencies
  still open.
- `core/records.py`: `CrEntry.stacked` (set to `True` by the `stack` command,
  `commands/delivery.py` around line 225, and kept on a CR once it is merged; cleared for every CR
  of the batch, merged ones included, when the batch leaves a stack, `commands/orders_apply.py`,
  `_mode`), and `BatchRecord.stack_agent` (set by `agents set stack`). So a batch that leaves a
  stack and comes back to one gets the line again for its new first stack: that is trigger-Q2's
  mode-switch case, and it holds as is.
- `commands/batch_status.py` (379 lines; `MAX_FILE_LINES` is 400 in
  `skills/chantier/scripts/cli/tests/test_code_targets.py`), `status(args)`: builds the output
  lines (the batch line, autosync, other batches, the unpaused line, the last closed batch, one row
  per CR, `_order_lines`, `_seen_lines` for `board saw merged`, then the unread asks count). It
  already imports `state_word` from `chantier.stacks`. The CR record-sees-forge-merged-pr (same
  batch) grows `_seen_lines` in this file.
- Cards: `skills/chantier/references/foreman.md`, "A stack batch ... The stack grows from the
  bottom", bullet **The first take** (around line 274), and "A mode switch", *to a stack* (around
  line 350). The Chief of Staff in direct mode follows `foreman.md` ("Steering a batch yourself"),
  so no change to `chief-of-staff.md` is needed.

## What changes

### 1. The condition and the line (`stacks.py`)

- Replace the unused `stack_forms(d) -> bool` with `stack_due(d) -> list[CrEntry]`: the CRs that
  make the batch's first stack due, in `chain` order, or `[]` when it is not due. It returns the
  list when all hold, else `[]`:
  - `d.mode == "stack"` and `d.status == "running"`;
  - `d.stack_agent` is not set;
  - no CR of `d.crs` (every CR of the batch, merged and cancelled ones included, not only
    `chain(d)`) has `stacked` set (retro-Q1);
  - the CRs of `chain(d)` that are neither release nor fix, with `status == "ready"`, a `pr`, and
    every dependency of `_open_after(d, c)` with `status == "ready"`, number `FORMING` or more;
    those are the CRs returned.
- Beside it, `stack_line(d) -> list[str]`: with `stack_due(d)` non-empty, one line
  `stack: take stack now: CR-324, CR-326 ready with a PR, no stack made yet (`take stack --epoch
  <n>`)` (ids joined by `, `, the literal `<n>`); else `[]`. The line's text lives here, not in
  `batch_status.py`.
- Keep `FORMING`; update its comment if it names `stack_forms`.

### 2. The call (`commands/batch_status.py`)

- Only the call: `stack_line` joins the existing `from chantier.stacks import ...` line, and
  `status` appends `*stack_line(d)` right after the CR rows and before `_order_lines`. Shown with or
  without `--refresh` and `--notes`; it writes nothing. No helper is added in this file.
- The file stays at or under 400 lines (`MAX_FILE_LINES`) with record-sees-forge-merged-pr's change
  to `_seen_lines` in too. This CR adds at most one or two lines; if the rebase on the other CR
  would cross 400, move code out of `batch_status.py` (for example `_seen_lines` into a module of
  its own) rather than raise the limit.

### 3. The card (`skills/chantier/references/foreman.md`)

- **The first take** bullet: add one sentence: while it is due, `status` prints `stack: take stack
  now: <crs> ...`; that line is the trigger: take it in the same turn you read it (the bullet's rule
  stays the reference; the line only reminds it, and only for the batch's first stack).
- "A mode switch", *to a stack*: no change of rule; optionally one clause that the same `status`
  line names the first take there too.
- Nothing in `chief-of-staff.md`, `driver.md`, `concepts.md`, the agent files or the hooks.

### 4. Scenario and its README

- `scenario/run_scenario.py`, `stack_batch` (step 13, "A stack on request ..."): the scripted
  Foreman's early `take stack` there is followed by `agents set stack -` and no `stack` call, so
  after the driver rounds hand the CRs back `ready` with a PR and before the first `stack <crs>`
  call, add checks:
  - `status` prints one `stack: take stack now:` line naming the ready CRs in order;
  - with a stack driver recorded (`agents set stack <id>`), the line is absent; then `agents set
    stack -` again;
  - after `stack <crs>` marks them, the line is absent; and, where the step later records the
    stack's merge, the line is still absent after it.
  If the step's order makes one of these points unreachable, place it at the nearest point of the
  same step where the condition holds, and say so in the PR.
- `scenario/README.md`: one item in the stack list (beside "a stack (`open --mode stack`) of
  independent CRs ...") that names the trigger line and its checks, with its `(test: ...)` tag for
  the unit test below, in the file's format.

## Out of scope

- No line for the later takes (first PR of a CR, restack after a merge, final order), and no line
  for a second stack after the first one merged (trigger-Q1, retro-Q1).
- No field in `STATUS.md`, `STATUS.json`, the CR board pane or the web board (trigger-Q3); so no
  pane screenshot is owed under AGENTS.md.
- No rail: `take stack` keeps its refusals; nothing starts automatically (trigger-Q5).
- No new command, no new record field, no event.
- No change on parallel or series batches.

## Evidence and gates (AGENTS.md)

- One parametrized unit test, in-process, on prepared `BatchRecord`s of `stack_due` and
  `stack_line` (in `skills/chantier/scripts/cli/tests/test_stack_label.py`, its docstring widened,
  or a small file of its own), cases: two ready CRs with a PR, none stacked, no agent: due, both
  named in order, and the exact line; only one ready with a PR: not due; a stack driver recorded:
  not due; one open CR already `stacked`: not due; only a merged CR `stacked` and two new CRs ready
  with a PR: not due (retro-Q1); a ready CR whose open dependency is `working`: not counted; a
  release and a fix CR ready with a PR: not counted; a parallel batch: not due; a paused batch: not
  due. Keep `just test` within its budget (at most 30 s above 18.5 s on the user's Windows
  machine).
- `tests/test_code_targets.py` passes: `batch_status.py` at or under 400 lines, with the other CR in.
- `just check`, passing on Linux, macOS and Windows; run in the worktree at the rebased head
  before the first push.
- `just eval-dry-run` in the worktree before the first push (a change under the CLI's `src/`).
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI, a card and the
  scenario). In the batch, if this CR is the stack's top, the local `chantier gate` run of
  `just scenario` at its head (Windows coverage), moving to the CR that joins on top if any.
- Not owed: `just mod` (no change to `hooks/` or `types/`); a pane screenshot (the pane's fields
  are unchanged).
- No version edit by hand.

## Open questions

None.
