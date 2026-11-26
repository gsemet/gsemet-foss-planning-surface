## Summary

A CLI refusal is where a role most often learns what to do next, but several refusals only said what was wrong. Every refusal raised by the batch rails now names, in backticks, the next command to run, and a test keeps it that way. Final "stop now" refusals are listed with their reason in an allow-list that the test counts and prints.

## Deliverables

Completed refusal texts keep their current words and gain a tail naming the command (`take <cr> --note "<why>" --epoch <n>`, `order slots`, `lease <unit>`, `close --stopped <name>`, and so on). Conditions and exit codes do not move.

```text
M9: 36 refusals scanned in 4 files, 7 allow-listed
```

The new gate (`tests/test_refusal_gate.py`) parses `rails.py`, `rails_release.py`, `rails_idle.py` and `core/leases.py` with `ast`, takes the command names from the CLI's own parser, and fails on a refusal with no command span that is not allow-listed, on a stale allow-list entry, and on a scan below the floor of 36.

`just test` wall time, same machine, measured by the author of the change: 128.54 s on the base (b64d3c1) and 117.52 s at the head (42da173); the gate itself runs in 0.09 s, so the gap is machine noise, not a saving or a cost.

## Blast radius

Grade: 1. Refusal texts only gain a tail; a plain `git revert` restores them.

## Autonomous decisions

- The gate lives in a new file `tests/test_refusal_gate.py` rather than `test_rail_refusals.py`, because a file over 400 lines fails the code-size test.
- The two test-seam refusals of `core/leases.py` are allow-listed as "test seam" (the specification's default).
- A small helper `_owner` in `rails_idle.py` keeps `_declared` under the function-length limit.

## Known gaps

- None.

<details>
<summary>Details</summary>

## Changes

- `rails.py`, `rails_release.py`, `rails_idle.py`, `core/leases.py`: command tails on the refusals the specification lists.
- `scenario/run_scenario.py`: the `close --stopped` hint check follows the backticked text.
- `tests/`: the M9 gate, plus command-span assertions in the slot, take and missing-lease tests.

## Impacts

Roles that hit a refusal are told the command to run next. No other behaviour change.

## Test plan

- [x] New tests fail on the previous code (the gate flags the uncompleted refusals)
- [x] Local gates at `42da173`: `just check` (2688 passed), `just eval-dry-run` (19 of 19), `just scenario` pass
- [x] Evidence: before at `b64d3c1`, after at `42da173`: the M9 line above, printed by `pytest -s -k M9`
- [x] Review: approved at `42da173`
- [x] Verified at `42da173`
- [x] CI green at `42da173` (5 of 5 checks)

## Internal references

- CR-489 sc03-refusals-name-next-step, batch-31 (stack, after CR-488)

</details>
