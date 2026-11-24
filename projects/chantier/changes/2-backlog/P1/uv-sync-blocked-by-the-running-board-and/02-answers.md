Short name: `board-restart`

1. board-restart-Q1: **Who may restart the board.** A: one action, on the user's yes each time, that may stop the surface's board whoever started it (a clean stop after the writer's last cycle) and start it again on the checkout's build. It rewrites AGENTS.md's stop rule and the card line "never stop or restart the board". Item 1 of the request (`uv sync` blocked) is already done by 56f753e6.
2. board-restart-Q2: **Which build serves a shared surface.** A: while a chantier dev session holds its seat, its checkout's build serves the surface, and other projects' watchers start no other board. Folds in the inbox item `which-build-starts-the-surface-server-wi`.
Destination: next batch (3-ready): it touches `sync-checkout.md`, `session-start-chief-of-staff.md`, `serve` and AGENTS.md, after CR-471's cut; order it with `watcher-runs-through-several-events-inst` (the watcher's start and stop), not in parallel. May fold in the inbox item `two-surface-servers-run-at-once-on-one-p` (the user decides).

Defaults taken on the spec-writer's open questions (2026-11-24; consequences of board-restart-Q2 A, no new question asked):
3. board-restart-D1: a plain `serve` and `webui` also refuse under the dev-seat rule, as `serve --restart` does (otherwise Q2 A leaves a way round it).
4. board-restart-D2: the inbox item `two-surface-servers-run-at-once-on-one-p` is folded into this CR (the same start race).
5. board-restart-D3: "holds its seat" means the seat names the dev session and that session's watcher lock is held now; a stale seat blocks nothing.
