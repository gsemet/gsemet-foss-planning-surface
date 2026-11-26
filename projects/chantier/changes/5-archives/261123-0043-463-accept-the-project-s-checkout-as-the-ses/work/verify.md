# Verify CR-463

Head: 450b8784d7c83e87a6fb227bd32f87c213a9d356

Claims, each judged at 450b878:

1. Spec sections 1-3 (session_checkout, P6/P7/P11, init, permissions reads): `git diff origin/main...HEAD -- skills/chantier/scripts/cli/src` read; matches the spec (one rev-parse of the cwd, owners surface/clone/project/other/none, P6/P7 texts per owner, P11 cwd=surface_root, init refuses only linked, remote reads cwd=repo.root, settings from session top).
2. Tests: `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_session_folder.py -q` -> `17 passed in 33.20s` (layouts nested/beside x surface/clone/worktrees/other, in-project, P11, P10, init, missing clone).
3. Cards (session-start, chief-of-staff, foreman, claude-code, copilot) diff read: say what the code does, as the spec lists.
4. Review box: `chantier log 463`: "r2 approved at 9bb9c9b, committed as 450b878" proves the review at 450b878.
5. CI at head: log note `gh pr checks 440 at 450b878: check x3 pass, eval-dry-run pass, scenario pass`; `gh pr view 440` headRefOid = 450b8784d7c83e87a6fb227bd32f87c213a9d356.
6. PR description (read via `gh pr view 440 --json body`): renders, no images, Summary/Deliverables/Changes match the diff, Known gaps names the waived gate; no stale mark.

Not captured: the before run (new tests on the base, to show the clone cell fails today): my writes are limited to the CR worktree and the CR folder, so the tests could not be copied into a detached base worktree. The spec's own statement and the diff (old code read the cwd's toplevel against session_root) stand; not claimed as run.

VERIFIED

## Description pass at 450b8784d7c83e87a6fb227bd32f87c213a9d356

Judged: `gh pr view 440 --json body` against `git diff origin/main` and `tests/test_session_folder.py` lines 91-112.
- Deliverables table, rows "linked worktree of the surface" and "linked worktree of the clone": the After cell says only "P7 FAIL", but the test (`surface-worktree`, `clone-worktree`) and `_check_checkout` (`here.top == here.main.resolve()`) give P6 FAIL too (message "neither the surface's checkout ... nor the project's clone"). Claim inaccurate; the clone row's Before cell lists both, so the omission reads as P6 ok.
- Role names, Internal references, Known gaps (waived gate, pointer line, UNVERIFIED before-run noted in Test plan), Review box (note "r2 approved at 9bb9c9b, committed as 450b878"): fine.

NOT VERIFIED

## Description pass 3 (head 450b8784d7c83e87a6fb227bd32f87c213a9d356)

Claim 6 revised: NOT VERIFIED at 450b878. Command: `gh pr view 440 --json body` against `git show origin/main:.../commands/preflight.py` (P6: top == session_root; P7: gitdir == repo.git_dir) and `git diff origin/main -- .../preflight.py`, `core/repo.py`, plus `test_session_folder.py` line 109 (`"other": (neither, "P7 ok   not a linked worktree")`).
The Deliverables table's last row says Before "P6 FAIL" and After "P6 FAIL, naming both accepted folders". On the base, another repository's git dir differs from the surface's, so P7 also FAILS before; after, it is not a linked worktree, so P7 is ok. The row omits the P7 change (Before should be "P6 FAIL, P7 FAIL", After "P6 FAIL, P7 ok"). The other four rows match the base code and the diff.

NOT VERIFIED

## Description pass 4 (head 450b8784d7c83e87a6fb227bd32f87c213a9d356)

Claim 6 revised: VERIFIED at 450b878. Command: `gh pr view 440 --json body` against `git diff origin/main` (preflight.py `_check_checkout`, repo.py `session_checkout`/`linked_text`, intake.py, permissions.py) and `pytest tests/test_session_folder.py` -> `17 passed in 32.82s`. Every Deliverables cell matches: the last row now reads Before "P6 FAIL, P7 FAIL", After "P6 FAIL (naming both), P7 ok"; the linked-worktree rows list P6 and P7 FAIL. Changes list matches the diff (the one-line EXEMPT entry in test_store_reads.py is bookkeeping for the new function, not a delivered change). Known gaps and the Review box unchanged from the earlier pass.

VERIFIED
