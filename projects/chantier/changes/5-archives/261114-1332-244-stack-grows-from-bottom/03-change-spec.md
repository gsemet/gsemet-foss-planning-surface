# Change Specification: the stack grows from the bottom

## Goal

The user (2026-11-14): "je veux la stack complète comme prévue", and, in their own words
(answer 7): "Quand une stack est demandée : dès que 2 PR sont prêtes tu fais la stack. Quand une
troisième arrive tu défais et refais pour avoir une stack de 3. Celle du haut est en draft, mais
l'utilisateur peut merger en dessous. Puis quand la PR devient verte la stack est mergeable. Puis
ça continue. Quand l'utilisateur a mergé une partie, tu refais silencieusement une nouvelle
stack, etc."

In a stack batch the native stack is made on the forge as soon as two PRs are ready. Each further
CR joins on top as soon as it has its PR, as a draft; the stack is undone and made again with it.
The user may merge the ready PRs below while the drafts on top go on; when a draft turns ready,
the stack is mergeable up to it. After a partial merge, a new stack of what remains is made
silently. One slow CR no longer blocks the stack.

What happened (batch-17, `intake/request.md`): at 07:41 five CRs were ready (221, 237, 232, 233,
234) and no stack could exist, because CR-225 to CR-228 had no PR yet: `forge-stack create`
refuses while any open CR of the stack has no PR, and the Foreman's card starts the stack driver
only when every open CR is ready or blocked.

## Decisions carried (`02-answers.md`)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | Grilled and specified first, then added at the end of batch-17's stack (one native stack at the end; budget raised to $210) | "Order in batch-17" |
| 2 | Readiness order: among independent CRs the first ready goes lowest; a CR that depends on another always stays above it | Words; Areas 1, 3 |
| 3 | The user may merge the bottom while the top goes on; the stack driver restacks the rest on the default branch and goes on | Areas 3, 4, 5 |
| 4 | Two `stack-ready` asks: one when the stack is first made, naming the CRs still to come; one when it is complete; none per addition | Areas 4, 5 |
| 5 | Grilled enough, including that it amends CR-233's card paragraphs that wait for every CR to be ready | Areas 3 to 6 |
| 6 | When a batch will not finish by the time the user gave, the steering session and the stack driver work toward the largest mergeable partial stack from the bottom by that time | Area 8 |
| 7 | The first stack at two ready PRs; a further CR joins as soon as it has its PR (a draft), by unstack then create; the top stays a draft while the user may merge below, and once it turns ready the whole stack is mergeable; after a partial merge, a new stack of what remains, silently (no ask). The earlier defaults stand: CRs ready at the same moment in their planned order; the delivery time sent by a Chief of Staff note; the batch going on after that time; the Foreman judging what can be ready in time | Words; Areas 2 to 8 |
| 8 | Every progress report, and the `stack-ready` asks, name the mergeable partial stack as it stands: "partial stack mergeable below <commit>", the commit being the head of the highest PR mergeable now, so the user knows at any time how far down they can merge ("Tu peux dire régulièrement « stack partielle en dessous du commit xxx »") | Words; Areas 2, 4, 5, 9 |
| 9 | A working CR that joins the stack is rebased by its own Driver, on the Foreman's `note rebase: stacked on <cr below>`; the stack driver never pushes a branch a live Driver holds | Areas 3, 4 |
| 10 | A CR already in the stack handed back ready: nothing for the user; the next report's "partial stack mergeable below <commit>" line says it, and its gaps come in the complete `stack-ready` | Areas 4, 5, 9 |
| 11 | At the time the user gave, if the stack is not complete: a `stack-ready … to come:` ask of the stack as it stands, when none was sent for it | Area 8 |

## Words used below

