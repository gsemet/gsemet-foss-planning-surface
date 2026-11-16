A read-only pane beside the chat in Claude Code that shows where every change request stands. On Claude only; Copilot is untouched.

## What changes

- **The index:** `3-requests/STATUS.json` gains `landed` and `trashed` (the last 50, newest first), `landed_total`, `trashed_total`, each batch's `heartbeat` and `orders_pending`, and each row's `blocked`, `silent_minutes` and `folder`. `SCHEMA` stays 2: no field changes meaning. It reads at most 100 `STATUS.json` files and never the forge. The CLI gets no new command.
- **The mod:** `hooks/hooks.json`, `hooks/register.tsx`, its tests in `hooks/register.test.tsx`, and `types/index.d.ts`, named in `.claude-plugin/plugin.json`. The pane opens when the skill's prompt expands; `/chantier-board` toggles it. While open it checks the shown files every 15 seconds and reads one again only if it changed.
- **Docs:** `README.md` and `CONTRIBUTING.md`. The cards do not change.

## Checks

- `just check` and `just scenario` pass; the scenario covers the new fields and the limit of 50.
- `claude plugin validate .` passes with two older warnings (no marketplace description, no icon). `claude plugin test .`: 17 pass. CI has no `claude` binary, so these two are a local step, documented in `CONTRIBUTING.md`.
- The mod type-checks with `tsc` 5.9.3 and the engine's own `.d.ts`, also a local step.

## Not proven yet

- The run in the desktop app on this repository, which the specification's "Done when" asks for.
- `$.process.run` is documented "CLI only": the `git rev-parse` that finds the main checkout is unproven on Claude Desktop. If it is refused, the pane says so in one line and draws nothing else.
- Copilot ignoring `hooks/` rests on its documentation, not on a run: its manifest's 1.0.0 `$schema` puts it under Agent Plugins semantics. A structure test keeps that line and checks the manifest names no hooks.
- The mod API is early access and may change between Claude Code releases.
