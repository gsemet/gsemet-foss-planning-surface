# An ordered stack is checked as a git chain

In a stack or series batch, a CR that is meant to start from another CR must have that CR's head in
its history. `ship` refuses, recording nothing, a CR whose branch does not. The stack driver checks
the chain with `git merge-base` before it concludes that no restack is needed. Specification v1.

## Goal

From Studio's batch-07 retro (`intake/request.md`). The ordered stack CR-439..CR-445 was linear on
the forge only: the PRs' bases formed a chain, but CR-440, CR-442 and CR-444 had been cut from main.
`take CR-446` was refused. A first stack driver wrongly concluded that no restack was needed. Two
restacks followed and voided the gates and verdicts of five CRs (about +$15-25).

What the user wants (stack-chain-Q1..Q4 and the restatement): in a stack or series batch, each CR
already stacked starts from the head of the CR below it. `ship` refuses otherwise and names both
CRs, before a gate or a verdict is paid on that head. The stack driver checks with `git merge-base`
before it concludes "no restack needed" (one card line). The CLI restacks nothing (no git write) and
has no flag that forces past the refusal: the restack is the fix.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
|---|---|---|
| Q1 A | Refused at `ship`: at each `ship` of a CR already stacked, the CLI refuses when its branch is not based on the head of the CR below. The message names both CRs: `CR-442: branch not based on CR-441's head`. | 1 |
| Q2 A | One card line: the stack driver checks with `git merge-base` that each branch starts from the head of the CR below before it concludes that no restack is needed. | 2 |
| Q3 A | Series batches as well as stack batches: wherever a CR is meant to start from another. | 1 |
| Restatement | No git write and no flag to force past the refusal. The fix is the restack. | 1, 2 |
| Q4 A | Grilled enough. Destination batch-30, joined with `order add`. | Coordination |

## Words used here

