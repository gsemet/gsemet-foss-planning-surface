# Local long gate by batch shape; ask the shape when a batch opens

Short name: `own-gate`. Destination: batch-31. Repository: `C:/Users/gaeta/Projets/chantier`.
This change touches only AGENTS.md and the cards (`skills/chantier/references/`). It changes no CLI code, no test and no scenario.

## Goal

The user, 2026-11-23: "I should have told you to run in stack mode." In batch-31, which ran
parallel, CR-467/468/469/470 were handed back `--no-gate` under the AGENTS.md rule that only the
stack's top owes the local Windows long gate. A parallel batch has no stack. Each of its PRs lands
alone on main, so that exemption never applied there. The fix:

1. The local long gate depends on the batch's shape, and AGENTS.md and the cards say so for each
   shape: parallel, series and stack (own-gate-Q1).
2. At a batch's opening, the Chief of Staff asks the user for the shape and gives its
   recommendation, drawn from the overlap of the CRs' files. Parallel is no longer taken by
   default (own-gate-Q2).

## Decisions carried (02-answers.md)

- **own-gate-Q1 (A):** in a parallel batch, each PR passes the local long gate before it is
  called ready to merge, because each lands alone on main. The exemption "owed by the stack's top
  only" applies to a stack batch only. AGENTS.md and the cards say this for parallel, series and
  stack.
- **own-gate-Q2 (A):** the Chief of Staff asks the user for the shape at the opening, with its
  recommendation drawn from the overlap of the CRs' files, and does not take parallel by default.
  `status` shows the shape. It already does: `batch_status.py` prints `shape <mode>` through
  `status/words.py`'s `shape_word`. No CLI change.

The series case follows from the same reason as parallel: a series PR merges alone on main, one
by one from the bottom (`concepts.md`, "Series"). This specification therefore treats a series
like a parallel batch (each PR owes the run). Open question 1 asks the user to confirm this.

## What changes

### 1. `AGENTS.md` (root of the chantier repository)

Replace the "Windows coverage" sentences of the long-gate bullet (today: "Windows coverage: in
each batch, the CR on top of the stack also passes the long gate `scenario` locally (`chantier
gate <cr> scenario`) at its head before the user merges; when a CR joins on top, the local run
moves to it.") with a rule that names the shape:

> Windows coverage: a PR the long gate covers also passes the long gate `scenario` locally
> (`chantier gate <cr> scenario`) at its head before it is called ready to merge. In a parallel
> or series batch, each such PR owes this run, since each lands alone on main. In a stack batch,
> only the CR on top of the stack owes it, and when a CR joins on top the run moves to it.

The wording may be tightened, but it must keep three things: the run per PR in parallel and in
series, the stack's top only in a stack, and the run moving to a CR that joins on top. Edit
nothing else in AGENTS.md.

### 2. The cards: one reading of such a rule, by shape

All four cards today speak of "a rule that asks the stack's top (or the top) for a local run".
For a batch with no stack, they also define a "batch's top": the last open non-release CR, or the
last of the ready ones in `status`'s order. That top owes the run while the other CRs hand back
`--no-gate`. That definition caused the batch-31 error. Replace it everywhere with this one
reading, stated once in `driver.md`'s long-gate bullet ("Means: carries, conflicts and the early
push", the paragraph that begins "A rule that also asks the stack's top for a local run") and
referred to from the other cards:

- **Stack batch:** unchanged. The stack's top owes the run. The stack driver keeps its local gate
  at the mergeable top (`driver.md`, "The local gate at the mergeable top"), and
  `foreman-stack.md`'s clause on partial asks stays.
- **Parallel or series batch:** each CR the rule covers runs the local gate at the pushed head it
  hands back ready. It runs it before the PR turns out of draft, unless a pass or a carried pass
  (`ship`'s `carried:` line) is already at that head, and it hands back with no `--no-gate`. A
  rule that names a pipeline job as the long gate is still checked as today. The local run is in
  addition to that job, not instead of it. A fix CR counts as any CR. A Release driver still runs
  no local gate for this rule, as today. A CR the project's rules exempt from the long gate (for
  instance docs only) owes no local run; see open question 2. A CR covered by a waiver (`order
  waive`) still owes the local run unless the waiver's words name that gate. This is the rule
  that applies to the top today, extended to each CR.
- **The `take` note:** in a parallel or series batch, `long gate: this CR runs <command>
  locally` (alone, or after `rebase: <merged cr> merged; ` in the same note). In a stack, it
  stays `long gate: the stack's top runs <command> locally`. Remove the note `long gate: the
  batch's top runs <command> locally` from every card.
- **The ask clause:** in a parallel or series batch, each covered CR's `ready-to-merge` and
  `pr-in-draft` ask carries `local gate <cr> at <sha7>: passed|failed|not run`, not only the
  top's ask. The format of `foreman.md`'s `asks` line list does not change.

Card by card (line numbers as of `b4cb7066`; see "Rebase on batch-31's siblings" below):

- **`skills/chantier/references/driver.md`**
  - Line ~217, the pointer "A rule that asks the batch's or the stack's top for a local run":
    reword it to "A rule that asks a local run (each CR outside a stack, the stack's top in one)".
  - Lines ~540-556: replace the "batch's top" definition and its `status` read with the
    per-shape reading above. The paragraph keeps four points: the run happens before the PR
    turns out of draft, after the take note's rebased head, a failure is a round, and the Release
    driver runs none.
  - Line ~293 ("a waived CR, or the stack's top") and lines ~638-645 (a waived top still runs the
    gate): say "a waived CR that owes the local run (each CR outside a stack, the stack's top in
    one)".
  - The stack driver's section (lines ~1171-1410: "The local gate at the mergeable top" and the
    lines after it): no change in meaning. Only remove any "batch's top" wording found there.
