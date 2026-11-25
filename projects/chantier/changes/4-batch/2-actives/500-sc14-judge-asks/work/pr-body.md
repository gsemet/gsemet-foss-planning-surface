# CR-500: `chantier judge` words the ask to the user (PART 1), early conflict check (PART 2)

Regrouped CR (children 14+15), one branch, one PR, based on CR-497's branch.

## Summary

- PART 1: `judge <cr> --epoch N [--local-gate] [--record ["sentence"]]` words the readiness ask from the record; `--record` records it as `asks` does. Tests in `tests/test_judge.py` (26 tests, 0.94 s), a scenario step, AGENTS.md line.
- PART 2: not yet done in this round.

## Known gaps

- Part 2 pending (this body is for round 1).
- Long gate: the ubuntu scenario job owns it; the local Windows run is owed only by the CR on top of the chain (CR-514).
- `--record` prints only the lines `asks` prints (the scenario wants them first); the spec's section 1 lists `ask:` first.
