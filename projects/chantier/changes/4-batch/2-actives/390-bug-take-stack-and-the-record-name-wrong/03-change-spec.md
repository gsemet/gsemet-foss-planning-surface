# Change Specification: take stack and the record name the right base in a stack batch

## Goal

In a stack batch, the CLI must never point a CR at the wrong base. Two cases were seen in batch-28
(2026-11-19), after the stack driver's order O-24:

1. `take stack`'s row for CR-383 read "not on its place ... (note rebase: stacked on CR-369)".
   The stack's order puts CR-383 on CR-382, and its code needs CR-375. A Driver that followed the
   note would have rebased onto the wrong CR.
2. The record gave CR-387 (working, first take) the base CR-386's branch, which did not exist
   yet. Its `take` had given it CR-383's branch.

After this change:

- In a stack batch, `take` and the record compute a CR's base with **one function**, so the base
  the take prints and the place the record gives never differ.
- The "stacked on" CR that `take stack` names is the CR just below in the stack's order that has a
  PR, or the nearest open dependency when that dependency sits higher in the stack.
- The record never names a branch that does not exist yet.

## The cause, as read in the code (`skills/chantier/scripts/cli/src/chantier/stacks.py`)

The archived record (`5-archives/batches/batch-28.json`) holds:

| CR | order | `after` |
| --- | --- | --- |
| CR-383 | 10 | `[CR-375, CR-370, CR-369]` |
| CR-387 | 12 | `[]` |

Three functions name a CR's base today, and they disagree:

- `start_base` gives the base that `take` prints (`commands/facts.py` `_base_of`, in the
  `worktree: ... base <ref>` line). For a CR with open dependencies it takes the **last one
  written in `after`**. For CR-383 that is CR-369, while its code needs CR-375.
- `stack_base(..., planned=True)` gives the record's place. For an unplaced CR with an `after`, it
  falls back to `start_base`, so CR-383's note named CR-369. For an unplaced CR with no `after`,
  it takes the CR just below it in `chain(d)`, whether or not that CR exists yet, and ignores the
  `start_on` recorded at the take. So CR-387 got CR-386, which was still queued with no branch,
  instead of CR-383.
- `start_on_for`, called by `take` in `commands/driver.py`, picks the nearest earlier CR with a PR
  and freezes it in `start_on`. It does this only for a CR with no open dependency.

The planned base is read by:

- the stack rows' base column (`commands/facts.py` `_stack_ref`, through `stack_lines`, printed by
  `take stack` and by `stack` with no CR);
- the rows' `not on its place` tail (`_off_place_tail`, through `off_place`);
- the board's base (`board/crs.py` `base_of`);
- `forge-stack`'s bottom refusal (`commands/forge_stack.py` `_no_bottom`);
- `carry.py` `head_base`.

## What changes

### 1. One base function for an unplaced CR of a stack batch (`stacks.py`)

Add one function, for example `stack_start(b_data, c, repo) -> str`. It applies to a CR of a stack
batch that is not a release, not a fix, and not placed by `stack` (`not c.stacked`). It returns the
branch the CR starts on and its record's place. Its rules, first match wins:

1. **The base its take fixed.** When `c.start_on` is recorded and the CR that owns that branch is
   not ended, return `c.start_on`. This is today's test in `start_base`.
2. **The CR below it that has a PR, or a higher dependency.** Walk `chain(b_data)` down from `c`
   and take the first CR that has a PR recorded (`x.pr`); its branch is on the remote. Skip a CR
   below that has no PR yet.
   - If one of `c`'s open dependencies sits higher in the stack's order than that CR, return the
     nearest open dependency instead. "Nearest" means the open dependency that sits highest in
     `chain(b_data)`, whatever its place in `after`.
   - Otherwise return the branch of the CR with the PR.
3. **No CR below has a PR.** Return the nearest open dependency in the stack's order (as defined
   in rule 2), or, with none open, the default branch.

An open dependency that is not in the chain (a fix CR) ranks below every CR of the chain.

### 2. Wiring it in (`stacks.py`, `commands/driver.py`)

