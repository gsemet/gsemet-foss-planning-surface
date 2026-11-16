# Change Specification: a model per role on each host

Date: 2026-11-16. Split from model-defaults-board-config by its Q18 (the user's choice): (B), the
second of a stack of three. Sources: [request](intake/request.md); the grill is
model-defaults-board-config's [answers](../model-defaults-board-config/02-answers.md) (Q3, Q5,
Q6, Q8 to Q10, Q12 as narrowed by Q17, Q13, Q16, the Chief of Staff's grill cost line decision)
and its [intent](../model-defaults-board-config/01-intent.md). No tracker issue.

## Depends on, and the stack

The stack, bottom to top: [copilot-role-models](../copilot-role-models/03-change-spec.md),
[copilot-model-catalog](../copilot-model-catalog/),
[model-defaults-board-config](../model-defaults-board-config/03-change-spec.md) (A), this CR
(B), [board-config-page](../board-config-page/) (C, on A and B).

- copilot-role-models: the Copilot agent files' `model:` lines, the `hosts/copilot.md` rows
  "Models", "Models at an agent's start" and "The model a role ran on", the
  `evals/copilot/RUNBOOK.md` section "Models" and `evals/kit/copilot_models.py`. This CR edits
  what that one writes.
- copilot-model-catalog: where `MODELS["copilot"]` is built. Where this CR changes a Copilot
  `Model`'s `start` value (section 2), the change goes there.
- A: the configuration in layers, every role setting per host (`hosts.<host>.roles`, Q16), each
  value with its layer, a role's default model from `config/chantier.defaults.yml` and its
  configured model from the user layers only (A, section 3), the batch's frozen record. This CR
  replaces A's rule "any other configured model on Copilot is refused" with the four starts below.
- C shows this CR's starts on the board.

## Goal

The user changes a role's model on either host, from the configuration. Where the host can start
the role's named agent with a model given at the start (Claude Code, proved), that agent keeps
its own tools and runs the chosen model. Where it cannot yet (Copilot, until proved), a generic
agent runs the role, its whole contract in its prompt, with the chosen model, and chantier says
plainly that its tools are the caller's, not restricted. Each host declares that one capability,
so Copilot (or a host added later) moves to the first case by changing one value. The Copilot
Coder's agent file stops enforcing its model, and the Copilot eval gains the probe that tells
whether a named Copilot agent runs a model given at its start.

## Decisions carried from the grill

- Q3: no generated agent file, anywhere (plugin, managed folder, workspace, user folder). What a
  host cannot apply at an agent's start is refused on that host, with the reason.
- Q5, Q6: a model per role, configurable, on both hosts, is in scope. Claude Code: the Agent
  tool's `model` parameter wins over the agent file's `model` (proved, used in every batch).
  Copilot: documented, unproved: a model given at the start wins over a custom agent's `model`
  unless the agent sets `model-policy: required`. Neither host changes a named agent's tools at
  its start.
- Q8, narrowed by Q9: per role, nothing set: the plugin's agent with its file's model; an agent
  name: the user's own agent runs the role (its file, its tools, its model); a model other than
  the default: on a host that can start a named agent with a model, the role's agent starts with
  that model and keeps its file's tools; on a host that cannot, no agent file is used and a
  generic agent starts with the role's whole contract in its prompt, rebuilt by chantier, and the
  model. This is the user's configuration, said by the CLI, the board and the playbook, never a
  fallback. Each host declares the capability; Copilot switches once proved, with nothing else to
  rewrite; a host added later declares its own.
- Q10: a role's tools change only by naming the user's own agent. No `tools` field restricts
  anything. A generic agent has the caller's tools: the CLI says "the caller's tools, not
  restricted".
- Q13: on Copilot, the user's own agent named for a role together with a model is refused with
  the reason at the batch's open (and wherever the playbook is read); no generic agent in its
  place.
- Q12, narrowed by Q17: `model-policy: required` is removed from `chantier-coder` only (the
  probe's agent), not from the other thirteen Copilot agent files, until the proof covers them.
  Copilot's capability stays "no" until the user's Copilot run; this CR prepares the probe. The
  test asserting `model-policy: required` changes accordingly.
- Q16: the configured model is per host (`hosts.<host>.roles.<role>.model`); nothing is resolved
  for a host from another host's section.
- The Chief of Staff's decision, accepted: a Spec-writer or Spec critic started as a generic
  agent, or replaced by the user's own agent, leaves the grill line of `cost`; `cost --explain`
  says so. The AGENTS.md named exception (the cost code knows `spec-writer` and `spec-critic` by
  agent type) is not extended.
- Spec critic: yes (on the CR before the split).

## What changes

All CLI paths below are under `skills/chantier/scripts/cli/src/chantier/`.

### 1. The host capability (`playbook/models.py`)

- `SETS_MODEL_AT_START` becomes `NAMED_AGENT_MODEL_AT_START = {"claude": True, "copilot":
  False}`, every use renamed. Its comment: whether this host starts a named agent with a model
  given at the start, so that model runs and the agent keeps its file's tools; only what the
  host's reference marks proved; a host added later declares its own value; Copilot's turns
  `True` once the eval's probe (`evals/copilot/RUNBOOK.md`, "Models") shows a named agent ran the
  requested model, together with the removal of `model-policy: required` from the agent files the
  proof covers. It is the one switch.
- `ESCALATION` does not change (Copilot: none).

### 2. The Copilot start value (where copilot-model-catalog builds `MODELS["copilot"]`)

- A Copilot `Model`'s `start` becomes its identifier (`Model(id, name, id)`): CR-296 round 6
  proved that a generic `task` start with `model: gpt-6.1-sol` ran Sol (the host's record:
  `modelSelectionSource: explicit_override`). `MODELS["claude"]` keeps its aliases.

### 3. The four starts (`playbook/config.py`)

Per role, for the host whose view is asked, from A's default model and configured model:

| Configured (user layers) | Host can (named agent with a model) | Host cannot |
| --- | --- | --- |
| nothing, or a model equal to the default, no `agent` | `plugin`: the plugin's agent, no model passed | the same |
| `agent` only | `named`: the user's agent, no model passed (its file's model) | the same |
| a model other than the default, no `agent` | `named`: the plugin's agent, the model passed | `generic`: a generic agent, the model passed, the role's contract in the prompt |
| `agent` and a model | `named`: the user's agent, the model passed | refused (Q13) |

- The resolved role records `start` (`plugin`, `named`, `generic`).
- A's Copilot refusal `cannot set a model when it starts an agent ...` is gone: on Copilot the
  case "a model, no agent" now starts generic. copilot-role-models' tests and evidence that
  expected it on a Copilot model now expect the generic start.
- The refusal (Q13), one problem line at the path and line of the `model` key that makes it:
  `role "<role>": <Host> cannot start a named agent with a model (hosts/<file>.md, "Models at an
  agent's start"): remove "model" for <role> under hosts.<host>.roles, or name the model in your
  agent's own file`. It belongs to that host's view only: `playbook`, `preflight` (P12) and `open`
  on that host refuse (exit 2 where they do today), so a batch never opens with it; the other
  host's view is unaffected.

### 4. What the CLI prints (`playbook/lines.py`, `plugin_files.py`, `commands/opening.py`)

- `playbook` (and `playbook --batch`), one line per role, A's layer labels kept:
  - `plugin`: `coder: agent=chantier:coder model=(its file's)` (unchanged);
  - `named` with a model: `coder: agent=chantier:coder model=opus (claude-opus-5-5, Claude Opus
    5.5) [repository]`;
  - `generic`: `coder: agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra)
    [surface project] tools=(the caller's, not restricted)`.
- `team_lines` (the `team:` lines of `take`, `round`, `handoff`) carry the same forms.
- The generic start's prompt (Q8, "rebuilt by chantier"): wherever the CLI prints a role's
  opening lines or first line (`chief_prompt_lines` for `playbook`'s `<role> prompt, first line:`;
  `worker_prompt_lines` for `take`, `round`, `handoff`), for a role that starts generic it adds,
  right after them: `<role> contract (a generic agent: copy it unchanged, without the two leading
  spaces, after the opening lines):`, then the body of the plugin's agent file for that role and
  host (everything after its frontmatter, the `# chantier-agent:` line included), each line
  indented by two spaces. The role keeps its card through the prompt's `Read` line, as today. No
  file is written.
- `open` records each role's `start` in `batch.json`'s `playbook`; `playbook --batch` prints it.
  A batch opened before this change prints as today.
- `concepts.md`'s exemption from "ten lines at most" already covers `playbook`, `take`, `round`,
  `handoff`.

### 5. `cost --explain` (`commands/cost/command.py`, `_explain_notes`)

- For `spec-writer` and `spec-critic`, when the configuration read now, for the batch's host,
  starts the role other than `plugin` with the plugin's agent (`generic`, or `named` with the
  user's agent), one line per such role: `Grill line: <role> starts as a generic agent (or: as
  your agent <name>), so its spend is counted with the Chief of Staff's steering, not on the grill
  line`. A `named` start of the plugin's own agent with another model keeps its agent type and
  stays on the grill line: no note. Nothing else in `costs/` changes; the grill line's detection
  by agent type (`costs/sessions.py`, `costs/transcripts.py`) stays as it is.

### 6. The Copilot Coder's agent file (`com.github.copilot/agents/chantier-coder.agent.md`), Q17

- The frontmatter line `model-policy: required` is removed from this file only. Nothing else
  changes in it (`model:`, `tools`, `strict-tools-list`, `user-invocable`, the body byte for
  byte), so both hosts' bodies stay identical (AGENTS.md). The thirteen other Copilot files and
  the Claude Code files (`agents/`) do not change.
- Effect at run time: none from chantier. Copilot's capability stays `False`, so chantier passes
  no model when it starts a named Copilot agent, and the file's `model:` runs. The removal serves
  only the probe (section 8): an operator's explicit start of `chantier-coder` with another model.

### 7. Cards and host references (`skills/chantier/references/`)

- `concepts.md`, "Starting an agent": a new bullet: `agent=(generic)` printed: start the host's
  generic agent (the host reference's row "Start a generic agent"), pass the model as printed,
  and put the printed contract lines after the opening lines; its tools are the caller's, the
  card bounds what it does; a parent never chooses it, it only follows what the CLI prints. The
  rest unchanged (copied as printed, never retried without the model or with another).
- `chief-of-staff.md`, "The team": the four starts in one sentence (Copilot refuses the user's own
  agent with a model); a role started generic runs with the caller's tools, not restricted, which
  the Chief of Staff tells the user when it shows the team. The sentence "A host that cannot set a
  model ... refuses a `model`" is replaced.
- `driver.md` and `foreman.md`: where they say the agent and model are passed as printed, add "or
  the generic agent with the printed contract lines (concepts, Starting an agent)".
- `hosts/claude-code.md`, row "Models at an agent's start": gains "named agent with a model: yes
  (`NAMED_AGENT_MODEL_AT_START`); a model changed in the configuration starts the role's named
  agent with that model, its tools unchanged". No generic row (never used on Claude Code).
- `hosts/copilot.md` (on top of copilot-role-models' rows), the start rows:
  - "Start a Driver or a worker", "Start the Spec-writer", "Start the Spec critic", "Start the
    Retro critic": "no model (the capability is none, below)" becomes "no model, as the CLI
    prints the plugin's or your agent; when the CLI prints `agent=(generic)`, the row Start a
    generic agent instead".
  - "Models": the file's model runs when no model is passed; every plugin agent's file sets
    `model-policy: required` except `chantier-coder`'s (removed for the eval's probe, Q17).
  - "Models at an agent's start (capability, start value)": "named agent with a model: no, until
    the probe of `evals/copilot/RUNBOOK.md`, "Models", shows a named agent ran a requested model
    (`NAMED_AGENT_MODEL_AT_START`). Documented, unproved: a model given at the start wins over the
    file's unless the file sets `model-policy: required`
    ([CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#command-line-options)).
    Observed (copilot-role-models' text, kept). Start value: the identifier, used by a generic
    start. A model changed in the configuration starts a generic agent; the user's own agent with
    a model is refused." The old text "capability: none ...; no start value", the refusal
    "cannot set a model when it starts an agent" and its trial line are gone.
  - new row "Start a generic agent (a role configured with another model)": "`task`, `mode:
    background` where the role's start row has it, the generic agent (`agent_type:
    general-purpose`, unproved as to the exact value: CR-296 round 6 ran a generic agent this
    way), `model:` the printed start value, the prompt with the printed contract lines; its tools
    are the caller's, not restricted. Proved: a generic `task` start with `model: gpt-6.1-sol` ran
    Sol (CR-296 round 6, the host's `subagent.started` record)".
  - "The model a role ran on" gains: after a start with a model, the parent reads in its
    session's `events.jsonl` the `model` of that start's `subagent.started` event; when it differs
    from the printed identifier, the parent stops that agent's work, reports both identifiers and
    the host's text (rule 7), and starts nothing else for it. Unproved as a routine; read after the
    start, not a guarantee before it.
  - The "Startup core" sections of both references do not change (the startup budget test).

### 8. The Copilot eval's probe (`evals/copilot/RUNBOOK.md`, `evals/kit/copilot_models.py`)

On top of copilot-role-models' section "Models" and script:

- `evals/copilot/RUNBOOK.md`, "Models", a new step after the fourteen starts and the script's
  first run (so its count of fourteen holds). The step is the operator's explicit order, outside
  anything the CLI prints: chantier never passes a model to a named Copilot agent (the capability
  is `False`), so the Chief of Staff runs this one start only because the operator orders it in
  the eval, as the user's word, and says so in its reply. The operator writes to the Chief of
  Staff: "Eval probe, on my order: start the plugin agent `chantier-coder` with `task`, the prompt
  `model probe` and `model: gpt-6.1-terra`, and give me its answer." (a model other than its
  file's `gpt-6.1-sol`); the agent answers its refusal line. Then the operator runs `uv run
  --no-project python <this checkout>/evals/kit/copilot_models.py --probe gpt-6.1-terra` on the
  same session and pastes its output into the report. When the probe prints `ran the requested
  model`, the finding goes to an inbox CR, offered by the Chief of Staff to the user, that sets
  `NAMED_AGENT_MODEL_AT_START["copilot"] = True`, removes `model-policy: required` from the files
  the proof covers and updates `hosts/copilot.md`'s rows; otherwise the report names the recorded
  model and the host's exact text, and nothing is worked around. "What it proves" gains: whether a
  named Copilot agent runs a model given at its start, from the host's own record.
- `evals/kit/copilot_models.py` gains `--probe <identifier>` (standard library only, writing
  nothing): it reads the same session's `events.jsonl`, takes only the last ended subagent event
  (`subagent.completed` or `subagent.failed`), prints its type and the script's three fields
  (`model`, `firstDispatchedModel`, `modelSelectionSource`, `absent` when missing), then `ran the
  requested model` and exits 0 when `model` equals the identifier, else `ran <model>, not the
  requested <identifier>` (or `no ended subagent event`) and exits 1. Without `--probe` the script
  behaves as copilot-role-models specified.

### 9. Docs

- `docs/agents-and-models.md`, "Your own agents": the four starts as a table (Copilot refuses the
  user's own agent with a model), "the caller's tools, not restricted" for a generic start; to
  change a role's tools, name your own agent (Q10). "Models": the sentence copilot-role-models
  wrote about `model-policy: required` becomes "On Copilot the agent files' models run when no
  model is passed; a model you set starts a generic agent until Copilot is proved to start a named
  agent with a model (the eval's probe)". "A host that cannot set a model ... refuses a `model`"
  is removed. A note: a Spec-writer or Spec critic started generic, or as your own agent, is
  counted with the Chief of Staff's steering, not on the grill line (`cost --explain` says so).
- Release notes, as the project's release process asks.

### 10. Tests (`skills/chantier/scripts/cli/tests/`), few, parametrized, fast

- `test_plugin_files.py`, `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter`:
  `copilot["model-policy"] == "required"` becomes: absent for `coder`, `"required"` for every
  other role (Q17); `user-invocable` unchanged.
- copilot-role-models' parametrized test of `evals/kit/copilot_models.py` gains two `--probe`
  cases on its fake session: the last ended event's `model` equal (exit 0, `ran the requested
  model`) and different (exit 1).
- `test_playbook_config.py`, parametrized: the four starts on each host (Claude: `named` with the
  model; Copilot: `generic`, its `team:` line with `tools=(the caller's, not restricted)` and the
  contract lines printed by `take`; Copilot `agent` and model: the refusal's text, from
  `playbook` and `preflight`, the Claude view of the same file valid); `start` recorded by `open`;
  `cost --explain` prints the grill note when `spec-writer` is configured with the user's agent,
  and none for the plugin's agent with another model; copilot-role-models' cases that expected
  "cannot set a model when it starts an agent" moved to the generic start.

