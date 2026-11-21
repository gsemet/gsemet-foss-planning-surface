## Summary

In the last batch, most CR Drivers (the agents that carry one change request to a green PR) handed their CR back for lack of context before it closed, and each hand-back cost a fresh Driver that reads the cards again. This PR makes a Driver read less of its card before each step, makes a restarted Driver read only what is left to do, and moves the closing hand-off threshold from 100,000 to 115,000 tokens.

## Deliverables

The CR Driver's readings are now three manifest lines, each read when its step comes:

| Line | Read when | Limit (bytes, with the card's opening) |
| --- | --- | --- |
| `cr-driver` | before the first Coder | 18,000 |
| `cr-driver:ship` | before the first commit | (whole common path: 36,000) |
| `cr-driver:closing` | at the pushed-head `VERIFIED` | `resume: closing` restart: 13,000 with "Means: a Driver started again" |

- `driver.md`: opening cut to at most 2,500 bytes; new section "Means: a Driver started again"; "Means: worktree, rebase and push" split in two; "CR driver" split in "CR driver", "CR driver: ship and proof" and "CR driver: the closing".
- `concepts.md`: "Starting an agent" gets level-3 headings, its text unchanged.
- Closing hand-off threshold: 115,000 tokens, in four places.
- Measured bytes of the shipped card (opening plus sections), before the first Coder 16,224 (limit 18,000), whole common path 35,410 (44,974 at the base; limit 36,000), `resume: closing` restart 9,435 (with the section for a Driver started again) (limit 13,000), opening 2,475 (limit 2,500).
- **UNVERIFIED:** the effect on real Drivers (see Known gaps).

## Blast radius

Grade: **1**. Cards, one manifest, one test file and one scenario check; no CLI code, no agent file. A plain `git revert` restores the previous cards.

## Autonomous decisions

- None.

## Known gaps

- The tests and the scenario were not run locally (CI has not run them at `76b3173`: pending).
- No real Driver has read the new cards; the three-round measure is the next batch's (a worktree's cards load only once merged into the main checkout).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: readings by step, new and split sections, threshold.
- `skills/chantier/references/startup-manifest.json`: the three CR Driver lines; the other Drivers' lines follow the split section.
- `skills/chantier/references/concepts.md`, `foreman.md`: level-3 headings; threshold.
- `skills/chantier/scripts/cli/tests/test_startup_manifest.py`: parametrized byte limits, opening limit, line checks.
- `scenario/run_scenario.py`: the card check reads 115,000 and no 100,000.

## Impacts

No visual change. Drivers read fewer card bytes per step and hand off at the closing later.

## Test plan

- [ ] New or changed tests (they fail on the previous code): not run locally (quiet window); CI green at `76b3173`: pending at `76b3173`
- [x] Local gates at `76b3173`: `just check` (`just eval-dry-run` pending at `76b3173`)
- [x] Evidence: none beyond the tests, the scenario check and the proof of the verification (bytes measured on the shipped cards, listed in Deliverables)
- [x] Review: approved at `76b3173`
- [x] Verified at `76b3173`
- [ ] CI green at `76b3173`: pending at `76b3173`

## Internal references

- CR-420 driver-context-budget (batch-29)

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
