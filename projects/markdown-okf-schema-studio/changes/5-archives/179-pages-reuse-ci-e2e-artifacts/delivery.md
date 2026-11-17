# 179 — Pages deploy reuses the CI end-to-end reports — report

Landed 2026-10-28. PR #192 merged by the user as 3d65a586 + 0203bfef (two commits).

- pages.yml: `build-site` finds the newest green heavy CI run of the exact commit
  (`scripts/select_e2e_run.py`), downloads e2e-visual / e2e-integration / studio-reports and runs
  `just site-assemble`; fallback: `just site` (full suite). Separate `deploy-pages` job.
- `just site` unchanged locally; new `just site-assemble`, `just site-from-run RUN_ID`.
- Dry run: dispatch pages.yml with `dry_run=true` (no tag, no deploy; optional run_id).
- Proof: branch dry run 40782720690 failed (artifacts extracted over each other), fixed by
  0203bfef; dry run 40782850942 on ac3d7805 green. Normal CI on the final head was still running
  at merge (40783197563). Post-merge dry run on main: 40783429697.
- PROCESS GAP: the Driver implemented the change itself (no Coder/Inspector rounds, no independent
  review) and did not run `just check`; only pytest (38 passed) and the justfile format check. Normal
  CI on the final head passed after merge (40783197563). Review-only pass proposed to the CoS.
- Follow-up: P2 require-green-heavy-before-tagging.
