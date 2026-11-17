# Task T7 — Drop `retainContextWhenHidden`

Audit finding(s): P-05, CR 12 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t7`, branch `change-requests/135-t7-drop-retain-context` (local only, from origin/main).

## Scope

Rely on `setState` / `restorePreviewState` (scroll, edit state, comments panel) when a hidden preview comes back. `src/host-vscode/activation.ts`. Integrate after T6. Proof: reload suite and stress suite green; webview host memory with 20 hidden previews measured before and after (numbers in the report).

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
