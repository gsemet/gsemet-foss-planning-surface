---
type: cr-change-spec
description: Change specification of escalation-gaps, from the grill of 2026-11-17 and the spec critic's two rounds.
---

# Change specification: escalation-gaps

## Goal

The user, 2026-11-17, after CR-317 of batch-23 took five rounds on the batch's model and never
escalated: a CR that keeps failing, whatever the cause, must get a stronger model on the code it
writes, said in a note, and a CR that still fails once escalated must stop and come back to the
user. The escalation model is no longer a fixed name in the CLI: it is a setting of the
configuration, per host and per role, shown and edited like the roles' models.

## Today, and the gaps this CR closes

`skills/chantier/references/concepts.md`, section "Escalation" (about line 563), has five
triggers. The gaps seen (intake):

1. The rounds trigger needs the Inspector still `FIX-REQUIRED`: a `blocked rounds:` with a red CI
   job, a gate broken after a rebase, or a Verifier `NOT VERIFIED` never escalates.
2. `rounds:` and `fix:` hand-backs are excluded from the blocked-twice trigger.
3. A Debugger that explains the red check but whose fix fails again never escalates.
4. The stack driver's red check that needs code is no trigger.
5. The judging agents never escalate (stated nowhere as a rule).
6. "Once per trigger" lets a CR escalated on one trigger fail again on another with no rule for
   what follows.

The CLI: `skills/chantier/scripts/cli/src/chantier/playbook/models.py` holds
`ESCALATION = {"claude": "claude-opus-5-5", "copilot": None}`; `playbook/lines.py`
`escalate_line(host)` prints one `escalate:` line from it; `commands/rules.py` `playbook()`
appends it, live, even with `--batch` (not the configuration the batch opened with).

## Decisions carried from 02-answers.md

- **escal-Q1 (when).** A `blocked rounds:` hand-back, whatever its cause (a red CI job, a gate
  broken after a rebase, a Verifier `NOT VERIFIED`, an Inspector `FIX-REQUIRED`), makes the next
  round's Coder start on the escalation model (`escalate: rounds`), said in the note as today.
  `rounds:` and `fix:` hand-backs count for the blocked-twice trigger.
- **escal-Q5 (round 2).** The first `blocked rounds:`, whatever its cause, escalates the next
  rounds' Coder once the user grants rounds; blocked twice covers the other reasons.
- **escal-Q2 (who).** The agents that write code escalate: `coder`, `debugger`,
  `conflict-resolver`. The judging agents keep their model: `inspector`, `verifier`,
  `investigator`, `spec-writer`, `spec-critic` (and `retro-critic`, `demo-explorer`, which judge
  or explore and write no code). The escalation model is a configured setting per host, in the
  project's `chantier.yaml` and on the board's Configuration page, not a fixed name in the cards
  or the CLI; on Copilot it may differ from Claude Code.
- **Spec questions (settled 2026-11-17).** The Drivers do not escalate: blocked twice escalates
  the next rounds' Coder, a failed restack its `conflict-resolver`.
- **escal-Q4 (round 2, replaces the first Copilot settlement).** A configured `escalation` on
  Copilot is accepted; the escalated role starts as a generic agent with that model, as a
  configured `model` does today (`hosts/copilot.md`, row "Start a generic agent", line 31,
  proved in CR-296), on a role with no user `agent` (see the second-critique settlement below).
- **escal-Q3 (escalated, fails again).** A CR already escalated that fails again stops,
  `blocked`, and goes up to the Chief of Staff as a question for the user (one more round, drop
  it, another approach). No further round without the user.
- **escal-Q6 (round 2).** Only escalations made for that CR (its rounds' Coder, its own Debugger
  or conflict-resolver) count for "once per CR, then the user"; a stack-wide escalation note
  does not.
- **Settled by the Chief of Staff (second critique).** On Copilot, an `escalation` the user wrote
  on a role that carries the user's own `agent` is refused at validation, as a `model` there is;
  a shipped `escalation` on such a role does not apply (that role does not escalate on that
  host, and the escalation note says so). The user's agent is never replaced by a generic one.
- **Settled by the Chief of Staff (round 2).** The CLI knows no role names: `escalation` is
  accepted only on a role whose shipped defaults carry one; the cards say who escalates.
