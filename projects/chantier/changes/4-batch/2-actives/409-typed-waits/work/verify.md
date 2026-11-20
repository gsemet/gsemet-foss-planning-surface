Head: edce7ce6c04ebd79f52ea418a56451a7148902db

# Verify CR-409 typed waits, at edce7ce (full SHA above)

NOT VERIFIED

## Claims judged at edce7ce

1. Behaviour of the new commands, hub provider, journal type, board fields, validate (spec 4 to 7, 11.1).
   Command: `uv run --no-sync --project . pytest tests/test_waits.py tests/test_board_waits.py tests/test_forge_hub_waits.py tests/test_validate.py tests/test_startup_manifest.py tests/test_store_command_table.py tests/test_event_types.py tests/test_scenario_coverage.py -q -p no:cacheprovider` (in the worktree)
   Output: `170 passed in 27.77s`. PASS (these are the tests; the claims they exercise are as named in the spec 11.1 list; `test_startup_manifest.py` keeps the 45,000-byte driver cap).
2. Driver card pointer on the common path and the off-path text (spec 9): `git diff main...HEAD -- skills/chantier/references/driver.md` shows the one-line pointer "A wait of a known type: `--wait`, see ..." and the Means text. PASS.
3. AGENTS.md exception sentence (spec 8.1): FAIL. `git diff main...HEAD -- AGENTS.md` changes "Two named exceptions." to "Three named exceptions."; the same sentence then names First (batch end), Second (surface server), the `lease` item ("One more exception ...") and `wait` ("And one more"): four items. Spec 8.1: the count becomes the number of items the text names once `wait` is in, recounted at the rebased head.
4. Review box (`Review: approved at 40363bd (rounds 1-2) and f184ed0 (round 3)`): FAIL for round 3. `$CHANTIER log CR-409` has "r2 inspector approved at 40363bd" and "r2 approved at 40363bd, committed as f184ed02" (round 2); round 3 (the scenario case, `driver round round=3`) has no approval note at all, so f184ed0 is not the reviewed head of round 3. Also `git merge-base --is-ancestor 40363bd HEAD` and `... f184ed0 HEAD` both print "not an ancestor": both SHAs left the history by the rebase, and `ship` itself flagged `pr-body.md line 81 names 40363bd, not in edce7ce's history`. No carried-from note with a patch-id proof exists in the log.
5. Long gate at edce7ce: not proved. `gh pr checks 380`: `just scenario (ubuntu-latest)  pending`, `just check (windows-latest)  pending`; `just check (ubuntu-latest)`, `just check (macos-latest)` and `just eval-dry-run (ubuntu-latest)` pass. No `chantier gate` pass at this head (`ship` off: "no long gate passed at edce7ce"). The CR changes the CLI, so the long gate is owed before the PR is ready.
6. PR description: renders, and Summary, Deliverables and Changes match the diff (file list of `git diff --stat main...HEAD` vs the Changes section). Its Known gaps hold the GitLab approval gap (accepted by the brief). The Test plan Review line is out of format per claim 4. FAIL on that line only.
7. Matrix cells GitLab approval proof (spec 5.3, 11.4): not shipped, known and accepted; the unproved behaviour (`unproved`, no interest) is in the diff of `connectors/gitlab.py` and `hub/waits.py` and tested by test_forge_hub_waits.

## Evidence

before/after: no visual change; the after is claim 1's command output at edce7ce. No screenshots, none owed (no pane change).

## Verdict

NOT VERIFIED: claims 3, 4, 5 (pending), 6.
