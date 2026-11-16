# Verify CR-244

Head: 5233d07a70df75685659363c9ee6456612743e50

Verdict: NOT VERIFIED (the PR description, not the code; see Failed claims).

## Failed claims (at 5233d07)
1. Description Summary, "This PR carries the two commits of the 'a merge may come at any moment' change ... they drop at restack." At 5233d07 `git log --oneline -3` shows 5233d07 directly over 9bd0412 (CR-234): one commit, so the sentence contradicts the diff. Same for Internal references ("carries CR-233's two commits ...").
2. Description Test plan boxes name no SHA that exists: "Local gates at the pre-restack head", "Review: approved at the pre-restack head (... committed as the pre-restack head)", "[ ] Verified at `403887f`", "[ ] CI green at `403887f`". `gh pr view 180 --json headRefOid` gives 5233d07a70df75685659363c9ee6456612743e50, so the body (read from the forge) was not updated for this head. 403887f is no longer in the branch.
3. Review box: `chantier log CR-244 --batch batch-17` (complete) ends with the 403887f `ship` entries, the NOT VERIFIED verdict at 403887f and the waiver note. It holds no note of an approved pass or a carried review for 5233d07, so the Review box has no proving note at this head.
4. CI at 5233d07 was not green when read: `gh pr view 180 --json statusCheckRollup` gives `just check (ubuntu-latest)` SUCCESS; macos, windows, `just scenario`, `eval-dry-run` IN_PROGRESS. The waiver makes green GitHub CI the replacement for the long gate, so it is not yet shown.

## Judged at 5233d07
- Patch intent kept: for delivery.py, forge_stack.py, scenario/run_scenario.py and scenario/README.md, the added/removed lines of `git diff 21f5677 403887f -- <file>` and of `git diff 9bd0412 5233d07 -- <file>` are identical (PowerShell comparison of the +/- lines: `patch-same: True` for the four files). The conflicts were only in the cards.
- `just check` run in the worktree at 5233d07 (HOME, USERPROFILE, CLAUDE_CONFIG_DIR at scratch folders): ruff clean, mypy "Success: no issues found in 86 source files", `uv lock --check` ok, "63 passed in 17.34s", release-notes ok, exit 0.
- Reading pass: Grep `all ready or blocked|every PR is ready|every open PR of the batch's stack` in skills/chantier/references: no matches. `deliver by`: chief-of-staff.md 1, foreman.md 2, driver.md 1. `partial stack mergeable below|stack complete, mergeable|no stack yet`: status-layout.md 2, foreman.md 1, chief-of-staff.md 3.
- Description Deliverables, Changes and Known gaps match the diff `git diff --stat 9bd0412 5233d07` (9 files: delivery.py, forge_stack.py, five cards, scenario run_scenario.py and README.md). The Known gaps (README.md, docs; no screenshot) are right.

## Not proven at this head (specification Evidence 1-7, scenario 13a)
No gate pass at 5233d07 (the latest gate log, 20261114-095944.log, is at 6348448; the user waived the long gate for batch-17). The CR's CLI patch is the same, but the base moved: `git diff --name-only 9bd0412 3fb9129` shows CR-234 changed `forge_stack.py`... (via 9bd0412) and `scenario/run_scenario.py`/`fake_gh.py` under the proof, so the 6348448 pass does not carry (it ran on another base). I ran no scenario. This does not alone change the verdict; scenario CI on GitHub (`just scenario`, in progress) is the stand-in under the waiver.

## Evidence
No visible change; no before/after pairs captured (not needed: no UI). No screenshot due (board pane unchanged).

To get VERIFIED: update the PR description on the forge (drop the "two commits" sentences, name 5233d07 in the gates, Review and Verified/CI boxes, record a review note for 5233d07 in the log), and show CI green at 5233d07.
