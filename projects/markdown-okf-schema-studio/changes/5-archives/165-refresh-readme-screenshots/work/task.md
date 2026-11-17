# Task T1 — README screenshots show the current UI

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-165` on branch
`change-requests/165-refresh-readme-screenshots` (from `origin/main` d48739d7, own `npm ci`,
`playwright install chromium`). Part of release 1.0.0 (CR 163).

## Definition of done

- Every README picture regenerated from its capture scenario (no hand edits), same file names,
  LFS as today; the "not checked" ones audited and regenerated if outdated.
- myst-admonitions crop fixed in the scene framing (a test or check that fails on a cropped toolbar
  where cheap).
- Static pictures: no motion frame. CR 162 (toolbar motion, in flight) adds a load hint and
  tooltip/expand animations; captures must not depend on them (if the scenarios already disable
  motion or wait for a settled state, say so in the report).
- CR 161 (hotfix, in flight) may change the toolbar geometry: if it merges before this PR, rebase
  and regenerate the affected pictures.
- PR body: before/after pairs from the -assets branch.

## Gates

- `just check`; the README image generator (`scripts/generate-readme-images.py` or its `just`
  recipe) as documented; `okfreq validate --check-links --project-root .` if requirements or docs
  change. Normal CI green (no heavy needed unless the generator depends on the real-window suite:
  then heavy CI is the proof and local real-window runs are forbidden).
