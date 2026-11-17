## Summary

A role's model could be changed only where the host starts a named agent with a model, and on Copilot any configured model other than the default was refused. This PR lets the user change a role's model on either host from the configuration. Where the host can start the role's own agent with a chosen model (Claude Code), that agent keeps its tools and runs the model. Where it cannot yet (Copilot), a generic agent runs the role with its whole contract in its prompt and the chosen model, and chantier says plainly that its tools are the caller's, not restricted. Each host declares that one capability, so Copilot moves to the first case by changing one value.

## Deliverables

The four starts, per role and host (a model "other than the default" is one set in the user's configuration layers):

| Configured | Host starts a named agent with a model | Host cannot |
| --- | --- | --- |
| nothing, or the default model, no `agent` | `plugin`: the plugin's agent, no model passed | same |
| `agent` only | `named`: your agent, no model passed | same |
| a model other than the default, no `agent` | `named`: the plugin's agent, the model passed | `generic`: a generic agent, the model passed, the role's contract in the prompt |
| `agent` and a model | `named`: your agent, the model passed | refused, with the reason, at `playbook`, `preflight` and `open` |

What `playbook` prints for a Coder (Copilot, `hosts.copilot.roles.coder.model` set to another model):

```text
coder: agent=(generic) model=<identifier> (<identifier>, <name>) [<layer>] tools=(the caller's, not restricted)
```

Real runs (a project whose `chantier.yaml` sets `hosts.copilot.roles.coder.model: gpt-6.1-terra`):

```text
$ chantier playbook --host copilot
coder: agent=(generic) model=gpt-6.1-terra (gpt-6.1-terra, GPT-6.1 Terra) [surface project] tools=(the caller's, not restricted)
$ chantier playbook --host claude
coder: agent=chantier:coder model=(its file's)
```

With `agent: my-coder` added next to that model, on Copilot:

```text
chantier.yaml:6: role "coder": Copilot cannot start a named agent with a model (hosts/copilot.md, "Models at an agent's start"): remove "model" for coder under hosts.copilot.roles, or name the model in your agent's own file
```

`evals/kit/copilot_models.py --session s1 --probe gpt-6.1-terra` on a fake session whose last ended event ran Terra (exit 0), then Sol (exit 1):

```text
subagent.failed: model=gpt-6.1-terra firstDispatchedModel=absent modelSelectionSource=x
ran the requested model
subagent.failed: model=gpt-6.1-sol firstDispatchedModel=absent modelSelectionSource=x
ran gpt-6.1-sol, not the requested gpt-6.1-terra
```

Impactful choices:

- One switch per host, `NAMED_AGENT_MODEL_AT_START` (Claude Code `True`, Copilot `False`); a host added later declares its own value.
- A Copilot model's start value is its identifier, since a generic start with an identifier was observed to run that model.
- A generic start's contract is rebuilt from the plugin's agent file for that role and host and printed after the role's opening lines; no agent file is written anywhere.
- `chantier-coder`'s Copilot agent file loses `model-policy: required` (only that file), to let the eval's new `--probe` tell whether a named Copilot agent runs a model given at its start. Nothing flips on Copilot until that probe is run.
- A Spec-writer or Spec critic started generic, or as your own agent, leaves the grill line of `cost`; `cost --explain` says so.

## Blast radius

Grade: 2

Role resolution (`playbook/layers.py`, `playbook/lines.py`) feeds `playbook`, `take`, `round`, `handoff`, `open` and `cost --explain`. Default behaviour (nothing configured) is unchanged; revert is a plain `git revert`, and a batch opened before this change prints as before.

## Autonomous decisions

- A role with no opening lines in the CLI (the four Drivers and the Demo explorer) that resolves generic records `start: generic` and prints its `agent=(generic)` line but no contract lines: the specification names only the places that print opening lines.
- `cost --explain` on a configuration that is invalid when read says nothing about the grill line and does not fail.
- The four-starts decision lives in `playbook/layers.py` (where the model rules already are); `playbook/config.py` keeps the refusal's text.
- `tools=(the caller's, not restricted)` follows the model part on a generic role's line; a role's own needs stay their separate line.

## Known gaps

- A named Copilot agent started with a requested model is not yet observed (the probe of `evals/copilot/RUNBOOK.md`, Models, is the user's later run).
- A generic start on its configured model is not yet observed in a real Copilot session.
- The exact `agent_type` of Copilot's generic agent is unproved.
- The four Drivers and the Demo explorer, when started generic, get no printed contract lines.

<details>
<summary>Details</summary>

## Changes

- `playbook/models.py`: `NAMED_AGENT_MODEL_AT_START` replaces `SETS_MODEL_AT_START`; a Copilot model's `start` is its identifier.
- `playbook/layers.py`, `playbook/config.py`: the four starts, `start` recorded in the role record, the Copilot refusal for your own agent with a model (one problem line at the `model` key); the old "cannot set a model when it starts an agent" refusal is gone.
- `playbook/lines.py`, `plugin_files.py`, `commands/`: `playbook` and `team:` lines for `named` and `generic`; contract lines for the roles that print opening lines; `open` records `start`.
- `commands/cost/command.py`: the grill-line note in `cost --explain`.
- `com.github.copilot/agents/chantier-coder.agent.md`: one line removed.
- Cards and host references: Starting an agent, the Chief of Staff's team, Driver and Foreman wording, the Claude Code and Copilot model rows, a new "Start a generic agent" row on Copilot.
- `evals/copilot/RUNBOOK.md`, `evals/kit/copilot_models.py`: the `--probe <identifier>` step and option.
- `docs/agents-and-models.md`; scenario step for a Copilot generic start and the refusal; tests in `test_playbook_config.py`, `test_playbook_layers.py`, `test_plugin_files.py`, `test_copilot_catalog.py`.

## Human decisions

- A model per role is configurable on both hosts; no generated agent file anywhere, and what a host cannot apply at an agent's start is refused with the reason.
- A role's tools change only by naming your own agent; a generic agent has the caller's tools and the CLI says so.
- On Copilot, your own agent together with a model is refused at the batch's open.
- `model-policy: required` is removed from the Coder's Copilot file only, until the proof covers the others.

## Impacts

Users can set a role's model per host; on Copilot the role then runs as a generic agent with the caller's tools. No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `9414455`: `just check` pass; `just test` pass (298 passed); `just scenario` pass (Windows, via the CLI gate)
- [x] Evidence: the outputs pasted in Deliverables, run at `9414455`
- [x] Review: approved at `9414455`
- [x] Verified at `9414455`
- [x] CI green at `9414455` (`gh pr checks 255`: `just check` on three systems, `just eval-dry-run`, `just scenario (ubuntu-latest)` pass)

## Internal references

- CR-300 "Change Specification: a model per role on each host" (batch-22), third of a stack on the configuration layers.

</details>