- **The stack (as it stands):** the CRs of `chain()` (`commands/facts.py`), bottom first, taken
  from the bottom while each has a PR recorded; it stops at the first CR with no PR. Its order:
  the ready CRs first, in readiness order (decision 2; those found ready at the same take in their
  planned order), then the CRs with a draft PR, in the order they joined; a CR always above the
  ones it depends on (a ready CR whose dependency is a draft stays above it, among the drafts).
- **The mergeable part:** the CRs of the stack from the bottom while each is `ready` and its PR
  not a draft. The user may merge any PR of it, with all those under it. **Its commit** is the
  head of its highest PR (`head` of that CR in the record, seven characters): the user may merge
  everything below it, that commit included (decision 8).
- **Drafts on top:** the CRs of the stack above the mergeable part; their PRs are drafts.
- **To come:** the open CRs of the batch's stack with no PR yet, above the stack.
- **Complete:** every open CR of the batch's stack is in the mergeable part (the release, when
  the batch has one, on top).

## What changes

The CLI (`forge-stack`, `stack`), four cards, the scenario. No agent file (`agents/`,
`com.github.copilot/agents/`), no `hooks/` or `types/` (no `just mod`), no version edit.

### Area 1: `stack` accepts a partial order (`commands/delivery.py`, `stack`, lines 142-165)

Today `stack <cr>…` gives `order` 1..k to the CRs it names and `stacked=True`, and leaves every
other CR's `order` as it was, so naming only some CRs makes two CRs share an `order` and
`chain()` (sorted by `(kind == "release", order)`) mixes them. The stack driver names the CRs of
the stack (those with a PR) and not the ones to come.

