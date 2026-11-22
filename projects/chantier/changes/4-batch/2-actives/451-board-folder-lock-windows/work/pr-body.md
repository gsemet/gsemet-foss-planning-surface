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

- The by-hand run on a real Windows machine with the board running and its file watch (W3) is UNVERIFIED until the Verifier records it.

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

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: just check, just eval-dry-run
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-451 board-folder-lock-windows

</details>
