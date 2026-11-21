# A stack CR starts on another CR's branch only once that CR is ready

Spec v3 (2026-11-21), from `02-answers.md` take-draft-Q1 to Q5. Short name: `take-draft`. No
issue (origin: verbal; Studio's batch-06 retro, split out of `take-base-from-forge` by the Chief
of Staff on 2026-11-20). v3 over v2: Q5 (a CR with an open dependency is on its highest open
dependency's branch until placed) and the spec critic's fixes.

## Goal

In a stack batch, a new CR does not start on code that still has rounds to come. Studio's CR-429
was given the branch of CR-424, a working CR with an open draft PR and several rounds still to
come; the Foreman's take note had to send it to `origin/main`, and the retro counts that base as
wrong. From now on `take` starts a new CR with no open dependency on the nearest earlier CR that
has a PR only when that CR is handed back `ready`; otherwise on the default branch. A CR with an
open dependency starts on its highest open dependency's branch, whatever ready CR sits above that
dependency. And the base a taken CR prints is where its worktree and PR really sit: until the
stack driver places it, a `start_on` whose owner is still open, else its highest open dependency's
branch, else the default branch. The goals of the user's stack-Q4 (2026-11-17) hold: one linear
stack on the forge, set by the stack driver's final-order take at the batch's end, and never a
branch with no PR as a base.

Sources: `intake/request.md`, `01-intent.md`, `02-answers.md`; the user's stack-Q4
(`5-archives/261117-2134-333-take-base-nearest-pr/02-answers.md`) and that CR's spec;
`take-base-from-forge`'s answers (`5-archives/261121-0330-422-take-base-from-forge/02-answers.md`).

## Decisions carried

From `02-answers.md`:

1. **take-draft-Q1 (the user, 2026-11-21, on a Fable advisor's proposal: "Oui, B de Fable"):** a
   new CR starts on an earlier CR's branch only when that CR is handed back `ready`; when the
   nearest earlier CR with a PR is still working (or blocked), or there is none, it starts on the
   default branch. **This narrows the user's stack-Q4 (2026-11-17, "the nearest earlier CR of the
   batch that already has a PR") and take-base-from-forge Q5 (2026-11-20, "whatever its status
   and draft state"), and keeps their two goals:** one linear stack set by the end run, never a
   branch with no PR as a base. A CR that needs the code of a CR still working says so with
   `after`; otherwise CRs start side by side on the default branch and the final-order take orders
   them (one sentence in `concepts.md`, Stack: section 4).
2. **take-draft-Q2 (Fable advisor):** a CR taken on the default branch stays there until the stack
   driver places it. The printed base matches where the worktree and the PR really sit. No new
   field: a missing `start_on` on a taken CR already means the default branch.
3. **take-draft-Q3 (Fable advisor):** the walk stops at the first CR with a PR: when it is working
   and a lower one is ready, the base is the default branch. Skipping down would put two branches
   on one base, a tree stack-Q4 excludes.
4. **take-draft-Q4 (Fable advisor):** a taken CR whose `start_on` owner has ended (merged,
   cancelled, seen merged on the forge) prints the default branch until the stack driver places
   it. **One rule for every taken CR not yet placed: a `start_on` whose owner is still open, else
   the default branch** (Q5 adds: a CR with an open dependency, its dependency's branch). It is
   Q2's reason and what `leave_stack_starts` already says for a held or parked owner, and it never
   prints a base the worktree was not put on. v1's "unless a ready CR with a PR is below it" is
   gone. `_landed_line`'s `base:` line is unchanged (its message and when it prints; section 2
   keeps it so).
5. **take-draft-Q5 (Fable advisor):** a CR with an open dependency, queued or taken, until the
   stack driver places it: **its highest open dependency's branch (`_nearest_open`), else the
   default branch; no start candidate.** With Q1, a ready CR above the dependency may itself sit
   on the default branch, without the dependency's code, so starting the dependent on it would
   break what `after` promises, and its printed base would flip each time that CR turns ready or
   goes back to working. This base moves only when the dependency ends (then Q4's rule), and needs
   no new record. Left as today: with several open dependencies not stacked on one another, the
   highest one's branch does not hold the others' code.
6. **Destination (Fable advisor):** batch-30, after CR-442 and CR-438 where it can; no
   `depends.json`. Batch-30 runs this CLI live, so the new take rule applies to its later takes
   once merged: the Chief of Staff tells the Foreman at the merge.

Kept, in force (not reopened):

7. **stack-Q4 (the user, 2026-11-17)**, as narrowed by Q1: one stack-driver run at the batch's end
   owns the final order; the in-batch runs keep the stack current; the rule is for stack batches
   only.
8. **take-base-from-forge Q1 to Q4:** `take` adds no network read; a CR with a `merged@1` journal
   line for its recorded PR (`landed`) reads as ended for the start base; a `base:` line names it;
   with no journal line, the record is used.
9. **take-base-from-forge Q6/Q7:** a ready CR the stack driver has not placed reads its word from
   its recorded `pr_base`; on an open CR's branch it is ready to merge only when that CR is.
10. **take-base-from-forge Q9:** the release CR's base is unchanged (the top CR).

## Words used here

- **Earlier:** a lower place in `chain` (`stacks.chain`: the open CRs in `order`, apart and
  dependent CRs left out, the release last).
- **Has a PR:** `pr` is recorded and the CR is not in `landed`.
- **Handed back ready:** `status == "ready"`, whatever the PR's draft flag (a ready CR in a stack
  may keep a draft PR while it waits on a CR under it).
- **The start candidate:** walking `chain` down from the CR, the first CR that has a PR, when it is
  handed back ready; none when that first CR is anything but `ready`, or there is none. The walk
  never goes further down (Q3). Only a CR with no open dependency has one (Q5).
- **Open dependency:** a CR of `after` not ended and not in `landed` (`_open_after`). **Highest
  open dependency:** `_nearest_open`'s pick (highest in `chain`, a dependency outside the chain, a
  fix, ranking lowest).
- **Taken:** any status but `queued`. **Placed:** `stacked` is true (the stack driver's `stack`
  named it). A queued CR is never placed in what `stack_start` sees (a placed CR reaches it only
  through `start_base` with a `start_on`, recorded at a take).
- **Open owner:** `_live_start`'s test today: the CR whose branch is `start_on` is not ended, not in
  `landed`, not out of order.

## What changes

### 1. CLI: `skills/chantier/scripts/cli/src/chantier/stacks.py`

- `_below_with_pr` stays as it is. Add beside it `_start_candidate(b_data, c, landed)`: the pair
  `_below_with_pr` returns when that CR's status is `ready`, else `None`.
- `start_on_for`, stack branch: return the branch of `_start_candidate(...)` in place of
  `_below_with_pr(...)`'s, else `None`. The series branch, the `_alone`/`_open_after` guard (a CR
  with an open dependency gets no `start_on`) and the parallel `None` are unchanged. Docstring
  says the new rule.