- When the CRs named are only some of the open CRs of `chain()`, the named ones take `order`
  1..k in the order given, and the others take k+1.. in their current relative order (the release
  stays last through `chain()`'s key). Only the named CRs are marked `stacked`; the others keep
  their flag (an unnamed CR is not placed, so `stack_base` keeps its start base until it joins).
  Merged, cancelled and fix CRs are not renumbered. Naming every open CR behaves as today.
- One new refusal beside the existing one ("`<cr>` depends on `<dep>`: it cannot sit below
  it"): a named CR whose `after` holds an open CR of the stack that is not named:
  `<cr> depends on <dep>, which is not named: it cannot sit below it`.
- The help of `crs` says that naming some CRs puts them at the bottom, the others above in their
  order. The `stack-order` event is unchanged (it lists the CRs named).

### Area 2: `forge-stack` acts on the stack as it stands (`commands/forge_stack.py`)

- **`_plan`** (lines 54-99): the refusal of lines 67-73 ("… no PR recorded (`ship`): the stack is
  made once every PR is recorded") goes. `_plan` returns the rows of the stack as it stands (the
  bottom CRs with a PR, whatever their status), each with its status, and the CRs to come (id and
  status), beside the forge's host, owner and repository. The PR-link checks (`_pr_parts`, "not
  all in one repository") apply to the rows. With no PR at the bottom, `create` and `rebuild` are
  refused (exit 2): `no PR at the bottom of the stack: <first cr> is <status>, no PR`; `show`
  prints it as `check 1: …`, exit 2. It replaces "no PR recorded in the stack" (line 97). The
  rule of two ready PRs is the Foreman's, not the CLI's.
- **`create`, `rebuild`:** make the stack of the rows, bottom to top, drafts included. A CR that
  joins on top is a `rebuild`: it unstacks the forge's stack, retargets the new PR's base (and any
  other off the record) and creates the stack again (answer 7's "unstack, then create"). A PR of a
  CR to come is never retargeted.
- **`_unstack`** (lines 138-161): the "it also held #n, not in the batch's stack: a plain PR now"
  clause separates the PRs of CRs of the batch's stack left out of the rows from foreign ones:
  `(it also held #n of <cr>: a plain PR until it joins again)` for the first, the existing text
  for the second. `_rebuild` passes those PR numbers to it.
- **`_checks` / `show`** (lines 205-266), the five checks of the stack as it stands:
  - check 1: the stack is open (unchanged).
  - check 2: it holds every PR of the rows, and no other. Line 217 (`<cr> (no PR recorded)` as
    missing) goes: a CR without a PR is to come, not missing. A foreign PR stays
    `not in the batch's stack #n`; a PR of the batch's stack left out of the rows (its CR placed
    above one with no PR) is named `not in the stack as it stands #n (<cr>)`.
  - check 3: in the order of the record, bottom first (unchanged).
  - check 4, drafts, read against each CR's status: a PR whose CR is `ready` and is still a draft
    while every PR under it is ready (`check 4: still a draft #n`, the existing wording: the stack
    driver turns it ready); a PR whose CR is not `ready` and is not a draft
    (`check 4: not a draft #n (<cr> <status>)`); a draft under a PR that is not one
    (`check 4: a draft under a ready PR #n`). A draft on top of a CR that is not ready is no
    failure.
  - check 5: the release PR is on top when the release is in the stack (unchanged otherwise).
  - On success, one line: `stack #N ready: open, K PRs in order, partial stack mergeable below
    <sha7> (#m, M PRs)` (decision 8; `stack complete, mergeable below <sha7> (#m)` in place of
    `partial stack` when the stack is complete),
    then `, drafts on top #a #b` when there are, and `, the release on top` as today. When CRs are
    to come or drafts are on top, one more line, `to come: <cr> <status>…` (the drafts' CRs then
    those with no PR, bottom first). A complete stack prints no `to come:` line. Exit 0.
    `rebuild` passes the `to come:` line through, not as a failure (exit 0 when only `check 4:
    still a draft` lines and the `to come:` line follow the ready line, as it does today for
    drafts).
- The `forge-stack` help says "the stack batch's stack as it stands (the bottom CRs with a PR,
  drafts on top)".

`chain()` and `stack_base` (`commands/facts.py`) do not change: `chain()` sorts by `order`, which
Area 1 keeps in the stack's order.

### Area 3: the stack driver (`driver.md`, "Stack driver")

- The opening ("Your end is one native stack …", as CR-233 left it: one action from the top PR
  or one PR at a time from the bottom) adds: each take ends with the stack as it stands on the
  forge, its mergeable part ready, drafts on top; the batch's last take ends with it complete.
- **Ordering:** name with `$CHANTIER stack <cr>…` every CR that `take stack` prints with a PR,
  in the stack's order (Words): the ready ones first (those already in the mergeable part in
  their place, then the newly ready in their place order), then the drafts (those already
  stacked in their place, then the newly joined in planned order). The CRs to come are not
  named.
- **Who moves a branch:** a CR with no live Driver (`ready`, `blocked`) is rebased and pushed by
  you, as today (rewrite form, one command per branch, `ship`, proofs judged again with a
  `verifier` and an `inspector` when a move touched them). A `working` CR's branch is its Driver's:
  you never rebase or push it; the Foreman sends its Driver `[foreman→driver <cr>] note rebase:
  stacked on <cr below>` and the Driver rebases once before its next push and `ship`s
  (decision 9).
- **Making the stack** ("Once every PR of the stack is ready …"): becomes "Once two CRs are ready
  with their PRs, ordered, restacked, pushed, `ship`ped and green at the top": create the native
  stack with the means your prompt names (`gh stack` extension, or `$CHANTIER forge-stack
  create`), the CRs with a draft PR on top as drafts; turn ready every PR of the mergeable part.
- **A CR that joins** (it has a PR, a draft): order it on top (`stack`), have it rebased (above),
  then `$CHANTIER forge-stack rebuild` (unstack, retarget, create). The PRs below are not moved
  and stay ready: the user may merge them meanwhile.
