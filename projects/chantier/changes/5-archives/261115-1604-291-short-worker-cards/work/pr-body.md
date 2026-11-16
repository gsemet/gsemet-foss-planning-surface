## Summary

Every worker (Investigator, Coder, Inspector, Debugger, Verifier, Conflict resolver, Demo explorer, extra review step) was told to read the whole of `worker.md` (about 17 KB, every role's section) and `concepts.md` (about 53 KB, written for the steering sessions and the Drivers). In the last two real evaluation runs, cache writes were 46-77% of each worker role's cost. Each role now has its own short card holding only what it needs, and a worker reads that card alone. No role's contract changes: what it does, refuses, writes and replies stays the same.

## Deliverables

Size of a worker's opening read, before (`worker.md` + `concepts.md` at the base: 69,597 bytes for every role, as stored in git) and after (its own card):

| Card | Before (bytes) | After (bytes) |
| --- | --- | --- |
| `investigator.md` | 69,597 | 3,482 |
| `coder.md` | 69,597 | 4,232 |
| `inspector.md` | 69,597 | 5,290 |
| `debugger.md` | 69,597 | 3,353 |
| `verifier.md` | 69,597 | 10,333 |
| `conflict-resolver.md` | 69,597 | 3,544 |
| `demo-explorer.md` | 69,597 | 3,234 |
| `review-step.md` | 69,597 | 3,878 |

```text
before: prompt -> worker.md (every role's section) + concepts.md (whole)
after:  prompt -> <role>.md          (CLI prints the card named by the agent file)
```

Choices: `worker.md` is removed; `concepts.md` is no longer in a worker's prompt but stays as is for the steering sessions and Drivers; reply formats and caps are unchanged; the prompt's rules line for a worker reads "rank above it".

## Blast radius

Grade: 2. The cards are every worker's contract and the CLI prints their paths into every worker prompt; a missing rule in a card would only show in a real run. Rollback is a plain revert.

## Autonomous decisions

- The 14 agent files changed (7 roles on 2 hosts); `hosts/copilot.md` had no sentence to change, so it is untouched.
- The Driver's prompt template keeps "rank above them" (shared with Drivers); only the workers' lines say "above it".

## Known gaps

- The cost effect (fewer cache-write tokens per worker start) is not proved in this PR: only a real evaluation run, comparing cost per worker role, can show it.

<details>
<summary>Details</summary>

## Changes

- New cards in `skills/chantier/references/`: one per worker role plus `review-step.md`; `worker.md` removed.
- `agents/` and `com.github.copilot/agents/`: the card pointer and refusal name the role's own card (identical bodies).
- CLI: `plugin_files.py` prints one `Read <card>;` line; `commands/facts.py` `cards:` line no longer lists `worker.md`.
- Links from `driver.md`, `concepts.md` ("Starting an agent"), `chief-of-staff.md`, `hosts/claude-code.md`, `CONTRIBUTING.md`.
- Tests, scenario check, evaluation kit audit and dry run, scorecard rows follow the new names.

## Impacts

No visual change. Worker prompts name one short card instead of two long files.

## Test plan

- [x] New or changed tests (they fail on the previous code): the card and agent-file checks of `tests/test_plugin_files.py` and `tests/test_cli_runs.py`
- [x] Local gates at `307d8a8`: `just check` pass; `just scenario` pass on Windows (local gate) and in CI
- [x] Evidence: before at `d6836e4`, after at `307d8a8` (size table above)
- [x] Review: approved at `307d8a8`
- [x] Verified at `307d8a8`
- [x] CI green at `307d8a8`

## Internal references

CR-291 "One short card per worker role" (`291-short-worker-cards`).

</details>
