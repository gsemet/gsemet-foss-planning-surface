# Task T14 — Stable morph keys and incremental page init

Audit finding(s): P-07, P-08, CR 16 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t14`, branch `change-requests/135-t14-stable-morph-keys` (local only). Created by the orchestrator when the task starts, from the **integration branch tip** (`change-requests/135-audit-security-performance-pack`) unless the scope says otherwise, with a `node_modules` symlink to the main checkout.

## Scope

Keys without line attributes, hash keys, incremental insert points, single-flight `stabilizeLayout`, rAF-throttled `codeCopy.place`. `src/page/modules/contentMorph.ts`, `src/page/features/contentPatch.ts`, `insertPoints.ts`, `scrollCore.ts`, `src/page/modules/codeCopy.ts`. Proof: `runtimeContentPatch.test.ts` keeps all blocks below an inserted line.

## Definition of done

- The change above; a test that fails on the unchanged code (a pure refactor: tests unchanged and green); benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync (moved with the code for a refactor).
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