- **A draft that turns ready** (its CR handed back `ready`): it moves into the mergeable part.
  When it is the lowest draft, nothing moves: rebuild is not needed; read the stack back and turn
  its PR ready once the five checks hold. When drafts sit under it, order it below them (`stack`),
  rebase it and the drafts above (theirs by their Drivers' notes when working), `rebuild`, then
  turn it ready.
- **"The five checks"**: they read the stack as it stands (Area 2); drafts on top and the
  `to come:` line are no failure.
- **"After a partial merge"**: unchanged (one restack of what remains on `origin/<default
  branch>`, one `rebuild`); it hands back with no `stack-ready` (answer 7: silently).
- **A merge during a take** (decision 3): on `[foreman→stack] note merged: <cr>…`, re-read the
  stack (`$CHANTIER stack`), restack what remains on `origin/<default branch>` with the CRs being
  added (one restack, as "After a partial merge"), then `rebuild`. A `rebuild` refused because a
  PR of the plan merged meanwhile is an `anomaly` with the exact text, as any refused `rebuild`.
- **"Inserting into a ready stack"**: unchanged, the new CR joining at the place named once it
  has a PR (a draft until it is ready).

### Area 4: the Foreman (`foreman.md`, the stack batch paragraph, lines 156-180 on `main`)

On top of CR-233, this replaces "a stack driver takes the stack when its open CRs are all ready
or blocked" and CR-233's "until then it runs like a parallel batch with chains …":

- **The first take:** as soon as two CRs are `ready` with a PR (and neither depends on an open
  CR not ready). Until then the batch runs as CR-233 says (each CR ready on the default branch
  is an ordinary `ready` ask; a merge gets rebase notes).
- **Each later take**, one for everything that happened while no stack driver ran: a CR got its
  first PR (`status` shows it; it joins), a CR of the stack was handed back `ready` (it turns
  ready), a merge was recorded (a restack). Events while a stack driver runs wait for its end,
  except a merge (below).
- **A merge** recorded while a stack driver runs: send it `[foreman→stack] note merged: <cr>…`
  (all the CRs one message of the Chief of Staff recorded) instead of a new `take stack`; while
  none runs: one `take stack` for what remains, as CR-233's "A restack". CR-233's choice after a
  merge is a restack whenever a native stack of the batch is on the forge; its "Rebase notes"
  branch applies only before the first stack is made.
- **A working CR placed on another:** pass the stack driver's rebase need to its Driver with
  `[foreman→driver <cr>] note rebase: stacked on <cr below>` (Area 3).
- **The asks** (decisions 4 and 7), after the stack driver's hand-back and the five checks
  (`forge-stack show`, unchanged otherwise):
  - The first stack made: `$CHANTIER asks "stack-ready <stack link> partial stack mergeable below
    <sha7> <cr>=<link>… to come: <cr> <cr>…"` (the `<cr>=<link>` pairs: the mergeable part; to
    come: the drafts on top and the CRs with no PR; `<sha7>` as `forge-stack show` printed it).
  - The stack complete: `$CHANTIER asks "stack-ready <stack link> mergeable below <sha7>
    <cr>=<link>…"`.
  - Any other hand-back (a CR joined, a draft turned ready, a restack after a merge): no ask.
  - A CR of the stack handed back `ready` (decision 10): no ask. Record its gaps with `$CHANTIER
    note <cr> "gaps: …"` (`none` when it has none) and quote them after its link in the complete
    `stack-ready` (`<cr>=<link> gaps: …`); the next report's partial-stack line shows it once its
    PR is in the mergeable part. The Foreman's "Never merge without the user's word" bullet
    (lines 44-46), which makes every ready CR a `ready` ask, gets this exception.
- **The five checks** bullet (lines 181-184): "it holds every open PR of the batch's stack, and
  no other; … none is a draft" becomes "it holds every PR of the stack as it stands (the bottom
  CRs with a PR), and no other; in the record's order; no PR of a ready CR is a draft and every
  draft sits above the ready PRs; the release PR, when it is in the stack, on top".
- The `asks` line list (line 191) adds the commit and the `to come: …` tail to `stack-ready`.
- Lines 166-167 ("Its end is one native stack …", as CR-233 left it) add: made at two ready PRs,
  grown on top as each CR gets its PR, drafts on top.

### Area 5: the Chief of Staff (`chief-of-staff.md`)

- **"A stack batch"** (lines 552-564 on `main`, as CR-233 rewrote it): a `stack-ready … to come:
  …` ask is checked the same way (`forge-stack show`), then told to the user: the stack is
  mergeable up to its last ready PR (in one action from that PR, or one PR at a time from the
  bottom, per CR-233), the drafts on top and the CRs still to come named (number and slug), and
  the top goes on while the user merges; it grows silently, and its state is in each report. The
  `stack-ready` with no `to come:` says the stack is complete. Both name the commit, in the
  user's language ("partial stack mergeable below <sha7>", "stack partielle mergeable en dessous
  du commit <sha7>"). Each merge is recorded as CR-233
  says (`order merged`, bottom first, one message to the Foreman); no ask follows the restack.
- A CR of the stack that turns ready reaches the user through the next report's partial-stack
  line (Area 9), never as an ask; its gaps are quoted with the complete `stack-ready`
  (decision 10).
- **The plan at the go** (step 2, lines 384-390): the stack recommendation adds that the stack is
  made as soon as two PRs are ready, each further CR joins on top as a draft when it has its PR,
  the user may merge the ready ones below at any time, and a new stack of what remains is made
  silently after a merge.

### Area 6: `concepts.md`

- **Stack** (lines 101-111): "Once every PR is ready, the stack driver makes one native stack"
  becomes: as soon as two PRs are ready the stack driver makes the native stack; each further CR
  joins on top as a draft when it has its PR (`forge-stack rebuild`: unstack, then create); the
  ready PRs come first in readiness order, a CR always above its dependencies; the user merges the
  mergeable part at any time. **Stack ready**: the five checks of the stack as it stands (Area 4's
  wording). Add the words **stack as it stands**, **mergeable part**, **drafts on top** and **to
  come**.
- **Ready to merge** (lines 9-16, as CR-233 left it): a PR of the mergeable part of a verified
  stack is mergeable, with those under it; a draft on top is not.
- The partial-merge sentence (lines 123-124): what remains is restacked on the default branch,
  silently, and goes on growing.

### Area 9: every progress report names the partial stack (decision 8; `status-layout.md`, `chief-of-staff.md`)

- **`status-layout.md`**, "Progress", a new paragraph beside the chain and `main checkout:`
  paragraphs (lines 87-91 on `main`): in a stack batch with a native stack on the forge, every
  Progress report has one line in **Notes**: `partial stack mergeable below <sha7> (<cr> #<n>);
  to come: <cr> <cr>…`, or `stack complete, mergeable below <sha7>` once complete, in the user's
  language, the CRs by number and slug. With no stack on the forge yet: `no stack yet: <k> of 2
  PRs ready`. The Completion report has none (nothing remains). No new column, no CLI line in
  `STATUS.md` or `STATUS.json` (the board pane is unchanged, so no screenshot is due).
- **`chief-of-staff.md`**, "While it runs", bullet "Reports": in a stack batch, before each
  Progress report, read `$CHANTIER forge-stack show` (GitHub; read only) and take the line from its
  `partial stack mergeable below …` or failing checks: while a check fails (a take is changing the
  stack), the line says `stack changing: last mergeable below <sha7>` with the commit of the last
  report, or `stack changing` when none was told. On GitLab the line names the head of the
  highest MR of the chain that is ready on the forge, read with `glab mr view`.
- In direct mode the same, the Chief of Staff steering.

### Area 7: GitLab

On GitLab the stack stays a chain (no `forge-stack`). The order (Areas 1, 3) applies to the chain
too; the first MR on the default branch is ready, the others drafts, as today. Nothing else
changes there.

### Area 8: when the time will not hold (decision 6)

The time the user gave, and the finding that the batch will not finish by it, are the Chief of
Staff's (the CR batch-duration-plan, backlog P1, adds the floor, the delivery time and its bullet
"When the time will not hold", which points here for the mechanism and adds no step to the
Foreman's or the stack driver's cards). This CR gives those steps, in cards only; no CLI change,
no new order kind.

