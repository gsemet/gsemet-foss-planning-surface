# Change Specification: the stack holds when it breaks mid-way

## Goal

The stack driver copes with the cases that break a stack partway through. There are four:

- a CR dropped from the middle of the stack;
- a merge of the bottom PRs with no heavy CI at their own head;
- a stack driver that ends or restarts in the middle of a restack;
- sibling CRs that conflict once they are put in a line.

Today the cards have an insertion procedure and no removal procedure. Nothing records how far a
restack got. Sibling conflicts all surface at the end, one by one, at the stack driver.

The critic found these on 2026-11-14 (`intake/request.md`). This CR comes after CR-233
(merge-any-time) and CR-244 (stack-grows-from-bottom), and it changes what those two leave.

## Decisions carried (`02-answers.md`)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | Grilled and specified first, then added at the end of batch-17's stack (one native stack at the end, budget raised to $210) | "Order in batch-17" |
| 2 | A CR dropped mid-stack is removed cleanly: its commits out of the branches above (a rebase), its PR closed, the stack rebuilt without it, the checks run again on what changed (no stop to ask the user) | Area 1 |
| 3 | Replaced by answer 5: not carried | - |
| 4 | Grilled enough, after the restatement: a dropped CR removed cleanly; a restack's progress recorded so a restarted stack driver resumes; sibling conflicts handled as they come, not all at the end; after CR-233 and stack-grows-from-bottom | Areas 1, 3, 4 |
| 5 | Heavy CI runs only on the top PR by default. Merging in the middle of the stack without heavy CI at that head is the user's choice. Heavy CI on an intermediate head stays optional | Area 2 |

Answer 4's restatement still says "full CI green at every head before a partial merge is
offered". That is answer 3's wording, and answer 5 replaces it. This spec follows answer 5.

## What it builds on

