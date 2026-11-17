# Change Specification: Copilot role model defaults

Date: 2026-11-16 (third run, after Q10 and Q11 and the spec critic's fixes). Sources:
[intent](01-intent.md), [answers](02-answers.md), [original request](intake/request.md). No
tracker issue.

## Goal

On Copilot, each chantier role runs on the model the user chose: CR Driver on Claude Sonnet 5.5,
Investigator on GPT-5.6 Luna, Coder and Inspector on GPT-6.1 Sol, Verifier, Debugger and Conflict
resolver on GPT-6.1 Terra. Each model is named by its identifier, from a source. This CR changes
the four agent files, adds GPT-6.1 Terra to chantier's hand-written Copilot model list, updates
the documentation, and prepares the proof the user runs later on Copilot (Q2). Claude Code, every
other role and the cost computation stay as they are. Building chantier's Copilot model list from
GitHub's tables is the separate CR [copilot-model-catalog](../copilot-model-catalog/) (Q10).

## Decisions carried from the grill

- Q1: ship now, as a small independent CR. The models change in `com.github.copilot/agents/` and
  in the documentation. The future configuration CR
  ([model-defaults-board-config](../model-defaults-board-config/01-intent.md)) takes these values
  as its Copilot defaults; this CR does not wait for it.
- Q2: this CR does not run a Copilot session. It prepares an evaluation the user runs in a later
  CR on Copilot: for each role, the model the host records as used, and what to do when the host
  enforces another one. Supported hosts: the Copilot App (on the Copilot SDK) and the Copilot CLI.
  VS Code's local harness is not supported; the "Copilot harness in VS Code", arriving, uses the
  Copilot CLI and SDK. What Copilot allows is quoted from its own documentation, with links.
- Q3 and Q4: a Copilot model is named by its identifier (`gpt-6.1-terra`), not its display name
  (`GPT-6.1 Terra`), and the identifier comes from a source, never a guess.
- Q5: the identifier is the display name in lower case, each space becomes `-`, the dots stay
  (`GPT-6.1 Terra` → `gpt-6.1-terra`, `Claude Sonnet 5.5` → `claude-sonnet-5.5`); GPT-6.1 Terra's
  identifier `gpt-6.1-terra` is in the "Supported models" table of the Copilot CLI command
  reference. "An explicit `--model` takes precedence over a custom agent's `model` unless the
  agent sets `model-policy: required`": every chantier Copilot agent sets it, so the agent file's
  model is the one the host runs. CR-296's "Required model enforcement replaced requested model
  `gpt-6.1-sol` with `gpt-5.6-luna`" came from `chantier-coder.agent.md` declaring Luna; the fix
  is the file's model, not an override.
- Q6, Q7: superseded here by Q10; they go to copilot-model-catalog with Q5 to Q8's decisions.
- Q8: the Investigator stays on `gpt-5.6-luna`. (The comparison with the CLI reference's list is
  copilot-model-catalog's.)
- Q9: the cost computation does not change: on Copilot, `chantier cost` keeps its prices from
  copilot-session-usage. A bug found in copilot-session-usage is reported as an issue on that
  project, never worked around in chantier.
- Q10: a separate CR for the catalog. This CR ships the four `model:` lines, GPT-6.1 Terra added
  by hand to `MODELS["copilot"]`, the docs and the eval preparation. The copy of GitHub's tables,
  `just copilot-models`, `copilot-models.json`, a `MODELS["copilot"]` built from it and their
  tests are copilot-model-catalog's.
- Q11: the model check goes in the current `evals/copilot/RUNBOOK.md`; the inbox CR evals-rework
  moves it when it replaces that runbook.
- Spec critic: yes.

## What the host has shown (CR-296, Copilot App, 2026-11-16)

The record: the planning surface's `projects/chantier/changes/4-batch/3-done/296-improve-skill-boot/work/handoff.md`,
"Model evidence", lines 21-25 (from this CR's folder:
`../../../4-batch/3-done/296-improve-skill-boot/work/handoff.md`).

- Round 5: the named Coder (`chantier-coder`), started through `task` with the model
  `gpt-6.1-sol`, ran on its file's `gpt-5.6-luna`; the host said "Required model enforcement
  replaced requested model ...".
- Round 6: a generic agent started through `task` with the model `gpt-6.1-sol`; the steering
  session's event log, `subagent.started` and `subagent.completed`, carried `model: gpt-6.1-sol`,
  `firstDispatchedModel: gpt-6.1-sol`, `modelSelectionSource: explicit_override`. Read after the
  run, not a check before it. The record names no field of these events that names the agent.

## What changes

### 1. The Copilot agent files (`com.github.copilot/agents/`)

Only the `model:` line changes, in the same form as today (`[Display name, identifier]`); every
other frontmatter key (`model-policy: required`, `tools`, `strict-tools-list`, `user-invocable`)
and the body stay byte for byte. The Claude Code agent files (`agents/`) do not change.

| File | Today | After |
| --- | --- | --- |
| `chantier-cr-driver.agent.md` | `[Claude Sonnet 5.5, claude-sonnet-5.5]` | unchanged |
| `chantier-investigator.agent.md` | `[GPT-5.6 Luna, gpt-5.6-luna]` | unchanged |
| `chantier-inspector.agent.md` | `[GPT-6.1 Sol, gpt-6.1-sol]` | unchanged |
| `chantier-coder.agent.md` | `[GPT-5.6 Luna, gpt-5.6-luna]` | `[GPT-6.1 Sol, gpt-6.1-sol]` |
| `chantier-verifier.agent.md` | `[GPT-6.1 Sol, gpt-6.1-sol]` | `[GPT-6.1 Terra, gpt-6.1-terra]` |
| `chantier-debugger.agent.md` | `[GPT-5.6 Luna, gpt-5.6-luna]` | `[GPT-6.1 Terra, gpt-6.1-terra]` |
| `chantier-conflict-resolver.agent.md` | `[GPT-5.6 Luna, gpt-5.6-luna]` | `[GPT-6.1 Terra, gpt-6.1-terra]` |

The other Copilot agents keep their model (Demo explorer stays on GPT-5.6 Luna; the Opus roles
stay on Claude Opus 5.5). When the Debugger and the Conflict resolver start does not change.

### 2. The CLI's model list (`skills/chantier/scripts/cli/src/chantier/playbook/models.py`)

- `MODELS["copilot"]` stays hand-written and gains one row, after GPT-6.1 Sol:
  `Model("gpt-6.1-terra", "GPT-6.1 Terra", "")`. Nothing else in the file changes:
  `MODELS["claude"]`, `SETS_MODEL_AT_START` (`copilot: False`), `ESCALATION`, `normalise`,
  `resolve`, `HOST_NAMES`.
- Behaviour the user sees: `chantier playbook --host copilot` and `chantier preflight` now resolve
  `gpt-6.1-terra` (or `terra`) in `chantier.yaml`'s `model:`, then refuse it like any model on
  Copilot with "cannot set a model when it starts an agent" (unchanged). `model: gpt` stays
  ambiguous (Luna, Sol, Terra); `model: opus` still resolves to Claude Opus 5.5 alone.
- The cost computation does not change (Q9): `costs/` is untouched.

### 3. Documentation

- `docs/agents-and-models.md`, "Models": the Copilot column becomes:
  - CR driver: Claude Sonnet 5.5 (unchanged);
  - Coder: GPT-6.1 Sol;
  - Investigator, Demo explorer: GPT-5.6 Luna;
  - Inspector: GPT-6.1 Sol;
  - Verifier, Debugger, Conflict resolver: GPT-6.1 Terra;
  - every other row unchanged. The Claude column does not change (rows may be split to hold the
    Copilot values; each split row keeps Sonnet 5.5 on Claude). After the table, the sentence "On
    Copilot the models are its agent files' models" gains: the agent files set
    `model-policy: required`, so the file's model wins over a model passed at the start
    ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#command-line-options));
    seen in the Copilot App in CR-296 (a Coder started with GPT-6.1 Sol ran on its file's GPT-5.6
    Luna).
- `skills/chantier/references/hosts/copilot.md`, Tools table:
  - row "Models" becomes: "each plugin agent's file names its model (`[display name, id]`), with
    `model-policy: required`: Luna, Sol, Terra, Sonnet 5.5 or Opus 5.5. The identifier is the
    display name in lower case, spaces as `-`, dots kept, as the CLI reference's "Supported
    models" lists them ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference))."
  - row "Models at an agent's start (capability, start value)": keeps "capability: none; no start
    value" and the refusal with the CLI's message "cannot set a model when it starts an agent".
    The words "unproved" and "Trial that would settle it: ..." are replaced by the observation:
    "observed in the Copilot App (CR-296 rounds 5 and 6, 2026-11-16; record: the planning
    surface's `296-improve-skill-boot/work/handoff.md`, "Model evidence"): a plugin agent started
    through `task` with another model runs on its file's model, the host saying "Required model
    enforcement replaced requested model ..."; a generic agent took the model passed
    (`modelSelectionSource: explicit_override`). Documented, unproved here: the Copilot CLI's
    `--model` loses to an agent's `model-policy: required`" (link as above).
  - one new row, "The model a role ran on": "the steering session's `events.jsonl`,
    `subagent.started` and `subagent.completed`: `model`, `firstDispatchedModel`,
    `modelSelectionSource`, observed in CR-296 round 6 (record as above). `subagent.failed`
    carries `model` too, documented
    ([SDK custom agents](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/custom-agents)),
    not observed. Check: `evals/copilot/RUNBOOK.md`, Models".
  - Known host issues, each with its link, as one line under the table: a `model` array once
    refused by the CLI ([copilot-cli#2133](https://github.com/github/copilot-cli/issues/2133)); an
    SDK-provided agent's model dropped at `session.create`
    ([copilot-sdk#1609](https://github.com/github/copilot-sdk/issues/1609)); an unknown identifier
    falling back silently ([copilot-sdk#2856](https://github.com/github/copilot-sdk/issues/2856));
    sub-agents on another model than the session's with no sign, fixed in CLI v1.0.62
    ([copilot-cli#3824](https://github.com/github/copilot-cli/issues/3824)).
  - The "Startup core" section does not change, so the startup budget test
    (`test_startup_manifest.py`) holds.
- `docs/hosts.md`: the Foreman-mode table does not change. After the paragraph on direct mode
  (the one that ends "checked by `chantier preflight --direct`" and the heartbeat), one paragraph:
  on Copilot, chantier runs in the Copilot App (on the Copilot SDK, like Claude Desktop: the
  table's "Copilot SDK host", Foreman and direct mode) and in the Copilot CLI, in direct mode (a
  Copilot agent session in the terminal; the user's statement of 2026-11-16, unproved until a
  run). VS Code's local harness is not supported (it does not use the Copilot CLI or SDK); the
  Copilot harness in VS Code, arriving, uses them (unproved until a run).

### 4. The evaluation the user runs later (`evals/`)

- `evals/copilot/RUNBOOK.md`: a new section "Models", run in the same Copilot App chat, before
  the batch's go or after `close --yes`:
  1. The operator asks the Chief of Staff to start, with `task` and no model, each plugin agent
     `chantier-<role>` once (all fourteen), in the order the section lists them (the order of the
     script's table, below), one at a time: each waits for its answer before the next starts.
     Each gets the prompt `model probe` and answers its refusal line (a prompt that is not
     chantier's); that answer runs on the agent's model, so the host records it. About fourteen
     short calls.
  2. The operator runs `uv run --no-project python <this checkout>/evals/kit/copilot_models.py`
     (point below) on the Chief of Staff's session and pastes its output into the report.
  3. Where available, the operator also records the account's identifiers with
     `copilot --silent -p "/model --list --json"` (it works only sometimes,
     [copilot-cli#700](https://github.com/github/copilot-cli/issues/700)); a difference with the
     agent files' identifiers (`gpt-5.6-luna` among them, Q8) is reported, not fixed in the run.
  4. When a role ran on another model than its file's, or the host printed an enforcement or
     refusal message (a plan without the model included): the report names the role, the
     expected identifier, the recorded one and the host's exact text. Nothing is worked around:
     the agent file is not changed to follow the host, no override is passed. The finding goes to
     `hosts/copilot.md` ("Models" rows) through an inbox CR, which the Chief of Staff offers the
     user.
  - "What it proves" gains a line: each role runs on its agent file's model, from the host's own
    record.
- `evals/kit/copilot_models.py` (standard library only), writing nothing:
  - reads `events.jsonl` of a Copilot session (`--session <id>`; with none, the most recently
    modified folder of `<COPILOT_HOME or ~/.copilot>/session-state/`);
  - takes each `subagent.started`, `subagent.completed` and `subagent.failed` event, and from its
    `data` the fields CR-296 round 6 recorded: `model`, `firstDispatchedModel`,
    `modelSelectionSource`. It reads no other field unless the Coder finds it in the Copilot SDK's
    published event schema, cited by link in the script's docstring and in the PR; in particular
    no `agentType` (or any agent-naming field) without that source;
  - prints one line per event: its type, the three fields (`absent` for a missing one), and the
    agent field when a sourced one is present, else `no agent field in the event`;
  - then one row per role, in the runbook's order, the expected identifier read from
    `com.github.copilot/agents/chantier-<role>.agent.md` of this checkout. With a sourced agent
    field, a role's events are those naming it; without one, the n-th `subagent.completed` (or
    `subagent.failed`) event is matched to the n-th role of the order, and the row says
    `matched by order`. Recorded: the event's `model`, `not recorded` when absent. Verdict: `ok`
    or `MISMATCH`. `not started` only for a role a sourced agent field shows absent; when matching
    by order and the count of ended events is not fourteen, the script prints the two counts and
    every role row is `unmatched (event count)`;
  - exits 0 when every role is `ok`, else 1.

### 5. Tests (`skills/chantier/scripts/cli/tests/`)

Few, parametrized, fast (`just test` budget unchanged):

- `test_plugin_files.py`:
  - `test_the_model_table_names_every_model_the_agent_files_name` holds with `gpt-6.1-terra` in
    `MODELS["copilot"]` (it fails without it); extend it on Copilot: the agent file's display name
    equals `MODELS`'s name for that identifier.
  - `test_the_model_table_names_no_model_twice_per_host` holds unchanged.
  - new, one parametrized test of `evals/kit/copilot_models.py` on a fake session (`COPILOT_HOME`
    in a temporary folder, events with the round 6 fields and no agent field): all `ok` (exit 0),
    one `MISMATCH` (exit 1), one `not recorded`, a wrong count (`unmatched (event count)`, exit
    1); each line of an event without an agent field says `no agent field in the event`.
- `test_playbook_config.py`, `test_playbook_and_preflight_name_the_problem_and_its_line`: holds
  unchanged (`model: gpt` names Luna and Sol; `model: opus` still resolves on Copilot and is
  refused with "cannot set a model when it starts an agent").

## Out of scope

- chantier's Copilot model list built from GitHub's tables: the copy of `github/docs`
  `data/tables/copilot/` tables, the `just copilot-models` refresh recipe and its script,
  `copilot-models.json`, a `MODELS["copilot"]` built from it, the catalog rule (Q7), the
  comparison with the CLI reference (Q8), the plans shown, and their tests. All in
  [copilot-model-catalog](../copilot-model-catalog/) (Q10).
- The Claude Code agent files and Claude's models, prices and escalation.
- The other Copilot roles' models (Demo explorer, Opus roles), `model-policy`, tools and bodies.
- The configuration system of model-defaults-board-config (it takes these values later).
- Running any Copilot session, resuming CR-296, changing installed plugin files.
- Any change to how a Copilot batch is priced (Q9). A copilot-session-usage bug met during the
  work is reported as an issue on that project, not worked around.
- VS Code's local harness.
- Moving the model check out of `evals/copilot/RUNBOOK.md` (evals-rework's, Q11).

## Evidence

- `just check` (lint, tests, release notes) green on Linux, macOS and Windows.
- `just scenario` green (the CLI changes): the pipeline's `just scenario (ubuntu-latest)` job at
  the PR's head, and the local run on Windows when the CR is on top of its stack (AGENTS.md).
  `just mod` is not needed (`hooks/` and `types/` untouched).
- `git diff` of `com.github.copilot/agents/`: four `model:` lines changed, nothing else;
  `agents/` untouched; `costs/` untouched; `models.py`: one row added.
- `chantier playbook --host copilot` with no `chantier.yaml` prints the plugin's agents as before;
  with `roles: {coder: {model: gpt-6.1-terra}}` it refuses with "cannot set a model when it starts
  an agent".
- `evals/kit/copilot_models.py` run on the test's fake session, its output pasted in the PR.
- The Copilot proof itself (each role on its model, identifiers confirmed by the host) is the
  user's later run of `evals/copilot/RUNBOOK.md`, "Models"; the PR's Known gaps names it ("model
  defaults not yet observed in a real Copilot session").
- No CI job is added or changed.

## Open questions

None.
