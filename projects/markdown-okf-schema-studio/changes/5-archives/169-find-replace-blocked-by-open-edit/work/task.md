# Task T1 — find-in-preview stalls after the table menu change

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-169` on branch
`change-requests/169-find-replace-blocked-by-open-edit` (from `origin/main` eca17c42, own `npm ci`).

## Definition of done

- Root cause proven (or the #181 lead excluded) with evidence: code reading of the three merges,
  the find test's steps before line 228, any earlier trusted-suite test that leaves an edit open,
  and a diagnostic that records the page's edit state and the click target at the failure.
- A unit/headless check that fails on main where possible.
- Heavy CI integration passes entirely on the branch.
- SwRS / markers / `just requirements-update` / log entry if behaviour changes.

## Gates

- `just check`; `uv run --group requirements okfreq validate --check-links --project-root .`.
- Normal CI, then heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`).
