# 179 — Pages deploy reuses the CI end-to-end reports

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Pages deploy reuses the CI end-to-end reports instead of running the suite again
> 
> Type: build · Priority: P1 (raised by the user, 2026-10-28) · Filed 2026-10-28 from the user's question while preparing 1.0.0 · After 1.0.0
> 
> ## Observed
> 
> - The release pipeline runs the end-to-end suite twice. The CI jobs `visual` and `integration` run
>   it on the release commit and upload their reports as artifacts (`e2e-visual`,
>   `e2e-integration`, `.github/workflows/ci.yml`).
> - The `pages` job then calls `.github/workflows/pages.yml`. That workflow runs `just site`, which
>   depends on `e2e` (`site: e2e requirements-report` in `justfile`), so the whole suite runs again on
>   a fresh runner just to rebuild the gallery and the reports index.
> - Cost: release time, and one more chance for an e2e flake to block the Pages deploy. The
>   Marketplace publish is not affected, but the site, including `requirements.html`, stays on the
>   previous version.
> 
> ## Constraint found while triaging
> 
> - The push CI on main (the run that tags the release) runs only `static` and `visual`; `integration`
>   runs only in heavy runs, dispatched by hand. So the tagging run has no `e2e-integration`
>   artifact. Options: reuse the latest green heavy run of the tagged commit (and require one before
>   tagging), or build the gallery from the visual campaign only. Decide in the grill.
> - `pages.yml` only runs on a real `vX.Y.Z` tag that matches package.json and is in main, so the
>   change needs a test path that does not need a release (dry-run input or a test tag).
> 
> ## Expected
> 
> - On a release, `pages.yml` downloads the e2e report artifacts of the CI run that tested the
>   tagged commit, then builds the site from them (gallery, reports index, requirements page).
> - It runs the suite itself only as a fallback, when no artifacts exist (for example a manual
>   `workflow_dispatch` on an old tag).
> - `just site` keeps working locally.
> 
> Proof: a release dry run (or `workflow_dispatch` on a test tag) where the Pages job shows no e2e
> stage and the deployed gallery matches the CI screenshots.

## Decision (user, via the Chief of Staff, 2026-10-28)

Build the site from the e2e artifacts of the latest GREEN heavy run of the tagged commit; fall back
to running the suite when none exists. Keep `just site` working locally. Add a dry-run path that
needs no release tag. Coordinate with the release-notes hotfix (PR #190) which also edits
release.yml: touch pages.yml / justfile / scripts, and ci.yml's `pages` job only if needed.
