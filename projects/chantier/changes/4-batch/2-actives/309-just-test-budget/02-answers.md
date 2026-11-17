# Answers

## test-budget-Q1: trim or restate

2026-11-17, the user chose the recommended answer: profile and speed up the slow tests until `just test` is back within AGENTS.md's budget (18.5 s + 30 s on the user's Windows machine), keeping what they cover; the budget line stays as it is.

Spec critic: no, it changes the speed of tests, no behaviour.

## Spec questions (2026-11-17)

- test-budget-Q2 (parallel runner): yes. The Driver adds `pytest-xdist` (dev dependency, locked in `uv.lock`) and runs `just test` in parallel, AND makes the tests themselves faster (the profiled costs: git per test, `cost_world` rebuilt per test, the `surface` fixture, the held-port wait). Both, not one or the other.
- test-budget-Q3 (CLI code): yes. The Driver may speed up the CLI's own code (the STATUS rewriting after each save) with byte-identical output; then `just scenario` is due before the PR.
