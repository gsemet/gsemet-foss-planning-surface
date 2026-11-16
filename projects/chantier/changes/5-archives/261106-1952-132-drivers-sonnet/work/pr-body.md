## Why

The CR Driver runs Opus and is the largest Driver spend: $20.48 of batch-06's $64.28.

## What changes

- `agents/cr-driver.md` and `com.github.copilot/agents/chantier-cr-driver.agent.md`: the model
  becomes Sonnet 5.5, in the frontmatter only. The bodies are unchanged and stay identical.
- `test_structure.py`: `cr-driver` leaves `OPUS_ROLES`.
- `README.md`: the CR driver has its own row in the models table, and the sentence under it no
  longer says every role that judges runs Opus.
- `CONTRIBUTING.md`, `docs/tutorial-claude-code.md` and the Models row of
  `skills/chantier/references/hosts/claude-code.md` say the same.
- That Models row marks the CR driver on Sonnet as unproved, by the file's own convention: no
  transcript has shown it yet. The trial is the model a CR driver's transcript shows in the next
  batch.

`docs/tutorial-claude-code.md` is not in the specification's list; its "Done when" covers it.
`hosts/copilot.md` names no role's model and is unchanged.

## Out of scope

The stack, release and QA drivers, the Foreman, and a project's choice of a role's model.

## Evidence

At `7b4e2e5`, against its base `0cbdd58`:

| | Before | After |
| --- | --- | --- |
| `agents/cr-driver.md` | `claude-opus-5-5` | `claude-sonnet-5-5` |
| `chantier-cr-driver.agent.md` | `[Claude Opus 5.5, claude-opus-5.5]` | `[Claude Sonnet 5.5, claude-sonnet-5.5]` |
| Stack and release drivers, both hosts | Opus 5.5 | unchanged |
| QA driver, both hosts | Sonnet 5.5 | unchanged |
| README models table | one row for the CR, stack and release drivers, on Opus | the CR driver on its own row, on Sonnet |

The diff of each CR driver agent file is its one `model:` line.

A case-insensitive search for `opus` outside `.agents/` and `evals/results/`, and for "driver" next
to Opus or Sonnet, finds no text that says the CR Driver runs Opus.

Not shown: a live CR Driver on Sonnet. Only the frontmatter and the text are verified here; the
host reference marks it unproved.

## Checks

- Long gate `just check && just scenario`, local on Windows at `7b4e2e5`: passed, the scenario
  255/255 on the GitHub forge and 255/255 on the GitLab forge. `just check` run again by the
  Verifier: 28 passed.
- CI at `7b4e2e5`: `just check` passes on Linux, macOS and Windows, `just scenario` on Linux, none
  skipped.
