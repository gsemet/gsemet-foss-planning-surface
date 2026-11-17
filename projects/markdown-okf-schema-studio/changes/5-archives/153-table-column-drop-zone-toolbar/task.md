# Task T1 — Column drop zone vs the Fold toolbar button

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-153` on branch
`change-requests/153-table-column-drop-zone-toolbar` (from fresh `origin/main`, own `npm ci`).

## Definition of done

- Root cause proven (geometry logged in CI or a local real window), stated in the report.
- A test that fails on the unchanged code where possible; the heavy `tableMoves` step passes.
- Requirements traceability: SwRS updated, `@implements_req` / `@tests_req` on every touched leaf,
  `just requirements-update`, dated entry in the bundle's `tiers/log.md`.

## Gates

- `just check` (locked okfreq 0.16 via `uv run --group requirements okfreq`).
- Heavy CI on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`): integration passes.

## Scope 2 (five rows) — see 00-request.md

- Rebase on latest `origin/main` (a4338277 or newer) first.
- Five rows; unit tests, visual layout checks (banner reserve, palette/tall-box at 360 px) and
  tableMoves stay green; StRS/SwRS toolbar requirements, `requirements/tiers/log.md`,
  docs/user/toolbar.md (+ README/folding/CHANGELOG/README image as needed).
- Gates: `just check`, `just requirements-update`, `okfreq validate --check-links --project-root .`
  (project-locked okfreq); normal CI green, then heavy CI (`gh workflow run ci.yml --ref <branch>
  -f heavy=true`) with integration and visual green.
- Before/after screenshots, light and dark, on `change-requests/153-table-column-drop-zone-toolbar-assets`.
