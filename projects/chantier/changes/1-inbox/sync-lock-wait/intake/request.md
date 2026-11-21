# A blocked uv sync names chantier's holders, waits, never kills

Split from `sync-blocked-by-others` (sync-lock-Q4, 2026-11-21): when chantier's own `uv sync` is blocked (os error 32 on Windows) by chantier's own processes (a gate, a watcher, the board or hub), the sync names the processes that hold the `.venv`, waits, never kills, and tells the user after a few minutes (sync-lock-Q1 C, sync-lock-Q2 A).

Carried from sync-lock's spec and its critic, to grill:
- At a session's start, a sync blocked this way versus startup-core.md's "report the exact error and stop": a named exception, or report and stop, or go on unsynced with `sync pending` (critic finding 3, spec open question 6).
- In a shared planning surface, the board and hub that hold the `.venv` also serve other projects: wait on them like any holder, or stop and restart them as today (critic finding 4, spec open question 4); the session's own watcher too.
- How the holders are named: by the steering session with the shell (host text in `hosts/`), or by a read-only CLI listing (AGENTS.md's measured-cost rule: batch-29's mid-run kill, batch-17) (spec open question 3).
- "A few minutes": how long before the user is told, and whether the session keeps waiting after (spec open question 5).
- Evidence: the shipped-text check covers the four SKILL.md sync sentences and startup-core.md's exception (critic finding 7).

Depends on `sync-blocked-by-others` (the launch part) landing first.