**`start_base`.** In a stack batch, for a CR that is not a release and not a fix, `start_base`
returns `stack_start`. This drops the "last open dependency in the order of `after`" path for
stack batches. The release, the fix CR, a series batch and a parallel batch keep their rules
unchanged. The "last open dependency in the order of `after`" rule stays as it is in a parallel
batch.

**`stack_base`.** For a CR not placed by `stack` (and not a release), `stack_base` returns
`stack_start` for both values of `planned`. This replaces two current paths:

- the `start_base` path for an unplaced CR with an `after`;
- the chain-predecessor path for an unplaced CR with no `after`.

Nothing else in `stack_base` changes:

- a placed CR (`c.stacked`) still sits on the CR just below it in the chain, or on the default
  branch when it is first;
- the release still sits on the top CR;
- a fix CR keeps its current result.

Keep the `planned` parameter for its other callers. Rewrite the docstrings of `start_base`,
`stack_base` and `start_on_for` to state the rules above.

**`start_on_for` and `take`.** `start_on_for` returns the result of `stack_start`'s rule 2 for a
queued CR with no open dependency. That CR has no dependency, so the result is the nearest CR below
it with a PR. With no such CR it returns `None`, as today, and the CR starts on the default branch.
`take` (`commands/driver.py`) records it in `start_on` at the first take, as today. A CR with open
dependencies gets no frozen `start_on`, as today: its base follows its dependencies' places in the
stack. `take` and the record still read that base from the same `stack_start`, on the same record,
so they agree.

Results on batch-28's shape:

- **CR-383:** after O-24, CR-382 is the CR just below it with a PR, and none of CR-383's open
  dependencies sits above CR-382. The take, the stack row and the note all say CR-382:
  `(note rebase: stacked on CR-382)`.
- **CR-383 at its take,** before O-24: its open dependencies were CR-369 (order 1), CR-370
  (order 2) and CR-375 (order 4), so rule 2 compares the nearest CR below with a PR against
  CR-375. It never picks CR-369 because CR-369 is written last.
- **CR-387:** its `start_on` is CR-383's branch and CR-383 is open, so rule 1 applies. Even
  without rule 1, rule 2 skips CR-386, CR-385 and CR-384, which have no PR, and reaches CR-383. The
  take and the record both say CR-383's branch, never CR-386's.

### 3. `off_place` and the `take stack` row (`stacks.py`, `commands/facts.py`)

`off_place` keeps its shape: it compares `c.pr_base` with the planned base, which now comes from
`stack_base`, and so from `stack_start` for an unplaced CR. The CR named in
`(note rebase: stacked on <cr>)` follows `stack_start`'s rules. The tail's wording does not change,
so the cards stay true without edits: `driver.md`'s "note rebase: stacked on <cr below>" and
`foreman.md`.

### 4. The board (`board/crs.py` `base_of`)

`base_of` keeps calling `stack_base` and now gets the same base for an unplaced CR whatever
`planned` it passes. Its `why` word becomes:

- `stack` when the stack driver placed the CR;
- `dependency` when the base returned is one of the CR's open dependencies;
- `planned` otherwise.

### 5. Other callers

These take the new base as it comes and need no edit:

- `forge_stack._no_bottom`;
- `carry.head_base`;
- `driver.py`'s clean-rebase line (`stack_base(b.record, c, repo)`).

`forge-stack`'s rows never include an unplaced working CR (`to_come` stops them), so what the forge
is asked to do does not change.

## Decisions carried from `02-answers.md`

- The intent is the grill. The Chief of Staff settled it on 2026-11-20. The CR joins batch-29
  (factory, stack) once specified.
- **Question 1, settled yes.** In a stack batch, `take` and the record use one base function, so
  the take's printed base and the record's place never differ. A CR with open dependencies starts
  on the nearest of them in the stack's order, not on the last one written in `after`. This is
  sections 1 and 2.
- **Question 2, settled yes.** Rule 2's CR below must have a PR, so its branch is on the remote. A
  CR below with no PR yet is skipped, and when no CR below has a PR the base falls to rule 3. This
  is section 1.
