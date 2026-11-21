# A stack CR starts on another CR's branch only once that CR is ready

Spec v1 (2026-11-21), provisional. Short name: `take-draft`. No issue (origin: verbal; Studio's
batch-06 retro, split out of `take-base-from-forge` by the Chief of Staff on 2026-11-20). No grill
was held: the user delegated the night's spec questions to an advisor. **The central choice is
open (take-draft-Q1, below).** Every section is written on its recommended option, B, as provisional
text. If A is chosen, this CR has only Q2's part left (or nothing, if Q2 is answered no). If C is
chosen, sections 1 to 4 are rewritten.

## Goal

In a stack batch, a new CR does not start on code that still has rounds to come. Studio's CR-429 was
given the branch of CR-424, a working CR with an open draft PR and several rounds still to come.
The Foreman's take note had to send it to `origin/main`, and the retro counts that base as wrong.
Under option B, `take` starts a new CR on the nearest earlier CR that has a PR only when that CR is
handed back `ready`. Otherwise it starts the CR on the default branch. The user's stack-Q4
(2026-11-17) is kept: one linear stack on the forge, set by the stack driver's final-order take at
the batch's end, and never a branch with no PR as a base.

Sources: `intake/request.md`, `01-intent.md`; the user's stack-Q4
(`5-archives/261117-2134-333-take-base-nearest-pr/02-answers.md`) and that CR's spec;
`take-base-from-forge`'s Q1 to Q6 (`5-archives/261121-0330-422-take-base-from-forge/02-answers.md`),
Q5 being the split that made this CR.

## Decisions carried

There is no `02-answers.md` yet. The decisions in force, which this CR keeps:

1. **stack-Q4 (the user, 2026-11-17):** one linear stack on the forge. One stack-driver run at the
   batch's end owns the final order. A branch with no PR is never a base. The in-batch runs keep
   the stack current. The base rule is for stack batches only.
2. **take-base-from-forge Q1 to Q4:** `take` adds no network read. A CR with a `merged@1` journal
   line for its recorded PR reads as ended for the start base. A `base:` line names it. With no
   journal line, the record's base is used.
3. **take-base-from-forge Q6/Q7:** a ready CR that the stack driver has not placed reads its word
   from its recorded `pr_base`. On an open CR's branch, it is ready to merge only when that CR is.
4. **take-base-from-forge Q9:** the release CR's base is unchanged (the top CR).

Provisional, pending the user's (or the advisor's) answer: take-draft-Q1 = B, Q2 = yes, Q3 = no
skip. See "Open questions".

## Words used here

- **Earlier:** a lower place in `chain` (`stacks.chain`: the open CRs in `order`, apart and
  dependent CRs left out, the release last).