- `stack_start`: new rules, first match wins (docstring rewritten to say them):
  1. Unchanged: `start_on` with an open owner (`_live_start`).
  2. **New (Q2, Q4):** a CR taken, not placed, with no open dependency (`_open_after` empty): the
     default branch. This covers a taken CR with no `start_on` (it started on the default branch)
     and one whose `start_on` owner has ended, whatever CRs with a PR sit below it.
  3. Today's rules 2 and 3, split (no more comparison of the dependency's place with a CR below):
     - **3a (Q1, Q3):** a queued CR with no open dependency: the start candidate's branch, else the
       default branch. The place the record shows is then the base `take` will record.
     - **3b (Q5):** a CR not placed (queued or taken) with an open dependency: its highest open
       dependency's branch (`_nearest_open`). No start candidate, whatever ready CR with a PR sits
       above the dependency.
  4. A placed CR (it reaches `stack_start` only through `start_base`: `stacked` with a `start_on`)
     whose owner has ended, with or without an open dependency: today's rules 2 and 3 unchanged
     (`_below_with_pr` whatever the status, the nearest open dependency when it sits higher, else
     the default branch). Rules 2 and 3 name "not placed" or "queued", so every placed CR reaches
     this rule. `tests/test_stack_hold.py::test_a_placed_crs_start_on_owner_ended_falls_back_below_and_held_goes_to_default`
     and scenario step 13's check at `scenario/run_scenario.py:6639-6644` stay green (section 6).
     Q4 and Q5 are about CRs not yet placed.
  `landed` reads as ended in every rule, as today. The Driver may order the code differently (for
  instance the placed test first) as long as these results hold.
