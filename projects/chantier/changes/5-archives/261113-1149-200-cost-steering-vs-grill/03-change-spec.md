# Cost: steering turns are not grill turns

## Goal

In a direct batch, `cost` must count the Chief of Staff's steering as steering. Today a turn
that only *names* a CR's specification (in a Driver's prompt, for example) moves from the
budgeted `Chief of Staff, steering the batch` row to the `Chief of Staff, grill and
specifications with the user (outside the budget)` line. So the budget rail under-counts a direct
batch, the report's steering share is too low, and the scorecard compares direct and Foreman mode
on a wrong row. Run 1 of real-direct (2026-11-12, finding 3) showed steering at $1.18 instead of
about $3.6, the batch at $9.41 instead of $11.84, and orchestration at 50% instead of 61%.

The fix: inside the steering window, a turn goes to the grill line only when it does grill or
specification work. It must write a CR's intent, answers, specification or `work/specifying`
marker, or start a spec-writer. Naming a path, or reading one, is steering.

## The rule (decisions of 02-answers.md)

1. **Inside the steering window, a turn is a grill turn only if one of its tool uses:**
   - **writes** one of these: a CR's `01-intent.md`, `02-answers.md`, `03-change-spec.md` or
     `work/specifying` marker. A write is a host write tool whose **target path** ends in one of
     those names: `Write`, `Edit`, `MultiEdit` (`file_path`), `NotebookEdit` (`notebook_path`). On
     Windows, compare with `\` turned into `/`. Only the target path counts: a write to another
     file whose *content* names such a path is steering. Run 1's `retro.md` is one.
   - **starts a spec-writer**: an `Agent` (or `Task`) tool use whose `subagent_type` ends in
     `spec-writer`. This is unchanged.

   Everything else is steering:
   - an `Agent` prompt that is not a spec-writer's, even if it names `03-change-spec.md`;
   - a message to a Driver;
   - a shell command (`Bash`, `PowerShell`), whatever paths it names, even one that writes
     `02-answers.md` or `work/specifying`: no shell-write detection (02-answers.md, the shell-writes
     answer). This is the safe side: that spend counts in the budget. The card tells the Chief of
     Staff to write a CR's files with the host's Write tool (see "Cards");
   - a `Read`, `Grep` or `Glob` of those files.

   This rule decides by what the turn does, so it covers the causes the request suspected and any
   later one. A mistake on this side counts too much in the budget, which is the safe side.
2. **A turn is still attributed whole.** A turn that steers and also records an answer (or starts
   a spec-writer) goes entirely to the grill line, as today. Nothing is split inside a turn.
3. **Outside the steering window nothing changes.** This covers a Chief of Staff beside a Foreman,
   the part of a direct batch's Chief of Staff session before its claim or after a Foreman took
   over, and the `Chief of Staff, whole session` line. There the old rule stays: any tool use
   whose input names one of `GRILL_NAMES`, or that starts a spec-writer, makes a grill turn. That
   Chief of Staff starts no Driver, and its spend is outside the budget either way.
4. **The diagnosis is not taken as given.** The request says the cause is "a path that only
   appears in a `take` output or an Agent prompt". A `take` output is a tool result, and
   `costs.py` never reads tool results, so that part cannot be right as written. The Driver
   finds, on run 1's transcript, which tool uses moved the turns. The PR description says what it
   found (see "Evidence").
5. **The card says the same thing as the CLI**, in the same PR (see "Cards").
6. **Same lines, corrected figures.** The default budget, the shape of the `cost` table, the
   `cost --summary`, STATUS.md's Cost section and the reports do not change. A direct batch will
   now show a higher, true steering share. The PR description carries **one line for the next
   release notes** that says so. No release-notes file is written in this PR: the release CR
   writes them.
7. **The run 1 target is the steering window's own figure** (02-answers.md, the answer on
   decision 3's target): about **$3.56** at the close, with grill at $0 inside the window, not the
   report's $3.61. The PR explains the gap: the calls between `open` and the claim are outside the
   steering window and stay on the grill line (rule 3).
8. **No rewrite of the run 1 report and no new eval run.** `evals/results/real-direct-2026-11-12-run1.md`
   already carries the corrected figures, and only the user starts an eval.

## What changes

### CLI: `skills/chantier/scripts/cli/src/chantier/costs.py`

- `GRILL_NAMES` stays as it is.
- `_grill_use(block)` today returns true when the JSON of the tool use's input contains a
  `GRILL_NAMES` entry anywhere, or when it starts a spec-writer. It gets a strict form for the
  steering window: a spec-writer start, or a write tool whose target path ends in a
  `GRILL_NAMES` entry (rule 1). The loose form (today's) stays for tool uses outside the
  steering window (rule 3). The Driver chooses how to express this: one function with a
  parameter, or two functions.
- `usage(path, since, until, split, prices)` needs to know where the steering window is, so that
  it judges each tool use by the rule of the window it falls in. Today the steering window is the
  `since`/`until` of the call made with the claim window. The `since` call, made from the batch's
  opening, also covers the window.
- **Invariant:** one transcript gives one classification per turn, whichever call prices it. The
  `steered` call (the claim window) and the `since` call (from the batch's opening) in
  `_chief_line` must agree on every turn inside the window. Otherwise the lines stop adding up:
  `steer` is computed as `since` minus `steered`, and the grill line is `since`'s grill. Today
  `grill_turns` is built from every assistant record, including records outside the `since`/`until`
  window (the check sits before the `inside` test). Under the rule of the window a tool use falls
  in, that stays acceptable. The Driver states in the PR which time places a tool use (its
  record's `timestamp`).
- Update the docstrings of `_grill_use` and `usage`: they describe the rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/commands.py`

