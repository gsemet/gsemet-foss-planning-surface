# Task T1 — Strict requirement schemas with supersession and related links

Implement `00-request.md` (intent + autonomous decisions) in the worktree `../markdown-okf-schema-studio-wt-122` on branch `change-requests/122-strict-requirement-schemas`.

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

## Relaunch (2026-10-28) — overrides the gates above where they differ

- Base: origin/main f39a0aa5 (worktree fast-forwarded, clean). `okf-schema>=0.16.0` (PyPI).
- First: re-verify the recipe against okf-schema 0.16.0 (its `examples/okfreq-examples/.../base.schema.yaml`
  from the 0.16.0 sdist/wheel or tag), list any difference from the 0.15.0 recipe in the report.
- Mechanical change by a script (kept in the report); no hand edits of requirement files.
- Gates: `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`;
  `okfreq lint --check --check-links`; `okfreq update-coverage --check`. No real-window tests locally;
  normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`). Heavy integration
  on main is currently red in real-input `scenarioTableToolbar` (hotfix CR 167): report it as
  "also red on main" if that is the only red. No screenshots (no UI change).
