## Summary

On Copilot, each chantier role now runs on the model the user chose: Claude Sonnet 5.5 for the CR driver, GPT-5.6 Luna for the Investigator, GPT-6.1 Sol for the Coder and the Inspector, GPT-6.1 Terra for the Verifier, the Debugger and the Conflict resolver. The Coder previously declared Luna, so a Coder started with Sol ran on Luna because the agent files set `model-policy: required`. The fix is the agent file's model. This PR also documents what the host showed and adds a check the user can run later on Copilot.

## Deliverables

Copilot agent files, only the `model:` line changes:

| Agent file | Before | After |
| --- | --- | --- |
| `chantier-coder` | GPT-5.6 Luna | GPT-6.1 Sol |
| `chantier-verifier` | GPT-6.1 Sol | GPT-6.1 Terra |
| `chantier-debugger` | GPT-5.6 Luna | GPT-6.1 Terra |
| `chantier-conflict-resolver` | GPT-5.6 Luna | GPT-6.1 Terra |

- `gpt-6.1-terra` is added by hand to the CLI's Copilot model list, so `chantier.yaml` resolves it (and then refuses it on Copilot as any model: "cannot set a model when it starts an agent").
- `evals/kit/copilot_models.py` (standard library only) reads a Copilot session's `events.jsonl` and prints, per role, the expected identifier against the recorded one (`ok` or `MISMATCH`). The roles are matched by order, since no agent-naming field of the events is sourced.
- The script on the test's fake session (all roles recorded on their file's model), exit 0:

```text
coder: expected gpt-6.1-sol; recorded gpt-6.1-sol; ok (matched by order)
inspector: expected gpt-6.1-sol; recorded gpt-6.1-sol; ok (matched by order)
debugger: expected gpt-6.1-terra; recorded gpt-6.1-terra; ok (matched by order)
verifier: expected gpt-6.1-terra; recorded gpt-6.1-terra; ok (matched by order)
conflict-resolver: expected gpt-6.1-terra; recorded gpt-6.1-terra; ok (matched by order)
... (the other nine roles, also ok)
```

- Docs: `docs/agents-and-models.md`, `docs/hosts.md`, `skills/chantier/references/hosts/copilot.md` (observed behaviour, known host issues, how to read the model a role ran on) and `evals/copilot/RUNBOOK.md` ("Models" section).

## Blast radius

Grade: 1. Four model lines, one list row, docs and an opt-in script; Claude Code, costs and every other role are untouched. A `git revert` restores the previous behaviour.

## Autonomous decisions

- The script matches roles by order and reads only the `model`, `firstDispatchedModel` and `modelSelectionSource` fields, as no agent field was sourced from the SDK's event schema. For the same reason every event line says "no agent field in the event" without inspecting the event for one, as the specification words it.

## Known gaps

- Model defaults not yet observed in a real Copilot session: the user's later run of the runbook's "Models" section proves it.
- The script assumes `events.jsonl` lines look like `{"type": ..., "data": {...}}`, checked against the fake session of the test only.

<details>
<summary>Details</summary>

## Changes

- `com.github.copilot/agents/`: four `model:` lines.
- `skills/chantier/scripts/cli/src/chantier/playbook/models.py`: one `MODELS["copilot"]` row.
- `docs/`, `skills/chantier/references/hosts/copilot.md`, `evals/copilot/RUNBOOK.md`: documentation.
- `evals/kit/copilot_models.py`, `skills/chantier/scripts/cli/tests/test_plugin_files.py`: the check and its tests.

## Human decisions

- Ship the four model changes now as a small independent change; the Copilot model catalog is a separate change.
- A Copilot model is named by its identifier (`gpt-6.1-terra`), from a source, never guessed.
- The cost computation does not change.
- No Copilot session is run here; the user runs the evaluation later.

## Impacts

No visual change. Copilot users get the new role models; `chantier playbook --host copilot` accepts `gpt-6.1-terra` in `chantier.yaml` and refuses it as before.

## Test plan

- [x] New or changed tests (the model-table test fails without the Terra row)
- [x] Local gates at `943fcb4`: `just check` (262 passed)
- [x] Evidence at `943fcb4`: the script's output on the test's fake session (Deliverables)
- [x] Review: approved at `943fcb4`
- [x] Verified at `943fcb4`
- [x] CI green at `943fcb4`

## Internal references

- CR-297 copilot-role-models; follow-up: copilot-model-catalog.

</details>

