# Task T1 — Enter in the figure alt text validates and moves after the figure

Implement `00-request.md` (intent + autonomous decisions) in the worktree `../markdown-okf-schema-studio-wt-118` on branch `change-requests/118-figure-alt-enter-validates`.

## Definition of done

- The behaviour of the intent, with the autonomous decisions.
- A test that fails on the unchanged code (unit, webview or e2e as fits), plus the e2e the intent asks for.
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync; a fixed "Known issue" removed.
- UI change: before/after screenshots (cream theme + one dark theme) saved under `reports/` for the PR.
- Docs updated when a user-visible behaviour or setting changes.

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; retry once on a focus timeout; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report; never paste full logs.
