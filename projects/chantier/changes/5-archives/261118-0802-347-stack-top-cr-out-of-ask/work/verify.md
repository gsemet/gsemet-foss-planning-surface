# Verify CR-347

Head: a99c1b572c34efc5ad72a75f55f6cdd3209aaf21

Claims judged at ea0ecdac:

1. to_come unit cases pass at head. `pytest tests/test_stack_due.py -q -k to_come` (cli dir): `5 passed, 13 deselected`.
2. Same test file fails on base (origin/main, detached worktree, removed after): `ImportError: cannot import name 'to_come' from 'chantier.stacks'` / `1 error during collection`.
3. Scenario: `just scenario --unit stack --forge github` at head: `ok  stack (github): 177/177 checks, 329.2 s`; transcript scenario/results/scenario-20261118-083013-8844.md holds `[x] a working CR with a PR on its place that the stack driver has not placed is under `to come:`, working, and no `check 2` line names its PR`, the 13-bis section is present, no unchecked `[ ]` line (count 0).
4. Code: `git diff origin/main..HEAD` shows `to_come` in stacks.py (docstring as specified), `_plan` breaking on `to_come`, docstring updated, `_no_bottom` refusal `no PR placed at the bottom of the stack: {id} is working and the stack driver has not placed its PR {pr} yet` with EXIT_PRECONDITION.
5. Cards: concepts.md ("Stack as it stands" parenthesis and "To come"), foreman.md (to-come gloss only), driver.md (five checks parenthesis), scenario/README.md paragraph: all match the spec in the diff.

Not checked: PR description on the forge, `just check`/eval-dry-run (CI green per brief).

VERIFIED

## PR description pass (judged at ea0ecdac776a23f319b06047e5901c09189a6d01)

Command: `gh pr view 314 -R gsemet/chantier --json body -q .body`, against `git diff origin/main` (8 files) and pr-template.md audit.

6. Sections and order: Summary, Deliverables, Blast radius (grade 1), Autonomous decisions, Known gaps visible; one `<details><summary>Details</summary>` fold with blank lines, holding Changes, Human decisions, Impacts, Test plan, Internal references last, nothing after `</details>`. No Issues References (no issue line). No images.
7. Consistency with diff: `to_come` sketch equals stacks.py; `_plan` and `_no_bottom` refusal text match forge_stack.py; three cards, one 5-case parametrized test, one scenario check and README paragraph all match the diff; nothing delivered is unmentioned.
8. Internal references: CR name only in the last section; "stack driver" is a product term of the changed cards, defined on first use.
9. SHAs: Test plan cites `ea0ecda`; Review `ef9f979` matches `$CHANTIER log` note "r1 approved at ef9f9779, committed as ea0ecdac".
10. Known gaps: one bullet for the unscreened refusal text, matching the Autonomous decisions line.

VERIFIED

## Restack pass (judged at a99c1b572c34efc5ad72a75f55f6cdd3209aaf21)

Move: rebase onto CR-346 head 76a19a4. `git diff --name-only ef9f9779 76a19a4` brought run_scenario.py, chief-of-staff.md, driver.md, foreman.md, delivery.py, test_carry_ship.py. `git diff --stat 76a19a4 HEAD`: the same 8 files as before (README, run_scenario.py, concepts.md, driver.md, foreman.md, forge_stack.py, stacks.py, test_stack_due.py), 61 insertions, 12 deletions; stacks.py, forge_stack.py and the card hunks (to_come, `_plan`, `_no_bottom` refusal, concepts/driver/foreman text) unchanged in content.

1 (rejudged at a99c1b5). `pytest tests/test_stack_due.py -q` (cli dir): `18 passed in 0.22s` (includes the 5 to_come cases).
2 carried from ea0ecda: base-failure proof (ImportError on origin/main) concerns the base without the CR; the move does not touch it.
3 (rejudged at a99c1b5, base touched run_scenario.py). `just scenario --unit stack --forge github`: `ok  stack (github): 177/177 checks, 303.3 s`; transcript scenario/results/scenario-20261118-084504-38796.md: 177 `- [x]` check lines, 0 `- [ ]` check lines, line 6734 `- [x] a working CR with a PR on its place that the stack driver has not placed is under \`to come:\`, working, and no \`check 2\` line names its PR`.
4 (rejudged at a99c1b5). `git diff 76a19a4 HEAD -- skills/chantier/scripts/cli/src`: `to_come` in stacks.py, `_plan` using `to_come`, docstring updated, `_no_bottom` refusal `no PR placed at the bottom of the stack: {id} is working and the stack driver has not placed its PR {pr} yet` with EXIT_PRECONDITION: same as at ea0ecda.
5 (rejudged at a99c1b5). `git diff 76a19a4 HEAD -- skills/chantier/references`: concepts.md, driver.md, foreman.md hunks as specified (to-come gloss only in foreman).

PR description (6-10): not re-judged in this pass; carried from ea0ecda for content (patch content unchanged). Note for the Driver: the posted body's Test plan lines still cite `ea0ecda` (`gh pr view 314 ... | grep`: lines 58-62); update them to `a99c1b5` or `carried from ea0ecda` and re-run local gates at a99c1b5.

VERIFIED