- **`skills/chantier/references/foreman.md`**
  - "The user's boundaries", lines ~107-161. Keep the `--no-gate` check. Replace the paragraph
    "In a batch with no stack on the forge, the top is …", with its two moments (each ready
    hand-back, and when a CR becomes the top later), by this: in a parallel or series batch, each
    covered CR handed back ready with `--no-gate`, or whose record holds no passed or carried
    long gate at its head (`log <cr>`), goes back with `take <cr> --note "long gate: this CR runs
    <command> locally"`, with no ask. The `order add` and "top moves" sentences go. Keep the
    `deliver by <time>` rule, for each CR's ask (`not run`/`failed`, not sent back). Keep the
    clause on asks. Keep the waiver paragraph (lines ~152-161), reworded to cover "a CR that owes
    the local run" in place of "a waived top (the stack's top, or the batch's top as above)",
    with the note text by shape.
  - "`order merged`", lines ~494-503 (parallel and series rebase `take`): the rebase take
    carries the gate note (`rebase: <merged cr> merged; long gate: this CR runs <command>
    locally`) when the CR holds no passed or carried long gate at its new head. This applies to
    any CR, not only "now the batch's top". There is still no separate gate `take`.
  - Line ~466, the `asks` line list: no change in format.
- **`skills/chantier/references/foreman-stack.md`**
  - Line ~94: "In a batch with no stack, the same order note sends the batch's top's ask …"
    becomes "In a parallel or series batch, the same order note sends each covered CR's ask as it
    stands at the time, with its local-gate clause …". Lines ~115-131 (the stack's partial ask
    clause) do not change.
