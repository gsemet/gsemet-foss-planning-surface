# Verification of CR-120 at 585379d30d0a4593ec8e8aaef1c348cadca07446

Rebased on origin/main 49135f5 (ancestor check true). Project rules read (ules); none ask for evidence, so absent evidence would not change the verdict.

| Claim | Proof | Result |
|---|---|---|
| worker.md Investigator ends with an evidence plan; project rules rank above; nothing to see = one line | git diff 49135f5 585379d hunk in worker.md | ok |
| worker.md Verifier: before on detached worktree of base, after at pushed head, files in work/verifier/evidence/ with before-after.md, uncapturable evidence only changes verdict if rules require it | same diff | ok |
| driver.md CR driver validates plan, passes it to Verifier; Driver puts evidence in PR (gh pr edit --attach, others read help, uncapturable stays in work/) | same diff | ok |
| Stack driver: each CR keeps its plan | same diff | ok |
| concepts.md tree points to work/verifier/evidence/ | same diff | ok |
| Main's commits survive: 5adff96 (Push bullet line 32 force-with-lease, line 54 refused force push, line 92) and 49135f5 (Tips line in chief-of-staff.md:200) | git grep -n -i force 585379d -- driver.md; diff 49135f5..585379d touches only concepts.md, driver.md, worker.md and none of main's lines | ok |
| CLI untouched | diff --stat lists three card files | ok |
| just check / just scenario | CI green at 585379d, gate log work/gates/20261106-114754.log (reported by Driver, not re-run) | ok |

Evidence: work/verifier/evidence/ (before at 49135f5 on a detached worktree, removed; after at 585379d), see before-after.md.

VERIFIED