- `start_base`: no change (its held-owner and `after` paths stay). `stack_base` for a CR not placed
  goes through `stack_start` as today, so it gets the new rules; a placed CR keeps its placed rule.
- `off_place`, `to_come`: no code change; they read `stack_base(planned=True)`, so a working CR
  taken on the default branch whose PR is on the default branch is no longer reported off its
  place when a CR below it gets a PR, and a working dependent is to stack on its highest open
  dependency.

### 2. CLI: `skills/chantier/scripts/cli/src/chantier/commands/facts.py`

- `_base_of`: no change; it prints `start_base`, which follows section 1.
- `_landed_line`: its message, its placement and when it prints stay as today. Its recompute of
  the record-alone base must change: today it is `start_base` of a copy of the CR with
  `start_on=None`, and under section 1's rule 2 that copy of a taken CR reads the default branch,
  so the line would never print for a taken CR. The record-alone base becomes (all with no
  `landed`):
  - a placed CR: `start_base(d, c, repo)` (today's `first = c`, unchanged);
  - a CR taken, not placed, whose `c.start_on` owner is in `landed`: `start_base(d, c, repo)` (the
    record alone still holds that owner open, so it gives `start_on`);
  - any other CR: `start_base(d, as_queued, repo)`, where `as_queued` is a copy with
    `status="queued"` and `start_on=None` (what the take gives from the record alone, the
    dependency rule 3b and the release's and fix's rules included; not `start_on_for`, which
    returns `None` for a dependent, a parallel batch, a release and a fix).
  Compare it with the real `start_base(d, c, repo, landed)`; print the line as today when they
  differ and the first names a CR of `landed`. The Driver chooses the helper's shape.
  Known and accepted: the line can still print for a CR taken on the default branch (or on an
  earlier start base) whose would-be candidate later became ready and then landed; the record
  cannot tell it from a CR the forge read moved, and the line still points to the right
  `order merged`.

### 3. CLI: `commands/driver.py` and `core/records.py`

- `driver.py`, `_record_take`: no change in flow (`start_on` recorded only at the first take, from
  `start_on_for`).
- `core/records.py`, the comment on `start_on`: in a stack batch, the branch of the nearest earlier
  CR with a PR, not seen merged on the forge, when that CR was handed back ready at the first take
  (none for a CR with an open dependency); a taken stack CR with no live `start_on` is on its
  highest open dependency's branch, else on the default branch, until the stack driver places it.

### 4. Cards (`skills/chantier/references/`)

- `concepts.md`, "Batch modes", **Stack** (today lines ~249-253): "on the nearest earlier CR of the
  batch (by order) that already has a PR and whose PR the forge does not show merged (…), else on
  the default branch, recorded at its first `take` (a branch with no PR is never a base), so its PR
  is already on the stack" becomes "on the nearest earlier CR of the batch (by order) that has a
  PR, when that CR is handed back `ready` and the forge does not show its PR merged (…); when that
  CR is still working or blocked, or there is none, on the default branch; recorded at its first
  `take` (a branch with no PR is never a base)". Drop "so its PR is already on the stack". In the
  same sentence, "on the branch of its last dependency still open" becomes "on the branch of its
  highest dependency still open (by order)". Add two sentences: "Until the stack driver places it,
  a taken CR with no open dependency stays on that start base while its owner is open, else on the
  default branch; a CR with an open dependency is on its highest open dependency's branch." and "A
  CR that needs the code of a CR still working says so with `after`; otherwise CRs start side by
  side on the default branch and the final-order take orders them."
- `concepts.md`, **Dependencies** (today lines ~360-362): "The CR starts on the branch of its last
  dependency still open, in the order of `after`, else, in a stack, on the nearest earlier CR of
  the batch that has a PR and whose PR the forge does not show merged" becomes "The CR starts on
  the branch of its last dependency still open, in the order of `after` (in a stack, the one
  highest by order, whatever ready CR sits above it), else, in a stack, on the nearest earlier CR
  of the batch that has a PR, when that CR is handed back `ready` and the forge does not show its
  PR merged". The rest of the paragraph is unchanged.
- `foreman.md`, "The first take" (today lines ~383-384): "`take` starts every new CR on the nearest
  earlier CR with a PR (the CLI computes it; you choose nothing)" becomes "`take` starts every new
  CR with no open dependency on the nearest earlier CR with a PR once that CR is handed back
  `ready`, else on the default branch, and a CR with an open dependency on its highest open
  dependency's branch (the CLI computes it; you choose nothing)". Keep "never correct a base by a
  take note". CR-438 (`stack-shape-guard`) moves these stack bullets verbatim into a new
  `foreman-stack.md`: edit the bullet wherever it stands at this CR's rebase.
- `driver.md`, CR driver (today lines ~939-940): "the nearest earlier CR of the batch that has a PR
  that the forge does not show merged" becomes "the nearest earlier CR of the batch that has a PR,
  handed back `ready`, that the forge does not show merged, or, for a CR with an open `after`, its
  highest open dependency's branch". The rest of the paragraph is unchanged.
- `agents/`, `com.github.copilot/agents/`: no change.

### 5. The other readers the Driver checks

Each reads `stack_base` or `start_base` and so sees section 1's rule; none needs a code change by
this spec, but the Driver reads each and confirms its output still says the truth (a test or
scenario change where it does not):

- `board/crs.py`, `base_of` (the board's "on" and "why" for a CR in `chain`: a taken CR not placed
  now shows the default branch, a dependent its highest open dependency's branch, `why` "planned").
- `commands/forge_stack.py:96`, `_row`'s `"base"` (`stack_base(..., planned=True)`), and its
  `_no_bottom` (`off_place`, line ~106-114).
- `commands/carry.py`, `head_base` (its candidates: `stack_base`, `pr_base`, the planned place, the
  default branch, every other CR's branch), and `off_place` through `commands/facts.py`'s
  `_off_place_tail`.
- Also: `commands/driver.py:338` (the clean-rebase text), `commands/facts.py:211`,
  `commands/forge_stack_gh.py:186`, `stack_words.pr_base_of` (only when no `pr_base` is recorded).

### 6. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

The Driver checks every scenario step that takes a stack CR on another CR's branch, and makes
that CR `ready` where the step expects its branch.

- Step 13 (`run_scenario.py`, around lines 6600-6644):
  - The check at lines ~6606-6613 (`order after four --note two` leaves the base on `three`)
    **flips (Q5):** with `after` on `two`, `handoff four` prints `two`'s branch (the dependency's,
    though `three`, ready with a PR, sits above it); after `--note -`, `three`'s branch again (the
    start candidate: `three` is ready). Reword its label to say so.
  - The check labelled at line 6626 (`four`, placed, taken on `three`): `one`, `two`, `three` are
    ready there, so it keeps its expectation; reword the label to "the nearest earlier CR handed
    back ready with a PR".
  - The check at lines 6639-6644 (`four`, placed, falls back to `two`'s branch once `three` is
    cancelled, back to `three` with it): kept unchanged by section 1's rule 4.
- Step 13-bis (`stack_start_base`, today lines ~6776-6858): the docstring and the note at lines
  6777-6778 say "the nearest earlier CR handed back ready with a PR". Rewritten checks; the step may
  add CRs for the layouts (the Driver chooses them):
  1. Unchanged: no earlier CR with a PR (a later one does not count): default branch, no
     `start_on`.
  2. **Flipped:** an earlier CR `working` with a PR (a draft): the CR taken starts on the default
     branch, no `start_on`, and `handoff` prints `base origin/main`.
  3. New: the same earlier CR set `ready` (PR kept): the next CR taken records its branch and
     `handoff` prints it (it can be the kept check "the CR right before has no PR and an earlier
     one has").
  4. New (Q3): the nearest earlier CR with a PR is `working` and a CR below it is `ready` with a PR:
     the default branch.
  5. New: the nearest earlier CR with a PR is `blocked`: the default branch.
  6. New (Q2): the CR of check 2, taken on the default branch, still prints `base origin/main` in
     `handoff` once the CR below it is `ready` with a PR.
  7. New (Q4): a CR taken on a ready CR's branch prints `base origin/main` once that CR is merged
     or cancelled, even with a ready CR with a PR below it.
  8. New (Q5): a CR with an open `after` still starts on the dependency's branch, no `start_on`,
     with a ready CR with a PR above the dependency (below the CR).
  9. Kept, with the base CRs made ready: a cancelled or merged CR is skipped (the nearest ready one
     left with a PR is the base); a fix and a release are unchanged; an open `after` still starts
     on the dependency's branch; a parallel batch still starts on the default branch.
- Step 13-ter (`start_base_forge`, today lines ~6861-6920): set `a` `ready` before `take b` and `z`
  `ready` with its PR before `take d`, so checks 4 and 2 keep their expectations; the `base:` line
  checks are unchanged (check 2's line for `d`, taken with `start_on` on `z`, included) and prove
  section 2's recompute. Add one check (Q4 with the journal), before `order merged a`: once the hub
  saw `a` merged, and with `z` ready with a PR below, `handoff b` (taken on `a`) prints
  `base origin/main` and the `base:` line naming `a`.
- `scenario/README.md` (line 165, "a working one too"): "a ready one only; a working or blocked
  one, or a lower ready one past it, gives the default branch, a CR with an `after` is on its
  dependency's branch whatever ready CR sits above it, and a taken CR whose start CR has ended
  prints the default branch".

### 7. Tests (`skills/chantier/scripts/cli/tests/test_stack_base.py`)

- `STACKED`: unchanged (v2's `ready` on the placed CRs is not needed under Q5: case A no longer
  reads a start candidate).
- `CASES`:
  - **A** flips to `"b-3"` (CR-5 taken, not placed, open dependencies CR-3, CR-2, CR-1: the highest
    one, Q5; today CR-4 placed above wins). `test_a_cr_off_its_place_is_to_stack_on_the_cr_below_that_has_a_pr`
    follows: `off_place` gives `("b-1", "CR-3")`, the row ends `(note rebase: stacked on CR-3)`,
    and `pr_base = "b-3"` gives `None`; rename it to say its highest open dependency.
  - **D** flips to `"main"` (CR-8 taken, no `start_on`: Q2).
  - **B2**: `"b-1"` (CR-2 working with a PR above the dependency: Q5). Add **B3**, the same with
    `cr(2, status="ready")`: `"b-1"` too (Q5: a ready CR above the dependency does not override it).
  - **B** (`after` CR-3, CR-1, no PR anywhere): `"b-3"`, unchanged (re-checked under rule 3b).
  - New rows: **working** (`[cr(1), noPr(2, status="queued")]`, 2, `"main"`); **ready**
    (`cr(1, status="ready")`, `"b-1"`); **blocked** (`cr(1, status="blocked")`, `"main"`); **Q3**
    (`[cr(1, status="ready"), cr(2), noPr(3, status="queued")]`, 3, `"main"`); **Q2**
    (`[cr(1, status="ready"), cr(2, pr_base="main")]`, 2, `"main"`); **Q4-merged** and
    **Q4-cancelled** (`[cr(1, status="ready"), cr(2, status="merged"|"cancelled"),
    cr(3, start_on="b-2")]`, 3, `"main"`: the default branch even with a ready CR with a PR below).
  - C, D2, F keep their expectations.
  - The test also asserts, for a queued CR with no `after` (D2, working, ready, blocked, Q3),
    `start_on_for(d, c) == (None if want == "main" else want)`, and for the Q2 row
    `off_place(d, c, REPO) is None` (the Driver chooses how: a column or a branch in the test).
- `LANDED`: `below`, `below-all`, `live-start-on`, `empty-set` with `cr(1, status="ready")` and
  `cr(2, status="ready")` (same expectations); `dependency` unchanged (`"b-2"`, `"main"`); new
  **Q4-landed** (`[cr(1, status="ready"), cr(2, status="ready"), noPr(3, start_on="b-2")]`, 3,
  `{"CR-2"}`, `"b-2"`, `"main"`).
- New, parametrized: the `base:` line of `commands.facts._landed_line(d, c, REPO, landed)` (called
  in-process on prepared records, none placed, so no forge read), each row asserting the line
  names the expected CR, or is absent:
  - **dependency:** `[noPr(1), cr(2), noPr(3, after=["CR-2"])]` (CR-3 taken), `{"CR-2"}`: names
    CR-2.
  - **release:** `[cr(1, status="ready"), cr(2), <release CR-9 working>]`, the release asked,
    `{"CR-2"}`: names CR-2.
  - **start-on-between:** `[cr(1, status="ready"), cr(2, status="ready"), cr(3, status="ready"),
    noPr(4, start_on="b-2")]` (CR-4 taken on CR-2 before CR-3 had a PR), `{"CR-2"}`: names CR-2.
  - **start-on-chosen-past:** `[cr(1, status="ready"), cr(2, status="ready"), noPr(3,
    start_on="b-1")]`, `{"CR-2"}` (CR-3 taken on CR-1 once the forge showed CR-2 merged, scenario
    13-ter check 2): names CR-2.
  - **unaffected:** `[cr(1, status="ready"), cr(2, status="ready"), noPr(3, status="queued")]`,
    `{"CR-1"}`: absent.
- No new test file. The Driver runs the whole suite: `test_stack_hold.py`, `test_park_shared.py`,
  `test_hold_live_shared.py`, `test_hold_live_stack.py`, `test_park_stack.py` build stack CRs and
  must stay green (most go through the out-of-order rules first, or are placed).

## Overlaps in batch-30 (running)

- **CR-442 `stack-git-chain`** (pending): edits `stacks.py` (`stack_base`, `stack_start`,
  `start_base` gain or pass `landed`) and checks "a CR taken onto another CR's branch" through
  `_live_start`; a CR with no live `start_on` stays unchecked, which agrees with Q2, Q4 and Q5.
  Same functions as section 1: this CR goes after it and rebases onto it, keeping both rules.
- **CR-438 `stack-shape-guard`** (working): moves `foreman.md`'s stack rules into
  `foreman-stack.md` and adds `shape_line` beside `stack_due` in `stacks.py`. Section 4's Foreman
  edit lands wherever "The first take" stands at rebase; `stack_due`/`FORMING` are not changed.
- **CR-430 `park-live-cr`, CR-431 `hold-live-cr`** (merged): `leave_stack_starts` unsets
  `start_on` ("starts on the default branch"); section 1's rule 2 makes the printed base agree.
- **CR-443 `gate-hold-narrowing`, CR-436 `sync-blocked-by-others`**: touch `commands/driver.py` and
  `commands/facts.py` in other functions; file level only.

## Out of scope

- Parallel and series batches, the release's base, a fix CR's base.
- The `after` rule, except that a ready CR above the dependency no longer overrides it (Q5).
- A CR with several open dependencies not stacked on one another: the highest one's branch does
  not hold the others' code; left as today (Q5).
- The first take's threshold (two CRs ready with a PR), the in-batch runs, the final-order take,
  the Ordering rule.
- A base passed by the Foreman at the take (Q1's option C, not chosen); re-basing by `take --note`.
- A recursive check that the start candidate's own base is all ready.
- Any forge read in `take`; the `forge-stack` commands; the CR pane (no `STATUS.json` field
  changes, so no screenshot is owed).

## Evidence

- `just check` green (Linux, macOS, Windows).
- `just eval-dry-run` in the worktree (a change under the CLI's `src/`), before the first push.
- `just test` green within its budget, with section 7's rows; the tests call the CLI's functions
  in-process on prepared records (no shipped file is guarded).
- `just scenario` green with section 6's checks: the pipeline's `just scenario (ubuntu-latest)` at
  the PR's head, and locally on Windows (`chantier gate`) when this CR is on top of its batch's
  stack.
- No change to `hooks/` or `types/`, so no `just mod`. No host or default-configuration dependency,
  so no matrix.

## Open questions

None.