**CR-233** (PR #173, cards). The user may merge the stack in one action from the top PR, or one
PR at a time from the bottom. "After a partial merge" is the procedure for both.

**CR-244** (stack-grows-from-bottom; spec at
`.agents/changes/4-batch/1-pending/244-stack-grows-from-bottom/03-change-spec.md`):

- The words used below come from it: **stack as it stands**, **mergeable part**, **drafts on
  top**, **to come**.
- The first native stack is made at two ready PRs.
- A CR joins on top as a draft as soon as it has its PR, by `forge-stack rebuild` (unstack, then
  create).
- After a partial merge, the stack is restacked silently.
- `forge-stack` acts on the stack as it stands. `_unstack` and check 2 name a PR "of the batch's
  stack left out of the rows" apart.
- Decision 9 is binding here: a `working` CR's branch belongs to its Driver. The stack driver
  never rebases or pushes it. Instead the Foreman sends its Driver `[foreman→driver <cr>] note
  rebase: stacked on <cr below>`.

This CR keeps all of the above. Where it edits the same paragraphs or functions, it adds to their
merged text and replaces none of it.

## What changes

The CLI (`forge-stack`, `stack`, `take stack`), four cards and the scenario. Untouched:

- the agent files (`agents/`, `com.github.copilot/agents/`);
- `hooks/` and `types/` (so no `just mod` is needed);
- any version;
- any CI job.

### Area 1: a CR dropped from the stack (decision 2)

**When it applies.** A CR of a stack batch is dropped (`order drop`, or the Foreman's `cancel` of
a live dropped CR), and either:

- it has an open PR; or
- an open CR's branch sits on its branch.

`chain()` (`commands/facts.py`) already leaves the dropped CR out, so `take stack` prints the stack
without it. This area adds the removal on git and on the forge.

**`foreman.md`**, the stack batch paragraph (lines 156-180 on `main`, as CR-233 and CR-244 leave
it). Add one bullet, **A drop in the stack**:

- **Starting the removal:**
  - With no stack driver running, run `take stack --note "drop: <cr>"` right after the drop is
    applied.
  - With one running, send `[foreman→stack] note drop: <cr>`. It handles the drop before it goes
    on with its take.
- **A working CR above the dropped one** (decision 9: the stack driver does not touch its branch).
  Read its state with a plain `status` just before acting, as the card says, then send its
  Driver `[foreman→driver <cr>] note rebase: stacked on <cr below>, without <dropped cr>`. Here
  `<cr below>` is the CR now under it, or the default branch.
- **An open CR whose `after` names the dropped CR.** Keep the existing rule (foreman.md line 132:
  a cancelled dependency never frees a CR). Ask the Chief of Staff once whether the user drops
  that CR too or changes it, and hold the drop take until the answer comes. Decision 2 covers
  only the dropped CR's own removal: a dependant whose code builds on it cannot be rebased
  cleanly.
- **A release above the dropped CR.** It is stale, as foreman.md's release bullet already says
  ("a change of content (a new round, a drop)"). After the stack driver hands back, run `take
  <release> --note "redo: <cr> dropped"`, then `take stack` again, as for an insertion.
- **Closing the order.** `order done` follows the stack driver's hand-back. Nothing is asked of
  the user.

**`driver.md`, "Stack driver".** Add a paragraph **Removing a dropped CR** after "Inserting into a
ready stack". It applies to a take or a note that names `drop: <cr>`:

1. Turn every PR above the dropped one back to a draft first (`gh pr ready --undo`, `glab mr
   update --draft`). The user must not merge a stack that still holds the dropped commits.
2. Take the dropped commits out of each CR above that has no live Driver (`ready`, `blocked`),
   bottom up, in its own worktree:
   - The first CR above sits on the dropped CR's branch. Run `git rebase --onto <the branch now
     under it, or origin/<default branch>> <the dropped CR's branch>`.
   - Each CR above that one: `git rebase --onto <branch under it> <that branch's head before this
     take>`. The old head is the `head` that `stack` printed for that CR before the take's first
     rebase (Area 3).
   - Skip a `working` CR above: its Driver does it, on the Foreman's note.
   - A conflict that only needs resolving goes to a `conflict-resolver`.
   - A conflict that needs code goes through Area 4's route.
3. Push each moved branch with `--force-with-lease`, one command per branch, and `ship` each
   one. Judge again the proofs each move touched, as the restack paragraph says: a `verifier`
   given the move, and an `inspector` when the patch changed (always, after a
   `conflict-resolver`). Fix the PR body lines that `ship` names as stale.
4. Heavy CI at the top (Area 2). Then `$CHANTIER forge-stack rebuild`: it unstacks the stack that
   still holds the dropped CR's PR, and names that PR apart (see "CLI" below).
5. Close the dropped CR's PR with `gh pr close <n>` or `glab mr close <n>`, with no
   `--delete-branch` and no comment. The dropped CR's branch and worktree stay until the user's
   word at `close` (foreman.md line 93).
6. Turn the mergeable part ready, as CR-244 says. A release above stays a draft, waiting for the
   Foreman's `redo:`. Hand back as for any take.

Two lighter cases:

- A dropped CR with an open PR and nothing on its branch needs only steps 4 and 5.
- A dropped CR with no PR and nothing on its branch needs nothing from the stack driver.

**`driver.md`, "CR driver"** (the rebase paragraph, lines 383-398, beside CR-244's `rebase:
stacked on <cr>`). A note `rebase: stacked on <cr below>, without <dropped cr>` changes the rebase
command only: `git rebase --onto <base> <the dropped CR's branch>`, so the dropped commits leave
the branch. The rest is CR-244's rule:

- one rebase before the next push;
- `ship`;
- the long gate at the new head;
- the `verifier` given the move.

**`chief-of-staff.md`**, beside "Inserting a CR into a ready stack". Add a bullet **Dropping a CR
from a stack**. On the user's word, run `order drop <cr>` as today, then tell the user that:

- the CR's commits come out of the PRs above it;
- its PR is closed;
- its branch stays until `close`;
- the PRs above it are drafts, not mergeable, until the next report's partial-stack line (CR-244,
  Area 9) shows them mergeable again.

Nothing more is asked of the user.

**CLI, `commands/forge_stack.py`.** A dropped CR's PR is named apart from a foreign PR. (Under
CR-244 it would read as foreign, because `chain()` leaves cancelled CRs out.)

- `_plan` (lines 54-99) also returns the PR numbers of the batch's `cancelled` CRs that have a PR
  and are not of kind `fix`, with their CR ids. `_pr_parts` is not applied to them.
- `_unstack` (lines 138-161) gets a third kind in its "it also held" clause, beside CR-244's kind
  and the foreign one: `(it also held #n of <cr>, dropped: close it)`. `_rebuild` passes the
  dropped PRs to it.
- `_checks` check 2 (lines 215-223): a held PR of a dropped CR is a failure named apart,
  `check 2: …; dropped #n (<cr>): close it`. A foreign PR stays `not in the batch's stack #n`.
  CR-244's `not in the stack as it stands #n (<cr>)` stays as it is.

