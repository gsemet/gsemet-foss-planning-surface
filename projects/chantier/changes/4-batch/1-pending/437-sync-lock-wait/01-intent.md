# A blocked uv sync names chantier's holders, waits, never kills

Split from `sync-blocked-by-others` (sync-lock-Q4, 2026-11-21). Intent: when a `uv sync` of chantier's checkout is blocked by chantier's own processes (a gate, a watcher, the board or hub), the sync names the holders, waits, never kills one, and tells the user after a few minutes. The carried questions are in `intake/`.
