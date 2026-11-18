# Change Specification: `take` bases a stack CR on the nearest earlier CR with a PR

Short name: `take-base-nearest-pr`. No issue (origin: verbal, batch-23's retro, 2026-11-17).

## Goal

In a stack batch, one linear stack on the forge, not a tree. In batch-23 the PRs formed a tree:
Drivers based later CRs on branches with no PR or no commit yet, the merges of CR-309..314 moved
the bases, and three stack-driver runs were needed to restack (one failing on the forge's empty
unstack reply, since fixed by CR-313). From now on `take` bases a CR on the nearest earlier CR of
the batch that already has a PR, else on the default branch, and one stack-driver run, at the
batch's end, owns the final order of the stack.

Sources: `intake/request.md`, `02-answers.md` (round 1, "Spec questions" and "Spec questions,
round 2", 2026-11-17), the retro of `projects/chantier/changes/5-archives/batches/batch-23.md`
(first `[chantier]` point).

## Decisions carried from `02-answers.md`

1. **batch-Q8:** this CR joins the next batch, with the other five retro points of batch-23 and
   the four board CRs of 2026-11-17. (A scheduling fact for the Chief of Staff; nothing to code.)
2. **stack-Q4:** `take` bases a CR on the nearest earlier CR of the batch that already has a PR,
   else on main; one stack-driver run, at the batch's end, owns the final order of the stack (one
   linear stack on the forge).
3. **In-batch runs stay:** the stack-driver runs during the batch stay, to keep the stack current
   after a merge or a CR that joins; only the run at the batch's end may set the final order.
4. **The end run's start:** when every non-release CR of the stack has handed back (`ready` or
   `blocked`), before the release's take.
5. **Merges before the end:** the user may still merge a ready CR on main before the end run; the
   restack is done at once, as today.
6. **Scope:** the base rule applies to stack batches only, not parallel ones (nor series).
7. **A ready CR above drafts (round 2):** during the batch, a CR handed back ready that sits above
   drafts is still moved below them, as today, so "deliver by" and the partial ready-to-merge ask
   keep working; only the end run may reorder freely.
8. **A queued CR that cannot start (round 2):** a queued CR whose dependency is blocked or
   cancelled does not hold back the final-order take: it stays out of the stack and goes into the
   ask to the user.

## Definitions

