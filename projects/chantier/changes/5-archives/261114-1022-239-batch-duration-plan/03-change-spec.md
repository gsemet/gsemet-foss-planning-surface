# Change Specification: no delivery time without the batch's floor

## Goal

The user (2026-11-14), after two nights without the promised stack: "je suis très déçu, tu n'as
pas fait ce qu'il fallait pour livrer une stack cette nuit. C'est la deuxième nuit que ça ne
marche pas." In batch-17 the Chief of Staff said "you should have a stack when you wake up" with
no figure behind it, for 13 CRs on a dependency chain six deep (CR-221 → CR-237 → CR-222 →
CR-225 → CR-226/227 → CR-228), each long gate about half an hour under one lock.

From now on the Chief of Staff states a delivery time only from a **floor** it counts by hand from
facts the record and the forge already hold: the gates under the one lock, and the levels of the
dependency chain, each at least one long gate and one CI run. Before the go, when the floor
exceeds the time the user gives (a night), it proposes a cut. While the batch runs, every Progress
report gives the remaining floor and the updated delivery time, and says a slip of an hour or
more; when the time will not hold, the steering works toward the largest mergeable partial stack
by that time.

No estimator, no median, no new CLI command (the critic's review in `intake/request.md`, kept by
answer 2): the floor is a lower bound, never a prediction.

## Decisions carried (02-answers.md)

1. **Where and how it runs.** Grilled and specified, then added at the end of batch-17's stack
   (one native stack at the end; the budget raised to $210). This specification is written to go
   on top of the CRs now in batch-17 (see "Batch-17 and the other CRs").
2. **Who computes the floor.** The Chief of Staff, by hand: a card rule only, **no CLI change**
   (not a line printed by preflight). Before stating any delivery time, it counts the dependency
   chain's depth and the CRs times the long gate's time under the one lock.
3. **When the floor exceeds the time the user gives.** The Chief of Staff proposes a cut: the
   largest set of CRs that fits the time given, short chains first, the rest for later; the user
   chooses (not a warning alone).
4. **During the batch.** Every progress report gives the remaining floor and the updated delivery
   time; a slip of an hour or more is said (not an estimate given only before the go).
5. Grilled enough: yes, to the specification.
6. **No gate time on record.** The floor is the depth alone and no delivery time is told
   ("unknown"), not asking the user and not measuring the gate once.
7. **A slip past the time the user gave, during the batch.** Only reported, no new cut. The
   user: "Il signale juste. Il doit s'arranger pour livrer la plus grande stack partielle possible
   mergeable." When the time will not hold, the steering works toward the largest mergeable
   partial stack by that time, with the CR stack-grows-from-bottom.
8. **A per-level minimum.** Each level of the chain counts at least one long gate and one CI run
   (a level cannot start before the one under it is ready); the floor is the larger of the gates
   under the lock and the levels times (gate + CI).

## What changes

Cards only, in `skills/chantier/references/`: `chief-of-staff.md` and `status-layout.md`. No CLI
code, no scenario code, no agent file (`agents/`, `com.github.copilot/agents/`), no docs. Line
numbers below are those of `main` at the time of writing; other CRs of batch-17 edit the same
cards, so the Driver anchors on the quoted text, not the numbers.

### 1. `chief-of-staff.md`: a new subsection "The floor"

A new short subsection under "## Starting a batch", placed after step 4 (the end of the numbered
list and its "Reusing the last Foreman" and "An ask from a Foreman in a worktree" paragraphs,
before "## While it runs"), headed `### The floor`. It says, in the card's own style:

- **What it is.** The least time the batch can take, counted from facts, never a prediction:
  extra rounds, a Verifier or a wait add to it, and none of them is counted. It is said "at least
  about <h> h" and a delivery time from it "not before <time>", in the user's time zone.
- **The facts it counts:**
  - **The depth:** the longest chain of CRs that wait for one another (each CR's `after`: its
    `depends.json`, a chain the go approved or the Foreman recorded, the order of a series; a
    release CR waits for every other CR, one more level). It is said with the CRs of that chain,
    in order: "critical path: CR-221 → CR-237 → … ". A parallel batch with no `after` has depth 1.
  - **The gates:** the CRs still to pass their long gate. Long gates run one at a time under one
    lock ([concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), the long gate), so every CR's gate queues behind the others
    whatever the slots. A CR whose project rules exempt it from the long gate (`handback
    --no-gate`) does not count.
- **The two terms, and the floor.**
  - The **lock term**: the gates times the long gate's time.
  - The **chain term**: the depth times (the long gate's time plus one CI run's time), since a
    level cannot start before the one under it is ready.
  - The floor is the larger of the two; the line says which one it is.
