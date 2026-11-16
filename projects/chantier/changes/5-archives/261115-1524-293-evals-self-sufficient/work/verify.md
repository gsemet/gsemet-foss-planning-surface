# Verify CR-293

Head: 782385d683daa38e49372d384a6103f4b1ca23a2

All claims judged at 782385d683daa38e49372d384a6103f4b1ca23a2.

1. `just check` green: command `just check` in the worktree; output ends "200 passed in 29.37s", ruff/mypy/biome/lock/release-notes ok. PASS.
2. `just eval-dry-run`: exit 0, "dry run: 16 of 16 cases as expected"; output in verifier/evidence/eval-dry-run.txt. Cases quoted include other-sandbox, reset-foreign, reset-empty, publish, setup-prompt (all `ok`). dry_run.py points `sandbox.LOCAL` at a tmp path (line 145), and the main checkout holds no sandbox.local.json (ls: No such file). PASS.
3. README read-through from "Prerequisites": `sandbox.py publish <owner>/<name> [--yes]`, `sandbox.py reset [--yes]`, `sandbox.py merge <pr> [--workspace]`, `setup.py <campaign> <workspace>`, `audit.py <workspace> --sandbox` all exist (--help run for each); real-foreman/RUNBOOK.md has a "Start" section. Not run for real (PR Known gaps says so). PASS.
4. `cat evals/kit/sandbox.json` -> {"repository": "gsemet/chantier-eval-sandbox", "base": "6e87a36..."}; `git diff origin/main...HEAD --stat -- evals/kit/sandbox.json` empty: unchanged. PASS.
5. PR 243 description (gh pr view): sections render, Summary/Deliverables/Changes match the 13-file diff (kit, README, 5 runbooks, .gitignore, host card). Host card diff touches only the Auto-fix events bullets and the Configuration set_monitor line. Review box: log has "inspector approved at f257647..." (round start head) then "committed as 782385d": accepted. CI at the head: check x3, eval-dry-run, scenario all SUCCESS. Minor: Known gaps still says the scenario job has not passed at this head, although it is green now (stale wording, not a failure). PASS.

VERIFIED

6. Description pass at 782385d683daa38e49372d384a6103f4b1ca23a2 (gh pr view 243 body): renders; Summary/Deliverables/Changes match diff; SANDBOX_FORGE_REPOSITORY claim true (dry_run.py:169, sandbox_forge.py:7); set_monitor in setup.py and host card; Review box backed by log note "committed as 782385d"; gh pr checks 243 all 5 pass; internal reference only in last section; Known gaps coherent (stale scenario wording now gone). PASS.

VERIFIED
