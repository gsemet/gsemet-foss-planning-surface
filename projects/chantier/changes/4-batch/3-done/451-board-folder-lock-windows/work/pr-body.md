## Summary

On Windows a folder cannot be renamed while a process holds a handle inside it (a shell's working directory, an open file). Moving a CR folder (triage, abandon, ready drops, batch moves) failed after one second with a raw `[WinError 32]` that named no cause, and the board got the blame. A brief hold is now waited out, and a lasting one is refused with its likely cause.

## Deliverables

- `retry_held(op, *args)` and `HELD_WAIT_S = 10.0` in `core/files.py`: on Windows, a `PermissionError` is retried for up to 10 s with a growing pause (0.05 s to 0.5 s); on POSIX the op runs once. `retry` is unchanged.
- `FolderStore.move` uses it, so every CR folder move gets the wait.
- After the wait, the move is refused (exit code unchanged) with one line: the folder is likely held, nothing moved, the kinds of holder (shell or program whose working directory is inside it, a file open in an editor or viewer), what to do, and that the board need not stop. The OS error is kept at the end.
- `startup-core.md` gains the rule that no role changes its shell's folder into a CR folder; `concepts.md` points to it.

```text
before: rename fails once -> retry 1 s -> raw WinError 32
after:  rename fails -> retry up to 10 s (Windows) -> move, or refuse with the likely cause
```

## Blast radius

Grade: 1. One store function and one helper; POSIX behaviour is unchanged; a plain revert restores the old behaviour.

## Autonomous decisions

None.

## Known gaps

- UNVERIFIED: the by-hand run on Windows with the board running and its file watch (W3, no restart of the board). The move and refusal were proven on Windows without a running board; whether the board holds a handle on a CR folder remains unproven here.

<details>
<summary>Details</summary>

## Changes

- `core/files.py`: `HELD_WAIT_S`, `retry_held`.
- `store/folder.py`: `FolderStore.move` waits and refuses with the cause; `remove` keeps `retry`.
- `startup-core.md`, `concepts.md`: the shell-folder rule for every role.
- `tests/test_triage_moves.py`: portable checks (brief hold, lasting hold, other errors, abandon, cards) and Windows-only ones (a file held by a thread, a child process with its working directory inside the folder).

## Impacts

A held folder no longer fails the move at once on Windows; the refusal says what to do.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `d8594e5`: just check pass, just eval-dry-run pass (18 of 18); just scenario pass at `0ae00e3`
- [x] Evidence: on Windows at `0ae00e3`, a held folder is refused after "refused for 10 s" (11 s elapsed, nothing moved) and the same move succeeds once the holder ends
- [x] Review: approved at `0ae00e3` (the last change is a test-only fix of an assertion that failed on Linux and macOS)
- [x] Verified at `0ae00e3`
- [x] CI green at `0ae00e3`

## Internal references

CR-451 board-folder-lock-windows

</details>
