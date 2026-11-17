# CI parallel jobs (CR 024, 2026-10-22)

User: "la CI devient très longue, est-ce qu'on peut paralléliser certaines tâches. Règles: les jobs
en CI appellent des cibles justfile, idéalement 1 ou 2 max (1 pour setup (just dev ou just dev-ci)
et 1 pour faire n actions séquentielles)." Guideline written: `.agents/guidelines/ci.guidelines.md`.

Measured (run 39756648675): setup ~50 s, check+sphinx ~30 s, visual ~5 min, integration ~4 min 40,
review:finish + site a few s. Total 11 min (up to 18 min on slower runs).

## Decisions (user, 2026-10-22)

- Q1 (a): 3 test jobs (static, visual, integration) + 1 report job.
- Q2: every PR runs the e2e (visual + integration). No gallery/site on PRs; an optional job,
  manually triggered (workflow_dispatch boolean input), builds the gallery when needed.
- Q3: a final aggregate job named `checks` (branch protection unchanged).
- Q4: own worktree/branch `ci/parallel-jobs`, separate PR. User: the guidelines go in their own `docs:` PR
  (branch docs/agent-guidelines, c407fa4).
