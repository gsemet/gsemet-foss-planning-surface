# Verify CR-353

Head: 9433f8377cf3ca62d1eb5b3c17347243751e42ab

All claims judged at 9433f8377cf3ca62d1eb5b3c17347243751e42ab (worktree clean, pushed head).

1. In-process switch test (Evidence 1) - VERIFIED
   Command: `uv run --locked python -m pytest skills/chantier/scripts/cli/tests/test_rail_refusals.py skills/chantier/scripts/cli/tests/test_costs.py -q -k "direct or steer or window or claim"`
   Output: `21 passed, 22 deselected in 2.82s`. The parametrized test
   `test_the_chief_of_staff_claiming_a_foreman_batch_makes_it_direct` (claude, copilot, no-transcript cells) asserts steering direct,
   the `steering` event, the steering line, status first line, exit 3 on epoch 1, the take skeleton "Steering: the Chief of Staff", and no flip without a transcript.
   Note: it lives in test_rail_refusals.py rather than test_cli_runs.py (declared in the PR's Autonomous decisions); accepted.

2. Scenario direct unit (Evidence 2) - VERIFIED
   Command: `uv run --locked python scenario/run_scenario.py --unit direct`
   Output: `ok  direct (github): 75/75 checks, 81.5 s`.

3. Cost windows unit test (Evidence 3) - VERIFIED
   Same pytest run as claim 1 includes `test_a_steering_transcript_that_claims_again_is_priced_over_each_of_its_windows`
   (repeated claims return each window; one claim per transcript as before). Passed.

4. Card greps (Evidence 4) - VERIFIED
   `rg -n -c` of "never becomes direct", "never switches to direct mode", "never switches back to direct mode", "A Foreman batch does not switch" over skills docs agents com.github.copilot README.md: no match for any.
   `rg -U -n "A Foreman batch does not switch\s+to\s+direct" .`: no match (rc=1).
   `rg -n "Switching to direct mode" skills/chantier/references/chief-of-staff.md`: line 1569 "- **Switching to direct mode.** In order:" (plus entry row line 27, rule line 778).
   concepts.md line 343-347 "Steering session" names both flips (".. Chief of Staff transcript makes a Foreman batch direct").
   routing.md lines 11-12 name `switch to direct mode` and `switched to direct mode <batch>: stopped <cr>...|none`.
   hosts/claude-code.md line 38 names `mcp__ccd_session_mgmt__stop_session`; line 623 the Offering options row; chief-of-staff.md line 1413 the same row.

5. CI at the head - VERIFIED
   `gh pr checks 318`: just check (macos, ubuntu, windows) pass; just eval-dry-run (ubuntu) pass; just scenario (ubuntu-latest) pass (3m46s). PR is draft (as the spec asks). Windows local `chantier gate` is not mine.

6. Matrix - carried from work/verifier/matrix-r2.md (Head 9433f83..., all cells hold); no move since (same head).

7. PR description (as posted, `gh pr view 318 --json body`) - VERIFIED
   Identical to work/pr-body.md. Renders (sections, fold, no images). Summary/Deliverables/Changes match the diff of 18 files (`git diff --stat origin/main...HEAD`): seat.py, rails.py, costs and cost modules, tests, scenario, cards and docs listed; agents/ untouched as the spec says. No role name outside Internal references; no username/home path. Known gaps names the unproved real switch and the unchanged chief_outside (inbox change cost-receipt-after-switch exists). Review box: `chantier log CR-353` has "r2 approved at 855b320f, committed as 9433f83", matches `Review: approved at 9433f83`. Unchecked boxes (Verified, CI green) are for after this pass; local gate numbers (578 passed, 17 of 17) are the Driver's gate claims and CI at the head is green for the same gates. No STALE mark.
