# Task T1 — Only http, https and mailto links are opened outside VS Code

Implement `00-request.md` and `01-intent.md` (intent, expected behaviour, autonomous decisions) in the worktree `../markdown-okf-schema-studio-wt-132` on branch `change-requests/132-link-scheme-check-before-open-external`.

## Definition of done

- The behaviour of the intent, with the autonomous decisions.
- Reproduce the bug first when the item asks for it, in a real VS Code window; state in the report whether the before-shot matches the problem described.
- A test that fails on the unchanged code (unit, webview or e2e as fits), plus the tests the item asks for.
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync; a fixed "Known issue" removed.
- UI change: before/after screenshots (cream theme + one dark theme) in a real VS Code window, saved under `reports/shots/` for the PR. The reviewer rejects a before-shot that does not show the problem.
- Docs updated when a user-visible behaviour or setting changes.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; retry once on a focus timeout; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report; never paste full logs.
