# 197 — Re-run recovery: artifacts must come from the current attempt

Type: fix (CI) · Priority: P1 for the 1.0.1 stack · Follow-up of CR 195 (PR #207, round cap reached).
Stacked above #207 (branch `change-requests/195-require-green-heavy-before-tagging`).

Defect proven by CR 195 (proof run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40800186540):
after `gh run rerun <id> --failed`, `actions/download-artifact` by `name:` returned the ATTEMPT-1
artifact, not the newer one from attempt 2. Pages downloads `studio-reports` (and the report job
merges stage artifacts) by name, so after the documented recovery path (re-run failed jobs on the
1.0.1 merge push) the site and the merged report could use stale attempt-1 reports.

Fix: make every artifact that a later job or Pages consumes unique per attempt (e.g. suffix
`-attempt-${{ github.run_attempt }}`) and make every consumer download the current attempt's name
(in ci.yml, pages.yml with `reports_from_caller`, and `select_e2e_run.py` / `site-from-run`, which
must pick the latest attempt's artifacts of a run). Keep upload/download pairs consistent.

Also (same area, small):
- If feasible, relax the 2-hour visual/integration stage gap in `e2e-campaign.mjs report` when both
  stages carry the same CI run id (so "Re-run failed jobs" works more than 2 h later); else document.
- Update the recovery section (CONTRIBUTING, ci.guidelines) accordingly.

Proof: a throwaway workflow on the branch (removed before the final commit) showing that after
`--failed` re-run the consumer reads the attempt-2 artifact; workflow tests for the naming; selector
tests for multi-attempt runs. `just check` green; READY PR with `--base
change-requests/195-require-green-heavy-before-tagging`; normal CI + one heavy.
