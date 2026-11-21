# Verify CR-449

Head: 6774cd718f9b6b0f895dbce907838346176ff177

All claims judged at 6774cd71 (worktree clean, `git rev-parse HEAD` equals the PR head `headRefOid`).

1. Diff scope. `git diff --stat origin/main...HEAD`: one file, `.agents/guidelines/change-requests-lifecycle.guidelines.md`, 40 insertions. OK.
2. Placement. `grep -n` of the headings: "Project rules" section line 91, **Pull request** line 103, **Early heavy CI** line 108, **CI** line 148. OK.
3. Content, read in the diff: command `gh workflow run ci.yml --ref <branch> -f heavy=true`; paths `test/visual/`, `test/integration/`, `test/shared/stressPlan.ts`; words draft, provisional, round 1, fast gate; override sentence; stack sentence; cap sentence; headSha check; re-dispatch rule. All present. OK.
4. Parallel section unchanged: the only diff hunk is at lines 105-146 (one mention of the section name in the new bullet, line 127); the section is at line 178, untouched. OK.
5. Decisions, quoted from the bullet:
   - hc-Q1: file is the process guideline; only that file changed (claim 1).
   - hc-Q2: "The rule applies when the round 1 diff touches `test/visual/`, `test/integration/` or the stress list ... Other change requests keep the current steps."
   - hc-Q3: "dispatches the same command once after round 1, then once after each round that fixes a red `integration` or `stress` job ... It never dispatches when the last heavy run is green. Rule 13 ... that run is the last green heavy run when the head has not changed since it ran."
   - hc-Q4: "Its own Driver pushes and opens the draft pull request against the base that `take` printed. The stack driver only restacks later".
   - hc-Q5: "after round 1, whatever the round's review verdict ... checkpoint commit ... fast gate ... Push the branch without the long gate" and "This overrides the chantier Driver card's 'gate before the first push'". driver.md line 519 holds the overridden sentence.
   - hc-Q6: "the early draft counts in the user's cap ... At the cap, the Driver pushes the branch and dispatches the heavy run without opening the pull request."
   - Fix 5: the bullet's reason sentence matches origin/main's preflight text ("runs only the static stage"); gate log shows "visual, viewer-graph, integration, report and gallery stages skipped on Windows".
   - Fix 6: "Check that its `headSha` is the head that was pushed ... it never proves a later head green ... read the run before **Verify**."
6. `uv run --no-sync --group docs --group release --group requirements pytest test/build/test_guideline_isolation.py -q`: `9 passed in 0.16s`. OK.
7. Gate log work/gates/20261121-110106.log, first line `gate CR-449 branch ... head 6774cd718f9b6b0f895dbce907838346176ff177`, last line `result: pass at 6774cd718f9b6b0f895dbce907838346176ff177` (ci-static passed). OK.
8. `grep -n "heavy:" .github/workflows/ci.yml`: line 9 `heavy:`, `type: boolean`, default false, under `workflow_dispatch` inputs. OK.
9. PR description (`gh pr view 457`): draft, base main, head 6774cd71. Sections of the template present, renders as plain markdown plus a text block; no images, no internal IDs or planning links; role term "Driver" is the product term of the change. Summary, Deliverables and Changes match the diff (one bullet; override sentence; stack, cap, reading the run, re-dispatch all in the diff). Impacts: "No visible change: process documentation only". Changelog "No user-facing change". No Known gaps needed (no UNVERIFIED claim). OK.
10. "No visible change" evidence line: the diff is Markdown only, no `src/`, UI or test file (claim 1), so no before/after capture exists to take. OK.

VERIFIED