- **The CR below** of a CR `c` in an ordered batch: the open CR of the batch (not `merged`, not
  `cancelled`) whose branch is `c`'s base as the record gives it today:
  - in a **stack** batch, `stacks.stack_base(d, c, repo)`. For a CR placed by `stack` (`stacked`),
    this is the branch of the CR under it in `chain`, and the default branch for the first one;
  - in a **series** batch, `stacks.start_base(d, c, repo)`: the branch of `rails.series_predecessor`
    while that CR is open, else the default branch.
  When the base is the default branch, or a branch no open CR of the batch owns, `c` has no CR below
  and nothing is checked. Read through these two functions, never by a copy of their rules. That
  way the base rules that park-live-cr and hold-live-cr change (a dependent of a held or parked CR
  sits on that CR's branch; a held or parked CR sits on the default branch) apply to this check
  with no further edit.
- **A CR meant to start from another** (the CRs `ship` checks): a CR that is neither a `release`
  nor a `fix` and is not held (`stacks.is_held`; with park-live-cr, not `apart`), and:
  - in a **stack** batch, is `stacked` (placed by `stack <cr>…`). A CR not placed yet (a working
    CR to come, one printed `not on its place`) is not checked: Q1 says "a CR already stacked",
    and its place comes from the stack driver's next `stack` or from its Driver's `rebase:` note;
  - in a **series** batch, has a CR below. Series has no `stacked` flag. Its CRs sit on their
    predecessor from their first take (`start_base`'s series rule), so every CR with an open
    predecessor is meant to start from it (Q3).
- **The head of the CR below:** the full SHA in that CR's `head` field, recorded by its last
  `ship`. It is the head the restack notes already name (`restack: on <cr below> <its head7>`) and
  the head `check_release_branch` reads. When the CR below has no recorded head (never shipped),
  nothing is checked. That is the case of a CR below with no PR, and no stacked CR or series
  successor sits on one in the normal flow: `stack` places only CRs with a PR, and a series CR is
  taken once its predecessor is `ready`.

## What changes

### 1. `ship` refuses a CR whose branch does not hold the head of the CR below (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`ship`),
`skills/chantier/scripts/cli/src/chantier/stacks.py` (a new read-only helper, e.g. `chain_below(d,
c, repo) -> CrEntry | None`, that returns the CR below per "Words used here", or None). Place it
beside `stack_base` and `off_place`, not beside `stack_due` (see Coordination).

- In `ship`, after the existing reads and **before** the `RenderedBatch` write, as
  `_refuse_foreign` is placed today: when the batch's mode is `stack` or `series`, the CR is meant
  to start from another, and its CR below has a recorded head, run `git merge-base --is-ancestor
  <below.head> <head>` in the CR's worktree. `<head>` is the worktree's `HEAD`, the head `ship`
  would record. Use the existing `commands/carry._ancestor` or an equivalent read. The command is
  read-only, like every other git call in `ship`.
- Exit 0: `ship` goes on as today.
- Exit 1 (not an ancestor): refuse with `EXIT_PRECONDITION` and record nothing (no `touch`, no
  `ship` event, no `carry` event, no lease claim written). The message starts with Q1's words and
  names both CRs, the short head of the CR below, its branch and the fix:

  `CR-442: branch not based on CR-441's head 1a2b3c4 (git merge-base --is-ancestor): restack it on chantier/batch-30/CR-441, push, then ship again; nothing recorded`

  The fix clause depends on the mode (see open question 1):
  - **stack:** `the stack driver restacks it (a working CR: its Driver rebases onto <branch below>, as the Foreman's \`rebase: stacked on <cr below>\` note says), push, then ship again`;
  - **series:** `its Driver rebases onto <branch below> (the Foreman's \`rebase:\` note), push, then ship again`.
  The CR ids, the short SHA and the branch are mandatory. The rest of the wording is the Driver's
  to fit to the line limit.
- Any other exit (git cannot read the head of the CR below, e.g. the commit is missing from the
  clone): refuse with `EXIT_PRECONDITION` and record nothing: `CR-442: git cannot read CR-441's
  head 1a2b3c4: fetch, then ship again`. This is not read as "based" and not skipped: a check that
  cannot run does not pass.
- No flag skips the check: `--conflict` does not, and no new option is added. The release CR keeps
  its own check (`driver_checks.check_release_branch`, at its release start), unchanged. A fix CR
  and a held CR are not checked.
- The check runs whoever calls `ship`: a CR driver, the stack driver for a CR it moved, a QA
  driver. The lease rules of `ship` are unchanged.
- `ship`'s docstring names the new refusal. `declare/delivery.py` (the `ship` help text) names it
  in one clause if that help lists `ship`'s refusals; otherwise it is unchanged.

Consequence the cards must state (section 2): during a restack, the CR below is shipped at its new
head before the CR above it is shipped. Bottom up is already the order the stack driver's card
gives ("Go on from the first CR, bottom up"). It becomes required: shipping the CR above first is
refused, because the CR below's recorded head is still the old one.

### 2. The cards (`skills/chantier/references/driver.md`)

- **Stack driver**, a new paragraph right after **"Who moves a branch."** (before "Order the
  stack's CRs"), in substance (Q2): **"No restack needed?"** Before you conclude that a CR needs no
  restack, check with `git -C <its worktree> merge-base --is-ancestor <head of the CR below>
  <its head>`, for each CR of the stack from the bottom, the head of the CR below read from
  `$CHANTIER stack`. Exit 0: it starts from the CR below. Any other exit: it needs a restack (or, for a
  working CR, its Driver's rebase on the Foreman's note). Matching PR bases on the forge prove
  nothing about the branches. Then ship the CRs you move bottom up: `ship` refuses a CR whose
  branch does not hold the recorded head of the CR below (`branch not based on <cr>'s head`), and
  a CR below is recorded at its new head only once it is shipped.
- **CR driver: re-takes** (or "CR driver: ship and proof", wherever the Driver judges a `ship`
  refusal reads best), one sentence: a `ship` refused with `branch not based on <cr>'s head` in a
  stack batch means your CR's place in the stack moved under it. Rebase onto the branch the
  refusal names, as for a `rebase: stacked on <cr below>` note, push with `--force-with-lease`, and
  `ship` again. In a series batch the same applies with the predecessor's branch. This is a move:
  "CR driver: moves and conflicts" applies.
- No change to `foreman.md`. Its existing notes (`rebase: stacked on <cr below>`, a series
  `rebase:` note) already carry the fix.
- `agents/` and `com.github.copilot/agents/` are unchanged (the contract lives in the cards).

### 3. Tests (`skills/chantier/scripts/cli/tests/`)

One new file, `test_stack_chain.py`, built on `stack_world.py` / `batch_helpers.py` as the other
stack tests are, parametrized and fast. It calls the CLI in-process on states the CLI built (`open`,
`take`, `stack`, `ship`) with real git commits in the worktrees:

- a stack batch, A and B stacked (`stack A B`), B's branch cut from main: `ship B` exits 2, the
  message holds `B: branch not based on A's head <A7>`, and the record is unchanged (B's `head`,
  `pr`, `pr_base` and the event count are the same as before the call);
- the same after B is rebased onto A's branch and pushed: `ship B` records as today;
- A shipped again at a new head (A amended and pushed), B not rebased: `ship B` is refused, naming
  A's new head;
- a series batch, B's predecessor A open, B's branch cut from main: refused the same way;
- not checked (each `ship` records): a stack CR not stacked yet; the first CR of the stack (base
  the default branch); a fix CR; a held CR; a series CR whose predecessor is merged;
- the head of the CR below unknown to git (a recorded `head` that is not a commit of the clone):
  refused with `git cannot read`, nothing recorded.

A guard on the shipped card, read from the repository at the head under test (not a copy):
`driver.md`'s "Stack driver" section holds `merge-base --is-ancestor` and `branch not based on`.
Add it to an existing card test if one already reads `driver.md` sections, else to
`test_stack_chain.py`.

Existing tests that ship a stacked or series CR whose branch was cut elsewhere (in
`test_carry_ship.py`, `test_stack_*.py`, `stack_world.py`, and others the Driver finds) are made
true to the chain: each such branch is rebased onto the CR below before its `ship`, as a real
restack would do. The check is never weakened to keep an old test green. `just test` stays within
its budget (AGENTS.md).

### 4. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In `stack_batch` (section 13), after `w.chantier("stack", one, two, three)` and the two
`forge_base` retargets, the scenario today ships `three` while its branch was cut from main. It
becomes the proof step:

- `ship three` exits 2, naming `three`, `two` and `two`'s short head, with
  `branch not based on`. Check that nothing was recorded (three's `head` and the last `ship` event
  unchanged).
- Then `restack(w, two, one)` and `restack(w, three, two)` (the existing helper: rebase onto the
  CR below, push with a lease, `ship`), bottom up. The ship bases the following checks read stay
  as they are today (`three` on `two`'s branch, `one` on `main`).

Every other scenario step that ships a stacked or series CR not based on the CR below is made true
to the chain the same way (with `restack`), not by weakening the check. The scenario's README names
the new check in section 13's description if that description lists `ship`'s checks.

## Evidence

- `just check` green (Linux, macOS, Windows per AGENTS.md); `just eval-dry-run` in the worktree
  (the change is under the CLI's `src/`).
- `just test`: `test_stack_chain.py` as in section 3, and the card guard reads `driver.md` as it
  ships at the head under test.
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI and the cards). In
  section 13, the refused `ship` with its message and the record unchanged, then the bottom-up
  restack and the accepted ships.
- The PR body quotes one real refusal line from the scenario's output.
- No host or default matrix: the check depends on neither the host nor a configured value.

## Out of scope

- Any git write by the CLI: `ship` restacks nothing and changes nothing on a refusal.
- A flag or an order to force past the refusal.
- Checking at `stack <crs…>`, at `forge-stack create|rebuild`, or at `take stack` (see open
  question 2).
- Checking a stack CR not placed by `stack` yet, even with a `start_on` (see open question 3).
- Commits a branch holds beyond the CR below (another CR's commits, a dropped CR's): the existing
  `_foreign_crs` refusal, the hold and drop removals and the PR-body checks keep that ground.
- Parallel batches, the release CR (its own check at its start), fix CRs.
- `foreman.md`, the Foreman's stack rules, and the new `foreman-stack.md` card.

## Coordination with batch-30

This CR joins batch-30 on top of the stack (`order add`). It depends on none of the CRs below; the
one that lands later rebases onto the other.

- **park-live-cr (CR-430) and hold-live-cr (CR-431).** Both change the base rules in `stacks.py`
  (`start_base`, `stack_base`, `series_predecessor` moving through `rails.py`, `is_held` moving to
  `rails.py` and re-exported). Both add stack driver paragraphs in `driver.md` after "A CR held out
  of the stack" and edit "CR driver: re-takes" (`rebase: <cr> dropped`). This CR reads the base only
  through `stack_base` / `start_base` and `is_held`, so their rules apply to the check unchanged.
  Re-apply after either lands: rebase. If `apart(c)` exists, exclude `apart(c)` instead of
  `is_held(c)` from the CRs checked. Keep this CR's `driver.md` paragraph right after "Who moves a
  branch." (a different spot from theirs). Put its re-takes sentence after the paragraphs they add.
  Their tests that ship a dependent or a CR above a held or parked one must still pass: a dependent
  sits on the apart CR's branch, which holds that CR's recorded head.
- **drop-to-next-batch (CR-428).** It edits `driver.md`'s "Removing a dropped CR" destination list
  and the orders code. No shared function. A drop's removal (`rebase --onto`, push, `ship`, bottom
  up) passes the check as written. Re-apply: rebase, nothing to adapt.
- **stack-shape-guard (`1-inbox/stack-shape-guard`, about to join).** It adds functions to
  `stacks.py` beside `stack_due` (the shape criterion, `shape_line`) and steps to
  `scenario/run_scenario.py`. It moves the Foreman's stack rules from `foreman.md` into the new
  `foreman-stack.md` and leaves the stack driver's card out of scope. This CR edits no Foreman text,
  so the move does not touch it. Re-apply, whichever lands second: rebase. Keep both CRs' new
  `stacks.py` functions, which sit in different places (this one beside `stack_base`/`off_place`).
  In `stack_batch`, keep both CRs' added steps. If stack-shape-guard's new steps ship a stacked CR,
  that ship must be on the chain (restack first).

## Open questions (for the Chief of Staff)

1. **Who fixes a refused `ship` of a working CR, and in a series.** The restatement says "the fix
   is the stack driver's restack". Today's cards give a `working` CR's branch to its own Driver
   (the stack driver never moves it; the Foreman sends `rebase: stacked on <cr below>`). A series
   batch has no stack driver at all. This specification sends a working stack CR and any series CR
   to their own Driver's rebase (refusal message and `driver.md`), and keeps the stack driver's
   restack for the CRs with no live Driver. Does the user agree, or must every refusal go through
   the stack driver (and, in a series, through the Foreman)?
2. **Only at `ship`?** In Studio's incident, the stack driver concluded "no restack needed" and so
   moved and shipped nothing. A `ship`-only check catches the broken chain at the next `ship` of a
   CR above, not at the stack driver's take; the card line (Q2) is the defence there. Should
   `stack --out-of-draft` or `forge-stack create|rebuild` also refuse a stack that is not a git
   chain? That would be a new refusal beyond Q1. This specification leaves it out.
3. **A stack CR taken onto another's branch but not placed yet** (`start_on` set, not `stacked`).
   Q3's words ("wherever a CR is meant to start from another") could cover it. Q1's ("a CR already
   stacked") do not, so this specification does not check it: it is "to come" until the stack
   driver places it, and refusing its Driver's `ship` would block a CR whose rebase the Foreman
   already owns. Confirm.
