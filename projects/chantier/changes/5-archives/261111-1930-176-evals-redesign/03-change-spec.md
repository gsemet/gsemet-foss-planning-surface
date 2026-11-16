# Change Specification: the eval campaigns, redesigned

Written 2026-11-11 from `intake/request.md` and `02-answers.md` (answers 1 to 5).

## Goal

In the user's words: "il faut un eval real en direct et un en foreman", "on redesign les evals
et on merge tout pour avoir un design propre", and Copilot is left "dans son coin".

After this CR, `evals/` has four campaigns and one way to judge them:

- `real-foreman`: today's `real`, renamed (real CRs on this repository, Foreman mode).
- `real-direct`: the same, steered by the Chief of Staff in direct mode, in a new session of its
  own that the user starts with a given prompt.
- `claude-planted`: `claude-smoke` and `claude-full` merged into one campaign. It covers the
  failures a real run does not produce.
- `copilot`: unchanged.

Every report has the same **scorecard**. It lists chantier's rails, and each run marks every rail
seen and right, seen and wrong, or not seen. It also gives the cost and the steering share, so two
runs can be compared line by line. The audit (`evals/kit/audit.py`) also runs on the real
campaigns and fills the part of the scorecard it can check. The rest is read by hand.

## Depends on

`3-ready/worker-write-guard-redesign` merges first. Its piece 7 adds to `evals/kit/audit.py` the
check that each worker's prompt holds a `writes:` line, and its piece 5 makes the steering session
look at `git status` before each report. Two scorecard rails come from those pieces (J12, J13
below), and the real-campaign audit builds on that check. This need is real, not just a shared
file.

## What changes

All the changes are in `evals/`, plus the eval paragraphs of `README.md` and `CONTRIBUTING.md`.
Nothing changes in the CLI (`skills/chantier/scripts/cli/`), the cards, the agents, the hooks or
the scenario.

### 1. The campaigns' folders (answer 1)

- `git mv evals/real evals/real-foreman`. The runbook's title becomes `# real-foreman`.
- New `evals/real-direct/RUNBOOK.md` (section 3).
- New `evals/claude-planted/RUNBOOK.md` (section 4). `evals/claude-smoke/` and `evals/claude-full/`
  are deleted (`git rm`); their content moves into it.
- `evals/copilot/RUNBOOK.md`: not touched. It still links to `../README.md#run-a-campaign`, so that
  anchor must still exist. It still runs `setup.py copilot`, so that key stays as it is.
- `evals/results/`: no file is renamed or edited. The past reports keep their names
  (`real-2026-11-05*.md`, `claude-smoke-*.md`, `claude-full-*.md`). Their links (`../README.md`
  and absolute GitHub links) keep working. `evals/README.md` says in one line that a report named
  `real-*` is a `real-foreman` run, and one named `claude-smoke-*` or `claude-full-*` is a
  `claude-planted` run, from before the merge.
- New report names: `results/real-foreman-<date>.md`, `results/real-direct-<date>.md`,
  `results/claude-planted-<date>.md`.
- Batch names go from every runbook (`| Batch | smoke |`, `full`): `open` numbers the batch
  (`batch-<n>`), and a batch has no name.

### 2. `evals/real-foreman/RUNBOOK.md` (answers 1, 3, 4, 5)

Today's `real/RUNBOOK.md`, with these changes:

- **CRs (answer 4):** 1 to 5 real, small items from the inbox (`.agents/changes/1-inbox/`). The
  Chief of Staff picks them, with the user's go. Each goes through the usual grill and
  Spec-writer before `open`, like any CR. They are not invented defects. The user decides what
  happens to their PRs.
- **Open:** `$CHANTIER open <A> <B> … --mode parallel --default-branch main --slots 3 --budget 20`,
  as today.
- **Start:** the prompt the user types in a new Code session of the Claude Desktop app, opened on
  this repository's main checkout, on `main`:

  ```text
  /chantier:chief-of-staff Run the chantier eval campaign real-foreman: follow evals/real-foreman/RUNBOOK.md.
  ```

  The operator is that session, a Chief of Staff in Foreman mode. Here the user is the real
  user: the go, the item picks and the PR decisions are theirs. The operator does not play them.
  The host's limits of `evals/README.md` (10 messages per session, the go typed in the desktop
  app) still hold.