- **batch-Q8.** This CR joins the next batch with the other five retro points of batch-23 and the
  four board CRs of 2026-11-17 (the Chief of Staff's concern; nothing to code here).

## What changes

### 1. Configuration: `escalation` per role, per host

- New role key `escalation` under `hosts.<host>.roles.<role>`, beside `model`, in
  `playbook/config.py` (`ROLE_KEYS` gains `"escalation"`; `_role` checks it with the same rules
  as `model`: one string, resolved by `models.resolve(host, ...)`, a plain `default`/`~`/`null`
  resets it, a quoted `"default"` is refused with `RESET_TEXT`).
- The CLI names no role: a user layer's `escalation` is accepted only on a role whose shipped
  defaults (`config/chantier.defaults.yml`, same host) carry an `escalation`; on any other role
  it is refused with one line, for example `role "inspector": "escalation" is set only on a role
  whose shipped defaults carry one: coder, conflict-resolver, debugger` (the list read from the
  defaults file, never typed in code). Which roles escalate, and why, is the cards' to say.
- On a host where a named agent cannot start with a model (`NAMED_AGENT_MODEL_AT_START[host]`
  False, Copilot today), the escalation follows the rules `model` follows there today
  (`layers._model_problems`, about lines 336-344; `config.start_refusal`, about lines 111-119):
  - on a role with no user `agent`, an `escalation` is accepted and the escalated role starts as
    a generic agent with that model (`start: generic`: `agent=(generic)`, the caller's tools, the
    printed contract lines);
  - on a role that carries the user's own `agent`, an `escalation` the user wrote is refused at
    validation, with the `start_refusal` text adapted to the key (remove "escalation" for
    <role> under hosts.<host>.roles, or name the model in your agent's own file), as a `model`
    there is refused; a shipped `escalation` on such a role does not apply: the role is absent
    from the effective escalation map on that host, so it does not escalate there (the
    trigger's note says `no escalation on this host` for it, as "No escalation printed" says).
    The user's agent is never replaced by a generic one.

  The resolved escalation carries its own `start` (`plugin`, `named` or `generic`), so the
  printed line says which.
- `config/chantier.defaults.yml`: `escalation:` on `coder`, `debugger` and `conflict-resolver`
  under both hosts: `claude-opus-5-5` under `hosts.claude`, and under `hosts.copilot` the
  Copilot identifier of Claude Opus 5.5 the file already uses (`claude-opus-5.5`). The file's
  header comment says what `escalation` is and that only a role carrying it here may set it. The
  test that keeps the defaults equal to the agent files,
  `skills/chantier/scripts/cli/tests/test_playbook_layers.py` (about line 52, today
  `assert set(node.value) == {"model"}`), accepts `escalation` beside `model` (each role's keys
  are `{"model"}` or `{"model", "escalation"}`, neither a reset) and still compares only `model`
  with the agent file; `escalation` is not in the agent files.
- `playbook/models.py`: `ESCALATION` and its comment are removed; nothing else reads them.
- Resolution (`playbook/layers.py`): the defaults layer is held apart and `judge()` resolves
  roles from the user layers only, so a default escalation would never reach the resolved
  record. `escalation` is resolved as `default_model` resolves a model: from the defaults layer,
  then the user layers above it (a user value wins; a plain `default` takes it back to the
  shipped one). A new `default_escalation(defaults, host, role)` beside `default_model`; the
  effective value per role, with its layer label (none for the shipped default), is held in the
  resolved configuration as a per-host map `escalation: {<role>: {id, name, start}}`, apart from
  `roles`, so the defaults still never count as a role setting.
- The batch records it: `open` stores that effective map in the batch's record (beside
  `data.playbook`, as `data.timing` is stored), even when no user file exists; a running batch
  keeps the escalation it opened with, whatever the files.

### 2. What the CLI prints

- `playbook` and `playbook --batch <batch>` (`commands/rules.py`, `playbook/lines.py`): each role
  line of a role with an escalation adds `escalation=<start> (<id>, <name>)` after its model, with
  its layer label when a user layer set it, and `(generic)` when that escalation starts generic.
  The last line stays one `escalate:` line, built from the effective escalation map:
  `escalate: coder opus (claude-opus-5-5, Claude Opus 5.5); debugger opus (...);
  conflict-resolver opus (...)`, or `escalate: (none on this host)` when no role has one. The
  shipped defaults alone (no user file) print it. With `--batch` it is read from the batch's
  recorded map, not the files; a batch recorded before this change, with no map, prints the
  shipped defaults' escalation for its host (as `recorded_timing` does for timing).
- The `team:` lines of `take`, `round` and `handoff` (`team_lines`) print `escalation=...` for a
  configured role whose escalation a user layer set, so a Driver reads it where it reads the
  worker's other keys. Otherwise the Driver reads the `escalate:` line of `playbook --batch`.

### 3. The board's Configuration page, and AGENTS.md

- `playbook/edit.py` `_row`: each role row gains an `escalation` entry shaped like `model`
  (`layers`, `effective`, `layer`) and a flag saying whether the row may carry one (its shipped
  defaults do); `KEYS` (the keys the page writes) gains `escalation`; `_flat` leaves it out of
  the generic leaves, like `model`.
- `board/web/js/views/config.js` (`roleRow`): an "Escalation" column, filled only on the rows the
  view flags (the page names no role), edited with the same model picker as the model (the
  host's catalog), with a "default" choice that resets it; a Copilot value shows it starts
  generic, as the model column does, and on a Copilot row with the user's own agent the cell
  shows the refusal (or that the shipped escalation does not apply), as the model cell shows
  its refusal. Strings in `board/web/js/i18n/en-board.js` and
  `fr-board.js`. The write goes through the existing `edit_surface_file` path and its checks,
  nothing new.
- `AGENTS.md`, the board paragraph ("it edits ... each role's agent and model, per host, in the
  project's configuration file"): amended in this CR's PR to "each role's agent, model and
  escalation, per host".
- Overlap: the CR `board-config-role-descriptions` also edits `edit.py` `_row` and `config.js`
  `roleRow`. Whichever of the two merges second rebases on the first; both changes add to the
  row and do not conflict in intent.

### 4. The cards: `concepts.md`, "Escalation", rewritten

- Opening paragraph: the escalation model is the role's `escalation` in the configuration, as
  `playbook` / `playbook --batch` prints it (the `escalate:` line, or `escalation=` on a `team:`
  line), passed as printed like any model; a printed generic start is started as "Starting an
  agent" says for `agent=(generic)`.
- **Who escalates:** only `coder`, `debugger`, `conflict-resolver`. The Drivers never escalate.
  The judging agents (`inspector`, `verifier`, `investigator`, `spec-writer`, `spec-critic`,
  `retro-critic`, `demo-explorer`) never escalate: a new one of them runs on its own model.
- **The triggers table** becomes:

  | Trigger | Who sees it | The new agent on the escalation model |
  | --- | --- | --- |
  | The rounds used up: a `blocked rounds:` hand-back, whatever the round's failure (a red CI job, a gate broken after a rebase, a Verifier `NOT VERIFIED`, an Inspector `FIX-REQUIRED`) | the CR Driver hands back `blocked rounds:` as always; the round limit stays the user's (`order rounds`): escalation never grants a round | once the user grants more rounds, the CR's next Driver is told `escalate: rounds` and starts the Coder of each new round on the coder's escalation model |
  | A CR blocked twice, for other reasons: two hand-backs `blocked` of the same CR that show trouble in the work: `refused`, `infra:` after its re-runs, `driver ended twice`, `stopped`, `rounds:` and `fix:` (a `question:`, `approval:`, `merge:`, `waits:`, `budget:` never counts; a Driver stopped from outside never counts), when the row above has not already escalated it | the Foreman (in direct mode the Chief of Staff), from `log <cr>` and the hand-backs | the CR's next Driver is told `take <cr> --note "escalate: blocked twice: <reasons>"` and starts the Coder of each new round on the coder's escalation model. A CR with no rounds (a release CR, a QA order's CR, whose `fix:` has no Coder to escalate): blocked twice goes straight to the user's question of "Once per CR, then the user" |
  | A red check the Debugger could not explain (its `diagnosis.md` names no cause with evidence) | the Driver that started it (CR or stack) | a new `debugger` on the same check, given the first `diagnosis.md` |
  | A conflict the resolver could not settle (other than "two product intents in conflict", which stays a question for the user) | the Driver that started it (CR or stack) | a new `conflict-resolver` on the same rebase, given the first `conflicts.md` |

  The restack row (a new stack driver on the escalation model) is removed: a failed restack
  escalates its `conflict-resolver` (the row above), and "blocked twice" no longer starts the
  CR's next Driver on the escalation model, only the next rounds' Coder.
- Gaps 3 and 4 need no row of their own: a Debugger whose explained fix fails again, and a stack
  driver's red check that needs code (sent as `anomaly` to the Foreman, then worked in the CR's
  rounds), end in the CR's hand-backs, which the two first rows count.
- **Said, never silent:** unchanged (`$CHANTIER note <cr> "escalated: <trigger>; <role> on
  <model as printed>"` before the start; one line per escalation in the retro).
- **Once per CR, then the user** (replaces "Once per trigger and per task"): a CR that holds an
  `escalated:` note made for that CR (its rounds' Coder, its own `debugger` or
  `conflict-resolver`) never escalates again and never swaps back. An `escalated:` note written
  on each CR of the stack for a stack-wide escalation (the stack driver's `conflict-resolver` on
  a restack) does not count for it. If such a CR fails again (a new `blocked` hand-back that
  counts for either of the two first rows, or its escalated `debugger` or `conflict-resolver`
  failing the same way), the Foreman (the Chief of Staff in direct mode) does not `take` it
  again: the CR stays `blocked` and goes up to the Chief of Staff as a question for the user,
  with the options one more round, drop it, another approach. No further round without the
  user's answer. A CR with no rounds blocked twice takes this same ask at once.
- **No escalation printed:** unchanged (`escalate: (none on this host)`, or no `escalation=` for
  that role: the trigger takes the existing route, the note says `no escalation on this host`).

### 5. The other cards and docs that name it

- `skills/chantier/references/driver.md`: the line at about 159 (read the `escalate:` line) names
  the `escalation=` of the `team:` line first, then `escalate:`; the paragraph at about 617 says
  `escalate: rounds` and `escalate: blocked twice` start each new round's `coder` on the coder's
  escalation model, and that the Driver itself keeps its model; the stack paragraph at about 754
  unchanged in substance.
- `skills/chantier/references/foreman.md` (about 186 and 317) and `chief-of-staff.md` (about
  1417): the two rounds-related routes as above, the "once per CR, then the user" ask (and the
  no-rounds CR's direct ask), and the restack lines: a failed restack goes to a new stack driver
  on the batch's model, its `conflict-resolver` escalating as in concepts.md. The ask to the
  Chief of Staff uses the existing means of those cards, no new one.
- `skills/chantier/references/hosts/claude-code.md`, row "Models": "a task under escalation runs
  the escalation model the role's `escalation` sets, as `$CHANTIER playbook` prints it".
  `hosts/copilot.md`, its models row: an escalated role starts as a generic agent with the
  printed escalation model (row "Start a generic agent", line 31, proved in CR-296), as a
  configured `model` does; a role with the user's own agent does not escalate on Copilot.
- `docs/agents-and-models.md` (about 145) and `docs/tutorial-claude-code.md` (about 233): the
  escalation model is the coder's, debugger's and conflict-resolver's `escalation` setting (Opus
  5.5 by default on both hosts), and only they escalate. The configuration doc that lists the
  role keys (where `model`, `agent`, `skills`, `tools` are listed) gains `escalation`.
- `evals/SCORECARD.md` J19: the expectation reworded to the new triggers and the stop after one
  escalation.
- Agent files (`agents/`, `com.github.copilot/agents/`): no change (the escalation is not a
  file's model).
- Overlap: the CR `take-base-nearest-pr` also edits `foreman.md` and `driver.md`; the overlap is
  textual only, resolved by whichever merges second rebasing.

## Out of scope

- Any change of the round limit or of who grants rounds (`order rounds` stays the user's).
- Escalating a judging agent or a Driver, or an effort setting.
- A CLI refusal that enforces the triggers: the cards say when and who; the CLI only checks,
  resolves and prints the models, and names no role (which roles may carry `escalation` comes
  from the shipped defaults file).
- The proof that a Copilot named agent takes a model at its start (`NAMED_AGENT_MODEL_AT_START`):
  escalation there uses the generic start, already proved.

## Evidence

- `just check` green (Linux, macOS, Windows).
- Tests, few and parametrized, in `skills/chantier/scripts/cli/tests/test_playbook_config.py`
  (update `ESCALATE` and the lines at 50, 60, 108):
  - shipped defaults, no user file, host claude: the `escalate:` line names coder, debugger and
    conflict-resolver on `opus (claude-opus-5-5, Claude Opus 5.5)`; host copilot: the same roles
    on `claude-opus-5.5`, each marked generic; a defaults file with no `escalation` prints
    `escalate: (none on this host)`;
  - a `chantier.yaml` setting `escalation: sonnet` on `coder`: the coder's role line shows
    `escalation=sonnet (...) [<layer>]` and `escalate:` names it; a plain `default` takes it
    back to the shipped one;
  - refusals, one parametrized test: `escalation` on `inspector` (a role whose defaults carry
    none); an unknown model; a quoted `"default"`;
  - Copilot: a user `escalation: gpt-6.1-sol` on `coder` is accepted and printed as a generic
    start;
  - Copilot, a role with the user's own `agent`: a user `escalation` on it is refused at
    validation with the `start_refusal`-shaped line; with no user `escalation`, the shipped one
    does not apply (the role is absent from `escalate:` and has no `escalation=` on its line),
    and no generic start is printed in place of the user's agent;
  - `test_playbook_layers.py` (about line 52): the defaults' roles carry `model` and optionally
    `escalation`, and `model` still equals each agent file's;
  - `open` with no user file records the shipped escalation map; `playbook --batch`: a batch
    opened before a file change keeps its recorded escalation; a record with no map prints the
    shipped defaults'.
- The board's config view (`config_view`): one test that the coder row carries `escalation` with
  its layer and the inspector row is not flagged, and that a write of it through
  `edit_surface_file` lands in the surface's `projects/<name>/chantier.yaml`.
- `just test` stays within its time budget (AGENTS.md).
- `just scenario (ubuntu-latest)` green at the PR's head (the change touches the CLI and the
  cards); the local `chantier gate` run if this CR is on top of the batch's stack.
- No screenshot rule applies (the pane is not touched).
