# A held CR folder: wait it out on Windows, then refuse with the cause

Spec v1 (2026-11-21). No grill was held: the user delegated tonight's spec questions to an advisor
("plus de question"), so there is no `02-answers.md`. Every behaviour, scope or risk choice is an
open question at the end (board-lock-Q1 to Q4); the text below is written on each one's
recommended option, provisional until answered.

## Goal

In the user's terms (from `intake/request.md`): triage moves a CR folder while the board runs, with
no stop and restart of the board. On Windows a folder cannot be renamed while a process holds a
handle inside it (its working directory, an open file); today a hold longer than one second makes
`triage` fail with a raw `[WinError 32]` that names no cause and no way out, and the board gets the
blame. After this CR:

- a brief hold is waited out, up to 10 seconds, and the move succeeds;
- a hold that lasts is refused cleanly: nothing moved, and the message says what holds a folder on
  Windows (a shell or a program whose working directory is inside it, a file of it open) and what
  to do, and that the board need not stop;
- the agents never park their own shell inside a CR folder, the cause proven on 2026-11-21.

## What changes

### 1. The move waits longer on Windows (board-lock-Q1 A, Q3 A)

- `skills/chantier/scripts/cli/src/chantier/core/files.py`: a second helper beside `retry`, named
  `retry_held(op, *args)` (name is the Driver's): on Windows only, it retries an op that raises
  `PermissionError` (WinError 5, access denied, and 32, sharing violation, both reach Python as
  `PermissionError`) for up to `HELD_WAIT_S = 10.0` seconds, with a growing pause (from 0.05 s to
  0.5 s); after the deadline it raises the last `PermissionError`. On POSIX it calls the op once, as
  `retry` does. `retry` itself (one second, used by reads and atomic writes) is unchanged.
- `store/folder.py`, `FolderStore.move`: `retry(source.rename, destination)` becomes
  `retry_held(source.rename, destination)`. This is the one function every CR folder move goes
  through, so the wait covers them all, not only triage: `triage` and the board's own triage and
  ready drops (`lifecycle/stages.py:move_backlog_item`, `lifecycle/backlog.py:move_item`,
  `board/write_api.py`), `abandon` and `restore` (`commands/intake.py`), a batch's moves at `order
  add`, `take` and their rollbacks (`core/batch.py`), and the archive moves
  (`commands/close_archive.py`). `FolderStore.remove` keeps `retry`.
- The wait happens under the lifecycle lock (`changes_lock`), whose waiters give up after 30 s
  (`LOCK_WAIT_S`): 10 s stays well under it.

### 2. A lasting hold is refused with its cause (board-lock-Q2 A)

- `FolderStore.move`, its `except OSError` branch: a `PermissionError` on Windows raises the
  `ChantierError` (exit code unchanged, `EXIT_EXTERNAL`) with this text, one line, the OS error kept
  at the end:

  ```text
  cannot move CR folder <source> to <destination>: still held after 10 s; nothing moved. On Windows a folder cannot move while a process holds it: a shell or a program whose working directory is inside it, or a file of it open in an editor or a viewer. Leave it (cd elsewhere, close the file) and run the command again; the board need not stop. (<OS error>)
  ```

  Any other `OSError`, and every error on POSIX, keeps today's text (`cannot move CR folder
  <source> to <destination>: <error>`).
- No process is scanned to name the holder: `procs.py` keeps its rule that Windows offers no
  supported way to read another process's directory (board-lock-Q2).
- Nothing else is written on the refusal: the folder stays where it was, and the callers' existing
  rollbacks (`core/batch.py`, `commands/close_archive.py`) run as today.

### 3. The agents keep their shell out of CR folders (board-lock-Q4 A)

- `skills/chantier/references/startup-core.md` (read by every role at boot) gains one short paragraph at
  its end:

  > Never leave your shell's working directory inside a CR folder: use absolute paths. On Windows a
  > folder a process stands in cannot move, and the CR's next move fails.

- The size stays within the manifest's startup limit (`startup-manifest.json`, `"limit": 12544`),
  checked by `tests/test_startup_manifest.py`.

### 4. The board's own handles (investigation, no change expected)

The code read for this spec found no long-held handle of the board on a CR folder: its reads are
scoped (`core/files.py:read_text`, `store/folder.py:read_bytes`), its `stat` walks short
(`board/fingerprint.py`, `board/files.py`), its git runs at the surface's root
(`writer/git_ops.py`, `cwd=self.root`). The Driver confirms this on Windows (Evidence, W3) at the
head under test, with CR-429's file watch in it once merged. If the board is found holding a
handle on a CR folder past 10 s, the Driver closes it at its source in the same PR and says so in
the PR's Deliverables; if it cannot, it stops and reports to the Foreman, with no workaround.

## Out of scope

- Triage's refusal while the board's writer is stopped (`store/surface.py:check_publish`): by
  design, unchanged. The refusal text of section 2 no longer sends anyone to stop the board.
- A copy-then-delete move when the rename fails: a fallback that leaves half a folder on a crash;
  never.
- The board doing the move itself: it already does, through the same `move_item`, and a hold by
  another process blocks it the same way.
- Naming the holding process (psutil scan, Windows Restart Manager): board-lock-Q2's options B and
  C.
- Any change to `retry`'s one-second wait for reads and writes.

## Overlaps with batch-30 (running)

- **CR-429 board-fingerprint-cache (2-actives):** adds the server's recursive file watch of the
  planning folder (`watchfiles`, ReadDirectoryChangesW on Windows). A recursive watch at the root is
  not expected to block a child folder's rename; W3 below proves it at a head that holds CR-429.
  Its tests (`test_surface_server.py`, `test_file_watch.py`) are not touched here.
- **CR-443 gate-hold-narrowing (1-pending):** edits `core/files.py` (`IGNORED`, the
  `.lease-hold.*.run` pattern stays); this CR adds a helper and a constant in the same file, a
  different region: the second to merge rebases.
- **CR-449 board-griller (1-pending):** edits `lifecycle/backlog.py` and `board/write_api.py`
  (its running-turn check on a backlog item's folder); this CR changes neither file, only the store
  move they call: no textual overlap, a behavioural one (a griller's move of an item may now wait
  up to 10 s on Windows).
- **CR-433 board-batch-chip-stale, CR-434 board-batch-kanban (2-actives):** read
  `lifecycle/stages.py`; this CR does not edit it.
- **CR-437, CR-438, CR-449, CR-450:** edit `tests/test_startup_manifest.py` or cards read at boot;
  this CR adds one sentence to `startup-core.md`: the second to merge re-checks the startup limit.
- No CR of batch-30 edits `store/folder.py` or `startup-core.md`.

## Evidence

The checks call the CLI in-process on a prepared planning folder, as `tests/` does; they read the
shipped `startup-core.md` from the repository at the head under test.

Portable (Linux, macOS, Windows), in `tests/test_triage_moves.py`:

- P1. A rename that raises `PermissionError(13, ..., None, 32)` three times then succeeds, with the
  helper's Windows check forced on and its sleep and clock replaced so the test takes no real time:
  `triage <item> --ready` succeeds, the folder is in `3-ready`, the old path is gone.
- P2. A rename that always raises it: `triage` exits with `EXIT_EXTERNAL`, the output holds "still
  held after 10 s; nothing moved" and "the board need not stop", the folder is still in `1-inbox`
  with its files unchanged, and no folder exists in `3-ready`.
- P3. A rename that raises `FileNotFoundError`, or `PermissionError` with the Windows check off:
  one attempt only, today's message text.
- P4. `abandon` on a held folder (P2's rename): the same refusal, the folder still in place (the
  wait covers every move, board-lock-Q3).
- P5. `startup-core.md`, read from the repository, holds the sentence of section 3;
  `test_startup_manifest.py` passes (the startup limit).

Windows only (skipped elsewhere with the reason named), with `HELD_WAIT_S` patched to 1 s so the
suite stays within its time budget:

- W1. A file of the CR folder opened by a thread (plain `open()`, no delete sharing) and closed
  after 0.3 s: `triage` succeeds.
- W2. A child process started with its working directory inside the CR folder and kept alive past
  the wait: `triage` refuses with section 2's text, nothing moved; once the child ends, the same
  `triage` succeeds.
- W3. By hand, recorded in `work/gates/` and quoted in the PR: on the user's Windows machine, with
  `chantier board` running on the planning surface (and its file watch, once CR-429 is merged) and
  the web client open on the CR's page, `triage` of an inbox CR to a priority succeeds with no
  board restart. The same run with a PowerShell `Set-Location` into the CR folder shows the
  refusal text, then succeeds after `Set-Location` out.

Platform matrix (the change depends on the OS, not on the host or a configured value):

- Windows, folder free: one rename, as today (P1 with zero failures is the same path).
- Windows, brief hold: waited out (P1, W1).
- Windows, lasting hold: refused with the cause, nothing moved (P2, W2, W3).
- Linux and macOS: one attempt, today's behaviour and text (P3); no hold exists there.

The long gate: `just scenario` (ubuntu-latest) green at the PR's head (a CLI and card change);
`just check` and `just eval-dry-run` in the worktree before the first push (a change under `src/`).
No scenario step is added: the scenario runs on Linux, where no folder is ever held.

## Open questions

- **board-lock-Q1. How long a held folder is waited for, on Windows.**
  - A (recommended): up to 10 s, with a growing pause, then the refusal of section 2. Covers a
    file watcher, an indexer or an antivirus scan, and a board read in flight; well under the
    lifecycle lock's 30 s.
  - B: up to 30 s: more patience, but a CLI command or a board request can then hang half a
    minute, and other lifecycle commands wait on the lock as long.
  - C: no longer wait (one second, as today); only the clearer refusal of section 2.
- **board-lock-Q2. Whether the refusal names the holding process.**
  - A (recommended): no scan; the message names the kinds of holder (a shell or a program standing
    in the folder, an open file) and what to do. Simple, no new Windows-specific code, keeps
    `procs.py`'s rule.
  - B: on the refusal only, a best-effort scan with psutil's `open_files()` of the user's
    processes, naming those with a file open inside the folder (a shell's working directory is not
    seen this way); slow on Windows (seconds) and silent on processes it may not read.
  - C: B plus reading each process's working directory on Windows (psutil can), which reverses
    `procs.py`'s rule that Windows offers no supported way to read it.
- **board-lock-Q3. Which moves get the wait and the refusal.**
  - A (recommended): every CR folder move, through `FolderStore.move` (triage, the board's drops,
    abandon, restore, a batch's moves and rollbacks, the archive moves): one place, one behaviour.
  - B: triage only (the backlog moves, the CLI's and the board's), leaving the batch and archive
    moves on the one-second retry.
- **board-lock-Q4. Whether the cards tell the agents to keep their shell out of CR folders.**
  - A (recommended): one sentence in `startup-core.md`, read by every role at boot (the second
    failure's proven cause was the Chief of Staff's own shell).
  - B: the sentence in the Chief of Staff's card only (`chief-of-staff.md`), the one that triages.
  - C: no card change; the refusal's text is enough.
