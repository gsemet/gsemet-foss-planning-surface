# A held CR folder blocks triage on Windows

From the Chief of Staff's session of 2026-11-21 (chantier project, planning surface): on Windows,
`triage` failed twice with `[WinError 32]` (the file is in use by another process) when it moved a
CR folder out of `1-inbox` while the surface server (`chantier board`) ran.

- First failure: the board was blamed; the way out was to stop the board and start it again, then
  triage. The order matters: on a planning surface, triage refuses while the board (its writer) is
  stopped, so stopping the board is no way to triage.
- Second failure (triage of `board-batch-compact`): it cleared once the Chief of Staff's own shell
  left the CR folder (its working directory was inside it), with the board still running. So the
  holder may be any process whose working directory, or an open file, is inside the folder.

## Analysis

- On Windows a folder cannot be renamed while any process holds an open handle inside it: a
  process's working directory, a file open without delete sharing (an editor, a viewer, a Python
  `open()`), an enumeration in progress. POSIX has no such rule.
- Every CR folder move goes through one function, `FolderStore.move`
  (`skills/chantier/scripts/cli/src/chantier/store/folder.py`), which already retries a
  `PermissionError` on Windows for one second (`core/files.py:retry`). A handle held longer than
  that (a shell parked in the folder) makes the move fail with a raw error that names no cause and
  no way out.
- The board reads the planning files by short, scoped reads and `stat` walks (`board/fingerprint.py`,
  `board/files.py`); no code was found holding a handle on a CR folder for long. The first
  failure's holder is not proven: a shell or another program is as likely as the board.
- CR-429 (batch-30, active) gives the server a recursive file watch (`watchfiles`,
  ReadDirectoryChangesW on Windows) of the planning folder: a new long-lived handle at the folder's
  root, which this CR's Windows check must cover.

## Intent

Triage (and every other CR folder move) succeeds on Windows while the board runs, with no stop and
restart of the board; a brief hold is waited out; a hold that lasts is refused cleanly, nothing
moved, with a message that says what holds such a folder and what to do; and the agents do not
park their own shell inside a CR folder.
