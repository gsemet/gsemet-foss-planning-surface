# Task T1 — Table menu vs row handle strip

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-168` on branch
`change-requests/168-table-menu-row-handle-overlap` (from `origin/main` b71fac7c, own `npm ci`).

## Definition of done

- Root cause proven from code and log geometry (menu rect vs row handle rect, z-index, stacking
  context), stated in the report, with the "does a real user hit it" answer.
- A unit or headless visual check that fails on main where possible (no real-window runs locally).
- Heavy CI integration passes entirely on the branch.
- SwRS updated if behaviour changes; markers; `just requirements-update`; log entry.
- Before/after screenshot of the table menu.

## Gates

- `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
