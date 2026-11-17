# 183 — Release 1.0.1 on top of the night-batch stack

Type: release + stack assembly · Priority: P1 · Owner decision 2026-10-29 (via the Chief of Staff):
"arrange toi pour bien finir toutes les CR demandées dans une stack mergeable. Rajoute tout en haut
une PR pour passer en 1.0.1 et vérifier que tout marche bien." Full autonomy until the end of the batch.

## Part A — the stack (phase 2, when the Foreman says the member PRs are final)

One gh stack, bottom to top (dependency-safe; CI/flake fixes low so the top heavy run benefits):

1. #196 `change-requests/182-pages-reuse-review-fixes` (pages.yml, select_e2e_run.py, justfile)
2. #193 `change-requests/173-ci-integration-hang-after-coexistence` (integration runner, ci.yml)
3. #194 `change-requests/180-alert-dropdown-stress-flake` (stress)
4. #191 `change-requests/178-mermaid-labels-clipped` (Mermaid; possibly reduced to what is proven)
5. #195 `change-requests/181-readme-reports-link-and-tiers-link` (README, package.json, site)
6. this CR, `change-requests/183-release-1-0-1` (version bump, CHANGELOG, notes)

Not in the stack: #154, #155 (older, not this batch). Rebase each branch on its parent only with
`git rebase` + `git push --force-with-lease origin change-requests/<branch>` (explicit ref). Never
GitHub "Update branch". Then `gh stack init <branches in order>` / `gh stack submit` so each PR's
base is its parent. Resolve conflicts (CHANGELOG, ci.yml, requirements generated lines) through a
Coder. Stress flakes are fixed, never ignored (rule 12).

## Part B — release 1.0.1 (phase 1, can start now from origin/main)

- Bump to 1.0.1 in package.json, plugin.json and every place `version.py` manages; plugin version
  must still equal the extension version (existing tests).
- CHANGELOG section 1.0.1 summarising the stack, written for users.
- Release notes for the GitHub release: `reports/release-notes.md` in this CR folder and wherever
  release.yml expects hand-written notes, same style as `../163-release-1-0-0/release-notes.md`, short.
- Analyse the release pipeline on merge to main: tag-release → release.yml (generated notes) →
  Pages. Compare with the 1.0.0 failures (CR 172: tag-release skipped; CR 176: release notes argv
  too long) and state explicitly whether a manual tag push will be needed. Do not tag/publish.

## Proof on the top of the stack

- normal CI and heavy (integration + stress) green on the top PR;
- `just check` and the full unit suite;
- the VSIX builds and its manifest shows 1.0.1, categories ["Programming Languages","Formatters"],
  keywords ["markdown","OKF","MyST"];
- requirements report and gallery build.

## Stress time budget (CoS, 2026-10-29) — before dispatching heavy on the top PR

Stress already takes about 20.5 min (timeout 30 min) with #203's new `find-in-preview` scenario.
Sum the stress time of every scenario in the assembled stack (#200 review-threads changes, #203, the
window-blur item if it lands). If the total is above about 25 min, fix it through a Coder:
shard stress into parallel jobs (preferred, keeps wall time short), or raise the timeout with a
written reason. Never ship a stack whose final heavy is cancelled by the timeout.

## Recovery path (CoS, 2026-10-29) — copy from CR 195's PR body into the pipeline analysis

If a flake fails integration or stress on the 1.0.1 merge push: the user clicks "Re-run failed
jobs" on that same run → heavy re-runs, then tag-release, release, pages; no new commit, no manual
tag. CR 195 proves that GitHub re-runs the skipped dependents and documents the exact steps; put
those steps in reports/release-pipeline-analysis.md and the release section of the PR body.