- The intent's test on a prepared state, covering both anomalies, is in Evidence.

## Out of scope

- The parallel and series modes, the release and fix CRs: their base rules do not change.
- `stack` (the command that places CRs), `_check_place`, `forge-stack`'s plans, and the cards'
  wording.
- A dependency that is still queued: it has no branch. Whether `take` should refuse a CR whose
  dependency is queued is not this CR.

## Evidence

The checks are calls in `skills/chantier/scripts/cli/tests/`, in the style of `test_stack_due.py`:

- a `BatchRecord(mode="stack", ...)` made of `CrEntry` values;
- a `Repo` stub that carries `config["default_branch"]` and `config["remote"]`;
- one parametrized test in a new `tests/test_stack_base.py`.

For every case the test asserts three things:

- `start_base(d, c, repo)`, `stack_base(d, c, repo)` and `stack_base(d, c, repo, planned=True)`
  return the same branch. This is the "one function" decision.
- That branch is the expected one.
- The branch belongs to a CR with a PR, or is the default branch, or is an open dependency's
  branch. It is never a queued CR's branch.

The cases:

- **A. CR-383 after O-24 (anomaly 1).**
  - Setup: CR-1 to CR-4 placed (`stacked=True`), orders 1 to 4, each with a PR and a branch. CR-5
    working, not stacked, order 5, `after=["CR-3", "CR-2", "CR-1"]`, with a PR and `pr_base` set to
    CR-1's branch.
  - Expect: the base is CR-4's branch. `off_place` returns `(CR-1's branch, "CR-4")`.
    `stack_lines` prints CR-5's row ending in `(note rebase: stacked on CR-4)`.
  - With `pr_base` set to CR-4's branch: `off_place` returns `None`.
- **B. Nearest dependency, not the last written (question 1).**
  - Setup: CR-1 to CR-3 working, orders 1 to 3, with no PR. CR-4 queued, order 4,
    `after=["CR-3", "CR-1"]`.
  - Expect: the base is CR-3's branch (rule 3). Before this change it was CR-1's.
  - Variant: CR-2 has a PR and CR-4's `after` is `["CR-1"]`. The base is CR-2's branch (rule 2:
    CR-2 sits above the dependency CR-1).
- **C. CR-387 (anomaly 2).**
  - Setup: CR-5 working with a PR. CR-6 and CR-7 queued, no PR, orders 6 and 7. CR-8 working, not
    stacked, order 8, `after=[]`, `start_on` set to CR-5's branch, `pr_base` set to CR-5's branch.
  - Expect: the base is CR-5's branch. `off_place` returns `None`. The stack row's `base` is
    CR-5's branch, not CR-7's.
- **D. Rule 2 skips a CR without a PR (question 2).**
  - Setup: as case C, without `start_on`, and with CR-7 working but without a PR.
  - Expect: the base is CR-5's branch. CR-7 is skipped although it has a branch.
  - Variant: no CR below has a PR, and there is no dependency. The base is the default branch
    (rule 3).
- **E. A placed CR is unchanged.** A `stacked=True` CR still gets the CR just below it in the
  chain, and the first placed CR gets the default branch.

One in-process `take` check, with the `world` or `repo` and `chantier` fixtures of
`tests/conftest.py`, as `test_batch_end.py` uses them:

- Setup: a stack batch prepared with case B's shape.
- Action: `chantier("take", "CR-4", "--epoch", 1)`.
- Expect: the printed `worktree: ... base <ref>` line names CR-3's branch, and the batch's
  `take stack` row for CR-4 shows the same base.

This is the check that the take's printed base and the record's place agree, end to end. The tests
read no shipped file, so the shipped-file rule does not apply. Keep them fast, within AGENTS.md's
`just test` budget.

Gates for a change under the CLI's `src/` (AGENTS.md):

- `just check` in the worktree, at the rebased head, before the first push;
- `just eval-dry-run` at the same point;
- the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head.

The behaviour does not depend on the host or on a configured value, so no host and default matrix
applies.
