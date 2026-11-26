# Stack CI: the merge-commit check accepts the forge's chained test merge

CI is red on every new run of a pull request above the bottom of a GitHub native stack: `check-no-merge-commits` reads the forge's chained test merges as merge commits of the branch. Fix the check without hiding a merge commit that a branch really carries.

Observed (2026-11-26, about 02:20Z):

- `scripts/check-no-merge-commits.sh` runs in `just ci-static` (jobs static, static-windows, then `checks`, the required check).
- Run 45741461955, PR #516 at 8ce169f (top of forge stack 528): the checked-out `refs/pull/516/merge` is a chain of test merges (main <- #512 <- ... <- #522 <- #516), and the script got base `origin/main` although the PR's base is CR-501's branch. The script skips only one test merge (`HEAD^1` must be an ancestor of the base), so it listed the ten chain merges and failed.
- Log: changes/4-batch/2-actives/500-clip-adapt-the-export-video-long-page-sa/work/ci-45741461955-static.log
- #512-#515 and #517-#522 keep their earlier green runs. Expected (one run observed): any new run of a stack PR above the bottom fails the same way (a push, a restack, or the forge's own restack after a partial merge). PRs outside the native stack are not affected (#529 is green).

The fix touches the script, its tests in `test/build/test_no_merge_commits.py` (see the `test_test_merge_*` cases) and the guideline or requirement text the project asks for.
