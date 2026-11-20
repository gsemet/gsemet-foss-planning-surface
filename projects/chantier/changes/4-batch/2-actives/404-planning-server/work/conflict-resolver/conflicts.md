# Conflicts: rebase of CR-404 onto origin/main (c51aea6a)

Commits 188f2dca and 97ffe81d (CR-401) were dropped by the rebase: already on main as 3866d764 and 7afbc5f3. Only 72222316 (now b6fe7071) conflicted, in 6 files (7 hunks).

- AGENTS.md hunk 1 (network sentence): main's `.lease-hold.*.run` text kept, and the CR's "the surface server's writer, whose fetch and push need it" added to the list of network users.
- AGENTS.md hunk 2 (exceptions): kept all three: the CR's "Third, the surface server's writer" paragraph, then main's lease exception paragraph, then the CR's rewritten "two named git exceptions" bullet (writer commands). Main's older text of that bullet (board "commits nothing itself") is superseded by the CR's.
- docs/planning-folder.md: main's `.lease-hold.*.run` record kept, plus the CR's "and the writer's lines" in the journal.
- docs/web-board.md: main's "(only the PRs a running batch waits for)" kept, followed by the CR's "The writer" bullet.
- scenario/run_scenario.py: both functions kept (`unit_name` from main, `stamp_now` from the CR).
- skills/chantier/references/session-start.md: main's "(only the PRs a running batch waits for)" kept, with the CR's writer sentences.
- batch_status.py imports: both sides' imports kept; ruff then ordered them (`from chantier.core import leases` moved below the writer_line imports). This one edit is in the worktree, uncommitted.

No BOM added (checked each resolved file's first bytes).

Fast gate, as run in the worktree: `just test` (pytest -q -n auto): 1234 passed, 13 skipped. `just lint` (ruff format --check, ruff check, mypy, uv lock --check, biome): pass after the import fix.
