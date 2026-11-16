# A running batch switches between any two modes

## Goal

The user's words (2026-11-14): a running batch can go from any mode to any other: series to
parallel, parallel to stack, stack to parallel or series, and so on. What is already delivered
(merged CRs) never changes. Today `order mode` takes one pair only (series to stack), and batch-18,
opened in parallel, was refused when the user asked for a GitHub stack ready to merge by morning.

This CR runs in batch-18 at the head of the queue, after CR-253 and CR-254 (`fast-scenario`,
`depends.json`); once it is merged, batch-18 switches to a stack (MS-Q4).

## Decisions carried (02-answers.md)

- **MS-Q1, to a stack (from parallel or series):** the open PRs are stacked; the stack driver
  rebases each on the one below, in order; CRs not yet started join on top.
- **MS-Q2, to parallel (from a stack or series):** each open PR is rebased on the default branch,
  its long gate and CI run again, and it leaves draft once ready.
- **MS-Q3, the order of a stack or series made by a switch:** the CRs already handed back `ready`
  at the bottom, in the order they became ready, then the others in the batch's order; the
  recorded chains (`after`) are kept.
- **MS-Q4:** this CR joins batch-18 at the head of the queue after CR-253 and CR-254; batch-18
  switches to a stack once it is merged.
- **Never changed by a switch:** the merged CRs (and so their PRs, branches and folders).

## Today

- `skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py`, `_mode`: refuses unless
  the batch is `series` and the note is `stack`; sets `b.record.mode = "stack"`, logs
  `b.log("mode", None, mode="stack")`, prints "is a stack now".
- `stacks.py`: `chain()` is empty outside a stack; `stack_base()` reads `c.stacked` and the chain;
  `start_base()` and `rails.waits_for()` / `series_predecessor()` read `order` and the mode.
- `stack` / `stack --out-of-draft|--draft` (`commands/delivery.py`) and `forge-stack
  create|show|rebuild` (`commands/forge_stack.py`, `forge_stack_gitlab.py`) work only in a stack
  batch; `rebuild` already unstacks (`_unstack`) and retargets (`_retarget`).
- The cards say the switch is series to stack only: `concepts.md` (Modes, line ~146),
  `chief-of-staff.md` (the order list, line ~887; "A series batch", line ~950), `foreman.md` (line
  ~168), `driver.md` ("Stack driver", line ~523), `hosts/claude-code.md` (the stack row, line ~291).
- Docs: `docs/batch-modes-texts.md` and `docs/batch-modes.svg` ("On request: switch to a stack"),
  `docs/use-cases-foreman.md` ("Switch to a stack.").
- Scenario: `batch_modes` (§13b, `scenario/run_scenario.py` ~4695-4797) checks that `order mode`
  is refused in parallel, `--note parallel` refused on a series, series to stack accepted, and
  refused on a stack. `scenario/README.md` "the three modes" bullet says so.

## What changes

### CLI: `order mode --note parallel|series|stack`

`_mode` in `orders_apply.py` accepts every pair of distinct modes, on the user's word (the Chief
of Staff runs it, as today).

- **Refused:** a note other than `parallel`, `series` or `stack` (usage line naming the three);
  the note equal to the batch's mode ("batch-NN is already a <mode>"); a closed or closing batch
  (as the other orders). Nothing written on a refusal.
- **Record, at once, one write:**
  - `b.record.mode` set to the new mode; the event `mode` logged with `from` and `to`
    (`b.log("mode", None, mode=<to>, previous=<from>)`); the order marked applied as today.
  - **To a stack or a series:** the `order` of the open CRs (not merged, not cancelled; a fix CR
    keeps its place outside, the release CR stays last) is rewritten by MS-Q3: first the CRs
    whose status is `ready`, by the time of their last `handback … ready` event in the batch's
    `events.jsonl`, oldest first; then the others in their current `order`. Then a CR that would
    sit below one of its `after` CRs still open is moved just above the highest of them (the
    chains are kept, never broken). Merged and cancelled CRs keep their `order` unchanged.
  - **Leaving a stack:** every CR's `stacked` is cleared (else `stack_base()` would read a place
    in a chain that no longer exists and give the default branch where a series needs the
    predecessor's branch).
  - **To a stack:** `stacked` stays false on every CR: the stack driver places them with `stack`.
