# Decisions (main session, 2026-10-25, autonomous)

Bounded scope for this CR:
- browser tests for the Mermaid and PlantUML entry points (DIAG-012, 013, 014, 031, 116);
- a check script for the *.markers.ts companion files, wired into `just check`;
- finer markers for the coarse cases listed in 01-intent.md.
Out of scope, stays in the backlog: replacing the ~40 approximate tests and the end-to-end tests
for StRS (split the remaining work into a new backlog item when this CR lands).
