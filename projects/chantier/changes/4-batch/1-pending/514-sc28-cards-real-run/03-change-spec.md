# SC28: The real run of the new cards, measured for the merge

Child 28 of 28, the last child, of the program `simplify-cards-and-prompts`. These rank above
this specification, in this order:

1. the program's `03-change-spec.md`: "Child 28", "Rules for every child", the merge rule,
   "Cost", "Pending items" and "Evidence for the program";
2. its `02-answers.md`: answers 9, 14 and 17 to 22, and F4, F6, F11, F17 and F20;
3. its `work/study-behaviour.md` (the M rules) and `work/study-fable-v2.md`.

This is for one Driver and one PR, in the running stack batch (batch-31). It is the top of the
stack.

Code read: `origin/main` at `8a960d34` (chantier 0.15.1), plus the specifications of children 1
to 27, which sit below it in `4-batch/1-pending/` (CR-487 to CR-513). Short forms:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `references/` is `skills/chantier/references/` (after child 24's swap, the only card set);
- `<top>` is this CR's worktree: the stack's top, at this PR's head.

Issue: none (a child of the program; no tracker issue).

## Goal

The owner's words (answers 1 and 14): the cards get much smaller, and no behaviour is lost. The
real-run measure and the quiz pass before the swap, and the swap merges with nothing in between.

Children 19 to 27 rewrite, swap, review and gate the cards. Each is validated on paper only: by
tests, the quiz of its own roles, brief sizes and a row inventory. This child is the one real run.
It does five things:

1. It prepares a sandbox campaign that runs the new cards: the plugin, the CLI and the eval kit
   all come from `<top>`, and the main checkout is not touched. Only the user starts the
   campaign (F6, floor rule 7).
2. It measures that run role by role against child 5's 0.15.1 baseline, on the program's eight
   figures.
3. It runs the quiz on every role, old cards and new side by side, under F4.
4. It closes the items that children 19 to 27 left for it: the budgets' `pending_owner` rows,
   the owner lists, the brief measure and the defaults to confirm.
5. It writes the one report the owner reads to decide whether children 19 to 28 merge as one
   unit.

The CR is handed back twice:

- **Round 1** (now): the plumbing, the quiz and the measures that cost no campaign. It is handed
  back validated, with the Known gap "campaign not run: waits for the user".
- **Round 2**: after the user's campaign, the measure, the results and the decision report.

## Place in the chain

- **Base: child 27's branch** (`sc27-card-gates-process`, CR-513), the stack's top before this
  CR joins. The Driver rebases on it before the first push.
- **Relied on below it.** If one of these is missing at the base, the Driver stops and says so.
  There is no stand-in.
  - **Child 5 (CR-491):**
    - `evals/kit/behaviour.py` with `--since`, `--folders` and `--out`;
    - `just behaviour`;
    - the fixture `evals/kit/behaviour-fixture/` and the dry-run case `behaviour`;
    - the committed baseline `evals/results/behaviour-<date>-v0.15.1.json` and `.md` (window
      from 2026-11-17).
  - **Child 6 (CR-492):**
    - `evals/kit/quiz.py` and `just quiz`, with `--cards`, `--case`, `--model`, `--max-usd`,
      `--plan`, `--against` and `--save`;
    - the cases in `evals/quiz/<role>/`;
    - the committed baseline files `evals/results/quiz-<date>-baseline-old-cards-<role>.json`.
  - **Child 7 (CR-493):** `chantier help <topic>` and `references/topics.json`.
  - **Child 10 (CR-496):** `chantier brief <role> [<unit>] [--cards <folder>]`.
  - **Child 13 (CR-499):** `chantier msg`. Its lines read "msg: seq <n> <kind> from <unit> to the
    Foreman (batch-N): delivered to its watcher" on success, and "not delivered: no watcher
    subscribed" (exit 2) on failure.
  - **Child 24 (CR-510):**
    - the swap: `references/` holds the new cards, and the quiz boots from `brief`;
    - `--cards <ref>` still works for a pre-swap ref, whose tree holds
      `references/startup-manifest.json` (sc24 hand-over item 1);
    - `evals/kit/audit.py`'s J1 and the dry-run fixtures are changed for the new cards;
    - the evals README's card links are fixed.
  - **Child 25 (CR-511):** `docs/proofs/cards-inventory.md` with its four owner lists.
  - **Child 26 (CR-512):**
    - `references/budgets.json` with its `pending_owner` rows;
    - `references/rules.json` with the detectors moved from `evals/kit/detectors.json`;
    - `tests/test_card_budgets.py`;
    - the kind-a quiz cases written but not run (sc26-Q3).
  - **Child 27 (CR-513):**
    - `evals/results/behaviour-accepted.md`, header only;
    - `behaviour.py`'s `to_answer` list (`accepted`, `re-ask`, `open`);
    - the M11 reminder step in `.github/workflows/ci.yml`.
  - Where a child's specification fixes a detail this file names differently (a file name, a
    key, a flag), the Driver follows that child's specification and names the difference in the
    PR.
- **Depended on by:** nothing. Each of children 19 to 27 waits on this CR's PR (the merge rule).
- **Merge:** children 19 to 28 merge as one unit:
  - in one sitting, in order;
  - with no chantier session started in between;
  - only after this child's campaign has passed on `<top>` (the program's merge rule; F11, Q8).
  - Nothing merges while the owner sleeps.

