# Verify CR-191 at 4feeab7

Verdict: VERIFIED.

- `just eval-dry-run` equivalent (`uv run --no-project python evals/kit/dry_run.py`) on Windows at 4feeab7: exit 0, 6 of 6 cases ok (clean, stray-merge, reset-leftover, merge-refused, stale-lock, force-tag-push), each naming its criterion (C12 #6, "not at its base", refused reasons, J5 + judge "uv.lock is not up to date"). Duration 121 s, so a separate recipe and a CI job (spec 7): present in justfile and ci.yml.
- CI on PR 136: all 5 jobs pass, including `just eval-dry-run (ubuntu-latest)`; check on 3 OSes passes (structure assertion for uv.lock in release CRs present at test_structure.py:461-464).
- Old-kit evidence (work/old-kit-dryrun.log): clean fails at d72df44 on the reset's verify (refs/pull/*), no `merge` command, and the C12 stray (#2 = release PR); a plain-shim run, noted as taken step by step.
- No network: sandbox.URL rebound in-process, GIT_ALLOW_PROTOCOL=file, fake gh first on PATH. forge.py, scenario/, cards and CLI unchanged in the diff.
- Docs: evals/README.md (rows + "Changing the kit"), CONTRIBUTING.md updated; AGENTS.md unchanged.
- Noted, not blocking: the PR body quotes 81 s; measured here 121 s (same conclusion). The PR body evidence checkbox still unticked.
