# CR-104 verify

Head: faf199444e9be518ed771cfa3d2c435e21b9fc2a (worktree HEAD = PR headRefOid = run 42023547444 headSha).

Raw proof in this folder: scenario-job.log, run-jobs.json, jobs-steps.txt, runners.txt.

1. New job exists in ci.yml: `scenario`, name `just scenario (ubuntu-latest)`, ubuntu-latest, same checkout/uv/just/Git-identity steps as `check`, then `just scenario`. Triggers (top of file): push on main and pull_request. No continue-on-error on it. VERIFIED.
2. Job green, both forges, every step passing. Job 127232021186 log, Run just scenario step:
   - `uv run ... run_scenario.py --forge github` -> `github: 156/156 checks passed in 35.6 s`
   - `uv run ... run_scenario.py --forge gitlab` -> `gitlab: 156/156 checks passed in 35.4 s`
   Steps all `success` (jobs-steps.txt). No FAIL/##[error] lines (only a Node 20 deprecation warning). VERIFIED.
3. Run time: job 12:00:46 -> 12:02:06 = 1m20s. Scenario runs took 35.6 s + 35.4 s = about 71 s, plus about 6 s runner setup and few seconds of cleanup. scenario/README.md says "about two minutes per forge"; Linux CI shows about 36 s per forge, so the README figure is a pessimistic (probably Windows-local) number, not contradicted by the log (not a failure; the README wording is simply loose on Linux). The short time is explained by the logged work, not by skipped forges.
4. `check` jobs stay green on three systems (same run): windows-latest (windows-2025), ubuntu-latest (ubuntu-26.04), macos-latest (runner macos-15-intel per ci.yml `include`; log shows image macos-15 and an x86_64 apple-darwin uv). All `Run just check` = success. ci.yml has `continue-on-error: ${{ matrix.os == 'macos-latest' }}`: the macOS check could fail without failing the run; here it genuinely succeeded (step conclusion success), so the green is not masked. Note this pre-existing leniency for the record.
5. `just check` passes: the `just check` step passed in all three CI jobs at this head; the caller reports a local pass too (not re-run by me).
6. Docs: diff shows CONTRIBUTING.md (two lines) and scenario/README.md say CI runs the scenario. Diff is only these 3 files; no test changed or skipped. VERIFIED.
7. Never merged: `gh pr view 26`: state OPEN, isDraft true, mergedAt null, autoMergeRequest null. First body line is exactly `**Eval run: do not merge.** The maintainer decides what happens to this PR.` VERIFIED. I changed nothing on the PR.

VERIFIED