## Hand-over notes addressed to child 28, gathered

These are every note the program and children 1 to 27 leave for this child. Each is carried in the
section named. The decision report (section 8) repeats this table with a "done / not exercised /
waits for the owner" column.

| # | From | Note | Here |
| --- | --- | --- | --- |
| 1 | Program merge rule; F11; children 19 to 27, Handback | Each of children 19 to 27 records `$CHANTIER wait <cr> merge <child 28's PR>`. While child 28 had no PR, some recorded it on child 28's CR, with a `--note` (sc26). Once this PR exists, the waits name it | section 9 |
| 2 | Program F6, child 28 Scope | A sandbox campaign run by the user, or on the user's word, with the plugin loaded from the stack's top worktree, outside the main checkout. Roles not seen are "no run", not failed | sections 3, 4 |
| 3 | Program child 28 Scope | Compare with child 5's baseline: card bytes read, turns, CLI errors and the S-list, the `chantier push` refusal rate, Driver runs per CR, the Foreman's and the Chief of Staff's wake shares, `msg` deliveries, cost per CR | sections 1, 4 |
| 4 | Program child 28 Scope; sc06 | `just quiz` on every role, old cards and new, side by side; F4's pass rule | section 5 |
| 5 | Program "Pending items" (`2-backlog/P3/evals-rework`) | Name result files by `evals/results/`'s convention at the base; use the date-first form if evals-rework has merged | sections 4, 5, 8 |
| 6 | Program child 28; sc26 H17, Q1 | Confirm each budget at what the run read, or ask a raise with the owner's line (M11); each `pending_owner` row is confirmed or cut by the owner | section 6 |
| 7 | Program "Pending items" (`1-inbox/foreman-idle-wakes`) | Re-read after child 28's measure, which repeats the wake-share measure | section 9 (handback) |
| 8 | Program "Cost"; F4 | Print the spend cap first; the quiz and the campaign spend outside the batch's `cost` | section 2 |
| 9 | Program "Evidence"; sc08 | The Copilot cells: no real run; the host rows say "untested" | "Evidence", matrix |
| 10 | sc04 (CR-490) | The write guard's scratchpad pass is unproved in a real session. Report `write_guard_refusals`. The S5 lines (scratchpad and `/dev/null)`) should fall to none. Check whether workers leave results in the scratchpad | section 4, figures |
| 11 | sc05 (CR-491) | Use `--folders` to isolate the campaign's workspace from the user's other sessions | sections 3, 4 |
| 12 | sc06 (CR-492) | The session roles take `--model claude-opus-5-5`; the judge is `claude-fable-5-2`. A Driver refused a headless CLI hands back the exact commands, and the Chief of Staff runs them | section 5 |
| 13 | sc07 (CR-493) | Unproved: whether roles read a topic when a line names it. Measure the `help` reads | section 4, figures |
| 14 | sc13 (CR-499) | Unproved: the Foreman watcher's `msg@1` delivery. Measure `msg` deliveries. "Unread messages in status" is a later CR if the measure shows the need | sections 1, 4 |
| 15 | sc15 (CR-501) | `conflicts` is seen only if the campaign has a parallel batch | section 3 (mode); open question 3 |
| 16 | sc17 (CR-503) | The new cards type the launcher. Default to confirm: keep it unless it adds more than 1 s per call | section 7 |
| 17 | sc19-Q1 (CR-505) | The board Griller's 2 KB budget covers its section only, while its brief holds the whole card (about 6 KB). Measure the brief; the owner decides | section 6 |
| 18 | sc24 (CR-510) | Item 1: `--cards <pre-swap ref>` is usable for the old-card quiz. Q1 and Q2 defaults to confirm. The audit's J1 and its fixtures changed: a failed audit check is classified | sections 3, 5, 7 |
| 19 | sc25 (CR-511) | The four owner lists (kind-a rows with their home; inferable and incident rows; removed rows; kind-a rows checked by quote alone). Q1 to Q3 defaults to confirm | sections 6, 7 |
| 20 | sc26 (CR-512) | Q3: the kind-a quiz cases were written but not run; child 28 runs them. Q1, Q2 and Q4 defaults to confirm. Detectors with no card sentence left the measure (Known gap) | sections 5, 6, 7 |
| 21 | sc27 (CR-513) | `behaviour-accepted.md` ships with its header only: child 28 adds rows, on the user's word only. `to_answer` lists the lines to answer. The local Windows gate moves to child 28. Q1 and Q2 defaults to confirm | sections 4, 7, "Gates" |
| 22 | sc20, sc21, sc22, sc23 (CR-506 to CR-509) | Defaults to confirm (section 7) | section 7 |
| 23 | Program "Rules for every child" (F17, F20) | Unproved claims are marked "unproved"; the added `just test` seconds are stated | "Gates and evidence" |

