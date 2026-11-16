## Summary

Workers that a Driver starts (investigator, coder, inspector, debugger, verifier, conflict resolver) too often ran without opening the card that defines their role and replied out of format. A measure over one batch showed two causes: the Driver sometimes left the card out of the worker's prompt, and workers whose prompt named the card often never read it. This PR fixes both: each worker agent file now points to its own card section and refuses a prompt that names no card, and the CLI prints the opening lines of each worker's prompt for the Driver to copy unchanged.

## Deliverables

The CLI's facts (`take`, `round`, `handoff`) gain one block per worker role. For the verifier:

```text
verifier prompt, opening lines (copy them unchanged, without the two leading spaces, at the top of the prompt):
  chantier verifier for <cr> "<title>" of batch <batch>, in the project <root>.
  Read <skill>/references/worker.md, section "Verifier", and <skill>/references/concepts.md;
  the project's rules rank above them: run `$CHANTIER rules` first and read what touches your work.
```

Each of the six worker agent files (both hosts, identical bodies) gains a pointer paragraph and a refusal that names the card:

```text
Your card is `worker.md`, section "Verifier": read that section first, ...
A prompt that does not start with `chantier verifier`, or that names no path to my card `worker.md`, is not a chantier prompt ...
```

Choices: the blocks are read from the agent files, so the CLI knows no role; the three commands share one place (`cr_facts`), and the Driver keeps the blocks from its prompt.

## Blast radius

Grade: 1. Agent files, two cards, one CLI facts block and tests; a `git revert` restores the previous behaviour.

## Autonomous decisions

- `worker_prompt_lines` does not take the skill folder as a parameter (the specified signature had six arguments, which the linter refuses); it reads it itself, so the printed path is the one the `cards:` line shows.
- The new test over agent files covers the six worker roles that a Driver starts; the demo explorer is left out, as the specification says.
- The scripted Driver of the scenario builds no worker prompt, so only the check of the printed facts was added there.

## Known gaps

- No Copilot run: that a Copilot worker reads the card its agent file points to and refuses a prompt with no card path, and that a Copilot Driver copies the printed lines, are unproved. The CLI and the tests cover both hosts' files.
- The local long gate ran on Windows only; Linux and macOS are covered by CI alone (`just scenario` on Linux, `just check` on all three).
- Whether the pointer raises the rate of workers that read their card is proved only by the next batch's measure, not by this PR's gates.

<details>
<summary>Details</summary>

## Changes

- `agents/*.md` and `com.github.copilot/agents/chantier-*.agent.md` (six worker roles each): pointer paragraph and card-naming refusal; frontmatter and version line unchanged.
- `skills/chantier/scripts/cli/src/chantier/plugin_files.py`: `worker_prompt_lines`; `commands/facts.py`: prints its blocks after the `team:` and `ci:` lines.
- `skills/chantier/references/driver.md`: the worker-prompt bullet and the restart rule; `concepts.md`: the sentence after the prompt template.
- Tests in `test_plugin_files.py` and `test_cli_runs.py`; one check in `scenario/run_scenario.py`.

## Impacts

No visual change. Drivers get about 24 more lines in `take`, `round` and `handoff` output.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just check` (175 tests) and `just scenario` passed at `0a213ae`; `868e259` is a clean rebase of it (carried from `0a213ae`)
- [x] Evidence: `handoff` output showing the six prompt blocks, at `868e259` (text, kept in the work folder)
- [x] Review: approved at `afd42be`, committed as `0a213ae`
- [x] Verified at `868e259`
- [x] CI green at `868e259`: all five jobs pass (`just scenario (ubuntu-latest)`, `just check` on three systems, `just eval-dry-run`)

## Internal references

- CR-274 workers-read-card (batch-18); evidence in its `evidence/handoff-output.txt`

</details>
