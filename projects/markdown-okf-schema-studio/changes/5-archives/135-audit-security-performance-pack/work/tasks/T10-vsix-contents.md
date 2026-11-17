# Task T10 — VSIX contents

Audit finding(s): P-13, S-10, CR 8 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t10`, branch `change-requests/135-t10-vsix-contents` (local only). Created by the orchestrator when the task starts, from the **integration branch tip** (`change-requests/135-audit-security-performance-pack`) unless the scope says otherwise, with a `node_modules` symlink to the main checkout.

## Scope

Exclude `**/*.map`, `docs/**` (keep only what the README or the walkthrough links), `.claude/**`, `pyproject.toml` from the VSIX. `.vscodeignore`. Proof: `vsce ls` shows no `.map`, size before/after in the report.

## Definition of done

- The change above; a test that fails on the unchanged code (a pure refactor: tests unchanged and green); benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync (moved with the code for a refactor).
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
