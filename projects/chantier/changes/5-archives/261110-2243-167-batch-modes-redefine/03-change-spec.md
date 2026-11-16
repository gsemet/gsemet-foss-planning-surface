# Change Specification: redefine the batch modes (parallel, series, stack)

## Goal

The user's words (2026-11-10): a batch has three modes, and each one says plainly how its pull
requests relate and who merges what, when.

- **Parallel (the default):** every CR starts from the default branch at once; the first one
  ready wins (the user merges in the order things become ready, unless told otherwise). After
  each merge, every PR still open is rebased onto the default branch and checked again.
- **Series:** the CRs have a precise order. The next CR starts from the previous CR's pushed
  branch once that one is handed back ready, and its PR is a draft. After the previous one
  merges, the next one is rebased onto the default branch and turns ready. The Chief of Staff
  guides the user merge by merge. On request, a series batch switches to a stack at once.
- **Stack:** parallel, with a stack driver: every CR at once, the PRs each on the previous one,
  the stack driver keeping the stack up to date; the user merges from the bottom up.
- A new SVG of the three modes in the README (not the batch lifecycle one), and clear
  explanations in the README and the docs.

What triggered it: batch-09, opened as a stack, started its three CRs at once, which the user
read as "not in series". Today `open` makes a stack by default, `--parallel` makes independent
CRs, and there is no series mode.

## Decisions carried from `02-answers.md`

1. Series: the Drivers do not work at the same time on new work; the next CR needs the previous
   one's commits (answer 1).
2. Parallel: after each merge, every PR still open is rebased onto the default branch and its
   checks run again, conflict or not; the proof stays bound to the current head (answer 2).
3. The default mode is parallel: a batch with no mode named is independent CRs from the default
   branch. Series or stack only when the user asks, or when a CR depends on another (answer 3).
4. Series: the next CR starts from the previous CR's pushed branch once that CR is handed back
   ready; its PR is a draft. After the previous CR merges, the next one is rebased onto the
   default branch and turns ready. If the previous CR changes during review, the next one is
   rebased (answer 4).
5. Series to stack, on request: every remaining CR starts at once, each on the previous one, a
   stack driver keeps the stack up to date (restack), and the user merges from the bottom up
   (answer 5).
6. Docs: a new SVG of the three modes in the README, separate from the lifecycle one, and clear
   explanations in the README and the docs (request, restated as grilled).

## What changes

### 1. The CLI (`skills/chantier/scripts/cli/src/chantier/`)

The CLI knows modes, not roles: it records the mode, refuses a take that the mode does not
allow, and prints each CR's base. It runs no rebase.

**`cli.py`, `open`:** replace `--parallel` with `--mode {parallel,series,stack}`, default
`parallel`. `--parallel` is removed (no alias: no fallback). The help says: `parallel`:
independent CRs, each on the default branch; `series`: one after the other, in the order given,
each on the previous one's branch; `stack`: independent CRs, then a stack driver stacks the PRs.

**`commands.py`, `open_batch`:** `data["mode"]` takes the value of `--mode`. The printed line and
`brief.md` ("- Mode: …") already show it. In `series`, the order of the CRs is the order of the
folders given to `open` (the existing `order` field). `open` in series exits 2 when a CR comes
before one of its `after` (from `depends.json`), with a message like `stack` gives: "<cr>
depends on <dep>: it cannot come before it in the series". The release CR and fix CRs are
outside the series, as they are outside a stack.

**The series predecessor (new, in `rails.py`, used by `commands.py` and `status.py`):** in a
series batch, a CR's predecessor is the nearest CR before it in `order` that is neither a
release nor a fix CR and not cancelled. A merged predecessor is met.