No other note addressed to child 28 was found in children 1 to 27.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 14 (Q16) | One card set; the real-run measure and the quiz pass before the swap merges; a rollback is a git revert | sections 3 to 5, 8 |
| Answer 22, F6, Q5 | A sandbox campaign run by the user or on the user's word, with the plugin from the stack's top worktree, outside the main checkout. Roles not seen are "no run" | sections 3, 4 |
| Answer 22, F4 | Quiz pass rule: no case scores 0 of 3 on the new cards that the old cards passed ("passed" = at least 1 of 3, sc06-Q4). The spend cap is printed first | sections 2, 5 |
| Answer 22, F11, Q8 | Children 19 to 28 merge as one unit, in one sitting, in order, with no session in between, after this campaign; nothing merges while the owner sleeps | sections 8, 9 |
| Answer 9, M10 | Each S-list line is filed as an inbox item or accepted in `evals/results/behaviour-accepted.md`; nothing is accepted without the user's word | section 4 |
| Answer 9, M11 | A budget raise needs "Budget change approved: <user>, <date>" in the PR body, written by the user, never by a Driver | section 6 |
| Answer 9, M14 | "Tool not in the role's list" lines are answered like S-list lines | section 4 |
| Program, child 28 Must not | No batch or campaign started without the user. The main checkout does not change. No card changes to pass the measure without a new quiz and a new measure | "Must not" |
| Program, child 28 Risk | The top of the stack owes the local Windows long gate and the pipeline's `just scenario (ubuntu-latest)`. No AGENTS.md change | "Gates and evidence", "AGENTS.md" |
| Program "Cost" | Spend outside the batch's `cost`, cap printed first; a budget order is the owner's | section 2 |
| Program "Evidence" | Claude Code with shipped defaults: this campaign. Copilot: "untested" | "Evidence" |

Three readings of the program, each the smallest that makes its sentence work:

- **"Turns"** is the run's model calls: `roles.<role>.model_calls`, per-run mean. A model call
  is one distinct assistant `message.id` (child 5).
- **"No floor rule's detector is worse than the baseline"** is read strictly, per (detector,
  role) seen in both files: the campaign's rate is not higher than the baseline's. Child 5's
  5-point threshold applies to its general `regressions` list, not to this rule. With five CRs, one
  matching call is a large rate. The report names each such call's role and detector, never its
  text.
- **"Cost per CR"** comes from the campaign's own record: `$CHANTIER cost --by cr` in the
  workspace, and the archived batch file. It is compared with run 4, the last old-card run of the
  same campaign (`evals/results/real-foreman-2026-11-22-run4.md`: stack, 0.14.0, $9.88, about
  $1.98 per CR). Child 5's baseline holds no cost.

## What changes

### 1. `evals/kit/behaviour.py`: `--against` and the `msg` count

Two additions. The JSON keeps `"schema": 1`, and the new keys are additive. Every other figure is
unchanged, including `regressions` and child 27's `to_answer`.

**a. `--against <results.json>`.**

- It names the file to compare with, instead of the automatic `previous` (the latest file in
  `--out`). `previous` and `regressions` are then computed against that file.
- If the file is missing, unreadable, or not a results file of `"schema": 1`: exit 2, naming the
  file.
- It adds a `comparison` key to the JSON and a "Comparison" section to the Markdown, right after
  the header lines.

The `comparison` key holds:

- `against`: the file's name.
- `roles.<role>`: one entry per role of the kit's role list. That list is the one `quiz.py` uses;
  import it, do not keep a second copy. Each entry has a `status`:
  - `compared` (seen in both files);
  - `no run` (not seen in the measured window);
  - `no baseline` (seen now, absent from the baseline).

  For `compared` roles, each figure is a pair `{old, new}`:
  - `card_bytes_per_run`: `card_bytes.per_run_mean`;
  - `model_calls_per_run`: the "turns";
  - `tool_calls_per_run`;
  - `usage_errors_per_run` and `refusals_per_run`: the sum of the `cli` template counts divided by
    `runs`;
  - `s_list`: the count of S-list lines for that role, old and new, plus the list of new
    templates;
  - `push_refusal_rate`: `pushes.rate`, `null` when no `chantier push` call was seen;
  - `force_with_lease_denied`: the raw count;
  - `help_reads` and `write_guard_refusals`: the totals;
  - `msg`: the new count of section 1b (`null` in the old file when the key is absent).
- `driver_runs_per_cr`: `{old, new}` of `mean` and of the share of CRs with one run.
- `wake_shares`: for `foreman` and `chief-of-staff`, `{old, new}` per wake kind.
- `checks`:
  - `card_bytes_lower`: `pass` is true when every `compared` role has `new < old`. `failing`
    lists each other role with its two figures. `no baseline` roles are listed apart and do not
    fail it.
  - `floor_not_worse`: for each detector with a `floor` number (read where child 26 moved them,
    `references/rules.json`), and each role in both files, `pass` is true when the new rate is not
    higher than the old. `failing` lists `{id, role, old, new}`.

The Markdown "Comparison" section holds:

- one table with a row per role and a column per figure, in the form `old -> new`;
- the `no run` and `no baseline` lists;
- the two checks, each "pass" or "fail" with its failing lines;
- one line: "Comparability: the baseline is the user's real sessions since <since>; this run is a
  sandbox campaign of five CRs. Steering roles' figures are counts, not statistics" (study-behaviour
  section 6).

**b. The `msg` count.**

- New key `roles.<role>.msg`: `{calls, delivered, not_delivered, other}`, built from the results
  of chantier calls whose subcommand is `msg`:
  - `delivered`: a result line ending "delivered to its watcher";
  - `not_delivered`: a result line starting "not delivered:";
  - `other`: anything else, a usage error or a refusal included. Those are still counted in `cli`
    as today.
- The Markdown role section gains one `msg` line.

**c. The fixture and the dry run** (`evals/kit/behaviour-fixture/`, `evals/kit/dry_run.py`, case
`behaviour`):