- **`chief-of-staff.md`**, beside batch-duration-plan's bullet (or, if this CR merges first, in
  "While it runs" after "Reports"): when the delivery time passes the time the user gave, record
  `order note - --note "deliver by <time>"` (it prints the line to send to the Foreman, and a
  restarted Foreman finds it). In direct mode you apply the Foreman's bullet below yourself. You
  tell the user nothing beyond what batch-duration-plan's report says.
- **`foreman.md`**, the stack batch paragraph, one new bullet **Deliver by a time:** on that
  order, until the time:
  - Free slots go first to the CRs that can join the mergeable part by then: those closest to
    `ready` whose dependencies are already in it or ready, short chains before long ones; a CR
    that cannot be ready by then is not started over one that can. You judge which, from each
    CR's state and chain (no estimate tool). No CR already started is stopped.
  - Name the time in the stack driver's take (`take stack --note "deliver by <time>"`).
  - At the time, the stack on the forge is what the user gets: send the `stack-ready … to come:
    …` ask of the stack as it stands if it is not complete and none was sent for it
    (decision 11). Then the batch
    goes on toward the complete stack.
- **`driver.md`**, "Stack driver", one new paragraph: a take whose note names `deliver by
  <time>` keeps the stack on the forge mergeable at that time. Turn ready only what is restacked,
  judged and green at the top before the time; leave the rest a draft on top. Never leave, at the
  time, the stack unstacked or a rebuild half done: a `rebuild` that cannot finish before the
  time is not started. Hand back with the stack as it stands.