- **Nothing merges during the run:** the section "Nothing merges" stays word for word, including
  the PR body's first line `**Eval run: do not merge.** The maintainer decides what happens to
  this PR.`. The run ends when every CR is `ready` (or `blocked`, with its reason) and nothing has
  merged.
- **Audit and report (answers 2, 3):** before any merge, any `pause` or any `close`, run
  `uv run --no-project python evals/kit/audit.py <this checkout> --real` (section 6), then
  `$CHANTIER cost --explain` and `$CHANTIER cost --by cr`. Write the report with the scorecard
  (section 5). Write it in a worktree of this repository, on its own branch, and open its PR: the
  main checkout changes neither its files nor its branch during the eval (AGENTS.md).
- **After the report (answer 5):** each of the run's PRs is merged or closed **within the day**,
  so a real CR opened as a "do not merge" draft does not go stale. Merged by the user:
  `$CHANTIER order merged <cr>`. Closed: `$CHANTIER order drop <cr>`. The Chief of Staff sends the
  line to the Foreman, as usual. Then the Foreman pauses the batch, the Chief of Staff gives the
  Completion report, and `close` comes on the user's word. Until then no other batch can open
  (`open` exits 2), so the next real campaign waits for this one to close.
- The "Check" section becomes the list of what the audit checks and what is read by hand
  (sections 5 and 6). The sentence "`evals/kit/audit.py` does not apply" goes.

### 3. `evals/real-direct/RUNBOOK.md` (answer 1, the start prompt)

The same campaign as `real-foreman`, steered in **direct mode**. The runbook does not repeat the
text both real campaigns share: it says "as [real-foreman](../real-foreman/RUNBOOK.md), except"
and lists only the differences.

- **Start:** a new Code session of the Claude Desktop app on this repository's main checkout, on
  `main`. The user pastes:

  ```text
  /chantier:chief-of-staff direct Run the chantier eval campaign real-direct, in direct mode: follow evals/real-direct/RUNBOOK.md.
  ```

  From a terminal, at the root of the main checkout, the equivalent is:

  ```text
  claude "/chantier:chief-of-staff direct Run the chantier eval campaign real-direct, in direct mode: follow evals/real-direct/RUNBOOK.md."
  ```

  The words "in direct mode" repeat the skill's `direct` argument. `chief-of-staff.md` takes
  either one ("invoked with `direct` or the user said so").
- **The session is new and its own.** It is not the Chief of Staff session that already runs
  this repository's backlog, and it is not a Foreman session. It is the steering session
  (`chief-of-staff.md`, "Steering a batch yourself"): it runs `preflight --direct`,
  `open --direct`, claims its epoch, renames itself `[env] Project [Chief of Staff - Batch <nn> -
  Direct]`, starts the Drivers itself and arms the heartbeat.
- **Open:** the `real-foreman` line plus `--direct`.
- **The host's limits:** no Foreman session, so no message between Desktop sessions. The
  10-message limit does not apply to the batch. The runbook says this.
- **What it proves on top of real-foreman:** the direct-mode lines that `hosts/claude-code.md`
  marks unproved (a Driver's `SendMessage` to `main`; the heartbeat in the Chief of Staff's own
  session), the `Chief of Staff, steering the batch` cost row, a refused force push judged and
  run by the Chief of Staff with the Driver told by note (CR-170, if one happens), and `order qa`
  refused while the batch runs. The report names each unproved host line it saw work.
- **Audit:** `audit.py <this checkout> --real`. The batch's `steering` is `direct`, and the audit
  reads the Chief of Staff's transcript as the steering session (section 6).
- **After the report:** as in real-foreman (answer 5), but with no Foreman. The Chief of Staff
  records `order merged`/`order drop` and acts on them itself, then pauses with `pause --epoch
  <n>`, gives the Completion report, and closes on the user's word.

### 4. `evals/claude-planted/RUNBOOK.md` (answer 1)

One campaign on the fictional `tasks-cli` project, with the planted failures a real run does not
produce: a red CI from the product, the round limit, a question for the user, and a release with
its fix, grant and approvals. Rebases, a change order, CRs added on the way and QA come along with
these.

- Its content is today's `claude-full` (same CRs A to F, R, V, same turns, same "Expected"). It
  also keeps `claude-smoke`'s checks that `claude-full` does not already state: one docs reviewer
  after the Inspector approves; on B (`done-unknown-id`), CI green on the first run.
- `evals/kit/setup.py`: the `claude-smoke` and `claude-full` keys become one key,
  `claude-planted`, with `claude-full`'s values. `copilot` stays. An unknown campaign is still
  refused with the list of keys.
- Stage: `uv run --no-project python evals/kit/setup.py claude-planted <workspace>`. Start in a
  new Desktop Code session on this repository, on the branch under test:

  ```text
  Run the chantier eval campaign claude-planted: follow evals/claude-planted/RUNBOOK.md.
  ```

- Every command in its turns and its "Expected" is checked against the current CLI (`$CHANTIER
  <command> --help`), since `claude-full` was last run on 2026-11-04. That was before `verdict`,
  the two-gate `handback ready`, the multi-command `gate`, the worker write guard, the force-push
  route and direct mode. Each "Expected" line states the current rule (for example: no
  `handback ready` without a passed long gate and a `VERIFIED` verdict at the PR's head).
- Cost and time: those of `claude-full` (about $15, 3 h; $25 budget), stated in the table.
- It plants nothing new: no planted write-guard refusal (out of scope of
  `worker-write-guard-redesign`, its answer 6) and no planted force push.

### 5. The scorecard (answer 2)

- New `evals/SCORECARD.md`: the single list of rails, one table row per rail. Columns: `id`
  (stable, never reused or renumbered; a retired rail stays as a row marked "retired"), `rail` (one
  sentence), `from` (the card or the CLI command that holds it), `where seen` (`real-foreman`,
  `real-direct`, `claude-planted`, `copilot`), `how marked` (`audit` with the check's text, or
  `by hand`).
- The marks are `seen, right`, `seen, wrong` and `not seen`. `seen, wrong` names the evidence (the
  event, the command, the transcript line). `not seen` is never a failure: the situation did not
  come up.
- Below the table, two lines every report fills: the **cost** (total, `cost --by cr`, the
  `cost --explain` breakdown) and the **steering share**, which is the steering row's cost (the
  Foreman's line; in direct mode `Chief of Staff, steering the batch`) divided by the batch's
  spend, as a percentage. A figure the CLI could not price is written `not measured` or
  `unknown`, never `$0.00` (`status-layout.md`, Cost).
- The starting list, the CLI's refusals first, then the cards' judgements. Write each row from
  the code and the card it names. The Driver checks every row against them, corrects the wording,
  and adds a rail it finds in them that is missing here. It removes none.

  | id | rail | from |
  | --- | --- | --- |
  | C1 | `take` refused with no free slot | `rails.check_slot` |
  | C2 | `take` refused while a CR's dependencies, or the release's other CRs, are open | `rails.check_take`, `waits_for` |
  | C3 | `take`, `round` and `order qa` refused past the budget (exit 5), then `blocked budget:` | `rails.check_budget`, driver.md |
  | C4 | `round` refused past the round limit (exit 5), then `blocked rounds:` | `rails.check_round`, driver.md |
  | C5 | `gate`: one argument per command, one long gate at a time in the repository, recorded with its head | `commands.gate` |
  | C6 | `verdict` refused on a worktree with uncommitted work, bound to the head | `commands.verdict` |
  | C7 | `handback ready` refused without a recorded PR, a passed long gate at the head (or `--no-gate` quoting a project rule, which the steering session checks) and a last verdict `VERIFIED` at the head | `commands.handback`, driver.md, foreman.md |
  | C8 | `ship` says what is off: uncommitted work, a head not pushed, no gate at the head | `commands.ship` |
  | C9 | every steering command carries its epoch; a stale epoch is refused (exit 3) | concepts.md, the CLI |
  | C10 | the heartbeat: `status --refresh --epoch` records it while a Driver runs; it ends after `pause` or on an idle wake | hosts/claude-code.md, foreman.md |
  | C11 | `release go`: an irreversible action waits for `go` (or the grant) | `rails.release_go` |
  | C12 | the Foreman merges only the release and its granted fixes, and records each with `order merged --epoch` | `rails.fix_go`, `check_granted_fix` |
  | C13 | `order qa` refused while a direct batch runs | `commands.order` |
  | C14 | `pause` refused while anything is live; `close` refused unless paused, and prices the final cost | `commands.pause`, `close` |
  | J1 | each agent starts with a `chantier <role>` prompt, its card and `$CHANTIER rules` | concepts.md |
  | J2 | a Driver is started by the steering session, a worker by a Driver | concepts.md |
  | J3 | a Driver writes no code; workers never commit, push or merge; read-only roles write only their notes and proof; workers create no worktree (except the Verifier's detached one) | driver.md, worker.md |
  | J4 | a Driver creates its worktree, rebases before the gate, pushes with a lease or a first upstream (never `--force`), and stages explicit paths | driver.md |
  | J5 | a CR's PR opens as a draft and turns ready only on the default branch, with no auto-merge and CI green at its head; in a real campaign its first line is the eval line | driver.md, real runbooks |
  | J6 | the Driver reads CI with the forge's CLI and judges it: a product red is a round, with a Debugger when the cause is not plain | driver.md |
  | J7 | a Verifier at the pushed head records the verdict; the evidence is in the PR's Deliverables | driver.md, worker.md |
  | J8 | an Inspector's `FIX-REQUIRED` on code is a new round; on `pr-body.md` alone it is not | driver.md |
  | J9 | a decision only the user can take is `blocked question:`, and the answer goes to a new Driver | driver.md, chief-of-staff.md |
  | J10 | after a merge, a ready PR in conflict goes back to a Driver with a `rebase:` note | foreman.md |
  | J11 | a refused force push: the Driver sends the `push` line and waits; the Chief of Staff checks the branch is the batch's, judges, runs it without asking the user, and reports one line | driver.md, chief-of-staff.md, status-layout.md (CR-170) |
  | J12 | each worker's prompt holds a `writes:` line; a guard pass shows its note on the board | worker-write-guard-redesign, pieces 1, 2, 7 |
  | J13 | the steering session looks at `git status` before each report: nothing written in the main checkout outside the planning folder | worker-write-guard-redesign, piece 5 |
  | J14 | the steering session reads the project's rules, removes the merged CRs' worktrees, writes the retro and pauses | foreman.md, chief-of-staff.md |
  | J15 | under the host's message limit, a refused send is reported, never sent another way | hosts/claude-code.md |
  | J16 | the Progress and Completion reports keep the format of `status-layout.md`, with the cost lines as printed | status-layout.md |
  | J17 | each plugin agent stays within its context window | the plugin's agents |

- `evals/README.md`, "The report": the template gains a `## Scorecard` section after "Findings".
  It holds every row of `SCORECARD.md`, in its order, with its mark and evidence, then the cost
  and the steering share. "Numbers" gains the steering share. The audit's output gives its rows
  ready to paste.

