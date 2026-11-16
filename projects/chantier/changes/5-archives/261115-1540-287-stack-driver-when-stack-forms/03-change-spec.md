# Change Specification: the stack driver starts when the stack can form

Short name: `stack-forms`. No issue (origin: verbal, from the study of batch-18's real eval runs
of 2026-11-15; real-foreman run 2, stack mode).

## Goal

In a stack batch the forge stack is made **once**, by the first stack driver, at the moment the
stack can form, and the CRs started after that moment are built on the stack instead of on the
default branch and restacked later. In run 2 the CRs were built on `main`, the first
`forge-stack create` was refused by GitHub (HTTP 422), and the batch ran 2 stack drivers, 6 CR
Drivers for 5 CRs and 3 conflict resolvers for what one take should have done.

## What happened (the evidence)

Workspace `C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15`, batch-01, stack,
5 CRs, 3 slots. Sources: the audit
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`, the batch's retro
(`.agents/changes/5-archives/batches/batch-01.md`, points 32 and 33), and the stack drivers'
transcripts (agents `a8ab6e04f1`, first take, and `a5f5cf3e45`, second take).

1. CR-101, CR-102 and CR-103 started at once on `main` (as `start_base` in `stacks.py` says
   today: "with none open, the default branch, whatever its place in a stack"). CR-104 and
   CR-105 started later, when slots freed, also on `main`, although CR-102 and CR-103 were already
   handed back `ready` with their PRs.
2. First `take stack` at 10:59:08Z, once CR-102 and CR-103 were `ready` (the Foreman's rule "as
   soon as two CRs are handed back `ready` with a PR"). The stack driver rebased CR-102 onto
   CR-101 (a conflict, a `conflict-resolver`, an `inspector`, a `verifier`) and CR-103 onto CR-102.
   Meanwhile CR-104 and CR-105 opened draft PRs on `main`.
3. `forge-stack create` (11:03:34Z) sent the five PRs to `POST repos/<o>/<r>/stacks` and the forge
   answered: `Pull requests must form a stack, where each PR's base ref is the previous PR's head
   ref (HTTP 422)`. Two causes, both in chantier:
   - `create` sends the PRs as they are on the forge and retargets none (only `rebuild`
     retargets, in `forge_stack.py` `_rebuild()` via `forge_stack_gh.retarget()`). The stack
     driver had rebased CR-102 and CR-103 onto the CR below, but their PRs' bases on the forge
     were still `main`, and the card forbids a retarget by hand. So `create` could not succeed on
     any PR the stack driver had moved.
   - The plan (`_plan()`) holds every bottom CR with a PR, a working one too: CR-104's and
     CR-105's PRs, on `main`, branches their Drivers' (the stack driver may not move them).
4. The stack driver handed back with no stack; the Foreman sent rebase notes to CR-104 and
   CR-105; both rebased (conflict resolvers on each, a CR-105 retake); a second stack driver ran
   `forge-stack rebuild` (11:13Z) and made the stack.

## What changes

### 1. Where a CR starts in a stack batch (CLI: `stacks.py`, `commands/driver.py` `take`)

**The moment the stack can form:** the record holds two CRs or more of the stack (the release and
a fix CR aside) handed back `ready` with a PR. This is the Foreman's first-take moment, unchanged
in its words, now named once in `concepts.md` and used by the CLI.

**The start base** (`start_base()`), in a stack batch, for a CR that is neither a release nor a fix
and has no open dependency (`after`):

- before the stack can form: the default branch, as today;
- from that moment: the branch of the **top of the stack's ready part**, that is, the highest CR in
  the stack's order (`chain()`), other than the CR itself, that is handed back `ready` with a PR.
  A CR started later joins on top of the stack, so it starts on the top of what is ready, wherever
  its own number sits in the record's order.

Unchanged: a CR with an open dependency starts on its last open dependency's branch; a release
starts on the top CR's branch; a fix CR on the default branch; the parallel and series rules.

**Recorded at the first take.** The start base moves as CRs become ready, so `take` computes it
once, when it takes a CR from `queued`, and records it on the CR (a new optional `CrEntry` field,
for instance `start_on`, the branch name; absent in older records, which keep today's behaviour).
`start_base()` then returns the recorded branch while the batch is a stack and the CR that owns
that branch is open (not merged, not cancelled); once that CR is merged or cancelled, or the batch
left the stack mode (`order mode`), the default branch, as today. A later `take` of the same CR
(a rebase, a round, a restart) does not change it.

Everything that reads `start_base()` follows without its own change: the `worktree: … base <ref>`
line of `take` and `handoff` (`facts.py` `_base_of()`), `stack_base()` for a CR not yet placed by
`stack`, the carry check of `handback ready` (`driver_checks.py` `_gate_missing()`), and the
board (`board/crs.py`). The Driver opens its PR on that base, as a draft (a PR on another CR's
branch is a draft: `concepts.md`, "Words").

### 2. The stack as it stands leaves out a working PR that is not on its place (CLI: `forge_stack.py` `_plan()`, `facts.py` `stack_lines()`)

A CR whose branch is its live Driver's (`working`) and whose PR's recorded base on the forge
(`pr_base`, as `ship` last read it) is not its place in the stack (`stack_base(…, planned=True)`)
is **not placed yet**: the stack driver may not move its branch, so it cannot sit in the stack.

- `_plan()` stops the stack as it stands at the first such CR, as it stops at the first CR with
  no PR today: it and the CRs above are "to come" (`_come()`), for `create`, `rebuild` and `show`.
  A working CR with no `pr_base` recorded is treated as placed (no forge read to doubt it).
- When it is the bottom CR, the refusal (`NoBottom`) names it: `no PR placed at the bottom of the
  stack: <cr> is working and its PR <link> is on <pr_base>, not on <planned base>` (exit 2, as
  today's `no PR at the bottom` refusal).
- `stack_lines()` (what `take stack` and `stack` print) ends that CR's row with
  `not on its place: its PR is on <pr_base>; to come until its Driver rebases (note rebase:
  stacked on <cr below>)`, so the Foreman sends the note from the take's own output.

A working CR placed by its start base (section 1) is on its place and is in the stack as a draft
on top, as today.

### 3. `forge-stack create` retargets before it creates (CLI: `forge_stack.py` `_create()`)

On GitHub, `create` retargets each PR of the plan whose base on the forge is not the record's
(the same `retarget(rows, where, done)` that `rebuild` runs), then posts the stack once, and
prints each retarget line (`#<n> base <old> -> <new>`) before the stack's line, as `rebuild`
does. With section 2 every PR of the plan is either moved by the stack driver or already on its
place, so a retarget never puts a PR on a base its branch does not hold. A refusal by the forge
keeps today's form: the exact text and `(forge-stack rebuild replaces a stack)`, with the
retargets already done listed first (as `rebuild` lists what it did). GitLab's `create` already
retargets: unchanged. `rebuild` and `show`: unchanged but for section 2.