- `_cost_rows` calls `costs.session_costs(..., split=steering)` with the claim window
  (`_window(d, uuid)`). This is the steering row of a direct batch, and it must use the strict
  rule.
- `_chief_line` makes three calls: `whole` (no split), `since` (from `d["created"]`, split) and
  `steered` (the claim window, split, only for a claimed transcript). Each must pass the claim
  window(s) of that transcript (`_window(d, uuid)`, for each claim of a Chief of Staff
  transcript in `chief_sessions(d)` / `_claimed(d)`), so that the strict rule applies inside it
  and the loose rule outside it.
- A Foreman's transcript is never split (`split=steering` is false). It is unchanged.
- Labels (`STEERING`, `STEER_OUT`, `GRILL_OUT`, `WHOLE`, `UNSPLIT`) and the output layout do not
  change.

### Cards

- `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself", bullet **Your
  epoch**: the parenthesis "(a turn that names a CR's `01-intent.md`, `02-answers.md`,
  `03-change-spec.md` or `work/specifying`, or starts a spec-writer)" becomes the new rule. A
  turn that writes one of those files, or starts a spec-writer, leaves the row. A turn that only
  names or reads them stays on it. A turn is attributed whole. The rest of the bullet does not
  change. In the same bullet (or in "Backlog and grill", where `work/specifying` and the answers
  are written), add one short sentence: the Chief of Staff writes a CR's `01-intent.md`,
  `02-answers.md`, `03-change-spec.md` and `work/specifying` with the host's Write (or Edit)
  tool, never with a shell command, because the CLI recognises grill work only by that write.
- `skills/chantier/references/status-layout.md`, second table (around line 133): "every call of a
  turn that names a CR's …" says the same rule in the steering window (writes or starts a
  spec-writer) and keeps "names" for the rest of the time since the batch opened. Without this
  change the two cards would disagree with each other and with the CLI.
- No other card states the rule. A Grep for "names a CR" and "grill turn" outside `.agents/` and
  `evals/results/` finds only these two cards, `costs.py` and the scenario. Both hosts' agent
  files (`agents/`, `com.github.copilot/agents/`) do not change.

### Tests: `skills/chantier/scripts/cli/tests/test_costs.py`

Extend `test_a_turn_naming_the_answers_is_grill_and_a_turn_without_is_not`, or replace it with
one parametrized test. Keep it short (AGENTS.md: tests few and fast). With a window given as the
steering window:
- an `Edit` of `x/02-answers.md` is grill;
- an `Agent` with `subagent_type` `chantier:spec-writer` is grill;
- an `Agent` with `subagent_type` `chantier:cr-driver` whose prompt names
  `x/03-change-spec.md` is steering;
- a `Write` of `x/retro.md` whose content names `03-change-spec.md` is steering;
- a `PowerShell` or `Bash` command that names `03-change-spec.md` is steering;
- a `Read` of `x/03-change-spec.md` is steering;
- a Windows path (`x\\02-answers.md` in the JSON) written by `Edit` is grill.

Outside the steering window, a `Read` of `x/03-change-spec.md` is still grill (rule 3).

### Scenario: `scenario/run_scenario.py`

- `direct_batch`: the Chief of Staff transcript built around line 1328 holds, inside the window,
  a grill turn (`answers`, an `Edit` of `x/02-answers.md`) and a spec-writer turn. Both must
  still leave the row, and their checks (lines ~1354–1374) stay. Add, inside the window, one
  steering turn whose tool uses only name a specification:
  - an `Agent` with `subagent_type` `chantier:cr-driver` and a prompt naming
    `03-change-spec.md`;
  - a `Read` of a `03-change-spec.md`.

  Check that this turn's calls are on the `Chief of Staff, steering the batch` row (its call
  count grows, the grill line's does not), and that the lines still add up (the `whole`, `a`,
  `b` and total relations, adjusted).
- `foreman_chief_lines` (Foreman mode, line 1124): add one turn whose tool use only **reads**
  (or names in a command) a `03-change-spec.md`. Check that it stays on the grill line. This
  proves rule 3: no change outside the steering window.
- `scenario/README.md` (line ~54) says what the direct-batch step proves. Add a few words if the
  new checks change that.

## Out of scope

- The split outside a steering window: a Chief of Staff beside a Foreman, the pre-claim part,
  the whole-session line. Rule 3.
- Splitting a turn's calls between the two lines (rule 2).
- The shape of the cost table, of `cost --summary`, of STATUS.md and of the reports; the default
  budget.
- Copilot's cost path (`copilot_session_costs`), which has no split.
- Rewriting `evals/results/real-direct-2026-11-12-run1.md`, re-running an eval, and the eval
  kit's `audit.py` (it reads the `Chief of Staff, steering the batch` row, and that row only
  gets the right figure).
- A release-notes file (rule 6: one line in the PR description only).

## Evidence

The project's gate, from AGENTS.md: `just check` and `just scenario`. This CR changes the CLI and
cards. It does not touch `hooks/` or `types/`, so `just mod` does not apply. Record the long gate
with `$CHANTIER gate <cr> "just check" "just scenario"`.

**Run 1's transcript, priced again.** This is a scratch command at the pushed head: no committed
test and no committed transcript. Put its command and output in the CR's `evidence/`, and give
their figures in the PR description, naming the transcript by its session id only.

- The Chief of Staff's transcript of run 1 is session
  `bd7f6b12-6a6f-436b-b052-ba60efdf5909`, a `.jsonl` in the host's project folder for the eval
  workspace `chantier-eval/real-direct-2026-11-12`. It has 56 subagent transcripts beside it.
  The batch's `batch.json` was deleted at `close`, so the recorded claim time is gone. The
  closest stand-ins, read from the transcript's tool uses:
  - `open --direct` at `2026-11-12T19:42:32.259Z`;
  - `foreman transcript … --epoch 1` (the claim) at `2026-11-12T19:42:38.695Z`;
  - `close --batch 1 --yes` at `2026-11-12T20:12:35.259Z`, whose output (with the $1.18 / $9.41
    figures) came back at `2026-11-12T20:12:39.287Z`.
- **What must hold**, pricing `costs.usage(<transcript>, <claim>, <close output time>,
  split=True)` with the claim window as the steering window:
  - the grill part is **$0, 0 calls**;
  - the steering row is the window's own figure, about **$3.56** (rule 7);
  - the steering row is the old row plus the old grill part for the same window, so no call is
    lost or counted twice.
- **Read-only pre-check by the Spec-writer** (today's code, and a strict rule as above swapped in
  as a test, on the transcript as it is now; the Driver confirms or corrects it):
  - with the old rule, the window holds a row of $0.987 (18 calls) and grill of $2.573 (41 calls);
  - with the strict rule, a row of **$3.560 (59 calls)** and grill of $0.000 (0 calls).

  The report's **$3.61** is the sum of the two lines `cost` printed at the close: the steering
  row ($1.18, the claim window) plus the grill line ($2.43, *since the batch opened*). So it also
  holds the calls between `open` and the claim, which sit outside the steering window and, by
  rule 3, stay on the grill line. Rule 7 makes the window's figure the target. The PR states the
  figure it got and explains the gap to $3.61.
- **Which tool uses moved the turns (decision 4).** The same pre-check finds, inside the window,
  the tool uses that name a `GRILL_NAMES` entry:
  - the 5 `Agent` starts of `chantier:cr-driver`, whose prompts name `03-change-spec.md`;
  - one `Write` of `4-batch/retro.md` at 20:04:43, whose *content* names `03-change-spec.md`.

  Before the claim, one `PowerShell` read of a `3-ready/…/03-change-spec.md` at 19:42:24 also
  names one. After the close, the `Write` of the run report names `03-change-spec.md` too.
  Because a turn is classified by every tool use in it, including ones made after the window
  ends, these later writes moved turns that had already been priced. That is why the row read
  $1.333, then $0.987, then $1.18, and why it reads $0.987 today. The PR says which of these the
  Driver confirmed, and that a `take` output (a tool result) played no part.
- **Both directions.** The unit test and the scenario steps above show that a turn that records an
  answer or starts a spec-writer inside the steering window still leaves the row, and that a turn
  that only names or reads a specification stays on it.
