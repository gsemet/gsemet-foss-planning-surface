# A held CR folder: wait it out on Windows, then refuse with the cause

Spec v2 (2026-11-21), from `02-answers.md`: no grill was held; the user delegated tonight's spec
questions to a Fable advisor ("plus de question"), whose answers board-lock-Q1 to Q4 (all A) and
the destination (batch-30) are recorded there and carried below.

## Goal

In the user's terms (from `intake/request.md`): triage moves a CR folder while the board runs, with
no stop and restart of the board. On Windows a folder cannot be renamed while a process holds a
handle inside it (its working directory, an open file); today a hold longer than one second makes
`triage` fail with a raw `[WinError 32]` that names no cause and no way out, and the board gets the
blame. After this CR:

- a brief hold is waited out, up to 10 seconds, and the move succeeds;
- a hold that lasts is refused cleanly: nothing moved, and the message says what likely holds the
  folder on Windows (a shell or a program whose working directory is inside it, a file of it open)
  and what to do, and that the board need not stop;
- no agent, whatever its role, parks its own shell inside a CR folder, the cause proven on
  2026-11-21.

## Decisions carried

- **board-lock-Q1 A:** on Windows a held folder is waited for up to 10 s, with a growing pause,
  then refused (section 1). Not 30 s (a CLI command or a board request could hang half a minute),
  not the one second of today (brief holds would keep failing).
- **board-lock-Q2 A:** the refusal names the kinds of holder and what to do; no process scan
  (section 2).
- **board-lock-Q3 A:** every CR folder move gets the wait and the refusal, through
  `FolderStore.move` (section 1).
- **board-lock-Q4 A:** one sentence in `startup-core.md`, read by every role at boot (section 3).
- **Destination:** batch-30. No batch-30 CR edits `store/folder.py`; no `depends.json` (see
  Overlaps for `startup-core.md`). W3 runs at a head that holds CR-429.

## What changes

### 1. The move waits longer on Windows (board-lock-Q1, Q3)

