# Verify CR-245

Head: 5ccb5e0d596ca86a7a4f9e8ede836f227afc79ba

Verdict: VERIFIED (with one open item: the CI `just scenario` leg was still pending when judged).

| Claim | SHA | Command | Output |
| --- | --- | --- | --- |
| `just check` passes (format, ruff, mypy strict, lock, pytest, release notes) | 5ccb5e0 | `just check` in the worktree, HOME/USERPROFILE/CLAUDE_CONFIG_DIR on scratch | ruff "All checks passed!", mypy "Success: no issues found in 79 source files", "63 passed", release-notes ok |
| CI at head, other legs | 5ccb5e0 | `gh pr checks 182` | check macos/ubuntu/windows pass, eval-dry-run pass; `just scenario (ubuntu)` pending |
| Scenario section 13a on GitLab (create retargets bottom first with `--hostname`, show writes nothing, second create retargets nothing, draft joins, check 1 to 5 forms, folded, complete chain, rebuild refused exit 4, `--stack` refused) | 5ccb5e0 | scratch runner importing `scenario/run_scenario.py`, running `forge_stack_cli` only, `--forge gitlab` | `PASS 21 FAIL 0`; lines seen: `check 1: !202 merged into ... not main: folded into CR-101`, `stack complete, mergeable below 6206234 (!203), the release on top`, `check 5: the release MR !203 is not on top (!999 targets it)`, rebuild exit 4 with forge text, `--stack is GitHub only: a GitLab stack is the chain of its MRs` |
| Scenario section 13a on GitHub unchanged, GitLab link in GitHub stack gives `not all in one repository`, `is neither` refusal | 5ccb5e0 | same runner, `--forge github` | `PASS 38 FAIL 0` |
| Reading pass: no "GitHub only"/"stays a chain"/"glab mr view`$" left in the cards | 5ccb5e0 | Grep in `skills/chantier/references` | no matches |
| GitLab forms carry "unproved" in the four cards | 5ccb5e0 | Grep count | chief-of-staff 9, driver 6, foreman 2, concepts 1 |
| Known gap stated: not run on real GitLab | 5ccb5e0 | `work/pr-body.md` | Known gaps names it |

Not run: the whole `just scenario` (waived by the user; GitHub CI replaces it). Its CI leg must be green at this head before merge.

Note: the Test plan boxes in pr-body.md carry `<sha7>` placeholders to be filled by the Driver.

## Description pass

Command: `gh pr view 182 --json body,headRefOid -q '.headRefOid,.body'` and `gh pr checks 182`, against `pr-template.md` and head 5ccb5e0.
Output: head 5ccb5e0d596ca86a7a4f9e8ede836f227afc79ba; all five CI jobs pass (check x3, eval-dry-run, scenario); `forge_stack.py` is 309 lines (body says 309); Test plan SHAs all 5ccb5e0 and boxes match verify.md/STATUS notes (review approved at 5ccb5e0, Verified, CI green); waiver gap named in Known gaps; no internal reference outside "Internal references"; sections and fold in template order. Result: VERIFIED.