### 11. Scenario (`scenario/run_scenario.py`)

- §20 (a planning surface): with `CHANTIER_HOST=copilot` and a surface project file setting
  `hosts.copilot.roles.coder.model` to another model, `playbook` prints `agent=(generic)` and
  `take` prints the Coder's contract lines; with `agent: my-coder` added, `open` refuses with
  Q13's line and moves nothing.

## Out of scope

- Flipping `NAMED_AGENT_MODEL_AT_START["copilot"]` to `True`, and removing `model-policy:
  required` from the thirteen other Copilot files: a later CR, after the user's Copilot run of the
  probe (Q12, Q17).
- Running any Copilot session (the probe is the user's later run).
- Any restriction of a role's tools by configuration (Q10); `skills`/`tools` needs keep their
  meaning (Q15).
- Extending the cost code's named exception to find a generic or user-named Spec-writer or Spec
  critic on the grill line.
- The configuration's layers and defaults (A); the board (C); the catalog (copilot-model-catalog).
- Generated or temporary agent files of any kind (Q3); escalation on Copilot.

## Evidence

- `just check` green on Linux, macOS and Windows; `just test` within its budget.
- `just scenario` green: the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and
  the local Windows run when this CR is on top of its stack (AGENTS.md). `hooks/` and `types/`
  untouched: no `just mod`.
- `git diff` of `com.github.copilot/agents/`: one line removed (`model-policy: required`) in
  `chantier-coder.agent.md`, nothing else; `agents/` untouched.
- In the PR, `chantier playbook` with a surface project file setting `coder: model:
  gpt-6.1-terra` under `hosts.copilot.roles`, run with `--host copilot` (the generic line) and
  `--host claude` (the plugin agent unchanged); with `coder: {agent: my-coder, model:
  gpt-6.1-terra}` there, the refusal's line on Copilot.
- `evals/kit/copilot_models.py --probe` run on the test's fake session, its output pasted in the
  PR.
- The proofs on a real Copilot session are the user's later run; the PR's Known gaps names them:
  "a named Copilot agent started with a requested model not yet observed (the probe of
  `evals/copilot/RUNBOOK.md`, Models)", "a generic start on its configured model not yet observed
  in a real Copilot session", and "the exact `agent_type` of Copilot's generic agent".
- No CI job is added or changed.

## Open questions

None.