- The Foreman main session gains two `chantier msg` calls, one delivered and one not delivered,
  in the host's JSONL form with no real text. `expected.json` gains the `msg` figures, worked out
  by hand in the PR.
- A second run of the case passes `--against <tmp>/previous.json`, the previous file child 5
  stages. It checks, against figures added to `expected.json`:
  - a role whose card bytes fell passes `card_bytes_lower`, and a role whose bytes rose fails it;
  - a floor detector whose rate rose fails `floor_not_worse`;
  - a role of the kit's list absent from both files is `no run`;
  - a role absent from the previous file is `no baseline`.

  Child 5's `previous.json` gains only the figures these checks need.
- `--against` naming a missing file exits 2.

**d. Not changed:** the privacy guard, the normaliser, `--prune`, `to_answer` and the file names.

### 2. The spend caps (printed first)

These are printed first in the PR body, under "Spend", before any run (program "Cost", F4). All
of them are outside the batch's `cost`. The figures are this specification's default (open
question 2).

| What | Cap | Who starts it |
| --- | --- | --- |
| Quiz, new cards, every role with cases (section 5) | $30: $10 for the three session roles, $20 for the others | the Driver, round 1 |
| Quiz, old cards, cases with no old score (section 5) | $15 | the Driver, round 1 |
| Campaign `real-foreman`, stack mode (section 3) | `--budget 20`, raised once to $30 on a `budget:` ask, per the runbook | the user |
| Total, outside the batch | $75 at most | |

`quiz.py` refuses a run whose estimate is above `--max-usd`, and stops at the cap (child 6). A
quiz step that would need more stops, and the Driver hands back with `blocked question:`, naming
the step, its estimate and the cap.

### 3. The campaign: how the user runs it on `<top>`

There are two text changes, and no code: `evals/README.md` and `evals/real-foreman/RUNBOOK.md`.

**`evals/README.md`**, a new subsection "A campaign on a PR's head", under "A sandbox campaign",
after its "Preparation". It holds the steps below, as generic text. "The PR's worktree" stands
where this specification says `<top>`. "The cards real run" is the example. A line says: "unproved
until the cards real run reports" (F17).

**`evals/real-foreman/RUNBOOK.md`**, one line under "Start": "To run a PR's head instead of the
main checkout, follow the evals README, 'A campaign on a PR's head'." The "Cost and time" row is
not changed here; round 2 updates it with this run's figures.

**The steps the user takes, in order.** These are the default. The plugin step is open question
1.

1. **When.** After round 1 is handed back validated, with both long gates green at its head.
   Then:
   - no other chantier session runs on this machine, because the plugin is re-pointed for every
     session in step 4;
   - batch-31's Chief of Staff and Foreman sessions are ended. Batch-31's record keeps every CR
     as it is; they resume later from `status`.
2. **Find `<top>`.**
   - In any shell: `git -C <main checkout> worktree list`. The line whose branch is this CR's is
     `<top>`.
   - Check `git -C <top> status --short` prints nothing.
   - Check `git -C <top> rev-parse --short HEAD` equals the SHA of round 1's ready line. Note it:
     `<campaign sha>`.
3. **The kit's local files.** Copy `evals/kit/eval-root.local.json` and
   `evals/kit/sandbox.local.json` from the main checkout into `<top>/evals/kit/`. Both are
   git-ignored there too, and the main checkout does not change.
4. **The plugin from `<top>`.** Quit Claude Desktop, then, in a shell:
   - `claude plugin uninstall chantier@chantier`;
   - `claude plugin marketplace remove chantier`;
   - `claude plugin marketplace add <top>`;
   - `claude plugin install chantier@chantier`;
   - then start Claude Desktop again.

   The commands are the README's prerequisite lines with `<top>` in place of the checkout.
   Unproved: that a directory marketplace loads `<top>` in place, as it loads the main checkout
   today; step 8 checks it.
5. **No board left running** (README, Preparation step 2).
6. **The sandbox**, from `<top>`:
   - `uv run --no-project python evals/kit/sandbox.py reset`, then read the plan;
   - then the same with `--yes`.
7. **The workspace**, from `<top>`:
   - `uv run --no-project python evals/kit/setup.py real-foreman <eval root>/cards-real-run-<YYYY-MM-DD>`.
   - Note the UTC time as `<start>`, for example `2026-11-26T08:00Z`.
   - Check that the `CHANTIER` line setup prints is `uv run --locked --project "<top>" chantier`,
     and that the `prompt` line names `<top>/evals/real-foreman/RUNBOOK.md`. If either names the
     main checkout, stop.
8. **Start the operator.**
   - In the Claude Desktop Code tab, open a new session on the workspace.
   - Paste setup's `prompt` line with the mode `stack`:
     `/chantier:chief-of-staff foreman Run the chantier eval campaign real-foreman in stack mode: follow <top>/evals/real-foreman/RUNBOOK.md.`
   - **Check before the go:** the skill load's "Base directory for this skill" is under `<top>`.
     If it is the main checkout or a plugin cache, end the session before the go. Nothing is spent
     but that turn. Re-point the plugin (step 4) or answer open question 1.
9. **The run.** Follow the runbook's "The user's turns":
   - the go after the plan;
   - each merge with `sandbox.py merge <n>` from `<top>`, then `order merged`;
   - one budget raise to $30 at most;
   - `final`: the audit, the cost and `close --yes`.