- `waits_for` (`rails.py`): in series, a queued CR also waits for its predecessor until that
  one is `ready` or `merged`, so `take` refuses it with the existing message ("<cr> waits for
  <pred> <status>: it starts once each is ready or merged") and `status` shows `waits for
  <pred> <status>`. Its `after` keeps its own rule.
- `_start_base` / `_stack_base` (`commands.py`): in series, the base is the predecessor's
  branch while the predecessor is not merged, else the default branch. The `worktree: … base
  …` line of the facts (`take`, `handoff`) and `ship`'s recorded base follow from it. A real
  `after` cannot point above the predecessor (refused at `open` and `order add`), so the
  predecessor's branch holds every dependency's commits.
- `order add` in series: the new CR goes on top (the next `order`), its predecessor the last CR
  of the series; refused with exit 2 if its `depends.json` names a CR that is not before it
  (only possible for a slug not in the batch, already refused today).

**The switch, a new order kind `mode`:** `$CHANTIER order mode --note stack` (no CR; added to
`ORDER_KINDS`, not to `CR_ORDERS`). Accepted only on a series batch with `--note stack`; any other
case exits 2 naming what is accepted ("order mode: only a series batch switches, to a stack").
Applied by the CLI at once: `mode` becomes `stack`, the series wait ends (a queued CR waits only
for its `after`), a `mode` event is logged, and the order awaits the steering session's `order
done` like any applied order. CRs already started keep their branches and bases; from then on
the stack rules apply (`take stack`, `stack`, `_chain`), the stack order starting from the series
order.

**Unchanged:** `take stack` and `stack` are refused unless the mode is `stack` ("batch <n> is not
a stack"); `depends.json`, `order after` and the release's `after` keep their rules in every mode;
the batch's `mode` field stays a string in `batch.json` and in `status --json`
(`status.py`).

### 2. The cards (`skills/chantier/references/`)

The rules each role judges by; the CLI's refusals are named, not repeated.

**`concepts.md`, "Batch" bullet:** replace "A batch's CRs run in parallel, each on the default
branch … `open --parallel` makes a batch with no stack at the end." with the three modes, as in
the Goal, and their mechanics: parallel (default; each CR and PR on the default branch; after each
merge every open PR rebased and checked again); series (the order given to `open`, `order add`
on top; the next starts once the previous is ready, on its branch, as a draft; rebased onto the
default branch once the previous merges; `order mode --note stack` switches); stack (each CR
starts on the default branch or its last open dependency, the stack driver stacks the PRs; after
a partial merge what remains is a new stack). Keep the sentences on dependencies, release and fix
CRs outside, and branch and worktree names. In "Dependencies", say that a series adds the
predecessor to what a queued CR waits for.

**`chief-of-staff.md`:**

- "A batch runs its CRs in parallel unless the plan says why not … the stack driver rebases
  afterwards": a batch is parallel unless the user asks for series or stack, or a selected CR
  depends on another; then the plan proposes series or stack and says why. Keep the rules on
  `depends.json` and queues.
- "Show the plan": "mode (a stack unless the CRs are independent)" becomes "mode (parallel unless
  the user asked for series or stack, or a CR depends on another; for a series, the order)".
- "Open": the command line with `[--mode parallel|series|stack]`, and "It makes a stack;
  `--parallel` makes independent CRs" becomes the three modes in one sentence each.
- New paragraph, **a series batch**: on each `ready` ask, tell the user which PR is next to merge
  (the bottom one, ready on the default branch) and that the others are drafts waiting on it;
  after the user says it is merged, `order merged`, then say what comes next. Never merge for the
  user. On the user's word "switch to a stack" (or the like), `order mode --note stack`.
- The demo offer ("the last of a stack"; "A parallel batch gets no offer") stays as it is.
- The intent table row "a batch, 'run the P1s', a stack" stays; add "series" to its trigger.

**`foreman.md`:**

- "a batch runs its CRs in parallel unless the plan says why not": "pick among the CRs `take`
  would accept, every one up to the free slots"; in a series batch `take` accepts only the next
  one, which is the rule, not a reason to wait.
- "A batch is a stack unless it was opened `--parallel`": "A stack batch (`--mode stack`, or a
  series switched by `order mode`)"; the rest of the stack driver paragraph is unchanged.
- "On an `order merged <dependency>`": extend by mode.
  - **Parallel:** after each `order merged`, every CR with a PR still open goes back to a Driver:
    a `ready` or `blocked` one with `take <cr> --note "rebase: <merged cr> merged"` (a new CR
    Driver, a slot, or it waits like a queued CR when none is free); a `working` one gets
    `[foreman→driver <cr>] note rebase: <merged cr> merged`. Conflict or not: its checks run again
    at the new head. A queued CR needs nothing.
  - **Series:** the CR whose predecessor merged goes back to a Driver with `take <cr> --note
    "rebase: <cr> merged"` and turns ready on the default branch. Whenever a CR's branch moves
    (a rebase, a new round after review), the started CR above it goes back to a Driver with
    `--note "rebase: <cr> moved"` (or the `note` line, when it is working), and stays a draft on
    that branch; each one moved this way moves the next.
  - **Stack:** unchanged: the stack driver restacks.
  - The existing rule for drafts waiting on a dependency stays, in every mode.
- "A CR whose dependency went back to a Driver after it started is restacked by the stack
  driver" and "the chain stands until the stack driver restacks": in a series or parallel batch,
  that CR gets the rebase note above instead.

**`driver.md`, "CR driver":** generalise the `rebase:` paragraph.

- `rebase: <cr> merged` with no open dependency or predecessor left: rebase onto
  `origin/<default branch>`, retarget the PR there if it was elsewhere, push with
  `--force-with-lease`, `ship`, run the long gate at the new head, read CI; green and mergeable,
  ready on the default branch: turn it ready and `handback ready <link>`. This is now also the
  path of a CR with no dependency at all, in a parallel batch.
- `rebase: <cr> moved`, or a base that `take` prints as another CR's branch: rebase onto that
  branch, keep the PR a draft, `handback ready <link> draft on <base>: waits for <cr>`.
- A CR taken back `blocked` for a rebase: after the rebase, hand back blocked with the same reason
  it had.
- A `note rebase: …` while working: rebase before the next push; the gate and CI run at the new
  head.
- A series CR's PR opens on the base `take` printed, as a draft: the existing rule ("a Driver
  does not retarget a PR" except on a `rebase:` note) holds.

**`driver.md`, "Stack driver":** one sentence: a stack batch is one opened `--mode stack` or a
series switched by `order mode`; after a switch, the stack's order starts from the series order.

**`routing.md`:** no new line (`note <text>` already carries the rebase note).

**`status-layout.md`:** no change.

The agent files (`agents/`, `com.github.copilot/agents/`) carry no mode: no change.

### 3. The docs

- **New `docs/batch-modes.svg`** with its `docs/batch-modes-texts.md` (the same pair as the other
  diagrams: the texts file holds every text of the SVG). Three lanes, one per mode, side by side
  or stacked, each showing on a time axis: when each CR starts, the base of each PR (default
  branch or the previous one), draft or ready, where the user merges, and what follows a merge
  (parallel: every open PR rebased and checked; series: the next one rebased, ready; stack: the
  stack driver restacks). Parallel is marked as the default. Series shows the switch to a stack.
  It does not draw the batch lifecycle (running, paused, closed): that is `batch-lifecycle.svg`.
- **`README.md`:** a new section "Batch modes" after "How chantier works" (or next to "Planning
  modes"), with the SVG and a short paragraph per mode, saying how to ask for each ("run these in
  series", "build a stack of these", nothing for parallel) and that a series switches to a stack
  on request. Line 105 ("the CRs run in parallel and are stacked afterwards") and lines 276-277
  ("Its CRs run in parallel … unless the batch is `--parallel`") are rewritten to the three modes.
  The intent table row "run the P1s", "build a stack of these" gains "run these in series".
- **`docs/use-cases-foreman.md`:** "Build independent pull requests" (parallel is the default:
  no flag; after each merge the open PRs are rebased), "Build a stack of pull requests" (asked
  for, `--mode stack`), and a new "Build a series of pull requests" (the order, the drafts, the
  merge-by-merge guidance, the switch). In "Steer a running batch", a row: "Switch to a stack." →
  `order mode --note stack`.
- **`docs/use-cases-direct.md`** lines 53-55: the same three modes, in one or two sentences.
- **`docs/cr-lifecycle-texts.md` / `cr-lifecycle.svg`** ("Stack (optional)"): check the wording
  still holds; change only what the new default makes wrong.

## Out of scope

- `docs/batch-pace.svg` (referenced nowhere today), `batch-lifecycle.svg`, and the edits of the
  `diagrams-modes-griller` CR (P1), which also touches the README and the docs SVGs: the new SVG
  here is a separate file; a README conflict between the two is resolved by rebase.
- The steering modes (direct, Foreman) and the planning modes (in-project, external).
- Any other mode switch than series to stack (stack to series, parallel to anything).
- A new stack driver behaviour beyond what the switch needs.
- No version bump by hand.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just scenario` passes (the change touches the CLI and the cards), with these steps in
  `scenario/run_scenario.py`:
  - Every `w.start(..., "--parallel", ...)` becomes no mode flag (parallel is the default) or
    `--mode parallel`; the check at line 1582 (`d["mode"] == "stack"`) becomes the default
    `parallel`, and the stack sections (lines 1597-1661, 2405-2408, 2467) open with
    `--mode stack`.
  - `open --parallel` is refused as an unknown argument (exit 2).
  - Parallel: `take stack` and `stack` are refused ("is not a stack"); after `order merged` on
    one CR, `take <other ready cr> --note "rebase: <cr> merged"` is accepted and its facts print
    the default branch as base.
  - Series, three CRs A, B, C in that order: `status` shows B `waits for A queued`; `take B` is
    refused until A is handed back ready; then `take B` prints `base` = A's branch, and C still
    waits for B. `order merged A`, then `take B --note "rebase: A merged"` prints the default
    branch as base. `open --mode series` with a CR before its `depends.json` dependency exits 2.
    `order add` in series puts the new CR on top, waiting for the last one.
  - Switch: on a series batch with C queued, `order mode --note stack` sets `mode` to `stack`,
    `take C` is accepted at once, `take stack` works. `order mode --note stack` on a parallel or
    stack batch, and `order mode --note parallel` on a series one, exit 2.
- `tests/test_structure.py`: no new test expected (structure only).
- The docs: `docs/batch-modes.svg` renders in the README on GitHub, and `docs/batch-modes-texts.md`
  holds every text the SVG shows.

## Open questions

1. **Stack: where does each CR start?** The restatement says "every CR at once, each on the
   previous one". This specification keeps today's mechanics: each CR starts on the default
   branch (or its last open dependency), and the stack driver puts each PR on the previous one
   once the CRs are ready. The other reading is that each CR starts on the previous CR's branch
   at its take, while that branch is still being written (the problem answer 1 raised for
   series). Which one does the user mean?
2. **Series and the demo offer.** Today the demo is offered when the last CR of a stack is ready,
   and never for a parallel batch. Should a series batch get the offer when its last CR is ready,
   or none? This specification leaves it to stacks only.
3. **Parallel, a blocked CR waiting for the user's answer:** answer 2 says every open PR is
   rebased after each merge. This specification includes a blocked CR with a PR (taken back,
   rebased, handed back with the same blocked reason). Should a CR blocked on a question wait
   for its answer instead, and be rebased then?
