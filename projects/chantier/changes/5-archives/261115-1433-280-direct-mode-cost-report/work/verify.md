Head: 315ff3618bf2bda64ac9eab10c3762c1bc5954fc

# Verify CR-280 at 315ff36

Scenario run: `just scenario --unit direct --verbose` in the worktree at 315ff36 (clean tree): `ok  direct (github): 60/60 checks, 84.9 s`. Transcript (untracked, gitignored): `scenario/results/scenario-20261115-151757-33604.md`; the relevant excerpts are copied to `verifier/evidence/direct-cost.txt`.

## Claims (all judged at 315ff36)

1. Whole-session line prices the whole session and names the batch part. Direct batch `cost` printed
   `Chief of Staff, whole session: $110.11 ($60.06 of it in the batch's spend), context 22,010 tokens; ...`.
   Adds up: 60.06 + 10.01 (steering outside budget) + 20.02 (grill) + 20.02 (before the batch) = 110.11; whole >= steering row ($30.03). Scenario check "the Chief of Staff's lines add up ... names the part in the batch's spend": pass. Parenthesis = headline spend ($60.06): pass.
2. `cost --by cr` on the direct batch: first line after the headline is `Chief of Staff, steering the batch, and its own subagents: $30.030 (3 calls)`, no `foreman:` line. Scenario check: pass.
3. Taken-over direct batch: `Chief of Staff, steering the batch, and the Foreman, with their own subagents: $40.040 (4 calls)`. Scenario check: pass.
4. Foreman mode unchanged. `pytest tests/test_cost_reading.py tests/test_cost_copilot.py -q` -> `8 passed`; they assert `foreman: $0.391 (30 calls)` (test_cost_reading.py:211) and `foreman: $1.000 (1 calls)` (test_cost_copilot.py:133), so a Foreman-mode `cost --by cr` still prints `foreman:`. Whole-session parenthesis left out there: the unchanged `$9.02` check passes.
5. Error wording: diff of command.py/sessions.py shows direct -> "no steering transcript recorded" / "the Chief of Staff runs", Foreman unchanged; `grep` finds no test asserting the old text for a direct batch (only scenario.py:2547, a Foreman batch, which passed in its unit run in CI).
6. Cards/docs: diff of chief-of-staff.md, status-layout.md, docs/costs.md, docs/use-cases-direct.md, scenario/README.md carries the new meaning as specified; agents/ untouched (`git diff --stat origin/main...HEAD`).
7. CI at 315ff36: `gh pr checks 230`: just check (ubuntu, macos, windows), eval-dry-run, just scenario (ubuntu-latest) all pass.
8. PR description (gh pr view 230): sections render, Summary/Deliverables/Changes match the diff (8 files). Observation: its Known gaps defers the captured outputs to this file, and the body quotes only the `cost` whole-session line, not the `cost --by cr` output; the Driver should paste the excerpts from `verifier/evidence/direct-cost.txt` into the body. Known gaps names the Windows budget warning. The Test plan "Verified at <sha7>" box is for the Driver to fill. Review box `approved at 9d4136c, committed as 315ff36` matches the Driver's log note "r1 approved at 9d4136c, committed as 315ff36". Not failed.

Not run by me: `just check` locally (CI shows it green on three OSes at this head).

VERIFIED

## Description pass at 315ff3618bf2bda64ac9eab10c3762c1bc5954fc
Command: `gh pr view 230 --json body` against `git diff --stat origin/main...HEAD` (8 files) and `verifier/evidence/direct-cost.txt`.
Output: body renders (sections, fold); Changes list the 8 files of the diff; the quoted `cost --by cr` block and the whole-session line match direct-cost.txt line for line ($60.060, $110.11 ($60.06 ...)); Known gaps names the Windows time-budget overrun; Review box 9d4136c/315ff36 matches the log note; no STALE or UNVERIFIED mark. The role names (Chief of Staff, Foreman) are product terms of a cost change. VERIFIED.

## Description pass, second run, at 315ff3618bf2bda64ac9eab10c3762c1bc5954fc
Command: `gh pr view 230 --json body,headRefOid` (head 315ff3618bf2bda64ac9eab10c3762c1bc5954fc); `git diff origin/main --stat` (8 files); `cat verifier/evidence/direct-cost.txt`; `chantier log CR-280`.
Output: Changes lists the 8 files of the diff; the quoted `cost --by cr` block is identical to the direct-cost.txt block (60.060, 30.030, 10.01, 20.02, 110.11 ($60.06 ...)); Known gaps names the Windows overrun; Review box 9d4136c/315ff36 matches the log note "r1 approved at 9d4136c, committed as 315ff36"; no STALE/UNVERIFIED mark; sections and fold are well formed. Role names are product terms of a cost/cards change. Observation: the first Deliverables line ($13.16 ($11.52 ...)) is the specification's example from an earlier real run, not captured at this head; the captured block below it is the proof. Not failed.
VERIFIED