### 6. The audit on every campaign (answer 3)

`evals/kit/audit.py`. It still only reads and changes nothing. It runs before `close` (it needs
`4-batch/batch.json`).

- **The real campaigns:** `audit.py <checkout> --real` reads this repository's batch. There is no
  local forge, no `.origin.git` and no `state.calls`.
  - **The log and the cost:** it reads the batch's `events.jsonl` (what `log <cr>` shows) and runs
    the CLI's `cost` and `cost --by cr` from the checkout. A `cost` that fails is printed with its
    exact text, and the scorecard's cost says `not measured`: no figure is made up.
  - **The forge, read-only:** for each recorded PR, `gh pr view <link> --json` gives the draft
    state, base, auto-merge, body's first line and checks at the head. It checks J5 and confirms
    that nothing merged. It never writes to the forge.
  - **The end state of a real run:** the batch is running, every CR is `ready` or `blocked` (each
    blocked one with its reason), and no `order merged` was recorded. The staged campaigns' checks
    that need a merge or a pause (`paused`, `3-done`, worktrees removed) are not run in this mode.
    Their rails are `not seen`.
  - **The main checkout:** the check "nothing written outside `.agents/changes/`" compares
    against the checkout's `git status --porcelain` at `open`, which the runbook has the operator
    save in the batch's folder. A path that was already dirty before the run is not a finding.
  - **Direct mode** (`batch.json` `steering: direct`): the steering transcripts are the Chief of
    Staff's, from its claim on (`foreman_transcripts`). Agents it started outside the batch (a
    Spec-writer, an explorer, a Griller's work) are listed apart and not audited as batch agents.
    A force push it runs on a Driver's `push` line is the J11 route, not a breach of "the steering
    session never pushes".
