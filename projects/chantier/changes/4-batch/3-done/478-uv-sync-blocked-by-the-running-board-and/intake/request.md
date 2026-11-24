# uv sync blocked by the running board, and the board on an old build

Priority P1, next batch (the user, 2026-11-22). Seen in batch-30 on Windows.

1. `uv sync --locked` in chantier's checkout is blocked while the board or a watcher runs `chantier.exe` from the venv: the sync cannot replace it. The Chief of Staff has to stop the board (on the user's yes) to sync.
2. The board runs a build older than the checkout ("board runs a build of chantier 0.14.0 older than this notice (source unknown)") for the whole batch, so merged fixes to the board are not live. Intent: a documented, one-step way to restart the board on the checkout's build after a merge that touches it. Related: inbox `which-build-starts-the-surface-server-wi`, `two-surface-servers-run-at-once-on-one-p`.
