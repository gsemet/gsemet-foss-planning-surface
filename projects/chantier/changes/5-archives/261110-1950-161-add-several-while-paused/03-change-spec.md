# Add several CRs to a paused batch before it resumes

## Goal

In the user's words: "on peut rajouter n CR quand le batch est en pause avant de le relancer".

While a batch is paused, `order add` can be run any number of times: each run adds one CR and the
batch stays paused. The batch runs again when the first added CR starts, at its `take`. No new
command. The rule is the same in direct and in Foreman mode. A running direct batch stays strict,
and its refusal no longer offers Foreman mode as the way out.

Seen in batch-09 on 2026-11-10: the user asked to add `status-command` and `planning-repo` to the
paused direct batch. The first `order add` (CR-159) set the batch running, so the second was
refused ("a running direct batch is strict"), and `pause` was refused too (CR-159 queued, order
O-11 pending). Only one CR could join per pause.

## Decisions carried from the grill (`02-answers.md`)

1. **What starts the batch again: the first start.** `order add` on a paused batch leaves it
   paused. The batch runs again when the first added CR starts (its `take`). No new command.
2. **Both steerings.** The rule holds in direct and in Foreman mode alike.
3. **The refusal message names only the pause.** When a running direct batch refuses `order add`
   (or `order qa`), the message says to add the CR once the batch is paused. It no longer names
   Foreman mode: which steering fits is the Chief of Staff's judgement (a user on Remote Control
   cannot steer a Foreman session).
4. **Priority:** P1.

## What changes

### CLI: `skills/chantier/scripts/cli/src/chantier/commands.py`

**`order` (function `order`, around lines 1005-1026).**

- The strict refusal on a running direct batch keeps its condition (kind `add` or `qa`, steering
  `direct`, status not `paused`, release and `--fix-for` excepted) and its exit code 2. Its text
  becomes, exactly:
  `a running direct batch is strict: add the CR once the batch is paused (`pause`)`
  (no mention of Foreman mode).
- `order add` on a paused batch no longer changes the batch's state: no `status = "running"`, no
  removal of `paused` or `summary`, no `reopen` event. The CR is added as today (queued, its folder
  in `4-batch/1-pending/`, its `after` recorded, the order recorded and `applied`). The output's
  effect line, in place of `<batch> was paused: running again; ...`, is:
  `<batch> stays paused: the first `take` sets it running again`
  This holds for `order add --release` and `order add --fix-for <cr>` too.
- `order qa` on a paused batch is unchanged: it still sets the batch running at once (its QA
  driver holds a slot from the order on, so the order itself is a start), with today's
  `was paused: running again` line. See open question 1.

**`take` (function `take`, around line 1299).**

- When the batch is paused and the take succeeds (every rail of `check_take` passed, or, for
  `take stack`, the stack checks and the budget passed), the batch is set running in the same
  write: `status = "running"`, `paused` and `summary` removed (the cost to date is void, as today
  at `order add`), and the event `reopen` logged before the `take` event. A refused take leaves
  the batch paused and unchanged.
- The output gains, right after the `took <cr> (...)` line, the line
  `<batch> was paused: running again; `pause` runs again at the end`.
- A take on a running batch prints nothing new.

