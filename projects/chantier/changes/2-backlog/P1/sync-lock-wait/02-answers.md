Short name: `sync-wait`

# Answers
1. sync-wait-Q1 (2026-11-21): **A sync blocked at a session's start.** A. The session goes on unsynced, with a `sync pending` line naming the holders, and syncs later when nothing runs; it never kills another's gate.
2. sync-wait-Q2 (2026-11-21): **The board and hub, serving other projects.** A. Waited on like any holder; never stopped to sync, nor the session's own watcher.
3. sync-wait-Q3 (2026-11-21): **Who names the holders.** A. The session itself, with its shell, by its host's text in `hosts/`; no new CLI tool (AGENTS.md's measured-cost rule).
4. sync-wait-Q4 (2026-11-21): **How long before the user is told.** A. 3 minutes: one line to the user naming the holders; the session goes on unsynced and tries again at its next turn.
Restatement (2026-11-21): a dev-mode `uv sync` blocked by chantier's own processes (a gate, a watcher, the board or hub, any surface's) kills nothing: the session names the holders with its shell, goes on unsynced with `sync pending`, tells the user after 3 minutes, and tries again at its next turn; the startup rule gets this named exception; the shipped-text check covers the SKILL.md sync sentences and startup-core.md's exception.
5. sync-wait (2026-11-21, the user's words): **Grilled enough, destination.** "et tou les inbox en cours de speficiation pareil tu mets dans le batch. ill faut traiter ces P1 et inbox cette nuit": batch-30, after sync-blocked-by-others.
Spec v1 (2026-11-21): the spec-writer wrote `03-change-spec.md` from Q1 to Q4 and the restatement, on CR-436's merged head (overlaps with CR-432 and CR-436 named, places found by text). Two open questions, built as A while the user asks none: 1. check first with `uv sync --locked --check` and P10 names its real-path rule in the dev mode; 2. look for holders before syncing, not only after a failed sync.
