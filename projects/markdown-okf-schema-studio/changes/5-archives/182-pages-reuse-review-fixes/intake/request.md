# 182 — Pages reuse: fixes from the post-merge review

Type: fix (build) · Priority: P1 · Approved via the Chief of Staff (2026-10-29): findings of the
post-merge Opus review of PR #192 become a follow-up PR. From origin/main; normal CI + a Pages
dry run on the branch. Full review: `reports/post-merge-review.md`.

1. F1 (major) `pages.yml:85-112`: the manual `run_id` input is trusted unchecked; a wrong run id
   deploys reports from another commit / failed / pull_request (fork) run / other workflow, and a
   missing `e2e-integration` is skipped silently. Fix: `select_e2e_run.py --run-id` applies the same
   checks (ci.yml, head_sha == HEAD, workflow_dispatch, success, integration success, artifacts
   live) and exits non-zero on mismatch.
2. F3 (minor): a `gh api` error or an artifact expiring between selection and download aborts the
   deploy instead of falling back. Fix: fall back to the suite (or fail closed, documented).
3. F4 (minor) `pages.yml:42`: `GH_TOKEN` job-wide; scope it to the selection/download steps.
4. F5 (minor) justfile `site-from-run`: `for ... && cp` ignores a failed download; leftovers in
   `out/reports` mix in. Fix: bash shebang recipe with `set -euo pipefail`, `rm -rf out/reports`.
5. F6 (nit): stage downloads are redundant with `studio-reports`; simplify if safe.
6. F2 (minor): document that on the automatic release path no heavy run of the release sha exists
   yet, so Pages falls back to the suite (backlog P2 require-green-heavy-before-tagging tracks the
   real fix).
7. Env fix seen by every Driver: `release-tests` fails in a fresh venv (`jsonschema` comes from the
   `requirements` group) — add `--group requirements` to the `release-tests` recipe.
