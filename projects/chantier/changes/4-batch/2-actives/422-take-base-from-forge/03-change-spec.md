# Change Specification: take's base and the ready word follow the forge

Short name: `take-base-from-forge`. No issue (origin: verbal; Studio's batch-06 retro, relayed by
its Chief of Staff on 2026-11-20, and chantier's batch-29).

## Goal

In a stack batch, two things the CLI says came from the recorded order of the CRs and were wrong
on the forge:

- **The base `take` prints.** Studio's CR-427 was told to start on CR-351's branch while CR-351's
  PR was already merged on the forge (not yet recorded merged); the Foreman had to tell each Driver
  to start on `origin/main`.
- **The `PR in draft` word and what it waits for.** In chantier's batch-29, CR-391, 392, 407, 408,
  409, 410 and 413 read `PR in draft, waits for <CR>` while their PRs were out of draft on `main`
  and mergeable: the CRs before them in the order were working, with no PR. A stale "PR in draft …
  after CR-425" label went into an ask in Studio the same way.

From now on the base `take` prints leaves out a CR whose PR the forge shows merged, and a ready CR
that the stack driver has not placed reads its word from its PR's base on the forge, not from the
order.

Sources: `intake/request.md`, `02-answers.md` (2026-11-20, Q1 to Q11).

## The network rule (AGENTS.md), settled

The CLI gains **no forge read**. Of the two ways allowed, this CR uses the state the hub and the
record already hold, and the agent passes nothing:

- for the base: the project's journal (`forge-journal.jsonl`), where the forge hub already writes
  a `merged@1` line for each PR of the running batch that the forge shows merged and the record
  does not hold;
- for the word: `pr_base` and `pr_draft` of the CR's entry, which `ship` already records from the
  forge.

Why not a base passed by the agent: it would be an unchecked claim, and one more step for the
Foreman at every take; the journal holds the fact at no call. The read `take` and `handoff`
already make for a stacked CR that has a PR (`commands/forge_base.py`, `stacked_read`) is not
touched.

## Definitions

- **Seen merged:** a CR of the batch for which the journal holds a `merged@1` line that is
  listed (known version, published type, payload accepted: `hub/journal.py`, `_listed`), whose
  `batch` is this batch, whose `cr` is this CR and whose `pr` is the CR's recorded PR link (so an
  old line does not hit a CR that came back with a new PR). Any such line counts, with or without
  `into_cr` or `landed_with`: a PR merged into another CR's branch is merged too, and its branch
  is no base.
- **Placed:** a CR the stack driver named in `stack <cr>…` (`CrEntry.stacked` true).
- **Recorded base:** `CrEntry.pr_base`, the PR's base branch on the forge as `ship` last read it;
  none when never read or when the last read failed.
- **Default branch:** `repo.config["default_branch"]`.

## What changes

All paths are under `skills/chantier/scripts/cli/src/chantier/` unless they start with another
folder.

### 1. The start base leaves out a CR seen merged (`stacks.py`, `hub/journal.py`, `commands/`)

- `hub/journal.py`: a new pure function that returns the ids of the CRs seen merged, from the
  journal's entries, the batch id and the batch's CRs (suggested: `seen_merged(entries, d) ->
  frozenset[str]`). It compares PR links as `board/crs.py`'s `link_of` gives them. It reads
  nothing itself; its caller reads the journal with `journal.read(repo.changes)[0]`.
- `stacks.py`: `start_on_for`, `stack_start` and `start_base` take the set as an optional last
  argument (suggested: `landed: frozenset[str] = frozenset()`), passed down to their helpers
  (`_below_with_pr`, `_nearest_open`, `_open_after`, `_live_start`, `top_cr`, and the series
  predecessor test of `start_base`). For these functions, a CR in the set reads as ended:
  - it is not the nearest CR below with a PR;
  - a `start_on` that names its branch is not live;
  - it is not an open dependency (`after`);
  - in a series batch it is not the open predecessor (the base is the default branch, as for a
    predecessor recorded merged);
  - it is not the release's top CR.

  With an empty set every function returns what it returns today. `stacks.py` must not import
  `hub.journal` (`hub/batch_prs.py` imports `stacks`): the callers pass the set.