- **Has a PR:** `pr` is recorded and the CR is not in `landed` (the journal's `merged@1`).
- **Handed back ready:** `status == "ready"`, whatever the PR's draft flag. A ready CR in a stack
  may keep a draft PR while it waits on a CR under it.
- **The start candidate:** walking `chain` down from the CR, the first CR that has a PR. **Under
  B**, it is a base only when it is handed back ready. If it is `working` or `blocked`, the base is
  the default branch. The walk does not go further down (Q3).

## What changes

### 1. CLI: `skills/chantier/scripts/cli/src/chantier/stacks.py`

- `_below_with_pr` stays as it is: the first CR with a PR below `c`. Add one helper beside it,
  `_start_candidate(b_data, c, landed)`. It returns `_below_with_pr`'s result when that CR's status
  is `ready`, and `None` otherwise (the CR is `working` or `blocked`, or there is none).
- `start_on_for`: its stack branch returns `_start_candidate(...)`'s branch instead of
  `_below_with_pr(...)`'s. The series branch, the `_alone`/`_open_after` guard and the parallel
  `None` are unchanged. Its docstring says the new rule.
- `stack_start`, rule 2: for a CR not yet taken (`queued`), use `_start_candidate` in place of
  `_below_with_pr`. The place that the record shows for a queued CR is then the base `take` will
  record. Keep the comparison with `_nearest_open` (an open dependency higher in `chain` still
  wins). This rule also applies to a taken CR whose `start_on` owner has ended (rule 1 no longer
  holds). Such a CR then reads the default branch unless a ready CR with a PR is below it. Update
  the docstring.
- **Q2 (provisional: yes): the start base is fixed at the first take, including the default
  branch.** Today, a taken CR with no `start_on` (it started on the default branch) gets rule 2
  recomputed at every read. If a CR below it later gets a PR, `handoff` prints that CR's branch
  while the worktree and the PR sit on the default branch. Under B, this happens every time a lower
  CR turns ready. New rule in `stack_start`: a CR that has been taken (status not `queued`), is
  neither a fix nor a release, has no open dependency (`_open_after` empty) and has no `start_on`
  reads the default branch until `stack` places it. No new field: today's records already mean
  "started on the default branch" by a missing `start_on` (`start_on_for` returned `None` at the
  take). `stack_apart.leave_stack_starts` (CR-430/CR-431, merged) already unsets `start_on` with
  the docstring "it starts on the default branch": this rule makes the printed base agree with it.
  A placed CR (`stacked`) keeps `stack_base`'s placed rule. A CR with an open dependency keeps
  rule 3.
- `stack_base` for a CR not placed goes through `stack_start` as today, so it gets both changes.
  `ready_word` and `draft_waited` read `pr_base` first (take-base-from-forge Q6/Q7) and do not
  change.

### 2. CLI: `skills/chantier/scripts/cli/src/chantier/commands/facts.py`

- `_base_of`: no change. It prints `start_base`, which now follows section 1.
- `_landed_line`: today it compares `start_base` of a copy of the CR with `start_on=None` against
  the real one. Under Q2, that copy of a taken CR would read the default branch, and the `base:`
  line would never print. The recompute must use the take's rule: compare
  `start_on_for(d, c_as_queued)` with no `landed` against `start_on_for(d, c_as_queued, landed)`,
  where `c_as_queued` is a copy with `status="queued"` and `start_on=None`. Print the line as today
  when the first names a CR of `landed`. Same message, same placement. The Driver chooses the
  helper's shape.

### 3. CLI: `skills/chantier/scripts/cli/src/chantier/commands/driver.py` and `core/records.py`

- `_record_take`: no change in flow (`start_on` is recorded only at the first take, from
  `start_on_for`).
- `core/records.py`, the comment on `start_on`: in a stack batch, the branch of the nearest earlier
  CR with a PR, when that CR was handed back ready at the first take. No `start_on` on a taken
  stack CR with no open dependency means the default branch.

### 4. Cards (`skills/chantier/references/`)

- `concepts.md`, "Batch modes", **Stack** (today lines ~249-253): "on the nearest earlier CR of the
  batch (by order) that already has a PR and whose PR the forge does not show merged … else on the
  default branch" becomes "on the nearest earlier CR of the batch (by order) that has a PR, when
  that CR is handed back `ready` and the forge does not show its PR merged; when that CR is still
  working or blocked, or there is none, on the default branch". Keep "recorded at its first take (a
  branch with no PR is never a base)". Add: a CR started on the default branch stays there until the
  stack driver places it.
- `concepts.md`, **Dependencies** (today lines ~360-362): the same wording in "else, in a stack, on
  the nearest earlier CR …".
- `foreman.md`, "The first take" (today line ~381, "`take` starts every new CR on the nearest
  earlier CR with a PR"): "… on the nearest earlier CR with a PR once that CR is handed back
  `ready`, else on the default branch (the CLI computes it; you choose nothing)". Keep "never
  correct a base by a take note". **CR-438 (`stack-shape-guard`, working in batch-30)** moves these
  stack bullets verbatim into a new `foreman-stack.md`. Edit the bullet wherever it stands at this
  CR's rebase.
- `driver.md`, CR driver (today line ~939): "the nearest earlier CR of the batch that has a PR that
  the forge does not show merged" becomes "… that has a PR, handed back `ready`, that the forge does
  not show merged". The rest of the paragraph is unchanged.
- `agents/`, `com.github.copilot/agents/`: no change.

### 5. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- Step 13-bis (`stack_start_base`, today lines ~6756-6826), rewritten checks:
  1. Unchanged: no earlier CR with a PR (a later one does not count): default branch, no
     `start_on`.
  2. **Flipped:** an earlier CR `working` with a PR (a draft): the CR taken starts on the default
     branch, no `start_on`, and `handoff` prints `base origin/main`.
  3. New: the same earlier CR set `ready` (PR kept): the next CR taken records its branch and
     `handoff` prints it.
  4. New (Q3): the nearest earlier CR with a PR is `working` and a CR below it is `ready` with a PR:
     the default branch.
  5. New: the nearest earlier CR with a PR is `blocked`: the default branch.
  6. New (Q2): the CR of check 2, taken on the default branch, still prints `base origin/main` in
     `handoff` once the CR below it is `ready` with a PR.
  7. Kept, made ready where they need a base: the CR right before has no PR and an earlier one has
     (now `ready`); a cancelled or merged CR is skipped; a fix and a release are unchanged; an open
     `after` still starts on the dependency's branch; a parallel batch still starts on the default
     branch.
- Step 13-ter (`start_base_forge`, today lines ~6840-6895): set `a` and `z` `ready` before the takes
  that expect their branch (checks 4 and 2). The rest is unchanged, including the `base:` line
  checks, which now prove section 2's `_landed_line` recompute.
- Line ~6606 ("starts on the nearest earlier CR with a PR (here the top of the ready part)"): `three`
  is ready, so the expectation holds. Reword the label to "the nearest earlier CR handed back ready
  with a PR".
- `scenario/README.md` (line ~162, "a working one too"): "a ready one only; a working or blocked one
  gives the default branch".

### 6. Tests (`skills/chantier/scripts/cli/tests/`)

- No new test file: the start base is batch workflow, which belongs to `just scenario`. Fix any test
  that asserts a stack start on a non-ready CR (grep `start_on_for`, `stack_start`, `start_base`
  with `"stack"`). `test_hold_live_shared.py`'s series case is unaffected.

## Overlaps in batch-30 (running)

- **CR-442 `stack-git-chain`** (queued): edits `stacks.py` (`stack_base`, `stack_start` and
  `start_base` gain or pass `landed`) and checks "a CR taken onto another CR's branch" through
  `_live_start`. A CR with no live `start_on` stays unchecked. This agrees with Q2: a CR taken on
  the default branch is never checked against a CR below. Under B, fewer CRs are taken onto another
  CR's branch. Text conflict in `stacks.py` and `concepts.md`: whichever merges second rebases
  onto the other and keeps both rules.
- **CR-438 `stack-shape-guard`** (working): moves `foreman.md`'s stack rules verbatim into
  `foreman-stack.md` and adds `shape_line` beside `stack_due` in `stacks.py`. Section 4's Foreman
  edit lands in whichever file holds "The first take" at rebase. `stack_due`/`forming` (two CRs
  ready with a PR) are not changed here.
- **CR-430 `park-live-cr`, CR-431 `hold-live-cr`** (merged): `leave_stack_starts` unsets `start_on`
  ("starts on the default branch"). Q2 makes the printed base agree. No code conflict.
- **CR-443 `gate-hold-narrowing`, CR-436 `sync-blocked-by-others`** (queued, ready): touch
  `commands/driver.py` and `commands/facts.py` in other functions (the stack driver's `lease:`
  line, the sync callers). File-level only.
- `commands/forge_base.py`: no batch-30 CR touches it, and this CR does not either. CR-428
  (`drop-to-next-batch`): no overlap.

## Out of scope

- Parallel and series batches, the release's base (the top CR, take-base-from-forge Q9), a fix
  CR's base, and the `after` rule.
- The first take's threshold (two CRs ready with a PR), the in-batch runs, the final-order take and
  the Ordering rule: stack-Q4 as shipped. Under B, the stack still forms bottom-up. Once one CR is
  ready, the next CR taken starts on it.
- A CR's start base after its first take: no re-basing by `take --note`. A CR whose start owner goes
  back to a Driver (a new round) after the take keeps its base. The stack driver places it.
- A recursive check that the start candidate's own base is all ready (Q3's note).
- Any forge read in `take`; `forge-stack` commands; the board and the CR pane (no `STATUS.json`
  field changes, so no screenshot is owed).

## Evidence

- `just check` green (Linux, macOS, Windows).
- `just eval-dry-run` in the worktree (a change under the CLI's `src/`), before the first push.
- `just scenario` green with section 5's checks: the pipeline's `just scenario (ubuntu-latest)` at
  the PR's head, and locally on Windows (`chantier gate`) when this CR is on top of its batch's
  stack.
- `just test` within its budget (no new test file).
- No change to `hooks/` or `types/`, so no `just mod`. There is no host or default-configuration
  dependency, so there is no matrix.

## Open questions

**take-draft-Q1: in a stack batch, may a new CR start on an earlier CR that is still working with
a draft PR?**

- **B (recommended): only on a CR handed back ready.** `take` starts a new CR on the nearest
  earlier CR with a PR when that CR is `ready`. Otherwise (`working` or `blocked`) it starts the CR
  on the default branch. Why: the code under a new CR is code a Verifier has passed, so no rebase
  is owed at each round of the lower CR. That is the base Studio's Foreman chose by hand and the
  retro asked for. stack-Q4's goals hold: one linear stack set at the batch's end, never a branch
  with no PR. Once `carry-by-patch-id` is in, the final-order take's clean moves cost no new gate.
  Real dependencies still go through `after`. Cost: CRs started in parallel on the default branch
  may conflict at the final-order take. A CR that needs a working CR's code must say so with
  `after`.
- **A: keep the rule (stack-Q4 as it stands).** The nearest earlier CR with a PR, whatever its
  state. Why: the user chose it four days ago. Each CR sees the code below it from the start, and
  conflicts appear early. Cost: CR-429's case recurs. A CR built on a lower CR is rebased at each of
  that CR's rounds. If the lower CR is blocked or cancelled, the upper one is moved to the default
  branch mid-work.
- **C: the Foreman names the base at the take** (`take <cr> --base <cr|default>`, checked by the
  CLI against the CRs with a PR). Why: the Foreman knows which CRs have rounds to come. Cost: one
  more judgment at every take, which compactions erode (`stack-shape-guard`'s problem).
  take-base-from-forge Q1 rejected a base passed by the Foreman as an unchecked claim, and the
  shape of the stack moves away from the CLI's rule.

**take-draft-Q2: is a CR taken on the default branch kept there until the stack driver places it?**
Recommended: yes (section 1). Today, `handoff` recomputes the base of such a CR and prints the
branch of a CR below it that got a PR later, while its worktree and PR are on the default branch.
Under B, this happens each time a lower CR turns ready. No: the printed base keeps following the
record, as today. This question stands under A too.

**take-draft-Q3: when the nearest earlier CR with a PR is working but a CR below it is ready, does
the new CR start on the ready one or on the default branch?** Recommended: the default branch. The
walk stops at the first CR with a PR. Starting on the lower ready CR would make the working CR and
the new CR two branches on one base (a tree until the final-order take), and the new CR would miss
the working CR's changes anyway. The other answer: skip working and blocked CRs down to the nearest
ready one.