- **Output:** one line naming the new shape and what follows, per target:
  - stack: "batch-NN is a stack now (order: A → B → C): the stack driver stacks the open PRs,
    the CRs to come join on top";
  - series: "batch-NN is a series now (order: …): each open PR is rebased on the one below, the
    ones above the bottom go back to draft";
  - parallel: "batch-NN is parallel now: each open PR is rebased on the default branch, its long
    gate and CI run again, and it leaves draft once ready";
  - leaving a stack adds: "run `forge-stack unstack` before any rebase".
- `rails.waits_for()`, `start_base()`, `stack_base()`, `ready_word()` and `draft_waits()` need no
  new rule: they already read the mode and `order`; the switch only changes those. A queued CR
  waits by the new mode's rule at once (in parallel or a stack only for its `after`; in a series
  also for its predecessor). The `status`/`STATUS.json` shape word follows `mode` as today.

### CLI: `forge-stack unstack` (new action)

Leaving a stack needs the forge's stack dissolved before any PR can be retargeted (a PR's base
cannot change while it is stacked, `driver.md`). `rebuild` creates the stack again, so a new
action is needed: `forge-stack unstack`, declared in `declare/forge_stack.py` (`choices` gains
`unstack`; help: "unstack: dissolve the open stacks that hold the batch's PRs and retarget each
open PR to the base the record gives; any mode").

- Accepted in any mode (the batch has just left a stack); refused in a batch with no open CR
  with a PR (nothing to do: exit 0 with "no open PR in batch-NN", not an error).
- **GitHub:** for each open stack that holds a PR of the batch's open CRs, `_unstack()` as
  `rebuild` does (same tries, same exact-text failure, exit 4); then `_retarget()` each open PR to
  `stack_base(d, c, repo)` read in the batch's current mode (parallel: the default branch or the
  last open dependency's branch; series: the predecessor's branch). No `_make()`. Prints the
  `unstacked #N` and `#n base old -> new` lines, or "no stack holds the batch's PRs".
- **GitLab:** retarget only (there is no stack to dissolve), as `rebuild` does on GitLab.
- A merged CR's PR is never touched (MS: never changed).
- It changes no draft state and no branch: the Drivers do that (below).

### Who does what after a switch (cards)

The steering session (the Foreman, or the Chief of Staff in a direct batch) reads the switch from
the order and acts by target. No CR already started is stopped.