- `stack_base`, `off_place`, `to_come`, `chain`, `next_merge`, `stack_due` and every caller other
  than the two below pass no set: the views, `stack`, `forge-stack`, `carry` and the rails read
  the record as today, and follow at `order merged`. With the same set, `start_base` and
  `stack_base` still come from `stack_start` (the invariant of `tests/test_stack_base.py`).
- `commands/driver.py`, `take`: read the journal once, compute the set, and pass it to
  `start_on_for` where the first take records `start_on` (`if c.status == "queued" and (start_on
  := start_on_for(d, c))`). The rails (`check_take_all`: a slot, the budget, a dependency not
  `ready`) do not read the set: a CR whose dependency is seen merged and not recorded merged is
  refused or taken exactly as today.
- `commands/facts.py`, `_base_of` (the `worktree: … base <ref>` line of `take` and `handoff`):
  for a CR with no forge read (`stacked_read` returns None), print `start_base` computed with the
  set. `cr_facts` gets the set from its caller or reads the journal itself; the Driver chooses,
  with one journal read per command.
- A new line in `cr_facts`, right after the `worktree:` line, only when the set changed the base
  (`start_base` with the set differs from `start_base` without it):

  `base: not <CR>'s branch: the forge shows its PR <link> merged, not recorded yet (order merged <CR>)`

  `<CR>` is the owner of the branch `start_base` gives without the set. The line is part of the
  facts the Driver's prompt block copies (`_cr_driver_block` takes `facts[2:]`); it is absent in
  every other case, so today's outputs do not change.
- With no journal file, or no line for the batch, nothing changes and nothing is refused. The CLI
  makes no call to a forge for this.
- `core/records.py`: the comment on `start_on` says "the nearest earlier CR with a PR not seen
  merged on the forge".

### 2. A ready CR not placed reads its word from its PR's base (`stacks.py`)

`ready_word(d, c, repo)`. The first tests stay: not `ready` gives None; no PR gives `ready
locally`; `pr_draft` not False, or a held CR, gives `PR in draft`. Then, for a CR of the chain:

- **Placed, or a release, or no recorded base:** today's rule, unchanged: `ready to merge` when
  every CR under it in `chain` is out of draft (`_out_of_draft`), else `PR in draft`.
