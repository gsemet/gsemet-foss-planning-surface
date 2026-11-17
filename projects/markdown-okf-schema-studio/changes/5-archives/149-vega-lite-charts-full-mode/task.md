# Task T1 — Vega-Lite and Vega charts, "Full" mode

Implement `00-request.md` and `01-intent.md` in `../markdown-okf-schema-studio-wt-149` on branch
`change-requests/149-vega-lite-charts-full-mode`, created by the orchestrator from the tip of the
CR below it in the stack (148, or the highest ready CR). This CR adds dependencies: run `npm ci`
in the worktree (own `node_modules`, no symlink), then `npm install` the allowed packages.

## Definition of done

- The intent; tests that fail on the unchanged code; SwRS and markers in sync; docs and README.
- Real-window screenshots (cream + one dark theme) under `reports/shots/`; bundle sizes before/after.

## Gates (foreground, in the worktree)

- `just check`; targeted e2e. Real-window suites only under `WINDOW-TESTS.lock`, with
  `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`. Summarize gate output (counts + failures only).

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
