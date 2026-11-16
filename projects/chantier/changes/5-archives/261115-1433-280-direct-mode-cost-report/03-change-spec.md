# Change Specification: direct mode's cost report says "Chief of Staff" and its lines add up

Short name: `direct-cost`. No issue.

## Goal

In a direct batch the Chief of Staff steers. Its cost report must say so: no line of `chantier
cost` names a Foreman when no Foreman ran. Its lines must also add up when read top to bottom. In
real-direct run 3 (2026-11-15, audit `C:/Users/gaeta/Projets/chantier-eval/real-direct-2026-11-15.audit.md`,
section "Cost") the report printed:

```text
Chief of Staff, steering the batch: $3.390 (62 calls, 30%)
...
Chief of Staff, whole session: $1.64, context 224,242 tokens; ...
```

and `cost --by cr` printed `foreman: $3.776 (70 calls)` as its first line. A whole session that
costs less than one part of it cannot be right as read, and `foreman` is the wrong role in
direct mode.

## Why the figure reads wrong today (the cause, for the Driver)

`skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py`, `_absorb`:
`c.whole_usd += sum(r["usd"] for r in whole) - inside`. Here `inside` is everything the Chief of
Staff's session spent inside its steering window, minus the spec-writer and spec-critic rows:
the steering row, its own subagents, and every Driver and worker of a direct batch, since they
are the session's subagents. So the "whole session" figure is in fact "the session minus the
batch's spend". The cards and docs say this ("the `Chief of Staff, whole session` line leaves the
steering window out"), but the label says "whole session". It is printed under a steering row
that it does not hold, so the two lines contradict each other.

## Decision carried

`02-answers.md`: the request's scope stands as written. "Fix the figure so the lines add up, and
name the steering role by the mode". The behaviour below is the plain reading of that sentence;
the open question at the end asks the user to confirm the first point.

## What changes

### 1. The whole-session figure covers the whole session, and says which part of it is the batch's

File: `skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py`.

- `Chief of Staff, whole session` is the price of every call of the Chief of Staff's session or
  sessions (`chief_sessions(d)`), over their whole life: the main transcript and every subagent,
  the steering window included. It no longer subtracts `inside`.
- When some of that sum is in the batch's spend (`inside` calls > 0: a direct batch, or a batch
  the Chief of Staff steered before a Foreman claimed it), the line names that part right after
  the amount:

  ```text
  Chief of Staff, whole session: $13.16 ($11.52 of it in the batch's spend), context 224,242 tokens; not counted: 0 compactions since the batch opened, which leave no record (about $0.12 each)
  ```

  The two amounts use `spend()`, so `at least` and `not priced` behave as on every other line.
  The parenthesis is left out when the session has no call in the batch's spend (a Foreman batch
  the Chief of Staff never steered). The line then reads as it does today, with the same figure
  as today.