- **To a stack (MS-Q1),** from parallel or series: as today after a series switch, the stack grows
  from the bottom. At once, if two CRs or more are already handed back `ready` with a PR, the
  first `take stack`; the stack driver orders the CRs from the record's order (`stack <cr>…`,
  which MS-Q3 set), rebases and pushes each PR on the one below (its own `ready`/`blocked` CRs;
  a `working` CR's Driver by the rebase note), puts each PR it moves to draft while the stack is
  made, `forge-stack create`, then turns the mergeable part ready. The CRs not started join on top
  as they get their PR. A PR that was ready to merge on the default branch and is not the bottom
  one is a draft during the restack: the Chief of Staff says so to the user at the switch ("the
  PRs above the bottom go to draft while the stack is made; do not merge them meanwhile").
- **To parallel (MS-Q2),** from a stack or series: from a stack, first `forge-stack unstack` (the
  steering session runs it; a refusal is an `anomaly` / ask with the exact text, no other means).
  Then every open CR with a PR gets its rebase: a `ready` or `blocked` CR is taken back with `take
  <cr> --note "rebase: mode parallel"`, a `working` CR's Driver gets `[foreman→driver <cr>] note
  rebase: mode parallel`. The Driver puts its PR to draft (`gh pr ready --undo` / `glab mr update
  --draft`, `ship --draft`), rebases on the base `take` prints (the default branch, or its open
  dependency's branch), runs the long gate and CI again, and hands back `ready`; it leaves draft
  once ready, as any parallel CR. The queued CRs start as slots free, on the default branch.
- **To a series,** from parallel or a stack: from a stack, first `forge-stack unstack`. Then each
  open CR with a PR is rebased on its predecessor's branch (the order MS-Q3 set), bottom first:
  the bottom one on the default branch, ready to merge once ready; each one above a draft on the
  one below, as any series PR. Who moves a branch: `take <cr> --note "rebase: mode series"` for a
  `ready`/`blocked` CR, the rebase note for a `working` one. See open points 1 and 2.
- **A running stack driver at the switch out of a stack:** see open point 3.
- **The release CR and fix CRs:** a fix CR stays outside every shape, untouched. A release CR
  not started waits by the new mode's rule (`waits_for`: ready in an ordered batch, merged in
  parallel). A started release: see open point 4.
- **Merged CRs:** never rebased, retargeted, reordered or reopened.

### Cards to edit

- `concepts.md`, Modes: "`order mode --note stack` switches the series to a stack" becomes: a
  running batch switches between any two modes with `order mode --note <mode>`, on the user's
  word; what the switch does to open PRs, the order (MS-Q3), and that merged CRs never change.
- `chief-of-staff.md`: the order list line (`order mode --note parallel|series|stack   # any mode
  to any other, on the user's word`); "A series batch" and "A stack batch": the user's word to
  switch (any of the three) → `order mode`; the line to the user at a switch (what goes to draft,
  do not merge it meanwhile).
- `foreman.md`: the stack batch paragraph ("or a series switched by `order mode`" → "or a batch
  switched to a stack by `order mode`"); a new bullet "A mode switch": by target, as above
  (`forge-stack unstack` first when leaving a stack, the rebase notes, no CR stopped).
- `driver.md`: "Stack driver" opening: a stack batch is one opened `--mode stack` or switched to
  a stack; after a switch, the stack's order starts from the record's order (MS-Q3). The CR
  driver's rebase on `note rebase: mode <mode>` (draft first, rebase on the printed base, long
  gate and CI, hand back).
- `hosts/claude-code.md`, the stack row: `order mode --note stack` and `forge-stack
  unstack` under the `chantier` rule (no new permission: it calls the same stacks and pulls API
  as `rebuild`).
- The Copilot and Claude Code agent files are not touched (no role body changes).

### Docs

- `docs/batch-modes-texts.md` and `docs/batch-modes.svg`: the line "On request: switch to a stack,
  at once (order mode --note stack)" becomes "On request: switch to any other mode, at once (order
  mode --note parallel|series|stack); merged CRs never change." (the SVG text kept in step with
  the texts file).
- `docs/use-cases-foreman.md`: the "Switch to a stack." row generalised, plus one row "Switch to
  parallel." (each open PR rebased on main, gate and CI again, out of draft once ready).

## Out of scope

- Changing the steering (Foreman / direct): a separate switch, untouched.
- A mode for a closed batch, or a switch at `open` beyond `--mode`.
- Any change to the stack driver's stacking steps themselves (ordering, five checks, insertion).
- Switching a single CR's shape (all CRs of the batch follow the batch's mode).
- A new forge means: `forge-stack unstack` uses the same API calls as `rebuild`.

## Evidence

New scenario cases go into CR-254's unit layout (`UNITS` in `scenario/run_scenario.py`; "Adding
a case": join an existing unit, refusals on a prepared state to pytest). Each new check maps to
its `scenario/README.md` coverage bullet with `(unit: …)` / `(test: …)`.

