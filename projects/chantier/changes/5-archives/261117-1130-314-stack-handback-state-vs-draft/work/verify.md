# Verify CR-314

Head: 8f2b9cf44d18de5a5d344860da36f5699c898e46

Second verification, after the move e385e30..8f2b9cf (clean rebase, old base 0412345 -> new base 9572ed5). Worktree clean (`git status --short` empty). CI green at this head per the prompt (5 checks); no gate pass run by me.

## 0. The move left the patch unchanged (PASS, at 8f2b9cf)
Command: `git range-diff 0412345 e385e30 9572ed5 8f2b9cf`
Output:
```
1:  ab9b0b5 = 1:  ab9b0b5 chore: format-check scripts ...
2:  e385e30 < -:  ------- feat(stack): show a CR's hand-back state ...
3:  9572ed5 = 2:  9572ed5 fix(forge-stack): ...
4:  8f2b9cf = 3:  8f2b9cf feat(stack): show a CR's hand-back state ...
```
The CR's commit is `=` (identical patch). Base change touched `forge_stack.py`, `forge_stack_gh.py`, justfile, scenario files, driver.md, chief-of-staff.md (`git diff --name-only 0412345 9572ed5`), but not `facts.py` (empty output of `git diff 0412345 9572ed5 --name-only -- .../commands/facts.py`). Scenario re-run below because the base touched scenario files and the stack commands.

## 1. Stack row labels from the CLI (PASS, at 8f2b9cf)
Command: `just scenario --unit stack --unit gitlab` (exit 0)
Output: `ok gitlab (gitlab): 33/33 checks, 45.3 s`, `ok stack (github): 144/144 checks, 327.4 s`.
Rows grepped from `scenario/results/20261117-115532-24480` (`grep -rhoE "CR-[0-9]+ (ready|working|queued|blocked)(, PR [a-z ]+ \([#!][0-9]+\))? worktree" ... | sort | uniq -c`), among them:
- `CR-106 ready, PR draft (#45) worktree` (1)
- `CR-106 working, PR out of draft (#45) worktree` (2)
- `CR-101 ready, PR out of draft (#40) worktree`
- `CR-101 ready, PR draft not read (!201) worktree` (GitLab `!n`)
- `CR-105 ready, PR draft not read (#201) worktree`
- `CR-106 ready worktree`, `CR-103 queued worktree` (no PR)

## 2. PR body sample rows (PASS, at 8f2b9cf)
The body's two sample rows, `ready, PR draft (#45)` and `working, PR out of draft (#45)`, both appear in the scenario output above (CR-106). The failure of e385e30 (`working, PR draft (#45)`, not a real row) is gone.
`gh pr view 264 --repo gsemet/chantier --json body` equals `work/pr-body.md` (`diff` differs only by one trailing newline); `headRefOid` = 8f2b9cf44d18de5a5d344860da36f5699c898e46. Sections present, Known gaps "None" (no UNVERIFIED claim, no failed accepted claim), no STALE mark. Body's Deliverables and Changes match the diff (`git diff --stat 9572ed5 HEAD`: README, run_scenario.py, concepts.md, driver.md, facts.py, test_stack_label.py). Body's SHAs: `8f2b9cf` (head) and the base `9572ed5`; "Test plan" scenario line "carried from fd1fc5b (clean rebases)" is superseded by section 1 here at the head. Review box: carried from e385e30: the patch is unchanged (section 0); the Driver's note for 8f2b9cf is the Driver's to hold.
The body's "before at the base 9572ed5 these rows read the derived words": carried from e385e30: `facts.py` unchanged by the base move (above), so the before behaviour is the same code.

## 3. Card diffs (PASS)
carried from e385e30: the commit's patch is identical (section 0; range-diff `=`).

## 4. just check and the label test (PASS)
carried from e385e30: the patch is identical; the base brought no change to `facts.py` or `test_stack_label.py`; CI (including `just check` jobs) green at 8f2b9cf per the prompt.

## 5. Main checkout untouched (PASS)
carried from e385e30: nothing in this pass touches the main checkout.

## Verdict
VERIFIED
