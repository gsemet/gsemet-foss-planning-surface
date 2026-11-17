# Task T1 — README-style HTML renders like GitHub, and shows its tags in edit mode

Implement `00-request.md` and the intent file(s) in the worktree `../markdown-okf-schema-studio-wt-141` on branch `change-requests/141-readme-html-guaranteed`
(created by the orchestrator when the CR starts, from the tip of `change-requests/135-audit-security-performance-pack`
or of the CR below in the stack, with a `node_modules` symlink to the main checkout).

## Definition of done

- The behaviour of the intent, with the autonomous decisions.
- A bug: reproduce it first in a real VS Code window; the before-shot must show the problem described.
- A test that fails on the unchanged code (unit, webview or e2e as fits), plus the tests the intent asks for.
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync; a fixed "Known issue" removed.
- UI change: before/after screenshots (cream theme + one dark theme) in a real VS Code window under `reports/shots/`.
- Docs updated when a user-visible behaviour or setting changes (user guide, slash menu, toolbar, settings).

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
- Summarize gate output (counts + failures only) in the report.

## Requirements traceability (mandatory, checked by the reviewer)

Follow `requirements/guidelines/requirements.guidelines.md`. In the same commit as the code:

- Every behaviour added or changed has a SwRS requirement (new or updated) under `requirements/`;
  a fixed "Known issue" line is removed.
- **Both links for every touched leaf requirement**: `@implements_req <ID>` next to the
  implementation (in `source_dirs`) and `@tests_req <ID>` next to **each** test that checks it (in
  `test_dirs`); markers on their own comment line, moved with the code on a refactor.
- Run `just requirements-update` (okfreq validate, lint indexes, update-coverage) and commit the
  generated changes with explicit paths; append a dated entry to the bundle's `tiers/log.md`
  (IDs, what changed, why, verification results).
- No non-exempt leaf requirement you touched is left without a source or a test link; no marker
  references an unknown ID. The report lists the IDs added or changed with their source and test
  files.
- Reviewer: `FIX-REQUIRED` when any of the above is missing.