- **pytest (refusals on a prepared state),** one parametrized test in the CR-254 pytest file that
  holds the `batch_modes` refusals (or a new `tests/test_mode_switch.py`, under 400 lines): `order
  mode --note <same mode>` refused for each of the three modes; an unknown note refused with the
  usage line; nothing written (the `batch.json` bytes unchanged).
- **pytest, the record:** on a prepared `batch.json` + `events.jsonl` (parallel, CRs A queued, B
  ready at t2, C ready at t1, D working, E merged), `order mode --note stack` writes the order
  C, B, A, D (ready by readiness time, then the others in their order) and leaves E's `order`
  unchanged; a second case where A has `after: [D]` gives C, B, D, A (the chain kept); the `mode`
  event carries `previous`. Leaving a stack clears every `stacked`.
- **Unit `series-deps`** (`batch_modes`, §13b): replace "`order mode --note parallel` is refused on
  a series" and "`order mode` is refused on a stack" with live switches:
  - parallel → stack with two CRs handed back ready: the order follows readiness; `take stack`
    works; `stack` accepts that order.
  - stack → parallel: `take <cr> --note "rebase: mode parallel"` prints `base origin/main` for a
    CR that was stacked on another; `status` shows no CR waiting for a predecessor.
  - parallel → series: a queued CR now waits for its predecessor; a ready CR's `take … --note
    "rebase: mode series"` prints its predecessor's branch.
  - series → parallel: a queued CR that waited for its predecessor is taken at once on
    `origin/main`.
  - a merged CR's record (status, order, pr, branch) identical before and after each switch.
- **Unit `stack`** (`forge_stack_cli`, GitHub part, `fake_gh.py`): after a stack is created,
  `order mode --note parallel`, then `forge-stack unstack` unstacks it (the fake's unstack call
  logged) and retargets each open PR to `main`; a second run prints "no stack holds the batch's
  PRs" with exit 0; `forge-stack create` is refused in the parallel batch as today.
- **Unit `gitlab`** (`forge_stack_cli`'s GitLab part): `forge-stack unstack` only retargets (no
  unstack call in the call log).
- **Card checks:** `test_plugin_files.py` only if CR-254 put card text checks there for the modes;
  otherwise none.
- `just check` on the three systems; `just scenario` before the PR (a CLI and cards change).

## Open points (behaviour, scope, risk), each with a default

1. **Parallel → series with several open PRs:** chain them all now (each rebased on its
   predecessor, the ones above the bottom back to draft), or apply the series only to the CRs not
   yet started and leave the open PRs on the default branch? Default: chain them all now, in the
   MS-Q3 order (a series made by a switch has that order, so its open PRs follow it).
2. **Stack → series: the mergeable part shrinks to one PR.** In a series only the bottom PR is
   ready to merge; the PRs that were ready to merge above it go back to draft. Default: yes, back
   to draft (that is what a series is); the Chief of Staff tells the user at the switch which PRs
   stop being mergeable.
3. **A stack driver running when the batch leaves a stack:** refuse `order mode` until it hands
   back, or accept at once? Default: accept at once (the user's word is recorded at once); the
   Foreman sends it `[foreman→stack] note mode: <mode>`, it stops after the branch it is pushing
   (no further rebase, no `rebuild`) and hands back; then `forge-stack unstack` and the rebase
   notes.
4. **A release CR already started (working or ready on top of the chain) when an ordered batch
   goes parallel:** its work sits on the top CR's branch, while a parallel release waits for the
   others to be merged. Default: the release is taken back with `take <release> --note "redo:
   mode parallel"` once the others are merged (its PR closed meanwhile, branch kept), as a stale
   release is today.
5. **The PRs that go back to draft during a switch to a stack (risk):** a PR ready to merge on the
   default branch becomes a draft on another CR's branch while the stack is made, and the user may
   merge one meanwhile. Default: the Chief of Staff names them at the switch with "do not merge";
   a merge anyway is recorded as any merge (`order merged`), and the stack driver restacks what
   remains, as "A merge during a take" says.
