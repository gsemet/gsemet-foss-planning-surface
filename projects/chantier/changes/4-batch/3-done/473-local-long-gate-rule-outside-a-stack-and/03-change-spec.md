# Local long gate by batch shape; ask the shape when a batch opens

Short name: `own-gate`. Destination: the running batch batch-31 (own-gate-Q3).
Repository: `C:/Users/gaeta/Projets/chantier`. This change edits AGENTS.md, the cards
(`skills/chantier/references/`) and the docs that say a batch is parallel by default. It changes
no CLI code, no test and no scenario.

## Goal

The user, 2026-11-23: "I should have told you to run in stack mode." In batch-31, which ran
parallel, CR-467/468/469/470 were handed back `--no-gate` under the AGENTS.md rule that only the
stack's top owes the local Windows long gate. A parallel batch has no stack. Each of its PRs lands
alone on main, so that exemption never applied there. The fix:

1. The local long gate depends on the batch's shape, and AGENTS.md and the cards say so for
   parallel, series and stack.
2. When a batch opens, the Chief of Staff asks the user for the shape and gives its
   recommendation, drawn from the overlap of the CRs' files. Parallel is no longer taken by
   default.

## Decisions carried (02-answers.md)

- **own-gate-Q1 (A):** in a parallel batch, each PR passes the local long gate before it is
  called ready to merge, because each lands alone on main. The exemption "owed by the stack's top
  only" applies to a stack batch only. AGENTS.md and the cards say this for parallel, series and
  stack.
- **own-gate-Q2 (A):** the Chief of Staff asks the user for the shape at the opening, with its
  recommendation drawn from the overlap of the CRs' files, and does not take parallel by default.
  `status` shows the shape. It already does: `batch_status.py` prints `shape <mode>` through
  `status/words.py`'s `shape_word`. No CLI change.
- **own-gate-Q3 (A):** grilled enough; specified for the running batch batch-31.
- **own-gate-Q4 (A):** each PR of a series batch owes the local run, as in parallel.
- **own-gate-Q5 (A):** a CR that the project's rules exempt from the long gate (in chantier,
  docs only or the eval kit only) owes no local run. This holds in parallel and series only
  (own-gate-Q8).
- **own-gate-Q6:** the local run fails while the user's board holds port 8765. The user's
  decision is a dynamic port: the port goes up by one until a free one is found. That is done in
  its own CR, `long-gate-webui-check-starts-a-second-bo`, widened to cover the dynamic port. This
  CR waits for it (`after`) so that each PR's local run can pass (see "Order in batch-31" and
  "Evidence").
- **own-gate-Q7 (A):** when a project's rule gives a rule per shape, the cards follow it. Only
  when the rule names the stack's top alone do the cards apply the reading "each covered CR
  outside a stack".
- **own-gate-Q8 (A):** a docs-only CR on top of a stack still owes the local run. Q5's exemption
  applies to parallel and series only.
- **own-gate-Q9 (A):** no Windows run covers the merged result, and that is accepted. Each PR's
  run is enough, carried over clean rebases as `ship`'s carry already proves. The merged result
  is left to the CI ubuntu job. The cards add no Windows run after a merge.

## What changes

### 1. `AGENTS.md` (root of the chantier repository)

