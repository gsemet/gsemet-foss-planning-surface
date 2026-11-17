# Task T25 — Unused-exports check and the Sphinx build decision

Audit finding(s): N-06, CR 28 — see [report.md](../backlog-audit-performance-security-maintainability/report.md).

Worktree `../markdown-okf-schema-studio-wt-135-t25`, branch `change-requests/135-t25-unused-exports-sphinx` (local only). Created by the orchestrator when the task starts, from the **integration branch tip** (`change-requests/135-audit-security-performance-pack`) unless the scope says otherwise, with a `node_modules` symlink to the main checkout.

## Scope

Add an unused-exports step to `just check`; remove dead exports. `src/node-services/build/sphinxBuild.ts`: remove it when no contributed command or setting reaches it (the extension does not export with Sphinx), otherwise keep it and say why in the report. Proof: check green.

## Definition of done

- The change above; a test that fails on the unchanged code (a pure refactor: tests unchanged and green); benches run before and after where named (numbers in the report).
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync (moved with the code for a refactor).
- Docs updated when a user-visible behaviour or setting changes.
- One Conventional Commit on the task branch (explicit paths, trailer `Assisted-by: Claude:<Model>`), not pushed.

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
