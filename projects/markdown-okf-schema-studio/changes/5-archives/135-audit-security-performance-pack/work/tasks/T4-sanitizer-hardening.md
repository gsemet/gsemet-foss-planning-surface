# Task T4 — Sanitizer hardening

Audit finding(s): S-05, S-08, S-09, P-09, CR 5 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t4`, branch `change-requests/135-t4-sanitizer-hardening` (local only, from origin/main).

## Scope

Always drop `<script>` in the live preview, remove `nonce` from the attribute allowlist, linear `removeNode`, a nesting depth cap (deeper content is cut with a visible marker), KaTeX style declarations validated. `src/core/security/html-sanitizer.ts`, `src/core/render/mathRenderer.ts`. Proof: security tests + `bench-sanitizer2.mjs` (50k removals under 500 ms, depth 10k no throw).

## Definition of done

- The change above; a test that fails on the unchanged code; benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.