**`pause` (function `pause`, around line 1696).** The refusal on a paused batch keeps its condition
and code; its text becomes
`<batch> is already paused (at <time>): `order add` adds work, the first `take` sets it running again, then `pause` runs again`.
Update the docstring ("`order add` sets it running first") to the same rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/state.py`

- `find_cr_batch` (around line 554) no longer skips a paused batch: a paused batch can now hold
  queued CRs, and `take <cr>` without `--batch` (and without `CHANTIER_BATCH`) must find the CR
  there. Its docstring and its error say "batch", not "running batch" (one batch at a time). The
  error text becomes `no batch holds <cr>`.
- `resolve_batch` and `open_batches` are unchanged: `status`, `cost` and `order` without `--batch`
  on a paused batch still answer `no running batch` (as `docs/use-cases.md` says).

### CLI: `skills/chantier/scripts/cli/src/chantier/lifecycle.py`

- `ensure_unclaimed` (around line 104) no longer skips a paused batch: its queued CRs are claims
  like a running batch's (merged and cancelled CRs stay ignored, as today). A CR folder already
  in a paused batch cannot be added a second time.

### CLI help: `skills/chantier/scripts/cli/src/chantier/cli.py`

- The `pause` help (line 168) stays as is unless it names `order add` as what sets the batch
  running; check the `order` and `take` help strings for the same and align them with the rule.

### Cards (`skills/chantier/references/`)

- `concepts.md`, **Batch** (lines 67-71): `order add` on a paused batch leaves it paused, any
  number of times; the first `take` sets it running again; `pause` runs again at the end and is
  refused on a batch already paused. Keep: a running direct batch is strict (`order add` and
  `order qa` refused, except a release CR); `order qa` on a paused batch sets it running at once.
- `concepts.md`, **Batch lifecycle**, item 3 **Paused** (lines 92-95): "It takes new CRs:
  `order add` adds them, any number, and the batch stays paused; the first `take` (or an
  `order qa`) sets it running again, and it pauses again at the end with the cost to date, which
  has grown." The closing paragraph (line 100-101) says the same in a few words.
- `chief-of-staff.md`, **The pause** bullet (lines 323-325): new work for the paused batch is
  `order add`, once per CR; the batch stays paused until the Foreman's first `take`; send the
  Foreman the usual order once all are added.
- `chief-of-staff.md`, **Closing** bullet (line 335): "on a batch set running again by a `take`
  or `order qa`" in place of "by `order add` or `order qa`".
- `chief-of-staff.md`, **The running batch is strict** (lines 382-385): unchanged rule; add that
  once paused, the batch takes any number of CRs before its first `take`.
- `chief-of-staff.md`, **The pause** in "Steering a batch yourself" (lines 393-396): "on their
  word, `order add --note <folder>` for each CR: the batch stays paused; your first `take` sets it
  running again, and `pause` runs again at the end."
- `foreman.md`, **Your goal** (lines 22-24): an order that adds work leaves the batch paused; your
  first `take` sets it running again; `pause` again at the end (`pause` on a paused batch is
  refused).

The agent files (`agents/`, `com.github.copilot/agents/`) hold no role contract and need no
change.

### Docs

The diagrams say what chantier should be: change each text and its SVG together.

- `docs/batch-lifecycle-texts.md`: the long description (line 3: "chantier order add (or order qa)
  sets it running again" becomes "chantier order add adds new CRs, any number, and the batch stays
  paused; the first take (or an order qa) sets it running again"), the "Paused to running" blocks
  (lines 116-126: the label `chantier order add`, then `the first take (or order qa)`, then the
  sentence "new CRs join it, any number; the first take sets it running again; it pauses again at
  the end, the cost to date grown"), and the same texts in `docs/batch-lifecycle.svg` (around
  lines 93-98, and its long description at line 3), fitted to the existing boxes.
- `docs/cr-lifecycle-texts.md` line 509 and `docs/cr-lifecycle.svg` line 283: "the batch is
  paused; new CRs join it, and the first take sets it running again".
- `docs/use-cases.md` lines 34-35, `docs/use-cases-foreman.md` lines 69-70,
  `docs/use-cases-direct.md` lines 20-22 and 65-66, `README.md` lines 13, 109 and 306-310: the same
  rule in the page's words (several CRs join a paused batch; the first start sets it running).
  `use-cases-direct.md` line 63 example may become "Grill the CSV export and the import, then add
  them to this batch."
- `scenario/README.md` lines 42 and 74-76: the direct mode line ("two CRs added to the paused
  batch, which stays paused until the first `take`") and the paused-batch line ("`order add`
  leaving it paused, `take` setting it running again").
- The release notes of past versions are not edited.

## Out of scope

- A new command (resume or otherwise): none, by the grill.
- `order qa` on a paused batch: it keeps setting the batch running at once (open question 1).
- `status`, `cost` and `order` without `--batch` on a paused batch: they still answer `no running
  batch`.
- The status-line hook (`hooks/register.tsx`) folds a paused batch; it stays so, queued CRs and all.
- Switching steering modes, and what the Chief of Staff proposes on Remote Control (the inbox item
  `options-by-environment`).
- The release's `order confirm` rule ("voided by a CR added after") is unchanged.

## Evidence

Run at the pushed head, with the output kept:

1. `just check` passes (Linux, macOS, Windows in CI).
2. `just scenario` passes (a CLI, cards and scenario change).

### Structure test: `skills/chantier/scripts/cli/tests/test_structure.py`

In `test_a_direct_batch_is_recorded_shown_and_strict` (line 283-285), the refusal of `order add`
and `order qa` on the running direct batch also asserts `"Foreman mode" not in err` and
`"once the batch is paused" in err`. No new test: the batch workflow belongs to the scenario.

### Scenario: `scenario/run_scenario.py`

- **Direct mode** (around lines 953-968, "a paused batch takes new work"): prepare a second CR
  beside `later`; run `order add` for both on the paused direct batch. Check after each that the
  exit is 0, the batch is still `paused` (with its `paused` time and `summary` kept), the CR is
  `queued`, and the output says `stays paused: the first `take` sets it running again`. Check
  that both CRs are in the batch. Then `fm.turn()`: check that the first `take` sets the batch
  `running` with `paused` and `summary` gone, that its output has `was paused: running again`,
  that the event log has `reopen` before that `take`, and that both new CRs are started (the
  slots allowing; otherwise the second at a later turn). Each is worked, merged, and the batch
  pauses again, as the existing checks say.
- **Direct mode, strict refusal** (around lines 898-902): also check the refusal text has no
  "Foreman mode".
- **`close_refusals`** (around lines 1209-1236): `order add` on the paused batch leaves it paused
  with its pause and summary (replace the check "sets it running again and clears its pause"
  with "stays paused, keeps its pause and summary, the CR queued, with the line that says so").
  `close` and `close --yes` then refuse naming the queued CR, as today. Then the steering takes
  the CR (`take <new> --epoch 2`, without `--batch`, which also proves `find_cr_batch` finds a
  paused batch's CR): the batch is running, with the `was paused: running again` line. Then the
  existing steps (`cancel`, `order done`, `close` saying `not paused` and `pause` comes first,
  `pause` again) go on unchanged.
- **`pause` on a paused batch** (around line 1186): check the new text names the first `take`.
- **A refused take on a paused batch**: with a paused batch holding a queued CR whose `after` is
  unmet (or with the slots at 0 by `order slots --note 0`), `take` exits non-zero and the batch is
  still `paused`, its `batch.json` otherwise unchanged.
- **A CR added twice**: a second `order add` of a folder already queued in the paused batch is
  refused (exit 2 or the conflict code `ensure_unclaimed` raises today), the batch unchanged.

## Open questions

1. **`order qa` on a paused batch.** The grill decided `order add` only. This specification keeps
   `order qa` as today: it sets the paused batch running at once, since its QA driver holds a slot
   from the order on. Should an `order qa` too leave the batch paused, so a QA and several CRs can
   be added before the batch runs again?