- **Not placed, not a release, with a recorded base:**
  1. the base is the default branch: `ready to merge`;
  2. the base is the branch of a CR of the batch that is not ended and not held: `ready to merge`
     when that CR reads `ready to merge` by this same function, else `PR in draft` (a walk that
     meets a CR twice stops with `PR in draft`);
  3. the base is the branch of a CR recorded `merged`: today's rule (the chain), since the forge
     retargets the PR when the branch under it goes and the record's base is then one `ship` late;
  4. any other base (a cancelled or held CR's branch, a branch of no CR): `PR in draft`.

A CR outside the chain (a fix, a parallel or series batch) keeps today's rule
(`pr_base_of(d, c, repo) == default`).

`draft_waited(d, c, repo)`, for the same split:

- held: the hold's text, as today;
- **not placed, not a release, with a recorded base:** base on the default branch: None (`its
  turn out of draft`), never a CR of the recorded order; base on an open CR's branch: that CR
  while it does not read `ready to merge`, else None; base on a merged CR's branch: today's rule;
  any other base: as today (the CR whose branch it is, else the branch);
- placed, a release, or no recorded base: today's rule, unchanged.

`draft_clause`, `draft_waits`, `state_word`, `pr_base_of`, `_check_out_of_draft` and the texts
they print keep their form. Everything that reads the word follows with no change of its own:
`status/words.py` (`state_label`, `notify`), `commands/delivery.py` (the hand-back line),
`board/crs.py`, `hub/batch_prs.py` (`to_review`, so the hub's `checks-red@1` covers these CRs
too), `STATUS.json`'s `readiness` and `label`. No field is added, renamed or removed; no label
takes a new form.

Effect on the two retro cases: CR-407 (not placed, `pr_base` `main`, out of draft) reads `ready to
merge` with a working CR before it in the order; a draft PR on `main` reads `PR in draft, waits
for its turn out of draft`, never "after" a CR it does not sit on.

Known limit, to state in the PR's Known gaps: the word is as fresh as the last `ship`. A PR
retargeted on the forge with no `ship` after it reads from the old base until the next `ship`;
the cards already ask for a `ship` after every change of draft state or base.

### 3. Cards (`skills/chantier/references/`)

- `concepts.md`, "Words":
  - **Ready to merge:** "in a stack batch, with every CR under it ready to merge too" gains what
    "under it" means: for a CR the stack driver placed, the CRs below it in the stack's order; for
    a CR not placed yet, the CR whose branch its PR's base is on the forge, as `ship` last read it
    (none when that base is the default branch). The recorded order alone never holds back a PR
    that is out of draft on the default branch.
  - **PR in draft:** its "waits for what is under it" list starts the same way: a CR not placed
    whose PR is a draft on the default branch waits for its turn out of draft, not for a CR of the
    order.
- `concepts.md`, "Batch modes", **Stack** (the sentence "on the nearest earlier CR of the batch
  (by order) that already has a PR") and **Dependencies** (the same words): add "and whose PR the
  forge does not show merged (a `forge saw merged` line of the journal)".
- `foreman.md`, the stack-batch bullets ("`take` starts every new CR on the nearest earlier CR
  with a PR (the CLI computes it; you choose nothing)"): add that `take` leaves out a CR the
  journal shows merged and prints the `base:` line naming it; the Foreman passes that base
  unchanged, never corrects a base by a take note, and the `order merged` the line names stays
  the Chief of Staff's. In the paragraph "until the first stack is made it runs like a parallel
  batch": say that the CLI now reads such a CR `ready to merge` (the ask is `ready-to-merge`
  with no remark on the record).
- `driver.md`, "In a stack batch the `base` that `take` prints may be another CR's branch: the
  nearest earlier CR of the batch that has a PR": add "that the forge does not show merged", and
  one sentence on the `base:` line (it explains the base; the worktree goes on the base the
  `worktree:` line names).
- `chief-of-staff.md`, `status-layout.md`, `routing.md`: no change (the three words and their
  icons keep their meaning for the user).
- `agents/` and `com.github.copilot/agents/`: no change.

### 4. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

New checks; none of the existing checks of the start-base step (the `start_on` checks) or of step
13b changes its expected result, since step 13b's CRs are placed by `stack a b c`.

In the start-base step, a stack batch, the `merged@1` line written by the hub's cycle on the fake
forge as the scenario's hub steps already do (never a line typed by the test):

1. CR `a` working with a PR, its PR merged on the fake forge, the hub's cycle run, no `order
   merged` yet: `take b` records no `start_on`, prints `worktree: … base origin/main` and the
   line `base: not <a>'s branch: the forge shows its PR <link> merged, not recorded yet (order
   merged <a>)`; `handoff b` prints the same two lines.
2. With an earlier CR `z` that has an open PR below `a`: `take b` records `start_on` = `z`'s
   branch and prints it as the base, with the `base:` line naming `a`.
3. After `order merged a`: `handoff b` prints the same base and no `base:` line.
4. With no journal line (the PR merged on the fake forge, no hub cycle): `take` prints `a`'s
   branch as today, and no `base:` line.
5. During 1, `status` and `stack` still show the record's plan (no crash, `a` still listed).

In step 13b, a new stack batch with **no** `stack <cr>…` call (CRs not placed), `a`, `b`, `c` in
that order:

6. `a` working with no PR; `b` shipped out of draft on `main` and handed back: the hand-back line
   starts `hand-back ready to merge`, `readiness` is `ready to merge` in the CR's and the batch's
   `STATUS.json`, the label draws 🟢 (today: `PR in draft, waits for <a>`).
7. `c` shipped as a draft on `main` and handed back: `PR in draft`, the clause ends `it waits for
   its turn out of draft`, the label reads `waits for its turn out of draft`.
8. `c`'s PR put on `b`'s branch on the fake forge, out of draft, shipped: `ready to merge` while
   `b` is; `b` turned back to a draft and shipped: `c` reads `PR in draft` and waits on `b`.
9. `c` with `pr_base` dropped from the record (an old record): today's rule, `PR in draft` and it
   waits on `a`.
10. `stack a b c` then run on that batch: the three read by the chain's rule again (`b` and `c`
    `PR in draft` over `a`, which has no PR).

`scenario/README.md`: its lines on the start base ("a CR starting on the nearest earlier CR with
a PR") and on the three words name the two new rules.

### 5. Tests (`skills/chantier/scripts/cli/tests/`)

Few and parametrized, in-process, no new slow test (`just test` stays within its budget):

- `test_stack_base.py`: one parametrized test of `start_base` and `stack_start` with a `landed`
  set (the nearest CR below in the set, a live `start_on` whose owner is in the set, an open
  dependency in the set, an empty set equal to today's result), and one of `ready_word` with
  `draft_waits` for the cases of section 2 (placed and not placed; base default, an open CR's
  branch ready or not, a merged CR's branch, a branch of no CR, no base; a two-CR loop of bases).
- One test of `seen_merged` with the published example of `merged@1` (`schemas.PUBLISHED`): the
  batch, the CR and the PR link must match; a line of another batch, of another PR link, of a
  newer version or with a refused payload does not count.
- Fix any existing test that asserted the old word for a CR not placed (grep `ready_word`,
  `PR in draft`, `waits for` in `tests/` and `hooks/register.test.tsx`; the hook's tests build
  their own labels and should not move).

## Out of scope

- Any new forge read in the CLI, in `take` or elsewhere, and any `--base` given by an agent.
- The base on a working CR's open draft PR (Studio's CR-429): unchanged, the user's answer
  stack-Q4 of 2026-11-17; filed apart as `1-inbox/take-base-on-working-draft`.
- The word of a placed CR, of a release, of a fix, and of a CR in a parallel or series batch.
- `stack_base`, `off_place`, `forge-stack`, `stack --out-of-draft|--draft`, `carry`, the board's
  base column (`board/crs.py`, `base_of`) and the rails: they read the record as today.
- The journal's types and the hub's cycle: no new line, no new read, `merged@1` unchanged.
- Recording a merge: still `order merged`, by the Chief of Staff.
- AGENTS.md's sentence on the CLI's network reads, which does not name the forge reads `ship`,
  `take`, `handoff` and `forge-stack` make today: filed apart as
  `1-inbox/agents-md-names-cli-forge-reads`.
- `hooks/`, `types/`, the web client: no change (no `just mod`; no screenshot of the pane owed,
  since no `STATUS.json` field and no label form changes; if the Driver does change a label's
  form, AGENTS.md's screenshot rule applies and the PR's Known gaps names it).

## Evidence

- `just check` green in the worktree at the pushed head (Linux, macOS and Windows in CI).
- `just eval-dry-run` green there (the change is under the CLI's `src/`).
- `just scenario (ubuntu-latest)` green at the PR's head, with checks 1 to 10 above; locally on
  Windows (`chantier gate`) when this CR is on top of its batch's stack.
- `just test` within its time budget.
- Every existing check of the start-base step and of step 13b passes with its expected result
  unchanged; a check whose expectation had to change is named in the PR with its reason.
- A grep in the PR's body: no new call of `gh`, `glab`, `connectors.read`, `pr_state` or
  `read_state` in the diff of `stacks.py`, `commands/driver.py`, `commands/facts.py` and
  `hub/journal.py`.
- No host or default matrix: nothing here depends on the host or on a configured value. No CI job
  is added or changed. No check guards a shipped file's content.

## Open questions

None.
