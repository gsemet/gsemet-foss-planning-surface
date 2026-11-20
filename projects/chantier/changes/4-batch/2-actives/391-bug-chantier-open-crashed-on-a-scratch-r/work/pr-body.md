## Summary

`chantier open` ended in a Python traceback in a planning surface whose project has no clone yet: it ran `git remote` in a folder that does not exist. It now refuses with the same one-line message the preflight check already gives ("no clone of the project at <path> ... clone it there"), and `git()` refuses any missing working folder with a clear error instead of an `OSError`.

## Deliverables

Before and after, `open --factory` on an external surface with no clone:

| | Result |
| --- | --- |
| Before | `NotADirectoryError` traceback (`FileNotFoundError` on POSIX) |
| After | `error: no clone of the project at <path> (remote <r>): clone it there`, exit code for a precondition, planning folder unchanged |

```python
# core/repo.py
def missing_clone(self) -> str | None: ...  # one message, used by preflight and by open
```

## Blast radius

Grade: 1. Local to two error paths; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The new test removes the clone with an `onerror` handler, because git's read-only objects make a plain `rmtree` fail on Windows.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `core/repo.py`: `Repo.missing_clone()` builds the no-clone message once (moved out of preflight's P8, whose output is unchanged).
- `commands/opening_record.py`: `open_settings` refuses with it before any git call or write.
- `core/git.py`: `git()` raises a `ChantierError` naming the folder when `cwd` is not a directory.
- Tests: `tests/test_open_no_clone.py` (default and configured clone path, `open` and `open --factory`), a unit case in `tests/test_cli_units.py`.

## Impacts

No visual change. A refused `open` leaves the planning folder untouched.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `6985ac6` (carried from `dc671de`, a clean rebase): `just check` pass (879 passed), `just eval-dry-run` pass (18 of 18)
- [x] Evidence: before at `b76d037`, after at `6985ac6` (text only: the table in Deliverables)
- [x] Review: approved at `6985ac6` (carried from `dc671de`, a clean rebase)
- [x] Verified at `6985ac6` (carried from `dc671de`, a clean rebase)
- [x] CI green at `6985ac6`: all 5 jobs pass, `just scenario (ubuntu-latest)` included

## Internal references

- CR-391 change-spec-chantier-open-crash

</details>
