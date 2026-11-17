# Task T3 — Comments sidecar write is symlink-safe

Audit finding(s): S-04, CR 4 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t3`, branch `change-requests/135-t3-sidecar-symlink` (local only, from origin/main).

## Scope

`lstat` before write, refuse a symlink target, write to a temp file and rename atomically. `src/session/features/comments.ts`, `src/core/comments/commentStore.ts`. Proof: memory-FS test with a dangling symlink.

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