- **The long gate's time: from the record only.** The latest passed runs of the gate in this
  project: in the batch's `events.jsonl`, the `gate` events of one `run` share that id; the run
  ends at the last event's `t` (UTC) and starts at the time in the `run` id
  (`<yyyymmdd>-<hhmmss>-<pid>`, the machine's local time, not UTC: convert before subtracting).
  With no run in this batch, the project's rules when they give the gate's time. A time with no
  source is unknown ("A brief … states a past fact only with its source", "The project").
- **A CI run's time: from the forge.** The latest passed runs of the project's CI on its PRs or
  its default branch, read on the forge read-only with what the session already uses (on GitHub,
  `gh run list --json`, each run's start and update times; on GitLab, `glab ci list`). A project
  with no CI on its PRs counts 0 for it (a measured zero, said as such). The record holds no CI
  event, so the forge is the only source. When it cannot be read (no `gh` or `glab`, no rights,
  no passed run yet), the chain term counts the gate alone and the line says `CI time unknown,
  not counted`; the delivery time is still told as `not before` (open question 1).
- **Unknown gate time.** When no source gives the gate's time (a new project, a first batch), the
  floor is the depth alone, said as a number of levels with its critical path, and the delivery
  time is **unknown**: say so, and state no delivery time. Nobody is asked for the gate's time and
  no gate is run to measure it.
- **No delivery time without it.** Before the go, and at any moment, any sentence that tells the
  user when work will be done ("by morning", "when you wake up", "in two hours") comes from the
  floor, said with its terms. With no floor in hours, no time is promised.

Example to put in the card (batch-17's figures, from `intake/request.md`; the CI time is left as
a symbol since this specification has no measured one): "lock: 13 gates × 35 min = about 7.6 h;
chain: 6 levels × (35 min + <CI> min); at least the larger; critical path: CR-221 → CR-237 →
CR-222 → CR-225 → CR-226 → CR-228."

### 2. `chief-of-staff.md`, "Starting a batch", step 2 "Show the plan" (lines 380-384)

The plan's list (the CRs and what each waits for, how many start at once, the mode, the budget,
the team, who steers) gains one item, placed after the budget: **the floor** ([The
floor](#the-floor)) with its two terms and the critical path, and the delivery time it gives
("not before <time>"), or "unknown" with the reason.

Then, a new paragraph in step 2, before "The limits are the same in both modes": **the cut.**
When the user has given a time (a night, "by 9 o'clock") and the floor exceeds it, the plan
proposes a cut: the largest set of CRs whose floor fits the time given, taking the short chains
first; a CR enters only with every CR it waits for, and a chain may be cut after any of its CRs.
The rest is named as "for later" (it stays where it is: `3-ready` or the backlog; nothing is
moved before the go). The plan shows both: the whole batch with its floor, and the cut with its
own floor. The user chooses; the go names the choice, and `open` takes only the CRs chosen. When
the user gave no time, no cut is proposed: the floor and its delivery time are said, nothing
else. With the delivery time unknown (decision 6), no cut can be counted: say so in the plan.

### 3. `chief-of-staff.md`, "While it runs", bullet "Reports" (line 493)

Add: every Progress report gives the remaining floor and the updated delivery time ([The
floor](#the-floor), counted again on the state `status --refresh` has just written: the CRs not
yet past their long gate at their current head, the depth of what remains, the gate's and the CI
run's times from their latest passed runs), in its **Notes** (`status-layout.md`). When the
updated delivery time is an hour or more later than the last one told to the user, the report
says the slip and its cause in one line, in the user's language (for instance "delivery not
before 09:40, was 07:30: CR-221 took 8 rounds"). A slip is reported only: no new cut is
proposed, and the batch's CRs stay as they are.

A new bullet after "Reports", **When the time will not hold:** when the delivery time passes the
time the user gave, the steering (the Foreman through your order, or you in direct mode) works
toward the largest mergeable partial stack from the bottom by that time: the CRs that can be
ready by then come first, and the stack is made and grown from the bottom as each becomes ready,
as the CR stack-grows-from-bottom specifies for the stack driver. The report's **Notes** names
which CRs that partial stack is expected to hold. This bullet only points to that CR's
mechanism; it adds no step of its own to the Foreman's or the stack driver's cards.

### 4. `chief-of-staff.md`, "Hard rules" (lines 42-65) and "Never" (lines 1008-1025)

- Hard rules, one new bullet after "Only the user starts work": **No delivery time without the
  floor.** A time of delivery is told to the user only from [The floor](#the-floor), with its
  terms; with no floor in hours (the gate's time unknown), none is told.
- Never, one new bullet: "Tell the user when a batch or a CR will be done without its floor."

The existing "No fallback … never … an estimate" bullet stays as it is: the floor is a count of
recorded facts, not an estimate standing in for a missing tool.

### 5. `status-layout.md`, "Progress" (lines 30-96)

- In the **Notes and Cost notes** bullet (lines 73-79), the list of what **Notes** holds gains
  "the remaining floor and the delivery time (`chief-of-staff.md`, "The floor"), a slip of an
  hour or more with its cause, and, when the time will not hold, the CRs of the partial stack
  aimed at".
- A new paragraph after the one on chains (line 87): "Every Progress report has one line in
  **Notes** with the remaining floor and the delivery time: `floor: at least about <h> h left
  (lock <n> gates × <m> min; chain <d> levels × (<m> + <c> min); critical path <CR-n> → …);
  delivery not before <time>`, or `delivery unknown: <reason>` with the depth and the critical
  path; and, when that time moved an hour or more later since the last report, one more line
  with the earlier time and the cause." The header line and the tables stay as they are: no new
  column.
- The Completion report (section "Completion") gets no floor line: nothing remains.

## Out of scope

- Any CLI change: no `plan` command, no line in `preflight`, `status` or `STATUS.md`, no new
  field in `STATUS.json` (answer 2). The board pane and the web board show nothing new, so no
  screenshot is due.
- Any estimator: no median of rounds, CI runs or Verifiers, no reading of archived batches for
  times (`5-archives/batches/*.json` keep no gate events anyway).
- The mechanism of the partial stack (made as soon as its bottom is ready, grown on top, merged
  from the bottom): the CR stack-grows-from-bottom (its answer 6 carries the same words of the
  user). This CR only says when the steering aims at it.
- The Foreman's and the Drivers' cards: the floor and the reports are the Chief of Staff's, in
  both steering modes (in direct mode the Chief of Staff already writes the reports).
- The docs (`docs/`, `README.md`) and the eval kit.

## Batch-17 and the other CRs

This CR edits two cards that CRs of batch-17 also edit, on other lines; a shared file is no reason
to wait, and it goes at the end of the stack as answer 1 says:

- CR-233 merge-any-time edits `chief-of-staff.md` step 2's stack recommendation (the sentences
  on `gh stack` and `forge-stack create`, after the plan's list) and "A stack batch". Section 2
  above adds an item to the plan's list and a paragraph before "The limits are the same in both
  modes": adjacent text, different sentences; the Driver keeps CR-233's wording.
- CR-238 allow-rules-ask edits "The project" (the P10 paragraph), "Forge permissions" and step 1:
  none of the lines above.
- CR-237 root-pyproject-launch (the Foreman's prompt, line 453), CR-223 cr-summaries ("Backlog
  and grill", "Steering a batch yourself"), CR-222 visualization-backend (the routing row "board
  on my phone"), CR-226 board-backlog-edit (a row of the routing table) and CR-227
  surface-autosync ("With a planning surface"): none of the lines above.
- No CR of batch-17 still open edits `status-layout.md` (CR-224 and CR-231, which did, are merged).
- The CR stack-grows-from-bottom (backlog P1, also bound for the end of batch-17's stack) changes
  the stack driver's and the Foreman's cards; section 3's new bullet points to it by name. When
  both join the stack, the order between them does not matter for this CR's text.

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes (AGENTS.md: a change to the cards passes it before its PR).
- A reading pass, recorded in the PR's Test plan:
  - `rg -n "floor" skills/chantier/references/chief-of-staff.md skills/chantier/references/status-layout.md`
    finds the subsection "The floor", the plan's item, the cut, the Reports sentence, the "When
    the time will not hold" bullet, the Hard rule, the Never bullet and the Notes line.
  - A worked example in the PR's Test plan: the gate's time from batch-17's
    `.agents/changes/4-batch/events.jsonl` (run `20261113-190315-26164`: started 19:03:15 local
    time, ended 18:27:15Z), a CI run's time from `gh run list --json` on the repository, and the
    two terms and the floor for batch-17's 13 CRs and depth 6, with the sums, which a reviewer
    can check.
  - The cards' links (`[The floor](#the-floor)`, `status-layout.md`) resolve.
- No file outside `skills/chantier/references/chief-of-staff.md` and
  `skills/chantier/references/status-layout.md` changes (`git diff main --stat`).

## Open questions

1. **A CI time that cannot be read.** Decision 8 counts one CI run per level, but the record holds
   no CI event, so its time comes only from the forge. When the forge cannot be read (no `gh` or
   `glab`, no rights) or the project's CI has no passed run yet, the answers do not say. Default
   taken in section 1: the chain term counts the gate alone, the line says "CI time unknown, not
   counted", and the delivery time is still told as "not before" (it stays a floor). The
   alternative is to treat it as decision 6 does: no delivery time.