10. **The plugin back.** Quit Claude Desktop, then run step 4's four commands with the main
    checkout in place of `<top>`, then start Claude Desktop again.
11. **Tell the Chief of Staff** one line: "campaign done: workspace cards-real-run-<date>, start
    <start>, mode stack, sha <campaign sha>", plus anything that went wrong. The Chief of Staff
    opens round 2 with that line in this CR's `02-answers.md`.

**Mode.** Stack, the mode of run 4, so cost and time compare with it. Stack mode also exercises
the most `chantier push` calls: the stack driver's rebases with `--force-with-lease`. `conflicts`
(child 15) is then "not exercised" (open question 3).

**What passes, for the run itself.** All three must hold:

- **R1:** every CR is `merged`, or `cancelled` with its reason in the report. The spend is at most
  $20, or at most $30 after the one raise.
- **R2:** step 8's check showed `<top>` as the skill's base directory, and the transcripts show
  `brief` boots: the `card_bytes.by_card` keys of section 4 include `brief`. If not, the run did
  not test the new cards: it is void, not failed, and it is redone.
- **R3:** every failed audit check (`audit.py <workspace> --sandbox`, run from `<top>`) is
  classified in the report as one of:
  - (a) the kit still expects old-card text: a kit finding, filed;
  - (b) a behaviour the new cards lost: blocks the merge until it is answered;
  - (c) seen in run 4 too: a known finding, named.

  None of class (b) is left without the owner's answer.

### 4. Round 2: the measure (the Driver, in `<top>`)

On the round 2 brief, which carries the user's line from step 11:

1. `git -C <top> diff --stat <campaign sha> HEAD -- skills hooks agents com.github.copilot` must
   print nothing. If it prints anything, the campaign ran on other cards: stop, and hand back
   `blocked question:` naming the files ("the campaign is redone").
2. `just behaviour --since <start> --folders "*cards-real-run-<date>*" --against evals/results/<child 5's baseline>.json`.
   It writes `evals/results/behaviour-<date>-v<X.Y.Z>.json` and `.md`, or the date-first form if
   evals-rework has merged at the base.
3. Read both files for anything that looks like a name, a path or a session's sentence, beyond the
   guard (as child 5 did). Then commit them.
4. **The figures the report reads** from the comparison:
   - the eight program figures;
   - `write_guard_refusals`, with the S5 scratchpad and `/dev/null)` templates: expected none
     (sc04);
   - `help` reads (sc07);
   - `msg` (sc13);
   - `tool_not_in_list`;
   - `pushes`.

   Also say whether any worker's result was left in a scratchpad path. That is read from
   `files_read` and the write-guard figures only, with no transcript text.
5. **Cost per CR:** read `$CHANTIER cost --by cr` from the operator's final turn, and the archived
   `5-archives/batches/batch-NN.md` in the workspace's planning folder, read-only. Set them beside
   run 4's figures: the total, the cost per CR, each CR, the Foreman and the stack driver.
6. **The campaign report** `evals/results/real-foreman-<date>-run5.md` (the next run number of the
   campaign, by the convention at the base). It follows the README's "The report" template. Its
   "The run" section names `<campaign sha>` and "plugin from the PR's worktree". R1 to R3 go in
   its Scorecard.
7. **The S-list (M10, M14)** comes from `to_answer`, its `open` and `re-ask` lines:
   - The Driver lists each line in its handback, with its role, kind, template, runs and rate.
   - The Chief of Staff files the lines that are tool bugs as inbox items (answer 3), and
     proposes the others to the user as accepted stumbling, each with a one-line why.
   - The user's answers are recorded in this CR's `02-answers.md`.
   - In a next round, the Driver adds the accepted rows to `evals/results/behaviour-accepted.md`,
     in this PR (sc27's table, byte-for-byte templates), and reruns step 2's command with
     `--out <scratchpad>`, to show those lines as `accepted`.
   - Nothing is accepted without the user's word.
8. **The README's campaigns table:** update the `real-foreman` row's "Last run" with run 5.

### 5. The quiz: old cards and new, side by side (round 1)

Run in `<top>`, at the rebased head, after section 2's caps are printed. Each step prints its
`--plan` line first.

- **New cards, every role that has cases:**
  - `just quiz chief-of-staff foreman griller --model claude-opus-5-5 --max-usd 10 --against <old files> --save cards-real-run-new-sessions`;
  - `just quiz <every other role with cases> --max-usd 20 --against <old files> --save cards-real-run-new-agents`.

  With no `--cards`, the boot is `chantier brief <role>`: the new cards.
- **Old cards, the cases with no old score**: cases added after child 6's baseline (child 25's
  `inf-*` cases, child 26's kind-a cases, child 27's new cases, any other).
  - The Driver lists them first: each case whose id is in no `<old files>` result.
  - Then: `just quiz <role> --cards <old ref> --case <id> --max-usd <the remainder of $15> --save cards-real-run-old-<role>`,
    one call per role, or one call per case where `quiz.py` takes one `--case` only.
  - Then the new-card steps above are rerun with these files added to `<old files>`, for those
    cases only (`--case`). Alternatively, their F4 result comes from one rerun of `--against`, if
    `quiz.py` compares saved files without new calls. The Driver uses whichever `quiz.py` offers,
    and spends nothing twice.
- **`<old ref>`**: the ref that child 6's baseline files record. All old scores then come from one
  card set. If those files name no ref, use the parent of child 24's first commit on the stack
  (a pre-swap tree, with the manifest).