- **Every campaign:** each check names its rail id from `SCORECARD.md`. After the PASS/FAIL lines
  the audit prints the scorecard table, read from `SCORECARD.md` so the list exists in one place.
  For each row with an audit check: PASS is `seen, right`, FAIL is `seen, wrong`, and a check with
  nothing to look at (no event of that kind) is `not seen`. Rows marked `by hand` are printed
  blank, for the operator. The audit exits 1 if a check names an id that is not in `SCORECARD.md`,
  or if an `audit` row has no check. The exit code still follows the FAIL lines.
- `claude-planted` and `copilot` keep today's checks (and piece 7's), with their rail ids.

### 7. `evals/README.md`, `README.md`, `CONTRIBUTING.md`

- `evals/README.md`: the opening paragraph and the campaigns table name the four campaigns (cost,
  last run). `real-foreman`'s last run is the 2026-11-05 report. `real-direct` says "not run
  yet". `claude-planted`'s last run is `claude-full`'s 2026-11-04 report, marked "as
  claude-full". The example prompt becomes `claude-planted`. "Run a campaign" is for the staged
  campaigns (`claude-planted`, `copilot`), and says the real campaigns follow their runbooks. The
  limit text that names `claude-full` names `claude-planted`. Add the scorecard and the line on
  old report names. The `#run-a-campaign` anchor stays.