- **Earlier:** lower `order` in the batch's record (`CrEntry.order`: the order `open` gave, `order
  add` on top, `order mode` reordering as today).
- **Has a PR:** `pr` is recorded on the CR (`ship` ran), whatever its status (`working`,
  `blocked` or `ready`) and whatever its draft flag.
- **Candidates:** the CRs of the batch that are not ended (not `merged`, not `cancelled`: the
  `ENDED` set of `rails.py`), not `kind == "fix"` and not `kind == "release"`, other than the CR
  taken.
- **Nearest earlier CR with a PR:** among the candidates with a lower `order` and a PR, the one
  with the highest `order`. None: the default branch.
- **Final order:** the order of the stack's CRs set by `$CHANTIER stack <cr>…` in the end run, free
  to move any CR. **Keeping the stack current:** what the in-batch runs do today, unchanged: make
  the stack (first take), add a CR that joins on top, move a newly ready CR below the drafts under
  it into the mergeable part, restack what remains after a merge, an insertion or a drop.

## What changes

### CLI: `skills/chantier/scripts/cli/src/chantier/stacks.py`

- `start_on_for(b_data, c)`: in a stack batch, for a CR that is neither a release nor a fix and
  has no open dependency (`_open_after` empty), return the branch of the nearest earlier CR with a
  PR (Definitions), else `None` (the default branch, as today). It no longer waits for the stack
  to form: the condition "two CRs handed back `ready` with a PR" (`stack_forms`, `ready_top`) is
  no longer read here. In a parallel or series batch it returns `None`, as today. Rewrite its
  docstring to say the new rule.
- `start_base`: unchanged in shape. A CR with an open dependency still starts on its last open
  dependency's branch (`take` still refuses it until that dependency is `ready`); the recorded
  `start_on` is used while the CR that owns it is not ended, else the default branch. Update the
  docstring's wording only where it names the old rule.
- `ready_top`: today read only by `start_on_for`; remove it if no caller is left (grep first).
  `stack_forms` stays: the first in-batch take still comes at two CRs ready with a PR.
- Nothing else in `stacks.py` changes: `stack_base`, `off_place`, `ready_word`, `draft_waited`
  keep their rules. A CR whose PR opens on another CR's branch is a draft (`PR in draft`, waiting
  on that CR), as it is today for a CR started on the ready part's top.

### CLI: `skills/chantier/scripts/cli/src/chantier/commands/driver.py`

- `take`: unchanged in flow. The start base is still computed and fixed at the first take only
  (`if c.status == "queued" and (start_on := start_on_for(d, c))`), so a later `take <cr> --note`
  never moves it. The `worktree: … base <ref>` line that `take` and `handoff` print
  (`commands/facts.py`, `_base_of`) reads `start_base`; it now prints the nearest earlier CR's
  branch.
- No new refusal: the CLI does not tell an in-batch run from the end run; which run may reorder
  freely is the cards' rule (below).

### CLI: `skills/chantier/scripts/cli/src/chantier/core/records.py`

- The comment on `start_on` (line ~106): the branch a CR of a stack batch started on, the nearest
  earlier CR with a PR at its first `take`.

### Cards (`skills/chantier/references/`)

- `concepts.md`, "Batch modes", **Stack** (lines ~204-217): replace "on the default branch until
  the stack can form (two CRs handed back `ready` with a PR); from then on a CR started starts on
  the top of the stack's ready part (the highest CR handed back `ready` with a PR), recorded at its
  first `take`" by: a CR with no open dependency starts on the nearest earlier CR of the batch (by
  order) that already has a PR, else on the default branch, recorded at its first `take`; a branch
  with no PR is never a base. Add: the stack-driver runs during the batch keep the stack current
  (made at two PRs ready, a CR that joins on top, a newly ready CR moved below the drafts, a
  restack after a merge at once, as today); one run at the batch's end, once every non-release CR
  has handed back (`ready` or `blocked`) and before the release's take, sets the final order,
  free to move any CR: one linear native stack on the forge. A queued CR whose dependency is
  blocked or cancelled does not hold that run back. The user may merge a ready CR on the default
  branch at any time before it.
- `concepts.md`, **Dependencies** (lines ~299-302): "The CR starts on the branch of its last
  dependency still open, in the order of `after`, else on the default branch, in a stack too until
  the stack can form, then on the top of the stack's ready part" becomes "… else, in a stack, on
  the nearest earlier CR of the batch that has a PR, else on the default branch"; keep "a CR's
  start base and its place in the stack are two things".
- `foreman.md`, the stack-batch bullets (lines ~265-305):
  - "**The first take** … From then on `take` starts every new CR on the stack (the top of its
    ready part)" becomes: `take` starts every new CR on the nearest earlier CR with a PR (the CLI
    computes it; the Foreman chooses nothing). The first take itself stays at two CRs ready with a
    PR.
  - "Until the first stack is made it runs like a parallel batch … each CR handed back `ready` on
    the default branch is an ordinary `ready-to-merge` ask" holds for a CR whose base is the
    default branch; a CR based on another CR's branch hands back `PR in draft`.
  - "**Each later take**", "**A merge**", "**Deliver by a time**" (lines ~273-292) and the partial
    `stack-ready-to-merge … to come: …` ask (line ~308): unchanged.
  - New bullet **The final-order take:** once every non-release CR of the stack has handed back
    (`ready` or `blocked`), none `working`, and none `queued` that could start (a queued CR whose
    dependency is blocked or cancelled does not count: it stays out of the stack), and before
    `take <release>`: `take stack --note "final order" --epoch <n>` (a running stack driver gets
    `[foreman→stack] note final order` instead, after its current work). The release's take then
    follows as today ("`take stack` first, then `take <release>`"). The ask that follows the
    end run's hand-back names each such queued CR left out (with its unmet dependency), beside the
    existing one-time ask for a cancelled dependency (line ~200). A CR that goes back to a Driver
    after the final-order take (a new round, a `rebase:`) makes it due again once that CR hands
    back.
- `driver.md`:
  - CR Driver, "In a stack batch the `base` that `take` prints may be another CR's branch: the top
    of the stack's ready part, once the stack can form" (line ~684): becomes "the nearest earlier
    CR of the batch that has a PR". Add in the same paragraph: the Driver creates its worktree on
    that base and no other, never on a branch with no PR (the existing rule "The PR's base is the
    `base` that `take` printed, never another", line ~297, is the one cited).
  - Stack driver, "**Ordering**" (line ~728) and "**A draft that turns ready to merge**" (lines
    ~795-798): unchanged (a newly ready CR is still moved below the drafts during the batch).
    Add one sentence to "Ordering": outside the final-order take, the CRs already stacked keep
    their relative order but for that move.
  - New paragraph **The final-order take** (a take whose note is `final order`): order every CR of
    the stack with a PR by the Ordering rule (the CRs handed back `ready` first, then the
    `blocked`, a CR always above its dependencies, as `stack` enforces), free to move any CR;
    rebase each moved CR on the one under it and push each branch with the form of line ~744 (the
    Push bullet's rewrite form, `git -C <worktree> push --force-with-lease -u <remote> <branch>`,
    one command per branch, as driver.md:269 writes it), `ship` each moved CR, `forge-stack rebuild` (or `create` if no stack is on the forge
    yet), read it back with `forge-stack show` (the five checks), turn the mergeable part ready and
    `stack --out-of-draft`; then hand back as today. One linear native stack is its end.
  - "**Recording a restack**" (line ~932) and the carry rules: unchanged (see the next section).
- `agents/` and `com.github.copilot/agents/`: no change (the contract lives in the cards).

### Consistency with `carry-by-patch-id` (same batch)

That CR records, with the long gate pass and the verdict, the base a CR was judged on, and
carries them over a clean rebase when the CR's own commits (patch-ids above that base) did not
change; a resolved conflict still gets a new long gate and a Verifier. This CR relies on it and
changes none of it:

- `start_on` is where a CR's branch starts, fixed at its first take; it is not the judged base.
  The base a pass or a verdict was judged on stays the one `carry-by-patch-id` records at the gate
  and the verdict; this CR adds no field and no event for it, and no code here reads `start_on`
  for a carry.
- From the batch after `carry-by-patch-id` merges (its carry-Q11), a CR started on a lower CR's
  branch, then rebased by an in-batch restack or by the final-order take onto another branch,
  keeps its pass and verdict when its own commits did not change: `carry-by-patch-id`'s case of
  CR-316 (a lower CR rewritten under new SHAs), so a clean move costs no new gate. In the batch
  that ships both CRs, a CR judged before `carry-by-patch-id` merges has no recorded base and gets
  a new long gate and Verifier at its next move (the one-time cost that CR names in its Known
  gaps); this CR's cards say nothing that contradicts it.
- The cards' wording added here names the carry as the cards hold it after `carry-by-patch-id`
  (its `ship` line `carried: …`); whichever CR merges second rebases its card text onto the
  other's, keeping both rules.

### Scenario (`scenario/run_scenario.py`)

- The check at line ~4885 ("a CR taken once two are ready with a PR starts on the top of the
  stack's ready part"): reword to the new rule; the expected `start_on` stays `three`'s branch
  (the nearest earlier CR with a PR).
- New checks in the same stack step, each through `take` and `handoff`:
  1. A CR taken while an earlier CR is `working` with a PR recorded (a draft, not `ready`), and
     no two CRs are `ready` yet: its `start_on` is that working CR's branch and `handoff` prints
     `base <that branch>` (the old rule gave `origin/main`).
  2. A CR taken while the CR right before it has no PR and an earlier one has: it starts on the
     earlier one with the PR, not on the one with no PR.
  3. A CR taken while no earlier CR has a PR (a later CR having one does not count): `base
     origin/main`, no `start_on` recorded.
  4. An earlier CR with a PR that is `cancelled` or `merged` is skipped; keep the existing check
     at line ~4897 (fall back to main once the owner is cancelled).
  5. A fix CR and a release CR are unaffected (fix: default branch; release: the top CR's
     branch), and a CR with an open `after` still starts on its dependency's branch.
  6. In a parallel batch, a CR taken while an earlier CR has a PR still starts on `origin/main`.
- Update `scenario/README.md` wherever it states the old start rule.

### Tests (`skills/chantier/scripts/cli/tests/`)

- No new test file: the start base is batch workflow, which belongs to `just scenario`
  (AGENTS.md). Fix any existing test that asserted the old rule (grep `start_on`, `ready part`).

## Out of scope

- Parallel and series batches: their bases do not change.
- The `after` / `depends.json` rule, the release's base, a fix CR's base.
- Moving a CR's start base after its first take (no re-basing by `take --note`).
- A CLI rail telling the final-order take from an in-batch one (the cards hold that rule).
- The carry itself (patch-ids, the judged base, the `carry` event): `carry-by-patch-id`.
- The push form itself: `driver-force-push-own-branch` keeps the stack driver's `git -C
  <worktree> push --force-with-lease -u <remote> <branch>` form; this CR only points to it.
- The other batch-23 retro points: their own CRs.
- `forge-stack` commands (`create`, `rebuild`, `show`, `unstack`): no change in what they do.
- The board and the CR pane: nothing they draw changes (no `STATUS.json` field added).

## Evidence

- `just check` green (Linux, macOS, Windows).
- `just scenario` green with the checks above (pipeline `just scenario (ubuntu-latest)` at the
  PR's head; locally on Windows when this CR is on top of its batch's stack, per AGENTS.md).
- `just test` within its time budget (no new slow test).
- No change to `hooks/` or `types/`: no `just mod`.

## Open questions

None.