Replace the "Windows coverage" sentences of the long-gate bullet (today: "Windows coverage: in
each batch, the CR on top of the stack also passes the long gate `scenario` locally (`chantier
gate <cr> scenario`) at its head before the user merges; when a CR joins on top, the local run
moves to it.") with a rule that names the shape:

> Windows coverage: before a PR is called ready to merge, it also passes the long gate `scenario`
> locally (`chantier gate <cr> scenario`) at its head. In a parallel or series batch each PR the
> long gate covers owes this run, since each lands alone on main (a docs-only or eval-kit-only
> PR owes none). In a stack batch only the CR on top of the stack owes it, a docs-only top
> included, and when a CR joins on top the run moves to it. No Windows run covers the merged
> result; that is left to the pipeline's ubuntu job.

The wording may be tightened, but it must keep each of these:

- each covered PR in parallel and in series;
- the stack's top only in a stack, a docs-only top included;
- the run moving to a CR that joins on top;
- no run on the merged result.

Edit nothing else in AGENTS.md.

### 2. The cards: the project's rule, read by shape

All four cards today speak of "a rule that asks the stack's top (or the top) for a local run".
For a batch with no stack, they also define a "batch's top": the last open non-release CR, or the
last of the ready ones in `status`'s order. That top owes the run while the other CRs hand back
`--no-gate`. That definition caused the batch-31 error. Replace it everywhere with the reading
below. State it once, in `driver.md`'s long-gate bullet ("Means: carries, conflicts and the
early push", the paragraph that begins "A rule that also asks the stack's top for a local run"),
and refer to it from the other cards.

- **A rule that names each shape (own-gate-Q7):** follow it as written. Chantier's new AGENTS.md
  rule is this case.
- **A rule that names the stack's top alone (own-gate-Q7):** read it by shape:
  - **Stack batch:** the stack's top owes the run, including a top the rules exempt from the
    long gate, such as docs only (own-gate-Q8). This is unchanged otherwise. The stack driver
    keeps its local gate at the mergeable top (`driver.md`, "The local gate at the mergeable
    top"), and `foreman-stack.md`'s clause on partial asks stays.
  - **Parallel or series batch (own-gate-Q1, Q4):** each CR the long gate covers runs the local
    gate at the pushed head it hands back ready. It runs it before the PR turns out of draft,
    unless a pass or a carried pass (`ship`'s `carried:` line) is already at that head, and it
    hands back with no `--no-gate`.
- **Under either form, in a parallel or series batch:**
  - A rule that names a pipeline job as the long gate is still checked as today. The local run
    is in addition to that job, not instead of it.
  - A fix CR counts like any CR.
  - A Release driver runs no local gate for this rule, as today.
  - A CR the project's rules exempt from the long gate owes no local run (own-gate-Q5).
  - A CR covered by a waiver (`order waive`) still owes the local run unless the waiver's words
    name that gate. This is the rule that applies to the top today, extended to each CR.
- **The `take` note:** in a parallel or series batch, `long gate: this CR runs <command>
  locally`, alone or after `rebase: <merged cr> merged; ` in the same note. In a stack, it stays
  `long gate: the stack's top runs <command> locally`. Remove the note `long gate: the batch's
  top runs <command> locally` from every card.
- **The ask clause:** in a parallel or series batch, the `ready-to-merge` and `pr-in-draft` asks
  of each CR that owes the run carry `local gate <cr> at <sha7>: passed|failed|not run`, not only
  the top's ask. The format of `foreman.md`'s `asks` line list does not change.
- **No run after a merge (own-gate-Q9):** no card asks a Windows run on the merged result.

Card by card. Line numbers are as of `b4cb7066`; see "Order in batch-31" below.

- **`skills/chantier/references/driver.md`**
  - Line ~217, the pointer "A rule that asks the batch's or the stack's top for a local run":
    change it to "A rule that asks a local run (by shape)".
  - Lines ~540-556: replace the "batch's top" definition and its `status` read with the reading
    above. Keep four points from the current paragraph:
    - the run comes before the PR turns out of draft;
    - a take note asks the run at the rebased head;
    - a failure is a round;
    - the Release driver runs none.
  - Line ~293 ("a waived CR, or the stack's top") and lines ~638-645 (a waived top still runs the
    gate): change the wording to "a waived CR that owes the local run".
  - The stack driver's section (lines ~1171-1410): the meaning does not change. Remove any
    "batch's top" wording, and add a line saying that a docs-only top still runs the gate
    (own-gate-Q8).
- **`skills/chantier/references/foreman.md`**
  - "The user's boundaries", lines ~107-161:
    - The `--no-gate` check stays.
    - Replace the paragraph "In a batch with no stack on the forge, the top is …", together with
      its two moments (each ready hand-back, and when a CR becomes the top later), by this: in a
      parallel or series batch, a CR that owes the run goes back with `take <cr> --note "long
      gate: this CR runs <command> locally"`, with no ask, when it is handed back ready with
      `--no-gate`, or when its record holds no passed or carried long gate at its head (`log
      <cr>`). An exempt CR, checked as the `--no-gate` check already does, does not go back.
    - The `order add` and "top moves" sentences go.
    - The `deliver by <time>` rule stays and now covers each CR's ask: the clause says `not run`
      or `failed`, and the CR is not sent back.
    - The clause on asks stays.
    - The waiver paragraph (lines ~152-161) stays. Where it says "a waived top (the stack's top,
      or the batch's top as above)", it now says "a CR that owes the local run", with the note
      text chosen by shape.
    - In a stack, the top handed back `--no-gate` by a docs-only exemption still goes back with
      the stack's-top note (own-gate-Q8).
  - "`order merged`", lines ~494-503 (the parallel and series rebase `take`): when the CR owes the
    run and holds no passed or carried long gate at its new head, the rebase take carries the
    gate note: `rebase: <merged cr> merged; long gate: this CR runs <command> locally`. This
    applies to any such CR, not only to the one that is "now the batch's top". There is still no
    separate gate `take`.
  - Line ~466, the `asks` line list: no change in format.
- **`skills/chantier/references/foreman-stack.md`**
  - Line ~94: change "In a batch with no stack, the same order note sends the batch's top's ask …"
    to "In a parallel or series batch, the same order note sends the ask of each CR that owes the
    run as it stands at the time, with its local-gate clause …".
  - Lines ~115-131 (the clause of the stack's partial ask): unchanged.
- **`skills/chantier/references/chief-of-staff.md`**
  - "The floor", "The gates" (lines ~1038-1044): under a rule that asks a local run, every CR of a
    parallel or series batch that owes the run counts, and the stack's top counts once in a
    stack. This replaces "the batch's top (or the stack's top) counts, once".
  - The plain-ask bullet, lines ~1237-1242 ("In a project whose rules ask the stack's top for a
    local run, the ask of a batch's top with no stack carries …"): this now applies to the ask of
    each CR that owes the run, in a parallel or series batch. Quote the clause the same way.
  - Line ~1253: remove the exception "except that, under that rule, once the last open
    non-release CRs are all ready together and the last of them in `status`'s order is the
    batch's top, offer the others as mergeable only together with that top or before it".
  - Line ~1268: remove "and the batch's top last". The rule on recording several merges at once
    stays.
  - Line ~1322 (the stack's partial ask): no change.

After the edit, `grep -rn "batch's top"` over `skills/chantier/references/` finds nothing. Past
release notes in `docs/release-notes/` stay as they are, since they are history.

### 3. The batch shape at the opening (`chief-of-staff.md`, `concepts.md`)

- Line ~718, "A batch is parallel unless the user asks for a series or a stack, or a selected CR
  depends on another …": replace it. The Chief of Staff asks the user for the shape at every
  opening, in step 2 "Show the plan", with the other plan items, and never takes parallel by
  default. The rest of that paragraph stays:
  - in parallel, a CR starts as soon as a slot is free;
  - touching the same file is not a dependency;
  - `depends.json` is only for a real need.
- Step 2, "Show the plan" (line ~880, the item "mode (parallel unless …)"): the mode becomes a
  question in the format of "Asking the user: a series". It is a batch question, so it carries no
  `<short name>-Q<n>` reference. It offers parallel, series (with the order) and stack, and marks
  the Chief of Staff's recommendation `(recommended)`. The recommendation weighs three things:
  - whether the CRs are linked: a CR's `depends.json`, or one CR building on another's change;
  - the overlap of the files their `03-change-spec.md` names: CRs that edit the same files, or
    are linked, point to a stack; independent CRs with disjoint files point to parallel;
  - the cost of the project's local-gate rule by shape: a parallel or series batch runs it once
    per covered PR, a stack once on its top. The floor's "gates" term shows this.

  The question names the shared files behind the recommendation, as the plan already names a
  wait on the same lines. An empty batch (a go before any CR is ready) is asked the shape too. A
  word the user gave earlier (for instance "run the P1s as a stack") answers the question, and
  none is asked.
- The Chief of Staff always passes `open --mode` with the user's answer. `status`'s `shape <mode>`
  line shows it, as today. `order mode --note …` still switches the shape on the user's word
  during the batch. In the "Starting a batch" routing row (line ~26), the words about the
  steering mode stay as they are.
- `concepts.md` line ~233 says "**Parallel** (the default, when the user names none)". That
  describes the CLI default of `open`, which stays. Add "the Chief of Staff always asks the user
  and passes `--mode`".

### 4. The docs that say parallel is the default and there is nothing to ask

In each of these lines, keep the fact that `open`'s default stays parallel, and add a clause that
the Chief of Staff asks the user for the shape at the opening, with its recommendation:

- `README.md:98`: "**Parallel** (the default; ask for nothing)". "ask for nothing" goes.
- `CONTRIBUTING.md:23`: "the CRs run in parallel unless you ask for a series or a stack".
- `docs/use-cases-foreman.md:32`: "Parallel is the default: no flag, no word."
- `docs/use-cases-direct.md:57`: "(the default)".
- `docs/batch-modes-texts.md:3`: "Parallel, the default: …".
- `docs/planning-folder.md:39`: "(parallel unless you ask otherwise)".

The Driver searches the docs for other such lines ("parallel is the default", "the default",
"unless you ask") and fixes any it finds the same way, naming each in the PR body. Where a doc
describes the local gate per batch, it follows section 1. `docs/gates.md` does not describe the
top's local run today and stays as it is.

### Order in batch-31

- **After the port CR (own-gate-Q6):** this CR waits (`after`) for
  `long-gate-webui-check-starts-a-second-bo`. That CR adds the dynamic port, so that the local
  `scenario` run passes while the user's board holds 8765. Its folder name goes in this CR's
  `depends.json` (`{"after": ["long-gate-webui-check-starts-a-second-bo"]}`) when the Chief of
  Staff adds it to the batch. This CR's branch starts after that CR is ready, and it rebases on
  the port CR's merge.
- **Before CR-471:** this CR lands before CR-471 (`slim-cards`). CR-471 then cuts the cards on
  this CR's head, as CR-471's own specification says. This CR works on the cards as they are, so
  the line numbers above hold up to CR-466's edits.
- **CR-466** (`own-branch-push`, in `2-actives`) touches `chief-of-staff.md` and `driver.md`
  too. This CR rebases on it if it merges first. The Driver finds each place by its words
  (`batch's top`, `top for a local run`, `stack's top for a local run`, `local gate`, `parallel
  unless`). The line numbers are hints only.

## Out of scope

- No CLI change. `open`'s default `--mode parallel`, `status`'s shape line, `gate`, `handback`,
  `take`, `order waive` and `stacks.py` stay as they are. The CLI does not know of the local-gate
  rule.
- The dynamic port, which belongs to `long-gate-webui-check-starts-a-second-bo`.
- No change to `agents/` or `com.github.copilot/agents/`; the agent files only name their card.
- No change to the stack driver's mergeable-top gate, the stack waiver (`order waive stack`) or
  the Release driver's exemption.
- No Windows run on the merged result (own-gate-Q9).
- What to do with batch-31's merged CRs 467-470, whose Windows run never happened, is for the
  Chief of Staff to settle with the user, not for this CR.
- Past release notes.

## Evidence

- `just check` passes in the worktree at the pushed head. It runs the card tests, which read the
  shipped cards and the startup manifest from the repository at that head.
- These commands read the shipped files at the head:
  - `grep -rn "batch's top" skills/chantier/references/` prints nothing;
  - `grep -n "Windows coverage" AGENTS.md` shows the rule by shape;
  - `grep -n -i "ask for nothing\|no flag, no word" README.md docs/` prints nothing.

  The PR's Deliverables quote these outputs.
- A reading proof in the PR body, one line per case. These are cards only, with no host or
  default dependency besides the shape:
  - parallel: each covered CR runs `chantier gate <cr> scenario` before its ready hand-back and
    hands back with no `--no-gate`. An exempt CR owes none. The Foreman sends a covered CR's
    `--no-gate` hand-back back with `long gate: this CR runs <command> locally`.
  - series: the same, and the rebase `take` after a predecessor's merge carries the note when
    there is no pass or carry at the new head.
  - stack: the stack's top runs it, a docs-only top included. The mergeable-top rule is
    unchanged.
  - a project rule that names each shape: followed as written. A rule that names the stack's top
    alone: the reading by shape.
  - opening: the plan asks parallel, series or stack with a recommendation, and names the shared
    files. The docs say the same, and say that `open`'s default stays parallel.
- The long gate: a cards change passes the pipeline's `just scenario (ubuntu-latest)` job at the
  PR's head, as AGENTS.md requires. Under this CR's own rule, in parallel batch-31 this PR also
  passes `chantier gate <cr> scenario` locally at its head before it is called ready to merge.
  That run can pass only once the port CR `long-gate-webui-check-starts-a-second-bo` is in this
  CR's base (own-gate-Q6). Until then, a local run that fails on port 8765 is that CR's known
  cause and does not count as a pass.
- No `just eval-dry-run` is owed, since nothing changes under the CLI's `src/` or `evals/kit/`.
  No `just mod` is owed, since nothing changes under `hooks/` or `types/`.