## Out of scope

- A CLI tool that orders the stack by itself (the stack driver orders it with `stack`).
- Hand-back timestamps to order CRs found ready at the same take (their planned order decides).
- The docs and README sentences about the stack made once every PR is ready (`README.md`,
  `docs/`, the SVGs, `CONTRIBUTING.md`) and the eval kit: a docs follow-up, as in CR-233.
- `start-on-unready-dependency` (named in the request as going with this CR): its own item.
- GitLab stack delivery beyond Area 7 (`2-backlog/P2/gitlab-stack-delivery`).
- Any merge by an agent: the user merges, as today.

## Order in batch-17, on top of CR-233 and CR-234

Neither branch is merged yet (PR #173 for CR-233, PR #175 for CR-234). This CR goes on top of
both in batch-17's stack (`order add`, decision 1) and is written against them:

- **CR-233 (cards):** it rewrites the paragraphs this CR amends: `foreman.md` (the stack
  driver's start, "until then … like a parallel batch", "After an `order merged`, by mode" with
  its restack / rebase-notes choice), `chief-of-staff.md` ("A stack batch", the plan at the go),
  `concepts.md` (**Ready to merge**, **Stack**), `driver.md` (the stack driver's opening). This
  CR keeps everything CR-233 says about merging one PR at a time and the merged-early case, and
  changes only: the start condition ("all ready or blocked" becomes "two ready PRs"), CRs joining
  as drafts, the restack-or-rebase choice (rebase notes only before the first stack), the merge
  during a take (a note to the running stack driver), and the asks (decisions 4 and 7).
- **CR-234 (`forge_stack.py`):** it adds `UNSTACK_TRIES`, raises `_unstack`'s still-open error
  with exit 4 and a new text, gives `_rebuild` a docstring, and adds scenario steps in 13a. This
  CR edits the same `_unstack` (its `outside` clause only, not the loop or the raise) and the same
  scenario section: keep CR-234's changes as they are and rebase on them.
- **batch-duration-plan (backlog P1, also bound for the end of batch-17's stack):** it adds the
  floor, the delivery time and the `chief-of-staff.md` bullet "When the time will not hold" that
  points to this CR. Area 8 adds the steps that bullet leaves to this CR. Whichever merges second
  puts Area 8's Chief of Staff line next to that bullet, in one wording.
- **batch-duration-plan** also edits `status-layout.md`'s **Notes** (a floor line) and the
  "Reports" bullet: Area 9's line sits beside its floor line; when the time will not hold, its
  "CRs of the partial stack aimed at" and Area 9's line are two lines, the aimed and the actual.
- Its card changes reach the running batch only once merged into the main checkout and reloaded,
  as CR-233's.

## Evidence

**Checks:** `just check` passes (Linux, macOS, Windows); `just lint` within it (each function
under fifty lines, no bare magic number: the two-PR threshold is the Foreman's, not the CLI's).

**Scenario** (`just scenario`, both forges; the CLI and cards change), in `run_scenario.py`
section 13a (`forge_stack_cli`) and its `README.md` list. `record()` gains a status per CR
(`ready` by default for the existing checks, which keep their meaning); `fake_gh.py`'s `drafts`
state already gives the drafts.

1. `a`, `b` ready with PRs, the release `r` with no PR: `forge-stack create` exits 0, posts
   `201 202` only; `show` prints `partial stack mergeable below <b's head, seven characters>
   (#202` and `to come: <r> …`, exit 0 (this
   replaces the check "refused when a stacked CR has no PR recorded").
2. A CR joins as a draft: `new` working with PR 204 (a draft on the fake forge), ordered on top
   with `stack a b new` (the release above, unnamed): `rebuild` unstacks #100, retargets #204 onto
   `b`'s branch, posts `201 202 204`; `show` prints `mergeable below <b's head> (#202`, `drafts on top #204`,
   `to come: <new> working, <r> queued`, exit 0.
3. check 4 against the status: `new` ready with #204 still a draft gives `check 4: still a draft
   #204`; `new` working with #204 not a draft gives `check 4: not a draft #204 (<new> working)`;
   #201 a draft under #202 ready gives `check 4: a draft under a ready PR #201`.
4. `stack a` naming one CR of three: `a` gets order 1, the others keep their relative order above,
   only `a` is `stacked`; `stack <x>` naming a CR whose `after` holds an unnamed open CR is
   refused with `which is not named`.
5. The complete stack: every CR ready with its PR, none a draft, the release on top: `show`
   prints `stack complete, mergeable below <r's head>` and no `to come:` line.
6. No PR at the bottom: `create` and `rebuild` exit 2 naming the CR, `show` prints `check 1: no
   PR at the bottom …`.
7. The insertion, partial-merge and refusal steps (including CR-234's unstack step) still pass,
   adjusted to the stack as it stands (the inserted CR with no PR is to come, then joins).

**Reading pass**, in the PR's Test plan: `rg -n "all ready or blocked|every PR is ready|every open
PR of the batch's stack" skills/chantier/references` finds none; the four cards say the same two
`stack-ready` asks and the silent restack; `status-layout.md` has the `partial stack mergeable
below` line and both `stack-ready` forms name the commit; `rg -n "deliver by" skills/chantier/references` finds
Area 8's rule in `chief-of-staff.md`, `foreman.md` and `driver.md`.

No CI job is added or changed.

## Self-containment for the Driver

Files: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py` (`stack`),
`skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py` (`_plan`, `_unstack`,
`_rebuild`, `_checks`, `_show`, `register`), `skills/chantier/references/driver.md`,
`foreman.md`, `chief-of-staff.md`, `concepts.md`, `status-layout.md`, `scenario/run_scenario.py`,
`scenario/README.md` (and `scenario/fake_gh.py` only if a step needs it). Read CR-233's and
CR-234's specifications in `.agents/changes/4-batch/2-actives/` and work on their merged text.

## Open questions

None: answers 7 to 11 settled them.
