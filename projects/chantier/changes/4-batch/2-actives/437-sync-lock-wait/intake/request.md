# A blocked uv sync names chantier's holders, waits, never kills

Split from `sync-blocked-by-others` (sync-lock-Q4, 2026-11-21): when chantier's own `uv sync` is blocked (os error 32 on Windows) by chantier's own processes (a gate, a watcher, the board or hub), the sync names the processes that hold the `.venv`, waits, never kills, and tells the user after a few minutes (sync-lock-Q1 C, sync-lock-Q2 A).

Carried from sync-lock's spec and its critic, to grill:
- At a session's start, a sync blocked this way versus startup-core.md's "report the exact error and stop": a named exception, or report and stop, or go on unsynced with `sync pending` (critic finding 3, spec open question 6).
- In a shared planning surface, the board and hub that hold the `.venv` also serve other projects: wait on them like any holder, or stop and restart them as today (critic finding 4, spec open question 4); the session's own watcher too.
- How the holders are named: by the steering session with the shell (host text in `hosts/`), or by a read-only CLI listing (AGENTS.md's measured-cost rule: batch-29's mid-run kill, batch-17) (spec open question 3).
- "A few minutes": how long before the user is told, and whether the session keeps waiting after (spec open question 5).
- Evidence: the shipped-text check covers the four SKILL.md sync sentences and startup-core.md's exception (critic finding 7).

Depends on `sync-blocked-by-others` (the launch part) landing first.

## Evidence from Studio (2026-11-21, relayed by Studio's Chief of Staff)

At about 03:33Z the chantier Chief of Staff's dev-mode `uv sync` of the shared chantier checkout stopped Studio's live CR-444 `just preflight` gate (PID 29808) and its watcher; the gate was re-run (about 4 minutes). The sync rule in chief-of-staff.md (around lines 792-795 and 1104-1108) checks only the Chief of Staff's own `$CHANTIER status`, which cannot see another surface's processes on the same checkout. Studio's proposed fix: before a dev-mode sync, look for live gates and watchers of every planning surface that uses the checkout, then wait or ask the user, and never stop a gate.
