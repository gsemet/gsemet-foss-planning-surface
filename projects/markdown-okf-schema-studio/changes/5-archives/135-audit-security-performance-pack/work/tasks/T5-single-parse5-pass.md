# Task T5 — One parse5 pass per page build

Audit finding(s): P-03, CR 10 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t5`, branch `change-requests/135-t5-single-parse5-pass` (local only, from origin/main).

## Scope

Delete `annotateSourceMappings` (duplicate of the sanitizer's `injectSourceMappings`), string-splice the CSP, cache the shell key, tree-level table alignment, no re-parse of the previous page in `planContentPatch`. `src/session/webview.ts`, `src/core/mapping/sourceMapping.ts`, `src/core/preview/contentPatch.ts`, `src/core/render/mystTables.ts`. Touches the sanitizer too: integrate after T4. Proof: `bench-render.mjs` page build at 55k lines down by about 1 s; contract tests unchanged.

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
