# An ordered stack is checked as a git chain

In a stack or series batch, a CR the record places on another CR's branch (placed by `stack`, or
taken onto it) must have that CR's recorded head in its history. `ship` refuses, recording nothing,
a CR whose branch does not, and `stack --out-of-draft` refuses a CR whose recorded head does not.
The caller of the refused `ship` rebases. The stack driver checks the chain with `git merge-base`
before it concludes that no restack is needed. Specification v2.

## Goal

From Studio's batch-07 retro (`intake/request.md`). The ordered stack CR-439..CR-445 was linear on
the forge only: the PRs' bases formed a chain, but CR-440, CR-442 and CR-444 had been cut from main.
`take CR-446` was refused. A first stack driver wrongly concluded that no restack was needed. Two
restacks followed and voided the gates and verdicts of five CRs (about +$15-25).

What the user wants (stack-chain-Q1..Q7 and the restatement): in a stack or series batch, each CR
the record places on another CR's branch (placed by `stack`, or taken onto it) starts from the
recorded head of the CR below it. `ship` refuses otherwise and names both CRs, before a gate or a
verdict is paid on that head; whoever ran the refused `ship` owns the branch and rebases it.
`stack --out-of-draft` refuses the same broken chain, because in a stack the stack driver may ship
nothing (the incident's path). The stack driver checks with `git merge-base` before it concludes
"no restack needed" (one card line). The CLI restacks nothing (no git write) and has no flag that
forces past either refusal: the rebase is the fix.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
|---|---|---|
| Q1 A | Refused at `ship`: at each `ship` of a CR already stacked, the CLI refuses when its branch is not based on the head of the CR below. The message names both CRs: `CR-442: branch not based on CR-441's head`. | 1 |
| Q2 A | One card line: the stack driver checks with `git merge-base` that each branch starts from the head of the CR below before it concludes that no restack is needed. | 3 |
| Q3 A | Series batches as well as stack batches: wherever a CR is meant to start from another. | 1, 2 |
| Restatement | No git write and no flag to force past the refusal. | 1, 2 |
| Q4 A | Grilled enough. Destination batch-30, joined with `order add`. | Coordination |
| Q5 | The caller of the refused `ship` owns the branch (driver.md, "Who moves a branch") and rebases it: no route through the stack driver or the Foreman. One refusal message for both modes. The check reads the CR below's recorded head, so a stacked working CR is refused at its next `ship` each time the CR below shipped a new round or was rebased, and rebases then without waiting for the Foreman's note. driver.md's `rebase: mode <mode>` paragraph is fixed (its pre-rebase `ship` would be refused), and every other `ship` before a rebase in the cards is found and fixed. | 1, 3 |
| Q6 | One more refusal, at `stack --out-of-draft` only (`_check_out_of_draft`): a named CR whose recorded head does not hold its CR below's recorded head; same helper, exclusions and `git cannot read` refusal; message ending `then stack --out-of-draft again; nothing recorded`; no flag; one card line in the stack driver's paragraph; one parametrized test; a scenario step if it costs one step. `stack <crs>`, `forge-stack`, `take stack` stay out of scope. | 2, 3, 4, 5 |
| Q7 | A CR taken onto another's branch and not placed yet is checked when its `start_on` is live (`stacks._live_start`); an unplaced CR with no live `start_on` stays unchecked. The wording "a CR the record places on another CR's branch (placed by `stack`, or taken onto it)" in "Words used here", section 1 and the Goal; the CR driver sentence names the first-ship case; tests split; existing test worlds made true to the chain. | Words, 1, 3, 4 |

## Words used here

- **The CR below** of a CR `c` in an ordered batch: the open CR of the batch (not `merged`, not
  `cancelled`) whose branch is `c`'s base as the record gives it today:
  - in a **stack** batch, `stacks.stack_base(d, c, repo)`. For a CR placed by `stack` (`stacked`),
    this is the branch of the CR under it in `chain`, and the default branch for the first one.
    For a CR not placed yet whose `start_on` is live (`stacks._live_start`), `stack_base` goes
    through `stack_start`, whose rule 1 returns that `start_on`: the CR below is the CR that owns
    that branch;
  - in a **series** batch, `stacks.start_base(d, c, repo)`: the branch of `rails.series_predecessor`
    while that CR is open, else the default branch.
  When the base is the default branch, or a branch no open CR of the batch owns, `c` has no CR below
  and nothing is checked. Read through these functions, never by a copy of their rules. That
  way the base rules that park-live-cr and hold-live-cr change (a dependent of a held or parked CR
  sits on that CR's branch; a held or parked CR sits on the default branch) apply to this check
  with no further edit.
- **A CR the record places on another CR's branch** (the CRs checked): a CR that is neither a
  `release` nor a `fix` and is not held (`stacks.is_held`; with park-live-cr, not `apart`), and:
  - in a **stack** batch, is either placed by `stack` (`stacked`, by `stack <cr>…`), or taken onto
    another CR's branch and not placed yet, with its `start_on` live (`stacks._live_start(d, c)`:
    the CR that owns that branch is neither ended nor held). A CR not placed yet with no live
    `start_on` (none recorded, or its owner merged, cancelled or held) is not checked: its place
    comes from the stack driver's next `stack` or from its Driver's `rebase:` note;
  - in a **series** batch, has a CR below. Series has no `stacked` flag. Its CRs sit on their
    predecessor from their first take (`start_base`'s series rule), so every CR with an open
    predecessor is placed on it (Q3).
- **The head of the CR below:** the full SHA in that CR's `head` field, recorded by its last
  `ship`. It is the head the restack notes already name (`restack: on <cr below> <its head7>`) and
  the head `check_release_branch` reads. Because it is the recorded head, a CR above is refused at
  its next `ship` each time the CR below shipped a new head (a new round, a rebase), until it is
  rebased onto it (Q5). When the CR below has no recorded head (never shipped), nothing is checked.
  That is the case of a CR below with no PR, and no stacked CR or series successor sits on one in
  the normal flow: `stack` places only CRs with a PR, and a series CR is taken once its predecessor
  is `ready`.

## What changes

### 1. `ship` refuses a CR whose branch does not hold the head of the CR below (CLI)

Files: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`ship`),
`skills/chantier/scripts/cli/src/chantier/stacks.py` (a new read-only helper, e.g. `chain_below(d,
c, repo) -> CrEntry | None`, that returns the CR below of a CR the record places on another CR's
branch, per "Words used here", or None). Place it beside `stack_base` and `off_place`, not beside
`stack_due` (see Coordination). One more read-only helper runs the git check and returns based /
not based / git cannot read; `ship` (here) and `stack --out-of-draft` (section 2) both call it.

- In `ship`, after the existing reads and **before** the `RenderedBatch` write, as
  `_refuse_foreign` is placed today: when the batch's mode is `stack` or `series`, `chain_below`
  returns a CR, and that CR has a recorded head, run `git merge-base --is-ancestor <below.head>
  <head>` in the CR's worktree. `<head>` is the worktree's `HEAD`, the head `ship` would record.
  Use the existing `commands/carry._ancestor` or an equivalent read. The command is read-only, like
  every other git call in `ship`.
- Exit 0: `ship` goes on as today.
- Exit 1 (not an ancestor): refuse with `EXIT_PRECONDITION` and record nothing (no `touch`, no
  `ship` event, no `carry` event, no lease claim written). One message for both modes (Q5): it
  starts with Q1's words and names both CRs, the short head of the CR below, the branch below and
  the fix:

  `CR-442: branch not based on CR-441's head 1a2b3c4: rebase onto chantier/batch-30/CR-441, push, ship again; nothing recorded`

  The CR ids, the short SHA, the branch below and the clause `nothing recorded` are mandatory. The
  rest of the wording is the Driver's to fit to the line limit.
- Any other exit (git cannot read the head of the CR below, e.g. the commit is missing from the
  clone): refuse with `EXIT_PRECONDITION` and record nothing: `CR-442: git cannot read CR-441's
  head 1a2b3c4: fetch, then ship again; nothing recorded`. This is not read as "based" and not
  skipped: a check that cannot run does not pass.
- No flag skips the check: `--conflict` does not, and no new option is added. The release CR keeps
  its own check (`driver_checks.check_release_branch`, at its release start), unchanged. A fix CR
  and a held CR are not checked.
- The check runs whoever calls `ship`: a CR driver, the stack driver for a CR it moved, a QA
  driver. The caller owns the branch it ships and rebases it on a refusal (Q5; driver.md, "Who
  moves a branch"): there is no route through the stack driver or the Foreman. The lease rules of
  `ship` are unchanged.
- `ship`'s docstring names the new refusal. `declare/delivery.py` (the `ship` help text) names it
  in one clause if that help lists `ship`'s refusals; otherwise it is unchanged.

Consequences the cards must state (section 3):

- During a restack, the CR below is shipped at its new head before the CR above it is shipped.
  Bottom up is already the order the stack driver's card gives ("Go on from the first CR, bottom
  up"). It becomes required: shipping the CR above first is refused, because the CR below's
  recorded head is still the old one.
- A working CR placed on another CR's branch is refused at its next `ship` (its first one
  included) each time the CR below shipped a new head since the CR's branch was cut or last
  rebased. Its Driver rebases then, without waiting for the Foreman's `rebase:` note (Q5).
- A `ship` meant to record a forge change before a rebase (a PR put back to draft, then `ship`,
  then the rebase) is refused when the branch is not yet on the CR below: the `ship` comes after
  the rebase and push, and records the draft state and the new base at once.

### 2. `stack --out-of-draft` refuses a CR whose recorded head does not hold the CR below's (CLI)

File: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`_record_drafts`,
`_check_out_of_draft`), with the helpers of section 1.

