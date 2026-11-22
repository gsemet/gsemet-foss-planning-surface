## Summary

In a stack batch, `take` starts a new CR on the nearest earlier CR with a PR only once that CR is handed back `ready`; otherwise on the default branch. A CR with an open `after` is on its highest open dependency's branch; a taken CR not yet placed prints the base its worktree really sits on.

## Deliverables

- `stacks.py`: `_start_candidate`, `start_on_for`, `stack_start` rules 1 to 4.
- `commands/facts.py`: `_landed_line` record-alone base recomputed.
- `core/records.py` comment; cards (`concepts.md`, `foreman.md`, `driver.md`).
- Tests: `test_stack_base.py` rows and a `_landed_line` test; scenario steps 13, 13-bis, 13-ter and README.

## Review

- [ ] Inspector approved

## Known gaps

- Long gate and Verifier pending.
- Stacked on CR-442's branch (PR #417).