- **`<old files>`**: child 6's `quiz-<date>-baseline-old-cards-<role>.json`, child 25's
  `quiz-<date>-old-<role>.json`, and this step's `cards-real-run-old-<role>` files. These are
  old-card results only, never a new-card file.
- **Pass:** every `--against` call exits 0: F4 holds on every role.
  - A case that scores 0 of 3 now, after an old pass, is a failure. The Driver hands back
    `blocked question:` naming the role, the case and its rule.
  - The Driver never changes a card in this CR to pass it (Must not).
- **The side-by-side table** (role, cases, old passes, new passes, cases at 0 of 3, F4) goes in the
  PR and in the decision report.
- **The judge** is `claude-fable-5-2` (child 6). The results record `claude --version`.
- **If the host refuses `claude -p` from a Driver** (sc06 Risk): no workaround. The Driver hands
  back with the exact commands above and the Known gap "quiz not run: the host refused `claude
  -p` from a Driver". The Chief of Staff runs them and commits nothing: the result files come
  back to this PR in a next round.

### 6. Budgets, `pending_owner`, the owner lists and the board Griller's brief (round 1, no spend)

- **Budgets table.** For each row of `references/budgets.json`:
  - the file;
  - its limit;
  - its size at the head, as `tests/test_card_budgets.py` counts it: LF bytes, `[R-nnn]` tags
    stripped (sc26-Q1);
  - its `pending_owner` mark, if any.

  Round 2 adds the campaign's bytes read per run for that file (`card_bytes.by_card`). The table
  goes in the PR and the decision report.
- **`pending_owner` rows** (sc26-Q1, H17). Each is put to the owner in the decision report, with
  two answers:
  - **confirm:** the limit stays at the size child 25 reached;
  - **cut:** the limit goes back to child 24's size, and the card is cut. That is a card change:
    a new quiz of that role and a new campaign measure (Must not), so a cut row is a CR of its own
    after the unit merges, filed by the Chief of Staff.

  The owner's answers are recorded in this CR's `02-answers.md`.
  - A confirm removes the mark from `budgets.json` in a next round, only once the PR body holds
    "Budget change approved: <user>, <date>", written by the user (M11, child 27's CI reminder).
  - The Driver never writes that line. Until then the mark stays, and the Known gap lists the
    row.
- **A raise.** A file the campaign shows above its limit is not raised here. The decision report
  asks the owner, naming the file, its size and the limit it needs. The same M11 line applies.
- **Owner lists** (sc25): the decision report links `docs/proofs/cards-inventory.md`'s four lists
  and gives their sizes:
  1. kind-a rows with their home;
  2. inferable and incident rows;
  3. removed rows;
  4. kind-a rows checked by quote alone.

  For list 4, it names the quiz case child 26 wrote for each row and that case's result from
  section 5. A row of list 4 whose case fails F4 is a failure of section 5.
- **Detectors that left the measure** (sc26-Q4): listed by id, from child 26's Known gap, with
  their baseline rates.
- **The board Griller's brief** (sc19-Q1, sc24-Q2), measured at the head:
  - `$CHANTIER brief board-griller <an inbox item of the planning folder>`, in bytes (LF);
  - the bytes of the Griller card's "Started from the board" section;
  - the length of `src/board/griller.py`'s `BRIEF`;
  - each against the 2 KB budget.

  The board Griller is "no run" in the campaign. The owner decides whether the 2 KB budget
  covers the section or the whole brief.

### 7. The defaults to confirm

The decision report holds one table:

- default;
- child;
- what it decided;
- what the campaign or the quiz showed: a figure, "not exercised", or "no run";
- the owner's answer, empty until given.

Its rows:

- sc17: keep the launcher unless it adds more than 1 s per call. The report gives the measured
  seconds per call from child 17's PR, and the campaign's `cli` usage errors.
- sc19-Q1: the board Griller's budget (section 6).
- sc20-Q1: staging folders per role. sc20-Q2: a new worktree per release attempt. Not exercised:
  real-foreman has no release.
- sc21-Q1: the Foreman's worktree override is dropped ("stop" and "hold" only). Exercised only if
  the Foreman acted on a worktree.
- sc22-Q1: a branch that is not the CR's own is never force-pushed, and the default branch is
  never pushed; another push is asked once. sc22-Q2: direct mode runs `brief foreman --epoch <n>`
  separately. Q1 is exercised by the stack's pushes; Q2 is not exercised (Foreman mode).
- sc23-Q1: child 26 freezes budgets at child 23's sizes. sc23-Q2: no router brief.
- sc24-Q1: `take` prints the brief command, seen in the Drivers' first turns. sc24-Q2: the board
  Griller's brief does not name the floor (the Known gap "the board Griller does not read the
  floor").
- sc25-Q1 to Q3: a kind-a row may be checked by quote alone until child 26 (list 4); an undecided
  removed rule is restored; the inventory is one file.
- sc26-Q1 to Q4: `[R-nnn]` tags stripped from the counts; ids required in role cards and
  `floor.md` only; kind-a quote rows get a quiz case (run in section 5); a detector with no card
  sentence leaves the measure.
- sc27-Q1: the CI reminder stays in `ci.yml` with no `edited` trigger. sc27-Q2: no quiz
  requirement in AGENTS.md.
- **The run's evidence on children 1 to 18.** Their defaults are confirmed at their own merge, not
  gated by this run. The report gives what the campaign showed for the four it exercises:
  - sc01-Q1: the stack push while the Driver holds the lease, from `pushes`;
  - sc04: `/tmp` stays refused, from `write_guard_refusals`;
  - sc13: `msg` delivery;
  - sc17: the launcher.

### 8. The decision report

File: `evals/results/cards-real-run-<date>.md`, in round 2, or the date-first form. It is the one
file the owner reads to decide. Its sections, in order:

1. **Verdict.** One line per acceptance item (A1 to A5 below) and per run check (R1 to R3), each
   "pass", "fail" or "waits for the owner". Then one line: "Merge children 19 to 28 as one unit:
   ready / not ready (<the items>)".
2. **How to merge.**
   - The order: CR-505, 506, 507, 508, 509, 510, 511, 512, 513, then this CR.
   - The rule: one sitting, no chantier session started in between.
   - If `git diff <campaign sha> <head> -- skills hooks agents com.github.copilot` is not empty
     at merge time, the run is redone.
   - The revert of the unit is a git revert (answer 14).
3. **Per-role comparison**, from section 4: the table, the `no run` and `no baseline` lists, and
   cost per CR beside run 4.
4. **Quiz**, from section 5: the side-by-side table.
5. **Budgets and `pending_owner`**, from section 6, with the owner's two answers per row.
6. **Owner lists** and detectors that left the measure (section 6).
7. **The board Griller's brief** (section 6).
8. **Defaults to confirm** (section 7).
9. **The S-list and tool lines**, from section 4.7: filed (with the item names), accepted (with
   the user's word), or waiting.
10. **Hand-over checklist**: the table of this specification with its status column.
11. **Host matrix and unproved points** (Evidence).
12. **Left for later:**
    - `1-inbox/foreman-idle-wakes`, to re-read with the wake shares;
    - "unread messages in status" (sc13), if `not_delivered` is above zero;
    - the audit's class (a) findings.

The report quotes no transcript text, no path of the user's machine and no session id. It holds
figures and file names only.

## Out of scope

- Starting the campaign. Only the user does it (floor rule 7).
- Any card, topic, `rules.json` or `budgets.json` change, except the removal of a `pending_owner`
  mark on the owner's answer and M11 line (section 6). No card text changes to pass a measure.
- Any CLI (`src/`), hook, agent wrapper or scenario change.
- A second campaign in another mode, `real-direct`, `full` or the `copilot` campaign (open
  question 3).
- A Copilot run: no reader, no campaign; the host rows say "untested".
- Filing inbox items: the Chief of Staff files them. Accepting an S-list line without the user's
  word.
- Recording waits on other CRs: the Foreman updates them (section 9).
- Running `audit.py` changes beyond what child 24 made; class (a) findings are filed, not fixed
  here.
- A new pytest file, or a test under `tests/`.
- Re-pointing the user's plugin, quitting Desktop, or ending any session. Those are the user's
  steps.

## Must not

- Start a batch, a campaign or a sandbox reset (floor rule 7). The Driver writes the steps; the
  user runs them.
- Change the main checkout: its files, its branch, its git-ignored files. Step 3 copies from it
  and writes nothing in it.
- Change a card to pass the measure or the quiz without a new quiz and a new measure (program).
- Write an owner's approval line ("Budget change approved"), or accept an S-list line, without the
  user's word.
- Commit a transcript, a user name, a home path, a session or agent id, or a project folder name.
- Push to a branch other than this CR's, or force a push other than this CR's own with
  `--force-with-lease`.

## Acceptance evidence

**Round 1** (in the PR):

1. The plumbing: section 1's diff, and `just eval-dry-run` green with the extended `behaviour`
   case. Its added seconds are stated.
2. The evals README's new subsection and the runbook line (section 3).
   `tests/test_command_names.py` passes: the new text names no `chantier` subcommand that does
   not exist.
3. "Spend" with the caps, printed before the quiz (section 2).
4. The quiz (section 5): the `--plan` lines, the result files committed in `evals/results/`, each
   `--against` exit 0, and the side-by-side table. Or the hand-back with the exact commands.
5. Section 6's tables: budgets and `pending_owner`, the owner lists' sizes, the detectors left out,
   the board Griller's brief bytes.
6. The hand-over checklist with its status column as it stands.
7. The gates below.

**Round 2** (after the campaign), the program's five:

- **A1** the measure files are committed: `behaviour-…json` and `.md` with `comparison`, the
  campaign report run 5, and the decision report.
- **A2** each role seen reads fewer card bytes than its old figure: `checks.card_bytes_lower.pass`.
- **A3** no floor rule's detector is worse than the baseline: `checks.floor_not_worse.pass`.
- **A4** the quiz passes F4 on every role: section 5.
- **A5** every new S-list and tool line is filed or accepted: `to_answer` holds no `open` or
  `re-ask` line once the accepted rows are in.

Plus R1 to R3 (section 3).

A1 to A5 and R1 to R3 passing is what "the campaign has passed" means in the merge rule.

## Gates and evidence

- **Before each push:** `just check` in `<top>` at the rebased head, and `just eval-dry-run`
  (round 1 changes `evals/kit/`).
- **The long gate:**
  - `just scenario (ubuntu-latest)` green at the PR's head. It is owed for the stack's card and
    CLI changes this head carries, though this CR changes only `evals/` and `docs/`-like text.
  - As the stack's top, the local Windows `chantier gate <cr> scenario` at the head when called
    ready. It moves here from child 27 (sc27).
  - It is rerun at round 2's final head: AGENTS.md owes it at the top's head, a results-only head
    included.
- **`just test` seconds (F20):** this child adds no test under `tests/`. The PR states `just test`
  measured at the base and at the head on the same machine, expected about 0 s. It also states the
  seconds the extended `behaviour` case adds to `just eval-dry-run`.
- **Checks that guard shipped files:**
  - The dry run reads the shipped `references/rules.json` (the floor detectors) and the shipped
    role list (through `quiz.py`), from the head under test.
  - The fixture's transcripts and `previous.json` are prepared inputs, for cases no shipped file
    holds (a comparison, a delivery line). They are paired with the shipped reads above.
- **No `hooks/` or `types/` change:** `just mod` is not owed.

### Host and default matrix

What the campaign proves depends on the host and on the shipped defaults. One line per cell:

- **Claude Code, shipped defaults:** this campaign (real-foreman, stack, Claude Desktop), the
  quiz, the measure.
- **Claude Code, a project's own `chantier.yaml` role settings:** not exercised by this run. The
  sandbox `shelf` keeps the shipped defaults. Covered by child 10's tests only.
- **Claude Code CLI with `--plugin-dir <top>`:** not used. Unproved that it replaces the installed
  copy (CONTRIBUTING.md).
- **Copilot, shipped defaults:** no run. Its roles are "no run", and the host rows say
  "untested". `behaviour.py` says "Copilot: not measured".

### Unproved (F17)

- That a directory marketplace pointed at `<top>` loads it in place in Claude Desktop (step 4).
  Step 8's check proves it or stops the run.
- That the host's transcript texts (wakes, denials, "No such tool available") are unchanged since
  child 5's fixture.
- The comparability of a five-CR sandbox campaign with real sessions since 2026-11-17 (the
  report's comparability line).

## Handback

- **Round 1:** validated, with these Known gaps:
  - "campaign not run: waits for the user";
  - "do not merge: merges with children 19 to 28 as one unit, after child 28's campaign";
  - every `pending_owner` row;
  - each file above its limit;
  - any quiz step not run, with its reason.

  The handback names this PR's link and the steps of section 3 for the Chief of Staff to give the
  user.
- **The waits (section 9):** the handback asks the Foreman to point each wait of CR-505 to CR-513
  at this PR's link: `$CHANTIER wait <cr> merge <this PR>`, and to clear any wait recorded on this
  CR with a `--note` in its place. The Driver records nothing on another CR.
- **Round 2:** validated when A1 to A5 and R1 to R3 pass, or with each failing item named.
  - The handback lists the S-list lines to answer (section 4.7) and the owner's open answers
    (sections 6 and 7).
  - It points the Chief of Staff to `1-inbox/foreman-idle-wakes`, with the wake shares.
  - The PR stays unmerged: the owner merges the unit (section 8.2).

### 9. The merge waits

Children 19 to 27 (CR-505 to CR-513) each wait on this CR's PR. This CR records no wait of its
own: it is the last of the unit. Its Known gap names the unit, and its decision report's verdict
says when the unit is ready.

## Risk

- **The top of the stack** owes the local Windows long gate and the pipeline's ubuntu scenario at
  its head, twice (rounds 1 and 2).
- **Spend:** up to $75 outside the batch (section 2), the campaign's share counted by its own
  `cost`.
- **Re-pointing the plugin** (step 4) changes the plugin for every Claude Code session on the
  machine until step 10. A session left running would load the new cards at its next reload,
  hence step 1. The main checkout is untouched.
- **A void run:** if step 8's check fails, the run is void (R2), and only one turn is spent.
- **Small samples:** five CRs make the steering roles' figures counts. The strict floor reading
  (Decisions) may fail on one call, which the owner then reads.
- **Privacy:** the measure reads the user's own transcripts. The guard plus the Driver's read
  before the commit protect it; a missed leak publishes a name or a path.
- **Quiz from a Driver:** the host may refuse `claude -p` (sc06), and then the Chief of Staff runs
  it.

## AGENTS.md

None (program, child 28 Risk). No CLI tool, no new write outside `evals/results/`, no new git
operation.

## Open questions

1. **How the plugin is loaded from `<top>` (risk).** The campaign needs Claude Desktop (the
   runbook: the desk, to start the Foreman and type the go). Desktop takes no `--plugin-dir`, as
   far as this program has proved. Re-pointing the user's install (step 4) makes every session on
   the machine run the stack's cards until step 10. Default: re-point the install, with step 1's
   "no other chantier session", step 8's check, and step 10's re-point back. The alternative is
   another way you prefer: a second Claude profile or user account, or a copy of `<top>` under
   another plugin name. Each is unproved and would change this child's steps.
2. **The spend cap outside the batch (cost).** Default: $75 at most, as $30 for the quiz on the
   new cards, $15 for the old cards on new cases, and the campaign's $20 budget with one raise to
   $30. Lower it, or raise it if the quiz's plan shows more cases than child 6's baseline did?
3. **One campaign mode only (scope).** Default: one `real-foreman` run in stack mode, the mode of
   run 4, so cost and time compare. `conflicts` (child 15), the parallel slots and the Foreman's
   parallel waves are then "not exercised". A second run in parallel mode would cover them, for
   about $10 to $12 more and one more session at the desk. Is one stack run enough for the merge?
