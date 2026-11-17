# Task T6 — Render only visible previews, once per document

Audit finding(s): P-01 (part), P-06 (part), CR 11 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t6`, branch `change-requests/135-t6-visibility-shared-render` (local only, from origin/main).

## Scope

Dirty flag per hidden panel (render on show), one render per `(document, revision, options)` shared by sessions of the same document. `src/session/previewManager.ts`, `src/session/hostEvents.ts`, `src/session/features/rendering.ts`. Proof: `previewManager.test.ts` counts renders: two sessions of one document = 1, hidden panel = 0 until shown.

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
