# Verify CR-389

Head: b87b254ef7f94891083406213726ab3e527a42a6

All claims judged at b87b254 unless noted.

1. New tests pass at the head. Command: `pytest test_board_forge_read.py test_board_prs.py test_forge_hub.py -q` -> `77 passed in 21.98s`. Full suite `pytest -q` -> `884 passed, 1 skipped in 128.39s` (matches the PR body's figure).
2. New tests fail on the base. Detached worktree at origin/main b76d037e, the head's three test files, base src (PYTHONPATH) -> `24 failed, 53 passed`, among them `test_a_native_stack_merged_in_one_go_is_told_landed_with_its_bottom`, `test_a_stacked_merge_is_signalled_landed_with_its_base_once_the_base_landed[1-reads5..]` and `[2-reads6..]`, `test_a_merged_pr_says_whether_its_merge_commit_is_on_the_default_branch[*]`, `test_the_github_query_reads_the_merge_commit_and_the_default_branch_history`. Base worktree removed.
3. Live read-only `gh` check: `forge_read.read` on gsemet/chantier #335, #342, #354 (evidence/live-gh.log):
   `335 merged main ... True` / `342 merged chantier/batch-28/cr-369-... ... True` / `354 merged chantier/batch-28/cr-385-... ... True`.
   `prs.rows_of` on #335+#342: `CR-370 ... landed_with {'cr': 'CR-369', 'at': '2026-11-19T09:29:53Z'}` (#342 merged 09:29:54, after its base at :53, so the time-based way cannot give it: the new way does). CR-369 landed_with None.
4. GITHUB_FIELDS contains `mergeCommit { oid }`; query has `dh: object(expression: "HEAD")` and `history(first: 100)` (asserted by the new test, passing in claim 1; read in the diff).
5. chief-of-staff.md `landed with` paragraph names "or the PR's own merge on the default branch (a native stack merged in one go)" (diff read).
6. PR description (PR #359, head b87b254, body identical to work/pr-body.md bar a trailing newline): Summary, Deliverables and Changes match the diff (forge_read, prs, journal docstring, CoS card, three test files); no image; Known gaps "None" is consistent (no UNVERIFIED claim). Review box: note `r1 body re-inspection approved at db5c3af`; db5c3af and b87b254 have the same `git patch-id --stable` (5350eb18...), a clean rebase, so the approval carries. Ship log shows no `carry` event; noted, not failing. Remaining unchecked boxes (Verified, CI) are the later steps.
7. Scope: `git diff --stat origin/main...HEAD`: 7 files, no CLI-surface or other change unmentioned.

Not run by me: `just eval-dry-run`, the long gate (the cards and CLI src changed; the pipeline's scenario job owns it).

VERIFIED
