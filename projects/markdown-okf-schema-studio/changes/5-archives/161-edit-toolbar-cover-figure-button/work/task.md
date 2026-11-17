# Task T1 — Toolbar vs figure Edit button

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-161` on branch
`change-requests/161-edit-toolbar-cover-figure-button` (from `origin/main`, own `npm ci`).

## Definition of done

- Root cause proven (geometry: toolbar rect vs figure edit button rect at the integration window
  size), stated in the report; a unit/visual check that fails on main where possible.
- Heavy CI `integration` passes on the branch.
- Requirements traceability: SwRS updated if behaviour changes, markers, `just requirements-update`,
  dated entry in `requirements/tiers/log.md`.

## Gates

- `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
