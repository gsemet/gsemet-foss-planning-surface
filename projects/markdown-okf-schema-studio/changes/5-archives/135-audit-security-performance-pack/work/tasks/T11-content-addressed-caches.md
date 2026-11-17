# Task T11 — Content-addressed caches for per-block work

Audit finding(s): P-04, P-12 (part), CR 14 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t11`, branch `change-requests/135-t11-content-addressed-caches` (local only). Created by the orchestrator when the task starts, from the **integration branch tip** (`change-requests/135-audit-security-performance-pack`) unless the scope says otherwise, with a `node_modules` symlink to the main checkout.

## Scope

Highlight, KaTeX, stat/realpath per render, toctree reads, schema listing; bounded caches. `src/core/render/highlight.ts` (or its Shiki successor), `mathRenderer.ts`, `src/core/security/resource-policy.ts`, `src/core/render/mystGridToctree.ts`, `src/core/frontmatter/okfFrontmatter.ts`. Proof: `bench-typing.mjs` second render of an unchanged document under 50% of the first.

## Definition of done

- The change above; a test that fails on the unchanged code (a pure refactor: tests unchanged and green); benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync (moved with the code for a refactor).
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
