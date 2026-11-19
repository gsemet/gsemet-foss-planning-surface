# Change Specification: take stack and the record name the right base in a stack batch

## Goal

In a stack batch, the CLI must never point a CR at the wrong base. Two cases were seen in
batch-28 (2026-11-19, after the stack driver's order O-24):

1. `take stack`'s row for CR-383 read "not on its place ... (note rebase: stacked on CR-369)".
   The stack order puts CR-383 on CR-382, and its code needs CR-375. A Driver that followed the
   note would have rebased onto the wrong CR.
2. The record gave CR-387 (working, first take) the base CR-386's branch, which did not exist
   yet. Its `take` had given it CR-383's branch.

After this change:

- the "stacked on" CR that `take stack` (and `stack` with no CR) names is the CR just below in
  the stack's order;
- the record's base for a CR the stack driver has not placed yet is the base its `take` gave it,
  and never a branch that does not exist yet.

## The cause, as read in the code (`skills/chantier/scripts/cli/src/chantier/stacks.py`)

The archived record (`5-archives/batches/batch-28.json`) holds CR-383 with
`after: [CR-375, CR-370, CR-369]` and order 10, and CR-387 with `after: []` and order 12.

- `off_place(d, c, repo)` compares the PR's base with `stack_base(d, c, repo, planned=True)`.
  For a CR not yet placed by `stack` (`c.stacked` false) that has an `after`, `stack_base` returns
  `start_base`. `start_base` takes the **last open dependency in the textual order of `after`**,
  so CR-383 got CR-369. The chain's order is not consulted.
- For an unplaced CR with no `after`, `stack_base(..., planned=True)` returns the CR just below it
  in `chain(d)`, whether or not that CR exists yet. CR-387 got CR-386, which was still queued with
  no branch. Its `take` had recorded `start_on` = CR-383's branch (`start_on_for`, fixed in
  `commands/driver.py` `take`), and `start_base` honours that. The planned path ignores it.

The planned path reaches these places:

- the base column of the stack rows (`commands/facts.py` `_stack_ref`, through `stack_lines`,
  printed by `take stack` and by `stack` with no CR);
- the row's `not on its place` tail (`_off_place_tail` → `off_place`);
- the board's base (`board/crs.py` `base_of`, `planned=not _open_after(...)`);
- `forge-stack`'s bottom refusal (`commands/forge_stack.py` `_no_bottom`);
- `carry.py` `head_base`'s candidate names.

## What changes

### 1. The planned place of a CR the stack driver has not placed yet (`stacks.py`)

Add one function to `stacks.py`, for example `unplaced_base(b_data, c, repo) -> str`. It gives the
base of a CR in a stack batch's chain that `stack` has not placed (`not c.stacked`), not a
release and not a fix. It applies three rules, first match wins:

1. **The base its take gave it.** When `c.start_on` is recorded and the CR that owns that branch
   is not ended, return `c.start_on`. This is the same test `start_base` already applies.
2. **The CR just below it in the stack's order that exists.** Walk `chain(b_data)` downwards from
   `c` and return the branch of the first CR that has left `queued`, i.e. one that has been taken
   at least once and so has a branch. The walk skips CRs still `queued`: their branch does not
   exist yet.
3. Otherwise, `start_base(b_data, c, repo)`: its last open dependency's branch, else the default
   branch. These are today's rules and they do not change.

`stack_base(b_data, c, repo, planned=True)` uses `unplaced_base` for such a CR, in place of the
two current paths:

- today an unplaced CR with an `after` goes through `start_base`;
- today an unplaced CR with no `after` gets the chain predecessor.

Nothing else in `stack_base` changes:

- a CR placed by `stack` (`c.stacked`) still sits on the CR below it in the chain, or on the
  default branch when it is first;
- the release still sits on the top CR;
- `planned=False` still returns `start_base`, which is what the CR's `take` printed in its
  `worktree: ... base <ref>` line (`facts.py` `_base_of`).

Update `stack_base`'s docstring to match. Drop the clause "a CR with an open dependency that
`stack` has not placed yet, on that dependency's branch" and state the three rules above.

With this:

- CR-383 (no `start_on`, since it had open dependencies at its take): CR-382 is just below it in
  the chain and is taken, so the note reads `stacked on CR-382`.
