# Task T1 — MyST cards, tabs and version directives

Implement `00-request.md` and `01-intent.md` in the worktree `../markdown-okf-schema-studio-wt-148`
on branch `change-requests/148-myst-cards-tabs-version-directives`, created by the orchestrator
from the tip of the CR below it in the stack (147, or the highest ready CR), with a `node_modules`
symlink to the main checkout.

## Definition of done

- The four parts of the intent; tests that fail on the unchanged code.
- SwRS updated (`requirements/`), `@implements_req` / `@tests_req` markers in sync.
- Before/after real-window screenshots (cream + one dark theme) under `reports/shots/`; README
  section with the new screenshots under `images/readme/`.
- Docs updated (`docs/user/`).

## Gates (foreground, in the worktree)

- `just check` (lint, types, unit, okfreq)
- Targeted e2e for the touched area. Real-window suites only under `WINDOW-TESTS.lock`, with
  `env -u ELECTRON_RUN_AS_NODE -u VSCODE_*`; revert regenerated `images/` PNGs unless intended.
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
