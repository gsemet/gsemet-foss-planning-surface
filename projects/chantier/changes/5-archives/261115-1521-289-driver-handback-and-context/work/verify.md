# Verify CR-289

Head: c1149ee588660c26d9ed1c4647fa8c8e37818d4b

All claims judged at c1149ee588660c26d9ed1c4647fa8c8e37818d4b.

1. Reader tests. `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_cost_reading.py -q` (in the worktree) -> `10 passed in 5.44s`; the 6 cases of the spec table (handed back, mid-call, resumed, large, missing, no tool call) are in the parametrized test.
2. Diff stat `git diff --stat origin/main..HEAD` (base f257647 = origin/main): run_scenario.py, driver.md, foreman.md, hosts/claude-code.md, batch_status.py, costs/sessions.py, test_cost_reading.py. Only the allowed files.
3. Greps (`git grep -n`): `ended, no hand-back recorded` batch_status.py:155 (foreman.md carries the flag wording as `ended, no hand-back recorded` in the spec's bullet; card edit present, diff 35 lines); `waiting on its own background work` foreman.md:545-547 and hosts/claude-code.md:565; `record your hand-back` foreman.md:597 and hosts/claude-code.md:563; `while waiting for <what>` driver.md:135; `a new short .verifier. start` driver.md:559; `130,000` driver.md:120,123,124,867; `Never call the host's hand-back` under skills/ once (driver.md:416); `context: <where it stopped` kept in driver.md and checked by scenario line 3580.
4. Scenario steps 1-5 present in `driver_liveness` (diff of scenario/run_scenario.py). Long gate: `gh pr view 239` at head c1149ee: just scenario (ubuntu-latest) SUCCESS, just check x3 SUCCESS, eval-dry-run SUCCESS.
5. Measure, repeated on the Foreman session's subagents (transcripts still present): peak prompts via usage sums, 0 compactions: a6a4eb93596c562ba 99,239; ac3061ac821af857f 116,972; afa8f5839de908336 119,401; a2c1f342e038708e6 38,554; ae6e32e6270cf2ba5 29,033. Matches the spec's tables (99,239 / 116,972 / 119,401). Eval peaks (123,512, 97,774) not repeated: carried from the spec.
6. Review box: `chantier log CR-289`: "r1 inspector approved at 842b800...", "r1 approved at 842b800, committed as 5b20e68, rebased onto origin/main as c1149ee..." consistent for a box citing 842b800 or c1149ee (carried).
7. PR description (gh pr view 239): Summary, Deliverables, Changes match the diff; Known gaps names the two unseen behaviours and the format risk. Note: the Test plan boxes still hold `<sha7>` placeholders and are unticked (the Driver fills them after this verdict); not judged a failure.

VERIFIED

## Description pass at c1149ee588660c26d9ed1c4647fa8c8e37818d4b
- Command: `gh pr view 239 --json body,headRefOid` and `git diff --stat origin/main...HEAD`: body matches the 7 changed files (sessions.py, batch_status.py, 3 cards, test, scenario); sections render; no role name outside Internal references; Known gaps present.
- Review box: `chantier log CR-289` shows "approved at 842b800, committed as 5b20e68, rebased onto origin/main as c1149ee".

VERIFIED

## Description pass (c1149ee588660c26d9ed1c4647fa8c8e37818d4b)
Posted body (gh pr view 239) audited against diff stat of 7 files and pr-template audit: sections in order, fold ok, Known gaps filled, no issue line so no Issues References, no grill decision so no Human decisions, role names are product terms (cards changed), SHAs c1149ee/842b800 match log notes. VERIFIED.
