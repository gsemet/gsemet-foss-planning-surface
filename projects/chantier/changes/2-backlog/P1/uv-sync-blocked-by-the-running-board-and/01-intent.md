# Restart the board on this checkout's build, and keep it there

Short name: `board-restart`. The user's report of 2026-11-22 (batch-30, Windows), P1, next batch.

The request had two items. The first, `uv sync --locked` blocked by the board or a watcher holding
the checkout's `.venv`, is already done by 56f753e6 (`sync-checkout.md`: check first, name the
holders, wait with `sync pending`, stop only the session's own board and watcher on the user's
yes). What is left is the second: the board runs an older build than the checkout for a whole
batch, so merged fixes to the board are not live, and stopping it does not help because another
project's seated watcher starts it again from its own build.

Intent: one documented action, on the user's yes each time, that stops the surface's board cleanly
whoever started it (after the writer's last cycle) and starts it again on the session's build
(board-restart-Q1); and, while a chantier dev session holds its seat, its checkout's build serves
the surface: other projects' watchers start no other board (board-restart-Q2, folding in the inbox
item `which-build-starts-the-surface-server-wi`).
