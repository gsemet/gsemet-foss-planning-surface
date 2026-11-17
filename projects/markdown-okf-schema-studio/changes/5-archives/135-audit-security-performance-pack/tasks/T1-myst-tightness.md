# Task T1 — Patch `computeBlockTightness` of `markdown-it-myst`

Audit finding(s): P-02, CR 9 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t1`, branch `change-requests/135-t1-myst-tightness` (local only, from origin/main).

## Scope

Split the source lines once per parse instead of once per directive fence, through the existing postinstall patch (`scripts/patch-myst-imports.mjs`). Prepare the upstream PR text in `reports/upstream-markdown-it-myst.md` (do not open it). Proof: `bench-render.mjs` parse at 55k lines at least 2x faster; contract tests unchanged.

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
