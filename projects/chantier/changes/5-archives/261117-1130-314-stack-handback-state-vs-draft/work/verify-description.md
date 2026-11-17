# Verify CR-314 description (posted PR 264 body)

Head: 8f2b9cf44d18de5a5d344860da36f5699c898e46

Command: `gh pr view 264 --json body -q .body` (read at the head above, PR base is the CR-313 branch, parent commit 9572ed5).

- Renders: sections Summary, Deliverables (table), Blast radius, Autonomous decisions, Known gaps, fold with Changes, Human decisions, Impacts, Test plan, Internal references; no image; no STALE mark. PASS.
- Changes match the diff: `git diff 9572ed5..HEAD --stat` lists README.md, run_scenario.py, concepts.md, driver.md, facts.py, test_stack_label.py; all six are in Changes, none unmentioned. `facts.py` diff shows `stack_label` used by `stack_lines`, reusing `pr_number` and `GITLAB_LINK`, labels `draft`, `out of draft`, `draft not read`, `!n` for GitLab, status alone with no PR: matches the table and Autonomous decisions. PASS.
- Sample rows: both appear in the scenario output recorded in verify.md section 1 (carried, patch unchanged). PASS.
- Test plan SHAs: `8f2b9cf` or carried with reason; Review carried from fd1fc5b is in the Driver's note ("r1 approval carried from fd1fc5b" at the 8f2b9cf rebase, `chantier log CR-314`). CI: `gh pr checks 264` shows 5 checks pass. Verified line matches verify.md (VERIFIED at this head). PASS.
- Known gaps "None": verify.md has no UNVERIFIED claim and no accepted failure. PASS.
- Role names: none outside Internal references/product terms. PASS.

VERIFIED