- **`skills/chantier/references/chief-of-staff.md`**
  - "The floor", "The gates" (lines ~1038-1044): under a rule that asks a local run, every
    covered CR of a parallel or series batch counts, and the stack's top counts once in a stack.
    This replaces "the batch's top (or the stack's top) counts, once".
  - The plain-ask bullet, lines ~1237-1242 ("In a project whose rules ask the stack's top for a
    local run, the ask of a batch's top with no stack carries …"): this now applies to each
    covered CR's ask in a parallel or series batch. Quote the clause the same way.
  - Line ~1253: remove the exception "except that, under that rule, once the last open
    non-release CRs are all ready together and the last of them in `status`'s order is the
    batch's top, offer the others as mergeable only together with that top or before it". Each
    PR has passed its own run.
  - Line ~1268: remove "and the batch's top last" from the rule on recording several merges at
    once. The rule itself stays: `order merged` for each.
  - Line ~1322 (the stack's partial ask): no change.

After the edit, `grep -n "batch's top"` over `skills/chantier/references/` finds nothing. The
release notes in `docs/release-notes/` stay as they are, since they are history.

### 3. The batch shape at opening (`chief-of-staff.md`)

- Line ~718, "A batch is parallel unless the user asks for a series or a stack, or a selected CR
  depends on another …": replace it. The Chief of Staff asks the user for the shape at every
  opening, in step 2 "Show the plan", with the other plan items. It never takes parallel by
  default. The rest of that paragraph stays: in parallel a CR starts as soon as a slot is free,
  touching the same file is no dependency, and `depends.json` is only for a real need.
- Step 2, "Show the plan" (line ~880, the "mode (parallel unless …)" item): the mode becomes a
  question in the "Asking the user: a series" format (`<short name>-Q<n>` is not needed: it is a
  batch question, not a CR's). It offers parallel, series (with the order) and stack, and marks
  the Chief of Staff's recommendation `(recommended)`. The recommendation comes from:
  - whether the CRs are linked (a CR's `depends.json`, or one building on another's change);
  - the overlap of the files their specifications name (`03-change-spec.md`): CRs that edit the
    same files, or are linked, point to a stack; independent CRs with disjoint files point to
    parallel;
  - the cost of the project's local-gate rule by shape: a parallel or series batch runs it once
    per covered PR, a stack once on its top. The floor's "gates" term shows this.
  The question names the shared files behind the recommendation, as the plan already names a
  wait on the same lines. An empty batch (a go before any CR is ready) asks the shape too. A
  user's word given earlier (for instance "run the P1s as a stack") answers it, with no question.
- `open --mode` is then always passed with the user's answer. `status`'s `shape <mode>` line
  shows it, as today. `order mode --note …` still switches shape on the user's word during the
  batch. In the "Starting a batch" routing row (line ~26), only the steering-mode words stay as
  they are.
- `concepts.md` line ~233 ("**Parallel** (the default, when the user names none)") describes the
  CLI's default of `open`, which this change keeps. Add "the Chief of Staff always asks the user
  and passes `--mode`" so the card and concepts agree.

### Rebase on batch-31's siblings

CR-466 (`own-branch-push`, in `2-actives`) and CR-471 (`slim-cards`, in `1-pending`) touch the
same cards. CR-471 moves rules of `chief-of-staff.md`, `foreman.md` and `driver.md` into pieces
read by `startup-manifest.json` actions. This CR rebases on whichever of them lands first. After
the rebase, the Driver finds each place by its words (`batch's top`, `top for a local run`,
`stack's top for a local run`, `local gate`, `parallel unless`), wherever CR-471 put it. The line
numbers above are hints only. A conflict with CR-471 is resolved by keeping CR-471's file split
and applying this CR's meaning in the piece where the rule now lives.

## Out of scope

- No CLI change. `open`'s default `--mode parallel`, `status`'s shape line, `gate`, `handback`,
  `take`, `order waive` and `stacks.py` stay as they are. The CLI does not know of the local-gate
  rule.
- No change to `agents/` or `com.github.copilot/agents/` (the agent files only name their card).
- No change to the stack's top rule, the stack driver's mergeable-top gate, the stack waiver
  (`order waive stack`), or the Release driver's exemption.
- `docs/gates.md` does not describe the top's local run today and stays as it is. Past release
  notes stay as they are.
- What to do with batch-31's merged CRs 467-470, whose Windows run never happened, is the Chief
  of Staff's call with the user. It is not this CR's.

## Evidence

- `just check` passes in the worktree at the pushed head. It covers the card tests that read the
  shipped cards and the startup manifest from the repository at that head.
- The repository's shipped cards and AGENTS.md at the head: `grep -rn "batch's top"
  skills/chantier/references/` prints nothing. `grep -n "Windows coverage" AGENTS.md` shows the
  per-shape rule. The PR's Deliverables quote both outputs.
- A reading proof in the PR body, one line per cell (cards only, with no host or default
  dependency beyond the shape):
  - parallel: each covered CR runs `chantier gate <cr> scenario` before its ready hand-back and
    hands back with no `--no-gate`. The Foreman sends a `--no-gate` hand-back back with `long
    gate: this CR runs <command> locally`.
  - series: the same, and the rebase `take` after a predecessor's merge carries the note when
    there is no pass or carry at the new head.
  - stack: unchanged (the stack's top, and the mergeable top).
  - opening: the plan asks parallel/series/stack with a recommendation, and names the shared
    files.
- The long gate: a cards change passes the pipeline's `just scenario (ubuntu-latest)` job at the
  PR's head (AGENTS.md). Under this CR's own rule, in a parallel batch-31 this PR also passes
  `chantier gate <cr> scenario` locally at its head before it is called ready to merge.
- No `just eval-dry-run` is owed (nothing under the CLI's `src/` or `evals/kit/`). No `just mod`
  is owed (no `hooks/` or `types/`).

## Open questions

1. **Series:** in a series batch, does each PR owe the local run, as in parallel (each merges
   alone on main, one by one), or none? This specification takes "each PR", from the reason the
   user gave in own-gate-Q1.
2. **Exempt CRs outside a stack:** the rule's "each PR" in a parallel or series batch, does it
   include a CR that the project's rules exempt from the long gate (in chantier, a docs-only or
   eval-kit-only change)? Today the batch's top owes the run "whatever its exemption". This
   specification takes "no": an exempt CR owes no local run, because no other CR relies on its
   run.