- CR-387 (`start_on` = CR-383's branch, CR-383 open): the record says CR-383's branch, the same as
  its take. It does not say CR-386.

### 2. `off_place` and the `take stack` row (`stacks.py`, `commands/facts.py`)

`off_place` keeps its shape: it compares `c.pr_base` with the planned base, which now comes from
rule 1. The CR it names in `(note rebase: stacked on <cr>)` is therefore the CR just below in the
stack's order that exists, or the CR whose branch the take gave it. It is never a dependency
picked by the textual order of `after`, and never a CR still queued. The wording of
`_off_place_tail` does not change, so the cards (`driver.md` "note rebase: stacked on <cr below>",
`foreman.md`) stay true and need no edit.

### 3. The board (`board/crs.py` `base_of`)

`base_of` now calls `stack_base(..., planned=True)` for every CR of the chain. The `why` word
stays:

- `stack` when the stack driver placed the CR;
- `dependency` when the base is an open dependency's branch;
- `planned` otherwise.

A not-yet-placed CR with an open dependency now reads the place rule 1 gives it, which is at or
above its dependencies in the chain. It no longer reads the textual last dependency. If the board
must keep showing "dependency", that word applies only when the returned branch is one of the
CR's open dependencies.

### 4. Other callers

- `forge_stack._no_bottom` and `carry.head_base` take the new planned base as is; they need no
  edit.
- `forge_stack`'s rows never include an unplaced working CR (`to_come` stops them), so what the
  forge is asked to do does not change.

## Decisions carried from `02-answers.md`

- The intent is the grill. The Chief of Staff settled it on 2026-11-20, with no question to the
  user.
- The CR joins batch-29 (factory, stack) once specified.
- The change is the one the intent names: `take stack`'s "stacked on" is the CR just below in the
  stack's order, the record's base matches the base its `take` gave, never a branch that does
  not exist yet, and a test on a prepared state covers both.

## Out of scope

- Where `take` starts a CR that has open dependencies (`start_base`'s "last open dependency in
  the order of `after`"). CR-383's own take printed CR-369 for that reason. The intent does not
  ask to change it; see the open questions.
- The parallel and series modes: `stack_base`'s planned path exists only in a stack batch.
- `stack` (the command that places CRs), `_check_place`, `forge-stack`'s plans, and the cards'
  wording.

## Evidence

A test on a prepared state, in the existing style of
`skills/chantier/scripts/cli/tests/test_stack_due.py`:

- a `BatchRecord(mode="stack", ...)` of `CrEntry` values;
- a `Repo` stub that carries `config["default_branch"]` and `config["remote"]`;
- one parametrized test, in a new `tests/test_stack_base.py` or added to `test_stack_due.py`.

It holds batch-28's shape in a few CRs:

- **Case A (CR-383).** Placed CRs CR-1..CR-4, `stacked=True`, orders 1..4, each with a PR and a
  branch. CR-5 is working, not stacked, order 5, `after=["CR-3", "CR-2", "CR-1"]`, with a PR and
  `pr_base` = CR-1's branch. Expect:
  - `off_place` returns `(CR-1's branch, "CR-4")`;
  - `stack_lines` prints the row ending `(note rebase: stacked on CR-4)`;
  - with `pr_base` = CR-4's branch, `off_place` returns `None`.
- **Case B (CR-387).** CR-5 is working with a PR. CR-6 and CR-7 are queued (no PR) with orders
  6 and 7. CR-8 is working, not stacked, order 8, `after=[]`, `start_on` = CR-5's branch, with
  `pr_base` = CR-5's branch. Expect:
  - `stack_base(planned=True)` and `stack_base(planned=False)` both return CR-5's branch;
  - `off_place` returns `None`;
  - the stack row's `base` is CR-5's branch, not CR-7's.
- **Case C (rule 2 skips the queued).** As case B, but with no `start_on` on CR-8. The planned
  base is CR-5's branch, the nearest taken CR below. CR-7 is skipped because it is queued.
- **Case D (no change for a placed CR).** A `stacked=True` CR still gets its chain predecessor,
  and the first placed CR gets the default branch.

The test calls the functions in-process. It reads no shipped file, so the shipped-file rule does
not apply. Keep it fast, within the `just test` budget of AGENTS.md.

Gates, per AGENTS.md, for a change under the CLI's `src/`:

- `just check`, run in the worktree at the rebased head before the first push;
- `just eval-dry-run`, at the same point;
- the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head.

The behaviour does not depend on the host or on a configured value, so no host and default
matrix applies.

## Open questions

1. Should `take` in a stack batch start a CR that has open dependencies on the same place rule 1
   gives, instead of the last dependency in the textual order of `after`? Today CR-383's take
   printed CR-369 while its code needs CR-375. This CR leaves that start unchanged, so for such a
   CR the place in the record (rule 1) and the base its take printed can differ until its Driver
   rebases.
2. Rule 2 counts a CR as existing once it has left `queued` (it has a branch). Should it instead
   require a PR, so that the note names a branch that is on the remote? A working CR below with
   no PR yet has only a local branch, which the PR above it cannot use as its base on the forge.