- `README.md` lines 483-484: the campaigns listed are `real-foreman`, `real-direct`,
  `claude-planted` and `copilot`.
- `CONTRIBUTING.md` lines 115-118: the campaigns and when to run each (see open question 2 for
  the old `claude-smoke` use).

## Out of scope

- Copilot: its runbook, its `setup.py` key and its audit part (see open question 3 for its report).
- The CLI, the cards, the agent files, the hooks, `scenario/` and `tests/`. `just scenario` is not
  needed (AGENTS.md: docs and the eval kit only).
- Running any campaign. The first `real-foreman`, `real-direct` and `claude-planted` runs are
  later work.
- Rewriting or renaming past reports.
- New planted failures, and a planted write-guard refusal.
- The planning-folder files that cite `evals/real/RUNBOOK.md` (see open question 1).

## Evidence

The Driver's proof, in `evidence/`:

1. **Links:** a one-off check (not committed) that every relative Markdown link in
   `evals/**/*.md`, `README.md` and `CONTRIBUTING.md` resolves, `#run-a-campaign` included.
   Output saved.
2. **No old names left:** `grep` for `evals/real/`, `real/RUNBOOK`, `claude-smoke` and
   `claude-full` outside `evals/results/` and `.agents/` shows only the line on old report names.
   Output saved.
3. **Setup:** `setup.py claude-planted <tmp>` stages 8 CRs in `2-backlog/P1/` and both review
   steps in `AGENTS.md`. `setup.py claude-smoke <tmp2>` is refused with the list of keys.
   `setup.py copilot <tmp3>` still stages. Outputs saved; the temporary folders are removed.
4. **The audit, staged mode:** on a batch folder from `just scenario --keep` (or one the Driver
   builds), it prints the PASS/FAIL lines with rail ids and the scorecard table. A check renamed
   to an unknown id makes it exit 1. Outputs saved.
5. **The audit, real mode:** on a batch folder shaped like a real run (running, CRs `ready`, a
   `steering: direct` variant), with `gh pr view` on one existing PR of this repository
   (read-only), it prints J5's row and the `not seen` rows for merge and pause. A failing `cost`
   gives `not measured`. Outputs saved.
6. **Runbook commands:** every `$CHANTIER` command in the three new runbooks, checked against
   `--help`. The list is saved.
7. `just check` passes.

The Inspector checks:

- `SCORECARD.md` and the audit's rail ids match.
- Every decision of `02-answers.md` is in the runbooks.
- `copilot/` is untouched (`git diff --stat`).
- No file in `evals/results/` is changed.

## Answers carried

| Answer | Where |
| --- | --- |
| 1, three campaigns, copilot as it is | sections 1, 2, 3, 4 |
| 2, one scorecard per rail, cost and steering share | section 5 |
| 3, an automatic audit for the real campaigns, the rest by hand | section 6 |
| 4, real small inbox items, picked with the user's go, PRs the user's | section 2 (and 3 by reference) |
| 5, each PR merged or closed within the day after the report | sections 2 and 3, "After the report" |

## Settled decisions

The open questions the spec-writer raised are settled in `02-answers.md` (answers 6 to 12, by a
Fable advisor on the user's delegation). Where they differ from the sections above, they win:

- `handback-after-rebase` and `heartbeat-odd-values` run in `real-foreman`; `real-direct` then
  takes fresh items. The Chief of Staff updates their `evals/real/` citations in the planning
  folder after this CR merges, before `open` (answer 6).
- `CONTRIBUTING.md`: both real campaigns before a release; one real campaign with one small CR,
  in the mode the change touched, after a change to a role or the flow; `claude-planted` after a
  change to how a batch handles failures; `copilot` for Copilot's mechanics (answer 7).
- Copilot's runbook, report and audit stay as they are: `evals/README.md` says the scorecard
  applies to the three Claude campaigns; no `copilot` value in `SCORECARD.md`'s "where seen", and
  no rail ids on Copilot's audit checks (answers 8 and 11).
- A real campaign may take any small real item not yet implemented, from the inbox, the backlog
  or `3-ready`; a specified one skips the grill (answer 9).
- A CR still blocked at the report is kept for a later batch, its reason in the report; the
  Driver checks what `close` does with a blocked CR and writes the runbook step from that
  (answer 10).
- No audit exit on an `audit` row without a check and no "retired rows" rule: the Inspector
  checks that `SCORECARD.md`'s ids and the audit's match (answer 12).

## Open questions

None.
