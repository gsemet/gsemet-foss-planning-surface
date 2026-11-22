## Summary

Two tests failed at random in `just check`. `chantier live --once --only <id>` could print a screen and exit 0 instead of refusing an `--only` that no board serves, and a test of the folder lock could pass its move when it should be refused. Both are made deterministic.

## Deliverables

Sequence of the `live --once` race, before the fix:

```mermaid
sequenceDiagram
    participant Main as once() loop
    participant R as reader thread
    R->>Main: last answer fed (model complete)
    Main->>Main: sees every model complete, prints screen, exit 0
    R-->>R: --only error kept (too late)
```

After the fix `once()` judges `--only` itself on the finished models before it prints, so the order of the threads no longer matters:

```python
with lock:
    _check_only(models)   # raises the --only usage error (exit 2)
    screen.plain(models, ...)
```

The folder-lock test now waits for its child process to report `up` before it tries the move.

Evidence (command and output):

```text
uv run --locked --group dev pytest -q -p no:xdist test_live_link.py test_triage_moves.py -k "(test_the_refusals_of_several_boards and only) or w2"   (50 serial runs)
50 x "3 passed, 23 deselected"

folder-lock test, 8 parallel loops, before the fix: 1 failed (assert (0 == 4)); after the fix, 8 loops x 7: 56 passed
```

The new live test forces the interleaving (every model complete before any reader error is kept) and fails on the previous code.

## Blast radius

Grade: **1**. One check added in `once()` and a test change; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The folder-lock test's flakiness was a test race (the child takes its working directory after `Popen` returns), so the fix is in the test, with no change to the lock code.

## Known gaps

- Linux and macOS were not run locally; CI covers them.
- The local run of the long scenario on the author's Windows machine failed one step (`webui` printing `board already running`) because another board holds the default port 8765 there; the pipeline's `just scenario (ubuntu-latest)` passes at the head.

<details>
<summary>Details</summary>

## Changes

- `commands/live.py`: `once()` calls `_check_only(models)` under the lock before printing.
- `tests/test_live_model.py`: a forced interleaving (every model complete before any reader error is kept) that fails on the previous code.
- `tests/test_triage_moves.py`: the child prints `up` and the test reads it before moving the folder.

## Impacts

No visual change. `live --once --only <unserved id>` always exits 2 with the `--only` sentence.

## Test plan

- [x] New or changed tests (they fail on the previous code): the new live test fails on the base code, passes at `aa8ca7f`
- [x] Local gates at `aa8ca7f`: `just check` pass (2141 passed, 20 skipped), `just eval-dry-run` pass (19 of 19)
- [x] Evidence: 50 serial runs of both tests, no failure, and the folder-lock test under 8 parallel loops, failing 1 of 56 before and 0 of 56 after, at `aa8ca7f`
- [x] Review: approved at `aa8ca7f`
- [x] Verified at `aa8ca7f`
- [x] CI green at `aa8ca7f`: `gh pr checks 437`, all five checks pass

## Internal references

CR-461 two-flaky-tests-of-batch-30

</details>