- `skills/chantier/scripts/cli/src/chantier/core/files.py`: a second helper beside `retry`, named
  `retry_held(op, *args)` (the name is the Driver's), and a module constant `HELD_WAIT_S = 10.0`.
  On Windows only, `retry_held` retries an op that raises `PermissionError` (WinError 5, access
  denied, and 32, sharing violation, both reach Python as `PermissionError`) for up to
  `HELD_WAIT_S` seconds, with a growing pause (from 0.05 s to 0.5 s); after the deadline it raises
  the last `PermissionError`. On POSIX it calls the op once, as `retry` does. `retry` itself (one
  second, used by reads and atomic writes) is unchanged.
- `store/folder.py`, `FolderStore.move`: `retry(source.rename, destination)` becomes
  `retry_held(source.rename, destination)`. This is the one function every CR folder move goes
  through, so the wait covers them all, not only triage: `triage` and the board's own triage and
  ready drops (`lifecycle/stages.py:move_backlog_item`, `lifecycle/backlog.py:move_item`,
  `board/write_api.py`), `abandon` and `restore` (`commands/intake.py`), a batch's moves at `order
  add`, `take` and their rollbacks (`core/batch.py`), and the archive moves
  (`commands/close_archive.py`). `FolderStore.remove` keeps `retry`.
- The wait happens under the lifecycle lock (`changes_lock`), whose waiters give up after 30 s
  (`LOCK_WAIT_S`): 10 s stays well under it.

### 2. A lasting hold is refused with its likely cause (board-lock-Q2)

- `FolderStore.move`, its `except OSError` branch: a `PermissionError` on Windows raises the
  `ChantierError` (exit code unchanged, `EXIT_EXTERNAL`) with this text, one line, the OS error kept
  at the end. `<N>` is built from `HELD_WAIT_S` as read at the time of the refusal (formatted with
  no trailing zeros: `10`, `1`, `0.5`), never written as a literal:

  ```text
  cannot move CR folder <source> to <destination>: refused for <N> s, the folder is likely held; nothing moved. On Windows a folder cannot move while a process holds it: a shell or a program whose working directory is inside it, or a file of it open in an editor or a viewer. Leave it (cd elsewhere, close the file) and run the command again; the board need not stop. (<OS error>)
  ```

  "Likely": a WinError 5 can be a real access denial (the folder's rights), not a hold; the OS
  error kept at the end lets the reader tell them apart. Any other `OSError`, and every error on
  POSIX, keeps today's text (`cannot move CR folder <source> to <destination>: <error>`).
- No process is scanned to name the holder: `procs.py` keeps its rule that Windows offers no
  supported way to read another process's directory.
- Nothing else is written on the refusal: the folder stays where it was, and the callers' existing
  rollbacks (`core/batch.py`, `commands/close_archive.py`) run as today.

### 3. Every role keeps its shell out of CR folders (board-lock-Q4)

`skills/chantier/references/concepts.md` (lines 739-752 at the spec's writing, rule 8's
background-task paragraph) already holds this rule, with its reason, but only "for a Driver and the
steering session": "No shell call changes its folder (`cd`, `Set-Location`, `pushd`, alone or
chained before a command) into a CR folder (any stage)", and "on Windows a process whose current
folder is inside a folder keeps that folder from being moved or removed (WinError 32), so a CR's
move between stages or a worktree's removal fails". This CR extends it to every role, and keeps one
wording:

- `skills/chantier/references/startup-core.md` (read by every role at boot) gains one short
  paragraph at its end, its rule clause word for word the concepts.md one:

  > No shell call changes its folder (`cd`, `Set-Location`, `pushd`, alone or chained before a
  > command) into a CR folder (any stage), whatever your role: name the target with absolute paths.
  > On Windows a process whose current folder is inside a folder keeps that folder from being moved
  > (WinError 32), so the CR's next move fails.

- `concepts.md`: its sentence "No shell call changes its folder (...) into a CR folder (any
  stage)." stays as is and gains a pointer after it: "Every role holds this rule:
  [startup core](startup-core.md)." The rest of that paragraph (the steering session and the
  worktree, the Driver's start folder, the reasons) is unchanged.
- The size stays within the manifest's startup limit (`startup-manifest.json`, `"limit": 12544`),
  checked by `tests/test_startup_manifest.py`.

### 4. The board's own handles (investigation, no change expected)

The code read for this spec found no long-held handle of the board on a CR folder: its reads are
scoped (`core/files.py:read_text`, `store/folder.py:read_bytes`), its `stat` walks short
(`board/fingerprint.py`, `board/files.py`), its git runs at the surface's root
(`writer/git_ops.py`, `cwd=self.root`). The Driver confirms this on Windows (Evidence, W3) at the
head under test, with CR-429's file watch in it. If the board is found holding a handle on a CR
folder past 10 s, the Driver closes it at its source in the same PR and says so in the PR's
Deliverables; if it cannot, it stops and reports to the Foreman, with no workaround.

## Out of scope

- Triage's refusal while the board's writer is stopped (`store/surface.py:check_publish`): by
  design, unchanged. The refusal text of section 2 no longer sends anyone to stop the board.
- A copy-then-delete move when the rename fails: a fallback that leaves half a folder on a crash;
  never.
- The board doing the move itself: it already does, through the same `move_item`, and a hold by
  another process blocks it the same way.
- Naming the holding process (psutil scan, Windows Restart Manager): refused by board-lock-Q2.
- A wait longer than 10 s, or triage-only waiting: refused by board-lock-Q1 and Q3.
- Any change to `retry`'s one-second wait for reads and writes.

## Overlaps with batch-30 (running)

- **CR-429 board-fingerprint-cache (2-actives):** adds the server's recursive file watch of the
  planning folder (`watchfiles`, ReadDirectoryChangesW on Windows). A recursive watch at the root is
  not expected to block a child folder's rename; W3 below proves it at a head that holds CR-429.
  Its tests (`test_surface_server.py`, `test_file_watch.py`) are not touched here.
- **CR-437 sync-lock-wait (2-actives):** edits `startup-core.md`, at the end of its first
  paragraph (the named exception to "report the exact error and stop"), with a check of that
  sentence; this CR appends a paragraph at the file's end, a
  different region. The second to merge rebases and re-checks the startup limit
  (`tests/test_startup_manifest.py`). No `depends.json`: a shared file is no dependency.
- **CR-443 gate-hold-narrowing (1-pending):** edits `core/files.py` (`IGNORED`, the
  `.lease-hold.*.run` pattern stays); this CR adds a helper and a constant in the same file, a
  different region: the second to merge rebases.
- **CR-449 board-griller (1-pending):** edits `lifecycle/backlog.py` and `board/write_api.py`
  (its running-turn check on a backlog item's folder); this CR changes neither file, only the store
  move they call: no textual overlap, a behavioural one (a griller's move of an item may now wait
  up to 10 s on Windows).
- **CR-433 board-batch-chip-stale, CR-434 board-batch-kanban (2-actives):** read
  `lifecycle/stages.py`; this CR does not edit it.
- **CR-438, CR-449, CR-450:** edit `tests/test_startup_manifest.py` or cards read at boot; the
  second to merge re-checks the startup limit.
- No CR of batch-30 edits `store/folder.py`.

## Evidence

The checks call the CLI in-process on a prepared planning folder, as `tests/` does; they read the
shipped `startup-core.md` and `concepts.md` from the repository at the head under test, never a
copy.

Portable (Linux, macOS, Windows), in `tests/test_triage_moves.py`:

- P1. A rename that raises `PermissionError(13, ..., None, 32)` three times then succeeds, with the
  helper's Windows check forced on and its sleep and clock replaced so the test takes no real time:
  `triage <item> --ready` succeeds, the folder is in `3-ready`, the old path is gone.
- P2. A rename that always raises it, `HELD_WAIT_S` left at its shipped value: `triage` exits with
  `EXIT_EXTERNAL`; the output holds "refused for <N> s, the folder is likely held; nothing moved",
  with `<N>` formatted from the `HELD_WAIT_S` in force (the test reads the constant, and asserts it
  is 10.0, the value of board-lock-Q1), and "the board need not stop"; the folder is still in
  `1-inbox` with its files unchanged, and no folder exists in `3-ready`.
- P3. A rename that raises `FileNotFoundError`, or `PermissionError` with the Windows check off:
  one attempt only, today's message text.
- P4. `abandon` on a held folder (P2's rename): the same refusal, the folder still in place (the
  wait covers every move, board-lock-Q3).
- P5. `startup-core.md`, read from the repository, holds the paragraph of section 3; `concepts.md`
  holds the same rule clause ("No shell call changes its folder (`cd`, `Set-Location`, `pushd`,
  alone or chained before a command) into a CR folder (any stage)") and the pointer to
  `startup-core.md`; `test_startup_manifest.py` passes (the startup limit).

Windows only (skipped elsewhere with the reason named), with `HELD_WAIT_S` patched to 1 s so the
suite stays within its time budget:

- W1. A file of the CR folder opened by a thread (plain `open()`, no delete sharing) and closed
  after 0.3 s: `triage` succeeds.
- W2. A child process started with its working directory inside the CR folder and kept alive past
  the wait: `triage` refuses with section 2's text, its `<N>` the value in force (`1`, the patched
  one), nothing moved; once the child ends, the same `triage` succeeds.
- W3. By hand, recorded in `work/gates/` and quoted in the PR: on the user's Windows machine, with
  `chantier board` running on the planning surface (with CR-429's file watch) and the web client
  open on the CR's page, `triage` of an inbox CR to a priority succeeds with no board restart. The
  same run with a PowerShell `Set-Location` into the CR folder shows the refusal text (`refused for
  10 s`), then succeeds after `Set-Location` out.

Platform matrix (the change depends on the OS, not on the host or a configured value):

- Windows, folder free: one rename, as today (P1 with zero failures is the same path).
- Windows, brief hold: waited out (P1, W1).
- Windows, lasting hold: refused with the likely cause, nothing moved (P2, W2, W3).
- Linux and macOS: one attempt, today's behaviour and text (P3); no hold exists there.

The long gate: `just scenario` (ubuntu-latest) green at the PR's head (a CLI and card change);
`just check` and `just eval-dry-run` in the worktree before the first push (a change under `src/`).
No scenario step is added: the scenario runs on Linux, where no folder is ever held.
