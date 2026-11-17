# Task T1 — Table toolbar vs five-row floating toolbar

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-167` on branch
`change-requests/167-table-toolbar-five-row-clearance` (from `origin/main` f39a0aa5, own `npm ci`).

## Definition of done

- Root cause from the geometry in the log and the code (`tableCellEditor.ts` /
  `clearPreviewControls` / scroll reveal), stated in the report; a unit or visual check that fails
  on main where possible (no real-window runs locally).
- Heavy CI integration passes on the branch past `scenarioTableToolbar`.
- SwRS updated if behaviour changes; markers; `just requirements-update`; log entry.

## Gates

- `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