`chain()`, `stack_base` and `order drop` (`commands/orders_apply.py`, `_drop`) do not change.

**`concepts.md`**, **Stack** (lines 101-124). Next to "Inserting a change into a ready stack", add
one sentence: a CR dropped from the stack is removed. The PRs above go to draft first. Its
commits come out of the branches above (by the stack driver, or by the Driver of a working CR).
Its PR is closed and its branch kept. The stack is rebuilt without it and judged again where it
changed. A release above is redone.

### Area 2: heavy CI at the top; a merge in the middle is the user's choice (decision 5)

Heavy CI still runs once at the top (driver.md lines 413 and 458; CR-244's "green at the top").
What changes is what the user is told, and an optional run on a head the user names.

**`chief-of-staff.md`, "A stack batch"** (as CR-233 and CR-244 leave it):

- When you tell the user about a `stack-ready` ask (the partial one or the complete one), add
  one clause in the user's language:
  - heavy CI ran at the top PR's head only;
  - merging a PR below it without heavy CI at its own head is the user's choice;
  - heavy CI can be run on that head if they ask.
- The partial-stack line of each report (CR-244, Area 9) does not repeat it.
- A merge in the middle is recorded as CR-233 says (`order merged`, bottom first), never
  questioned or refused.

**The optional run, on the user's word only:**

1. The Chief of Staff runs `order note <cr> --note "heavy CI: at its head"`.
2. The Foreman passes it on:
   - to a running stack driver, as `[foreman→stack] note heavy CI: <cr>`;
   - with no stack driver running, as `take stack --note "heavy CI: <cr>"`.
   - When the CR is `working`, its own Driver's CI already covers its head: the Foreman tells the
     Chief of Staff so, and nothing runs.
3. The stack driver runs the project's heavy CI at that PR's pushed head, by the means the
   project's rules give (a re-run, a label, a workflow dispatch). When the forge has already run
   it at that head, it only reads the result.
4. It judges the result as driver.md's CI bullet says: the head first, a skipped job is never
   green, one re-run for an infrastructure failure.
5. It notes the result in that bullet's form (`CI: gh pr checks <n> at <head7>: …`) and names it
   in its hand-back as `heavy CI <cr> at <head7>: green|red <checks>`.
6. The Foreman passes it up with `$CHANTIER asks "heavy-ci <cr> <head7> green|red <checks>"`. Add
   this kind to the `asks` list (foreman.md line 191).
7. The Chief of Staff tells the user.

A red result changes nothing by itself: the PR stays where it is, and the user decides. A red
result at the top is a red check, handled as today.

**`driver.md`, "Stack driver"**: add the `heavy CI: <cr>` note above. "Keep the stack green with
heavy CI once at the top" gains "by default; a head the steering session names gets it too".

**`concepts.md`, Ready to merge** (as CR-233 and CR-244 leave it): a PR of the mergeable part
below the top had heavy CI only at the top, unless the user asked for it at its head.

### Area 3: record a restack's progress so a restarted stack driver resumes (decision 4)

A restack after a partial merge, an insertion or a drop does a lot in one stack driver:

- it force-pushes every PR above that has no live Driver;
- it starts a `verifier`, and an `inspector` when needed, for each PR it touched.

That stack driver has no `context:` reading today: `note <cr>` measures the CR's Driver, not the
stack driver. Nothing tells a new stack driver how far the last one got.

**CLI, `commands/facts.py`, `stack_lines`** (lines 204-212). This is what `take stack` and
`stack` with no CR print. Each CR's row gains:

- ` head <head7>`: the head `ship` recorded, or `-` when none;
- ` restack: <the CR's last note that starts with "restack:">`, or ` restack: none`.

**CLI, `commands/delivery.py`, `stack`** with no CR (lines 142-165). After the rows, print one
line with the context of the recorded stack driver (`stack_agent`), measured the way `note`
measures a Driver's:

- `context: <n> tokens (agent <id>)`;
- or `context: not measured (<reason>)`, with the reasons of `_context_line` in
  `commands/driver.py`, lines 124-139.

`_context_line` takes the agent id as a parameter, and both callers pass theirs. `take stack`
does not print this line, because its agent has not started yet. These are additions to two
existing commands, not a new CLI tool.

**`driver.md`, "Stack driver".** Add a paragraph **Recording a restack**:

- Before a take's first rebase, run `$CHANTIER stack`. Its `head` values are the old heads.
- After each CR you move is rebased, pushed and `ship`ped, record `$CHANTIER note <cr> "restack:
  on <cr below or default branch> <its head7>, head <new head7>"`.
- After its proofs are judged, record `$CHANTIER note <cr> "restack: judged at <head7>"`. An
  `inspector`'s approval keeps its existing note (`move … (restack) inspector approved at
  <head>`).
- A `working` CR is its Driver's (CR-244, decision 9). It carries no `restack:` note from you.
- After each CR, read the `context:` line of `$CHANTIER stack`:
  - At 130,000 tokens or more, send `[stack→foreman] hand-back blocked context: <where it
    stopped, what is next>` and end. This applies the Driver's context rule (driver.md lines
    65-70) to the stack driver, and only when the last `context:` line read 130,000 or more.
  - At `context: not measured`, go on.
- **Resuming.** When a take's note names `resume:`, or a take finds the stack partly restacked,
  read `$CHANTIER stack` once. A CR you move is done when both hold:
  - its last `restack: on …` note names the CR below at that CR's current `head`, and names its
    own `head`;
  - a later `restack: judged at <its head>` note exists.

  Go on from the first CR, bottom up, that is not done, and never redo one that is.

**`foreman.md`**:

- A stack driver's `hand-back blocked context: …` is neither an anomaly nor an ask. Run `agents
  set stack -`, then `take stack --note "resume: <the hand-back's text>"`, then start a new stack
  driver on the batch's model (not the escalation model).
- A stack driver that ended with no hand-back (its agent gone, no `activity` for it) gets the same
  `resume:` take.
- A restack that failed is still an escalation (concepts.md line 352).
- Where the card lists the stack driver's lines, add `hand-back blocked context:` beside
  `hand-back ready`.

### Area 4: sibling conflicts handled as they come (decision 4)

Under CR-244 a CR joins the stack as soon as it has its PR. Its branch is first placed on the
stack's top at that join, one CR (or the few found at the same take) at a time. So conflicts
between siblings that started on one base surface at each join, in the order the CRs get their
PRs, rather than all at the end.

Where the conflict lands depends on the joining CR:

- **A working CR:** its own Driver meets the conflict when it rebases on CR-244's `rebase:
  stacked on <cr below>`. The CR driver's existing rule applies: a `conflict-resolver`, or a round
  when the conflict needs code. Nothing changes there.
- **A CR with no live Driver** (`ready`, `blocked`), joining or moved by the stack driver. This
  area states what happens, so that one such conflict holds back neither the rest of the take
  nor the stack below.

**`driver.md`, "Stack driver"**, at the join or move of a CR with no live Driver:

- A conflict that only needs resolving goes to a `conflict-resolver` at that join, as today.
- A conflict that needs code:
  1. `git rebase --abort` in that CR's worktree, and push nothing for it.
  2. Turn its PR to a draft (`gh pr ready --undo`, `glab mr update --draft`).
  3. Place it on top among the drafts with `stack` (above the CRs it does not depend on; the
     release stays last). It stays in the stack as it stands, as a draft on top. Its PR is
     retargeted by the rebuild, and its branch is not rebased.
  4. Go on with the rest of the take, the `rebuild` included.
  5. Before the hand-back, send `[stack→foreman] anomaly <cr> conflict: stacked on <cr below>:
     <files>`.

**`foreman.md`**, the anomaly handling in the stack batch paragraph, for `conflict: stacked on
<cr>: <files>`. Take the CR back with `take <cr> --note "rebase: stacked on <cr below>: conflict
in <files>"` before you read the five checks of the stack driver's hand-back. The take puts the
CR back in `working`, so its draft is no check 4 failure. Its Driver rebases by CR-244's rule,
with a `conflict-resolver` or a round. The CR turns ready in the stack at a later take, as any
draft that turns ready.

## Out of scope

- Heavy CI on every intermediate head by default (answer 5 replaces answer 3).
- A CLI check of CI at each PR's head in `forge-stack show`.
- Splitting one restack among several stack drivers.
- A trial merge of working siblings before they have a PR (open question 2).
- Deleting a dropped CR's branch or worktree: the user's word at `close`, as today.
- GitLab beyond the closes and drafts named above. The stack there stays a chain
  (`2-backlog/P2/gitlab-stack-delivery`).
- The docs, README, SVGs and eval kit sentences on the stack: a docs follow-up, as in CR-233.
- Any merge by an agent.

## Order in batch-17

This CR goes on top of CR-233 (PR #173) and CR-244 in batch-17's stack (`order add`,
decision 1). It is written against their merged text.

- **Cards:** `foreman.md`, `driver.md`, `chief-of-staff.md` and `concepts.md` change in the
  paragraphs those two rewrite. Keep their text, and add the bullets and paragraphs above.
- **`forge_stack.py`:** CR-244 changes `_plan`, `_unstack`'s clause and check 2. This CR adds the
  dropped kind beside CR-244's kinds, in the same places. CR-234 (PR #175) changes `_unstack`'s
  loop and raise; keep those as they are.
- **Scenario:** CR-244 gives `record()` a status per CR. This CR's steps use it.
- **Reaching the running batch:** its card changes reach the running batch only once merged into
  the main checkout and reloaded.

## Evidence

**Checks:** `just check` passes on Linux, macOS and Windows. `just lint` runs within it: each
function stays under fifty lines, and `130,000` is a card figure, not a CLI constant.

**Scenario** (`just scenario`, both forges): checks in `scenario/run_scenario.py`, section 13a
(`forge_stack_cli`), and in its `scenario/README.md` list.

1. A dropped CR's PR still held by the forge's stack. After `order drop <b>` (with `b` ready):
   - `forge-stack show` prints `check 2: … dropped #202 (<b>): close it` and exits 2;
   - `rebuild` unstacks with `(it also held #202 of <b>, dropped: close it)` and posts the stack
     without #202.
2. A foreign PR is still named `not in the batch's stack #999`.
3. The `stack` rows and context line:
   - `stack` with no CR prints each row with `head <head7>` (or `head -`) and `restack: none`;
   - after `note <cr> "restack: on … head …"`, that CR's row shows the note;
   - the last line starts with `context:` (`not measured …` in the scenario, which has no
     transcript);
   - `take stack` prints the rows with no `context:` line.
4. The existing 13a checks, CR-234's unstack step and CR-244's steps still pass.

**Reading pass**, in the PR's Test plan:

- `rg -n "drop: |without <dropped" skills/chantier/references` finds the procedure in
  `foreman.md`, `driver.md` and `chief-of-staff.md`.
- `rg -n "resume:|hand-back blocked context" skills/chantier/references` finds it in `foreman.md`
  and `driver.md`.
- `rg -n "heavy CI: |heavy-ci" skills/chantier/references` finds the optional run in the three
  cards.
- `rg -n "conflict: stacked on" skills/chantier/references` finds the stack driver's and the
  Foreman's rule.
- No card says that every head must be green before a partial merge.

No CI job is added or changed.

## Self-containment for the Driver

Files:

- `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py` (`_plan`, `_unstack`,
  `_rebuild`, `_checks`);
- `skills/chantier/scripts/cli/src/chantier/commands/facts.py` (`stack_lines`);
- `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`stack`);
- `skills/chantier/scripts/cli/src/chantier/commands/driver.py` (`_context_line`);
- `skills/chantier/references/driver.md`, `foreman.md`, `chief-of-staff.md`, `concepts.md`;
- `scenario/run_scenario.py`, `scenario/README.md`.

Read CR-233's specification (`.agents/changes/4-batch/2-actives/233-merge-any-time/`) and CR-244's
(`.agents/changes/4-batch/1-pending/244-stack-grows-from-bottom/`), and work on their merged text.

## Open questions (each with the default taken)

1. **How an optional heavy-CI result reaches the user.** Default: a new ask kind `heavy-ci <cr>
   <head7> green|red <checks>`. Alternative: it rides on the next `stack-ready` ask as a gap of
   that CR.
2. **Sibling conflicts before a CR has a PR.** Default: they surface at its join only.
   Alternative: at each join, the stack driver trial-merges each working sibling's branch onto the
   new top (`git merge-tree`), and the Foreman warns those Drivers early. That costs tokens at
   every join.
3. **A dropped CR that another open CR depends on.** Default: the existing ask (the user drops
   that CR too or changes it) comes first, and the removal waits. Alternative: the removal goes
   ahead, and the dependant goes back to its Driver.
4. **Closing the dropped PR.** Default: closed with no comment, branch kept. Alternative: a short
   comment saying it was dropped from the batch.