- Reading top to bottom, then: whole session = its part in the batch's spend + `steering the
  batch (outside the budget)` + `grill and specifications with the user` + what the session spent
  before the batch opened. The whole-session figure is never lower than any `Chief of Staff, ...`
  line above it, nor than the direct batch's steering row.
- Not changed: the unpriced bookkeeping (`whole_un` now holds the whole session's unpriced
  calls, not reduced by `inside_un`; the batch's part reports its own), the context size, the
  compaction count, the `steering the batch (outside the budget)` and `grill and specifications`
  lines, `_chief_unknown` (Copilot and a missing transcript still give `unknown`, never
  `$0.00`), and the batch's spend and budget. The whole session is still outside the spend and
  the budget.
- `chief_line`'s docstring and the comment in `_absorb` say the new meaning.

### 2. `cost --by cr` names the steering role by the mode

File: `skills/chantier/scripts/cli/src/chantier/commands/cost/command.py`, `_by_cr` (printing
only). The internal group key stays `"foreman"`, because `breakdown.cost_summary`,
`batch_status.py`, `closing.py`, `close_archive.py` and `board/costs.py` read it. Only the printed
label of that group changes:

- The group holds no Chief of Staff steering row (main row of type `chief-of-staff`): `foreman`,
  unchanged.
- It holds only Chief of Staff steering rows (a direct batch never taken over):
  `Chief of Staff, steering the batch, and its own subagents`. Run 3 would have printed
  `Chief of Staff, steering the batch, and its own subagents: $3.776 (70 calls)`.
- It holds both (a direct batch a Foreman took over):
  `Chief of Staff, steering the batch, and the Foreman, with their own subagents`.

`cost`, `cost --explain` and `cost --summary` already name the direct batch's steering
`Chief of Staff, steering the batch` (`breakdown.cost_label`, `_steers`): keep them as they are.

### 3. The cost errors name the steering session by the mode

The messages that say "Foreman" for a transcript that, in a direct batch, is the Chief of
Staff's:

- `command.py`, `cost`: `no Foreman transcript recorded: the Foreman runs `chantier foreman
  transcript ...``. For `d.steering == "direct"`: `no steering transcript recorded: the Chief of
  Staff runs `chantier foreman transcript <var> --epoch <n>``. The Foreman wording stays for a
  Foreman batch. The command's name `foreman transcript` does not change.
- `sessions.py`, `foreman_uuid`: `no Foreman transcript recorded`. Use the same mode-dependent
  wording. The function reads the record, so it can tell the mode.
- `sessions.py`, `cost_rows`: `no priced calls in the Foreman transcripts`. In direct mode, say
  `the steering transcripts (the Chief of Staff's)`.

The exit codes do not change.

### 4. Cards and docs say the new meaning

- `skills/chantier/references/chief-of-staff.md`, around line 1364: "the `Chief of Staff, whole
  session` line leaves the steering window out" becomes: the line prices the whole session,
  steering window included, and names in a parenthesis the part that is in the batch's spend.
  The compacting advice (line 1149) reads only the context size: unchanged.
- `skills/chantier/references/status-layout.md`, "Cost", second table: `whole session` is
  copied as printed, its parenthesis included. It is the one `Chief of Staff, ...` line that
  holds a part of the batch's spend, and the parenthesis says how much. "You copy, you compute
  nothing" still holds.
- `docs/costs.md`, last paragraph ("its line shows two figures ..."): say that the whole-session
  figure covers the whole session and names its part in the batch's spend in a direct batch.
- `docs/use-cases-direct.md`, "What it costs": the same, in one sentence.
- `scenario/README.md`, line ~202: "a whole-session line that leaves the steering window out"
  becomes "a whole-session line that holds the steering window and names it".

`agents/` and `com.github.copilot/agents/` are not touched. No card's role contract changes
beyond the wording above.

## Out of scope

- `cost --explain` and `cost --by cr` refused on a paused batch without `--batch` (run 3's
  operator note). That is another item of the eval study.
- The board's cost keys (`per_cr["foreman"]`) and what the board shows.
- A Foreman batch's `foreman` label in `cost --by cr` and the `Foreman` row of `cost`.
- Any change to what counts in the batch's spend or budget, to the grill attribution or to the
  steering window.
- The eval kit (`evals/kit/audit.py`): it reads the steering row, not the whole-session line.

## Evidence

- `just check` passes (lint, `just test`, release notes), on Linux, macOS and Windows.
- `just scenario` passes, the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's
  head, and, if this CR is on top of the stack, a local `chantier gate` run passes on Windows,
  as AGENTS.md says.
- Scenario, direct batch section (`scenario/run_scenario.py`, from line ~2002):
  - The check "the Chief of Staff's lines add up ... and the whole session leaves the steering
    row out" becomes: the whole-session amount minus its parenthesis amount equals today's
    figure (the five calls outside the batch's spend, the same tolerance). The parenthesis amount
    equals the headline's batch spend (one steering session) within $0.01. The whole-session
    amount is at least the steering row.
  - A new check runs `cost --by cr` on that direct batch. Its first line after the headline starts
    with `Chief of Staff, steering the batch, and its own subagents: $`, and no line starts with
    `foreman:`.
  - The compaction check on the whole-session line stays as it is.
  - If the scenario has a takeover case (Chief of Staff, then a Foreman's claim, around line
    ~2108), add a `cost --by cr` check there for the "and the Foreman, with their own subagents"
    label. If it has no priced transcripts there, say so in the PR's Known gaps rather than build
    a new fixture.
- pytest (`skills/chantier/scripts/cli/tests/test_cost_reading.py`): the Foreman-mode checks
  (`foreman: $0.391 (30 calls)`, `Chief of Staff, whole session: $9.02`, the a + b = whole check
  of `check_the_chief_lines_add_up`) keep passing unchanged. They prove the parenthesis is left
  out and the figure is unchanged when the Chief of Staff never steered.
  `test_cost_copilot.py` keeps its `foreman:` line and its `unknown` Chief lines. Add no new test
  file. If one refusal message test asserts the old "no Foreman transcript recorded" text for a
  direct batch, parametrize it with the direct wording. `just test` stays within its time bound.
- The PR body quotes, from a scenario run at the head, the direct batch's `cost` and
  `cost --by cr` outputs, showing the whole-session line with its parenthesis and the renamed
  steering line.

## Open questions for the user

1. The whole-session line: I took "fix the figure" to mean that it now prices the whole session,
   steering window included ($13.16 in run 3, "$11.52 of it in the batch's spend"). The other
   reading keeps today's figure ($1.64, the session minus the batch's spend) and only renames
   the line to say so, for example `Chief of Staff, whole session outside the batch's spend:
   $1.64`. Which one do you want? The specification is written for the first. The second would
   change only the label, the cards' wording and the scenario's text.