- `_check_out_of_draft` takes the `Repo` (passed from `_record_drafts`) and, for each named CR,
  after its existing checks (held, handed back ready with a PR, no draft under it): when
  `chain_below` returns a CR and both that CR and the named CR have a recorded head, run the same
  git check, `git merge-base --is-ancestor <below.head> <c.head>`, with the recorded head of each,
  in the repository (the main checkout or the project's clone; a CR worktree shares its objects).
  The exclusions are those of section 1 (a release, a fix, a held CR; a CR with no CR below or a
  CR below with no recorded head).
- Not an ancestor: refuse with `EXIT_PRECONDITION`, nothing written (no `pr-draft` touch or event
  for any named CR, the existing refusals' behaviour):

  `CR-442: branch not based on CR-441's head 1a2b3c4: rebase onto chantier/batch-30/CR-441, push, ship, then stack --out-of-draft again; nothing recorded`

- Any other exit: `CR-442: git cannot read CR-441's head 1a2b3c4: fetch, then stack --out-of-draft
  again; nothing recorded`.
- No flag skips it. `stack --draft` is not checked (a PR going back to draft is never a risk).
- The docstrings of `_record_drafts` and `_check_out_of_draft` name the new refusal; the `stack`
  help text names it in one clause if it lists `--out-of-draft`'s refusals.

### 3. The cards (`skills/chantier/references/driver.md`)

- **Stack driver**, a new paragraph right after **"Who moves a branch."** (before "Order the
  stack's CRs"), in substance (Q2, Q6): **"No restack needed?"** Before you conclude that a CR needs no
  restack, check with `git -C <its worktree> merge-base --is-ancestor <head of the CR below>
  <its head>`, for each CR of the stack from the bottom, the head of the CR below read from
  `$CHANTIER stack`. Exit 0: it starts from the CR below. Any other exit: it needs a restack (or, for a
  working CR, its Driver's rebase). Matching PR bases on the forge prove nothing about the
  branches. Then ship the CRs you move bottom up: `ship` refuses a CR whose branch does not hold
  the recorded head of the CR below (`branch not based on <cr>'s head`), and a CR below is recorded
  at its new head only once it is shipped. `stack --out-of-draft` refuses the same broken chain on
  the recorded heads: restack, push, `ship`, then `stack --out-of-draft` again.
- **Stack driver: "Who moves a branch."** The sentence on a working CR's Driver ("that Driver
  rebases once before its next push and `ship`s") adds: or at once when its `ship` is refused
  `branch not based on`, without waiting for the note.
- **Stack driver: bottom up where `ship` runs over several CRs.** The restack after a partial
  merge (step 3, "then `ship` each one once"), the insertion (step 2, "`ship` each one moved") and
  the drop's removal (step 3, "`ship` each one") say "bottom up" for those `ship`s.
- **CR driver: re-takes** (or "CR driver: ship and proof", wherever the Driver judges a `ship`
  refusal reads best), one sentence that names the first-ship case: a `ship` refused with `branch
  not based on <cr>'s head` (your first `ship` included, on a branch taken onto another CR's branch
  that has shipped a new head since) means the CR below moved under you. You own your branch:
  rebase onto the branch the refusal names at once, without waiting for a `rebase:` note, as for a
  `rebase: stacked on <cr below>` note (in a series batch, the predecessor's branch), push with
  `--force-with-lease`, and `ship` again. This is a move: "CR driver: moves and conflicts" applies.
- **The stack batch paragraph** ("that branch is the stack driver's, never rebased by you but on a
  note", ~939): add "or on a `ship` refused `branch not based on`".
- **The `rebase: mode <mode>` paragraph** (~946-953): its pre-rebase `ship` goes. Put the PR to
  draft on the forge first (`gh pr ready --undo`, `glab mr update --draft`), rebase onto the base
  `take` printed, retarget the PR, push with `--force-with-lease`, then `ship` (`--conflict` by the
  rule above): that one `ship` records the draft state and the new base. Say why in a clause: a
  `ship` before the rebase is refused (`branch not based on`) when the new mode puts the CR on
  another CR's branch.
- **The other `ship`s that follow a forge change** ("CR driver" ~203: "A change of a PR's base or
  draft state on the forge is followed by `ship <cr> <link>`"; "Means: carries, conflicts and the
  early push" ~484, the same rule): add one clause to each: a `ship` refused `branch not based on`
  there means rebase first, as that refusal says, then `ship`. The Driver searches the cards
  (`driver.md`, `foreman.md`, `qa-driver.md` and the others under `skills/chantier/references/`)
  for any other `ship` prescribed before a rebase on a CR placed on another CR's branch, and fixes
  each the same way. The `carries` refusal's "draft, then `ship`" (~539-546) applies to a PR on the
  default branch, which has no CR below: no change.
- No change to `foreman.md`'s stack rules. Its existing notes (`rebase: stacked on <cr below>`, a
  series `rebase:` note) still carry the move; a Driver refused at `ship` no longer waits for them.
- `agents/` and `com.github.copilot/agents/` are unchanged (the contract lives in the cards).

### 4. Tests (`skills/chantier/scripts/cli/tests/`)

One new file, `test_stack_chain.py`, built on `stack_world.py` / `batch_helpers.py` as the other
stack tests are, parametrized and fast. It calls the CLI in-process on states the CLI built (`open`,
`take`, `stack`, `ship`) with real git commits in the worktrees.

`ship`:

- a stack batch, A and B stacked (`stack A B`), B's branch cut from main: `ship B` exits 2, the
  message holds `B: branch not based on A's head <A7>` and `nothing recorded`, and the record is
  unchanged (B's `head`, `pr`, `pr_base` and the event count are the same as before the call);
- the same after B is rebased onto A's branch and pushed: `ship B` records as today;
- A shipped again at a new head (A amended and pushed), B not rebased: `ship B` is refused, naming
  A's new head;
- a stack CR not placed yet, taken onto A's branch (a live `start_on`), its branch cut from main:
  `ship` refused the same way (Q7);
- a series batch, B's predecessor A open, B's branch cut from main: refused the same way;
- not checked (each `ship` records): a stack CR not placed yet with no `start_on` recorded; a stack
  CR not placed yet whose `start_on` owner is merged, and one whose owner is held (Q7); the first CR
  of the stack (base the default branch); a fix CR; a held CR; a series CR whose predecessor is
  merged;
- the head of the CR below unknown to git (a recorded `head` that is not a commit of the clone):
  refused with `git cannot read`, nothing recorded.

`stack --out-of-draft`, one parametrized test (Q6): A and B stacked and handed back ready with PRs,
B's recorded head not holding A's recorded head: `stack --out-of-draft A B` exits 2 with `B: branch
not based on A's head <A7>` and `then stack --out-of-draft again; nothing recorded`, and
`batch.json` and `events.jsonl` unchanged (A not recorded out of draft either); the case with B's
recorded head on A's: accepted; and the `git cannot read` case.

A guard on the shipped card, read from the repository at the head under test (not a copy):
`driver.md`'s "Stack driver" section holds `merge-base --is-ancestor`, `branch not based on` and
`stack --out-of-draft again`, and its `rebase: mode` paragraph holds no `ship` before its rebase
(the guard asserts the paragraph's text order: `rebase` before the first `ship`). Add it to an
existing card test if one already reads `driver.md` sections, else to `test_stack_chain.py`.

Existing tests that ship, or turn out of draft, a stacked, taken-onto or series CR whose branch was
cut elsewhere (in `test_carry_ship.py`, `test_stack_*.py`, `stack_world.py`, and others the Driver
finds) are made true to the chain: each such branch is rebased onto the CR below before its
`ship`, as a real restack would do, and the test worlds' recorded heads form the chain. The check
is never weakened to keep an old test green. `just test` stays within its budget (AGENTS.md).

### 5. The scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In `stack_batch` (section 13), after `w.chantier("stack", one, two, three)` and the two
`forge_base` retargets, the scenario today ships `three` while its branch was cut from main. It
becomes the proof step:

- `ship three` exits 2, naming `three`, `two` and `two`'s short head, with
  `branch not based on`. Check that nothing was recorded (three's `head` and the last `ship` event
  unchanged).
- Then `restack(w, two, one)` and `restack(w, three, two)` (the existing helper: rebase onto the
  CR below, push with a lease, `ship`), bottom up. The ship bases the following checks read stay
  as they are today (`three` on `two`'s branch, `one` on `main`).

`stack --out-of-draft` (the section that checks its refusals, ~8871): add one refused call on a
broken chain, nothing written, only if a state with a CR's recorded head off its CR below's is at
hand there in one step; otherwise the parametrized test of section 4 is its proof, and the PR says
so.

Every other scenario step that ships, or turns out of draft, a stacked, taken-onto or series CR not
based on the CR below is made true to the chain the same way (with `restack`), not by weakening the
check. The scenario's README names the new checks in section 13's description if that description
lists `ship`'s checks.

## Evidence

- `just check` green (Linux, macOS, Windows per AGENTS.md); `just eval-dry-run` in the worktree
  (the change is under the CLI's `src/`).
- `just test`: `test_stack_chain.py` as in section 4, and the card guard reads `driver.md` as it
  ships at the head under test.
- `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI and the cards). In
  section 13, the refused `ship` with its message and the record unchanged, then the bottom-up
  restack and the accepted ships.
- The PR body quotes one real refusal line from the scenario's output.
- No host or default matrix: the checks depend on neither the host nor a configured value.

## Out of scope

- Any git write by the CLI: `ship` and `stack --out-of-draft` restack nothing and change nothing
  on a refusal.
- A flag or an order to force past either refusal.
- Checking at `stack <crs…>`, at `forge-stack create|rebuild`, or at `take stack` (Q6). `stack
  <crs>` sets the order before the restack it calls for, so its CRs are not on the chain yet by
  design; `forge-stack` follows `stack --out-of-draft`'s ground on the forge (the PRs' bases, the
  five checks), and reaches the forge, not the record's heads; `take stack` is the Foreman's handing
  of a stack to be restacked, where a broken chain is the stack driver's work, which its card's
  `merge-base` line and the `stack --out-of-draft` refusal now guard.
- A stack CR not placed yet with no live `start_on` (Q7).
- Commits a branch holds beyond the CR below (another CR's commits, a dropped CR's): the existing
  `_foreign_crs` refusal, the hold and drop removals and the PR-body checks keep that ground.
- Parallel batches, the release CR (its own check at its start), fix CRs.
- `foreman.md`'s stack rules, and the new `foreman-stack.md` card.

## Coordination with batch-30

This CR joins batch-30 on top of the stack (`order add`). It depends on none of the CRs below; the
one that lands later rebases onto the other.

- **park-live-cr (CR-430) and hold-live-cr (CR-431).** Both change the base rules in `stacks.py`
  (`start_base`, `stack_base`, `series_predecessor` moving through `rails.py`, `is_held` moving to
  `rails.py` and re-exported). Both add stack driver paragraphs in `driver.md` after "A CR held out
  of the stack" and edit "CR driver: re-takes" (`rebase: <cr> dropped`). This CR reads the base only
  through `stack_base` / `start_base`, `_live_start` and `is_held`, so their rules apply to the
  check unchanged. Re-apply after either lands: rebase. If `apart(c)` exists, exclude `apart(c)`
  instead of `is_held(c)` from the CRs checked. Keep this CR's `driver.md` paragraph right after
  "Who moves a branch." (a different spot from theirs). Put its re-takes sentence after the
  paragraphs they add. Their tests that ship a dependent or a CR above a held or parked one must
  still pass: a dependent sits on the apart CR's branch, which holds that CR's recorded head.
- **drop-to-next-batch (CR-428).** It edits `driver.md`'s "Removing a dropped CR" destination list
  and the orders code. No shared function. A drop's removal (`rebase --onto`, push, `ship`, bottom
  up) passes the check as written; this CR's "bottom up" in that list's step 3 is one word beside
  its edit. Re-apply: rebase, nothing to adapt.
- **stack-shape-guard (`1-inbox/stack-shape-guard`, about to join).** It adds functions to
  `stacks.py` beside `stack_due` (the shape criterion, `shape_line`) and steps to
  `scenario/run_scenario.py`. It moves the Foreman's stack rules from `foreman.md` into the new
  `foreman-stack.md` and leaves the stack driver's card out of scope. This CR edits no Foreman text,
  so the move does not touch it. Re-apply, whichever lands second: rebase. Keep both CRs' new
  `stacks.py` functions, which sit in different places (this one beside `stack_base`/`off_place`).
  In `stack_batch`, keep both CRs' added steps. If stack-shape-guard's new steps ship a stacked CR,
  or turn one out of draft, that CR must be on the chain (restack first).

## Open questions (for the Chief of Staff)

None. Spec v1's three open questions are closed by Q5, Q6 and Q7.