### 4. Cards (`skills/chantier/references/`)

- `concepts.md`, **Batch modes**, the **Stack** paragraph (lines 179-184) and **Dependencies**
  (lines 263-265, "else on the default branch, in a stack too: a CR's start base and its place in
  the stack are two things"): every CR with no open dependency starts at once on the default
  branch **until the stack can form** (two CRs handed back `ready` with a PR); from then on a CR
  started starts on the top of the stack's ready part, recorded at its first take, so its PR is
  already on the stack. "Stack as it stands" (line 196): the bottom CRs with a PR **on its place**
  (a working CR's PR on another base is to come until its Driver rebases). The stack is made at
  the first stack take, once.
- `foreman.md`:
  - "A stack batch …" (lines 253-263), **The first take**: name it "the moment the stack can
    form" (the same condition), and say that from it `take` starts every new CR on the stack.
  - **A working CR placed on another** (lines 267-269): in the same turn as each `take stack`,
    for each row printed `not on its place`, send its Driver `[foreman→driver <cr>] note rebase:
    stacked on <cr below>` (the CR below as the row's `base` names it); never hold the take for
    it; it joins at a later take.
  - "Each later take": a working CR that rebased onto its place (its `ship` reads the new base)
    joins like a CR that got its first PR.
- `driver.md`:
  - **CR driver** (the base rule around lines 612-626): in a stack batch the `base` that `take`
    prints may be another CR's branch (the top of the stack's ready part): create the worktree on
    it, open the PR on it as a draft; that branch is the stack driver's, never rebased by you but
    on a note. A `note rebase: stacked on <cr below>` received while working: rebase onto that
    CR's branch (not the default branch), retarget your PR to it (`gh pr edit --base`, `glab mr
    update --target-branch`) while it is in no native stack, push with `--force-with-lease`,
    `ship`. Fix the sentence "one rebase, onto the latest default branch" so it holds for the
    default branch's notes only.
  - **Stack driver**: "Ordering" (lines 664-668): a row printed `not on its place` is not named
    in `stack` (it stays above, to come); a working CR already on its place stays right above the
    CR its PR sits on. "Who moves a branch" (lines 670-673): such a CR is to come until its
    Driver rebases; the Foreman sends the note. "Making the stack" (lines 697-707): `forge-stack
    create` retargets the PRs of the stack as it stands and creates the stack in one command (no
    retarget by hand, still); the first take ends with the stack made, whatever a working CR is
    doing.
- No agent file (`agents/`, `com.github.copilot/agents/`) changes: the contract lives in the
  cards.

### 5. Docs

- `docs/use-cases-foreman.md` (line 42, "each PR based on the default branch. The stack comes
  after: when every CR is handed back ready"): the CRs start on the default branch until two are
  handed back ready; the stack is made then, and the CRs started after are built on it.
- `docs/batch-modes-texts.md` (the Stack text) and `README.md` (line 104, "once every PR is
  handed back ready the stack driver makes one native stack"): the stack is made as soon as two
  PRs are handed back ready, and the CRs started afterwards are built on it. If
  `docs/batch-modes.svg` carries the same words, they change with the text.
- `scenario/README.md` (lines 142-147, "each started on the default branch, then stacked
  afterwards"): add the CR started on the top of the stack's ready part, the working PR left out
  of the stack as it stands, and `create` retargeting.

## Decisions carried from `02-answers.md`

- The request's scope stands as written: the stack driver starts, and Drivers base on the CR
  below, at the moment the stack can form, so the forge stack is created once.
- Planned for the next batch (parallel), before the next release.
- No behaviour question was left open by the user; implementation detail is the agents'. The
  reading of "the CR below" in section 1 is this specification's; see the open question.

## Out of scope

- The words a ready stacked CR reads and its hand-back line (`ready_word()`, `_ready_lines()`):
  the sibling CR `stacked-ready-line-names-cr` (it edits `stacks.py` too; a shared file is no
  dependency).
- The order the stack driver gives the ready CRs (readiness against the record's order) beyond
  the two rules of section 4.
- A CR with an open dependency, a release, a fix CR, the parallel and series modes.
- The `gh stack` extension route: whether the extension retargets is not known; the card's rule
  that a refused means is an `anomaly` stands.
- The merge of a stacked PR (`release-merge-native-stack`) and the eval kit
  (`eval-sandbox-restack-wait`, `eval-judge-follows-pr-head`).
- The cost of verifying after a clean restack (`clean-rebase-light-verify`).

## Evidence

A change to the CLI, the cards and the scenario: `just check` passes on Linux, macOS and Windows,
and the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head before its PR.
Not a change to `hooks/` or `types/`: no `just mod`. The CR pane's fields are unchanged (no new
`STATUS.json` field is shown), so no pane screenshot is due.

Scenario (`scenario/run_scenario.py`), kept inside the existing stack unit's world (the unit is
near its budget: `scenario-stack-unit-budget`); no new world:

1. `scenario/fake_gh.py`, `POST …/stacks`: answer, as GitHub did, `HTTP 422: Pull requests must
   form a stack, where each PR's base ref is the previous PR's head ref` when a PR's base is not
   the previous PR's branch (the first on the default branch). Every existing `create` check
   still passes.
2. In `stack_batch` (section 13): CRs taken before two are `ready` print `base origin/main` (the
   existing check). Once two are `ready` with a PR, a CR taken from `queued` prints `base <the top
   ready CR's branch>`; after a third CR becomes `ready`, `handoff` of that CR still prints the
   same base (recorded, not recomputed); after the top ready CR is cancelled or merged, it prints
   `base origin/main`.
3. In the `forge-stack` section (13a, GitHub): two ready PRs whose forge base is `main`, the
   second planned on the first's branch: `create` prints `#<n> base main -> <branch>` then
   `stack #… ` and exits 0, one POST to the stacks endpoint. Run 2's case: a working CR above
   them with a PR on `main` (`pr_base` recorded `main`, planned on the CR below): `create` stacks
   only the placed PRs, the working one is in `to come:` of `show`, `take stack`/`stack` print its
   row with `not on its place`, and no PATCH touches its PR. After its `ship` with the forge base
   on its place, `rebuild` stacks it as a draft on top.
4. The bottom CR working with its PR off its place: `create` and `rebuild` exit 2 naming it
   (`no PR placed at the bottom of the stack: <cr> is working …`).
5. A batch switched from stack to parallel (`test_mode_switch.py` area, or the existing mode
   switch step): a CR with a recorded start base reads `base origin/main` after the switch.

Tests (`skills/chantier/scripts/cli/tests/`): no new test is needed; if one is added, it is one
parametrized case of `start_base()` on a prepared record (before the stack can form, after, the
start CR merged), within the `just test` budget.

## Open questions for the user

1. **"The CR below" a CR started once the stack can form.** This specification starts it on the
   top of the stack's ready part: the highest CR handed back `ready` with a PR, whose branch only
   the stack driver moves. The other reading starts it on the CR right under it in the stack's
   order whatever that CR's state, a working one too: one fewer rebase when both turn out in that
   order, but the new CR then rides a branch its Driver still rewrites and cannot become ready to
   merge before it. Keep the top of the ready part?
2. **One ready CR.** Basing starts at two ready CRs (the moment the stack can form, as the request
   says). Starting on a single ready CR's branch would save a restack too, but ties the new CR to a
   PR the user may still merge alone before any stack exists (it then gets a rebase note). Keep
   two?
