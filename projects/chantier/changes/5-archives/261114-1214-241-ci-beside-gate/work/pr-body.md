## Summary

A project's CI matrix often covers systems the developer's local long gate does not (Linux and macOS while working on Windows). Today the CR Driver (chantier's agent that takes one change to a green PR) runs the local gate first, then pushes, then reads CI, so a failure only CI can see arrives after a 35-minute gate and costs another round. This PR adds an opt-in mode, off by default: with `ci: beside_gate: true` in `chantier.yaml`, the Driver pushes at the approved round, opens a draft PR, and runs the long gate while CI runs. A red CI job that is the change's own stops the gate at once.

## Deliverables

The new key and what the CLI prints when it is on:

```yaml
ci:
  beside_gate: true
```

```text
ci: beside the long gate (chantier.yaml): push at the approved round, run the long gate while CI runs
```

| | Mode off (default) | Mode on |
| --- | --- | --- |
| Order | gate, push, PR, CI | push, draft PR, `ship`, then gate and CI side by side |
| Red CI job that is the change's | after the gate | stops the gate, then a debugger, then a round |
| Known gaps | unchanged | one bullet names the systems only CI covers |
| CLI output | unchanged | one `ci:` line in `playbook`, `take`, `handoff`; one line in `brief.md` |

Choices: the key is a mapping (`ci:`) to leave room for more CI settings; only a red job judged the change's stops the gate; the batch keeps the value it opened with.

## Blast radius

Grade: 1. Off by default; with no `ci` key every command prints what it printed before. Revert with `git revert`.

## Autonomous decisions

- `load` in `playbook/config.py` now dispatches the `prices`, `board` and `ci` keys through a table, to keep its complexity within the target; behaviour is unchanged.

## Known gaps

- The Driver's new order is unproved until a real batch runs on a project that turns the key on; no agent runs in the scenario.
- The scenario's new steps for the key were not run locally; they passed in CI (scenario job at `5d4e831`), and the long gate is replaced by CI for this batch.
- No screenshot is due (no board change).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/playbook/config.py`: validation of `ci`/`beside_gate`, new top-level message.
- `playbook/lines.py`, `commands/facts.py`, `commands/opening.py`: the `ci:` line, and the brief's line; `open` records the value in the batch's playbook.
- `skills/chantier/references/driver.md`, `chief-of-staff.md`, `concepts.md`: the Driver's order with the line, the force-push judgement, the routing row.
- `docs/agents-and-models.md`: the key.
- `scenario/run_scenario.py`: steps for the key, its off states, the mid-batch edit and four refusals.

## Human decisions

- Off by default; the project turns it on with a `chantier.yaml` key.
- A red CI job stops the gate.
- The systems only CI covers go in Known gaps.
- chantier's own repository turning it on is a separate item.

## Impacts

No visual change. Projects without the key see no difference.

## Test plan

- [ ] New or changed tests: scenario section 17b (not run locally)
- [ ] Local gates at `5d4e831`: `just check` (lint and tests) passed on Windows before commit, and in CI on Linux, macOS and Windows
- [x] Evidence: before at `effb478`, after at `5d4e831`: `playbook`, `take`, `handoff` with no `chantier.yaml` print the same lines
- [x] Review: approved at `b24f7c2` (diff against base), committed as `5d4e831`
- [x] Verified at `5d4e831`: output with no `chantier.yaml` identical to the base's; key on, off and the four refusals checked; card edits all qualified by the `ci:` line
- [x] CI green at `5d4e831`: gh pr checks 187: check (3 systems), eval-dry-run and scenario pass

## Internal references

CR-241 ci-beside-gate.

</details>
