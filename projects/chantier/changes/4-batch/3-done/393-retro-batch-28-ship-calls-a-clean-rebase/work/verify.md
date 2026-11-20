# Verify CR-393

Head: 960cdb80a37138c956396a148db64d6830872b6d

Claims, each judged at 960cdb80 (the pushed head):

1. Code matches the specification (head_base candidates: start base, pr_base, planned, default branch, other non-cancelled batch CRs' remote and local tips; _patch_ids checks both git calls; counts or first differing commit in the reason; driver.md bullet). Command: `git diff <cr-390 branch>..HEAD -- skills/chantier/scripts/cli/src skills/chantier/references`; read, matches sections 1-3.
2. New tests (batch-28 shape x3 cases, base at judgment, real change x3 with counts, git failure named) and existing ones pass at head. Command: `pytest test_carry_ship.py test_gate_carry.py -q`; output: `29 passed in 51.59s`.
3. The new tests fail on the previous code. Command: same pytest run on a detached worktree of the base with the new test files and PYTHONPATH on its src; output: `8 failed, 21 passed` (the 3 carry cases, gate base, 3 real-change cases, git failure). Detached worktree removed.
4. PR description (work/pr-body.md): Summary, Deliverables, Changes match the diff; Known gaps matches the spec; no images; no role names outside Internal references. Test plan boxes pending are the Driver's to fill.
5. CI at this head green per the Driver's note (check x3, eval-dry-run, scenario); not re-run.

VERIFIED

## Description pass (posted PR 361 body, judged at 960cdb80a37138c956396a148db64d6830872b6d)

Head: 960cdb80a37138c956396a148db64d6830872b6d

- Posted body (`gh pr view 361 --json body`) renders: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible; one Details fold with Changes, Impacts, Test plan, Internal references; blank lines after summary and before `</details>`; nothing after it. No images. No Issues References (spec has no issue).
- Summary/Deliverables/Changes match `git diff <base>..HEAD --stat`: driver.md, carry.py, crs.py, test_carry_ship.py, test_gate_carry.py.
- No internal ref outside Internal references; "Driver card" names a file the diff changes (product term).
- Known gaps matches the spec; no UNVERIFIED or STALE marks.
- Test plan: tests 8 of 29 (claims 2, 3 above); local gates per `chantier log` note at 960cdb8 (check, eval-dry-run 18 of 18); Review approved at d64a9961 in log, carried to 960cdb8 as clean rebase (log: committed 250aadb3 rebased, shipped with patch); Verified at 960cdb8 (log verdict event); CI green per log note at 960cdb8.

VERIFIED
