# Task T1 — Dependency update with security floors

Implement `00-request.md` and `01-intent.md` in `../markdown-okf-schema-studio-wt-151` on branch
`change-requests/151-dependency-update-security-floors`, created by the orchestrator from the tip
of the CR below it in the stack (150, or the highest ready CR). Run `npm ci` in the worktree (own
`node_modules`, no symlink), then the upgrades.

## Definition of done

- The intent; audits and `npm outdated` before/after in the report; every floor with its GHSA id.
- Requirements: if a requirement or a "Known issue" names a dependency version, update it with the
  usual traceability rules; otherwise no SwRS change is expected (state it in the report).

## Gates (foreground, in the worktree)

- `just check`; the full e2e suites (real-window ones under `WINDOW-TESTS.lock`, with
  `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`); `vsce package` dry run. Summarize gate output.
