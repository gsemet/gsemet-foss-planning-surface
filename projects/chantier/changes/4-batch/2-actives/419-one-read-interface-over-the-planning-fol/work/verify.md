# Verify CR-419

Head: eb5dbd66a823fca7335769e175b954d420cc98d0

Verdict: NOT VERIFIED

## Claims

1. Store conformance, structure test and code-targets pass (eb5dbd6): `pytest test_store_conformance.py test_store_reads.py test_code_targets.py -q` -> `50 passed, 18 skipped in 2.41s`. PASS.
2. Whole suite (eb5dbd6): `just test` -> `1447 passed, 20 skipped in 72.62s`. No expected output changed (existing tests only call-updated per diff stat). PASS.
3. Docs (eb5dbd6): `git diff <base>..HEAD -- CONTRIBUTING.md` adds the one sentence naming `tests/test_store_reads.py` and `Repo.store`. PASS.
4. Speed (spec 6, answer 13): evidence/speed.md and PR table: status 0.568 -> 0.563 s, board state 0.80 -> 0.90 s (+5 %, under 10 %). Not re-measured by me (carried from the Driver's evidence, not proof). PASS as stated, unproved by me.
5. `just test` time added: spec section 6 requires the PR to state the time `just test` adds. PR description does not state it; my run took 72.6 s here (budget 18.5 s + 30 s). FAIL.
6. Review box `Review: approved at eb5dbd6`: `chantier log 419` holds only `driver note note=round 2 inspector APPROVE (head a391c1eb + working tree)`, no note naming eb5dbd6 or "committed as eb5dbd66". The SHA the box cites has no approved-pass note. FAIL.
7. PR description: renders, Summary/Deliverables/Changes match the diff (78 files; store reads, readers, structure test, CONTRIBUTING). The `reading()` per-pass link-check scope is disclosed under Autonomous decisions and Known gaps. Test-plan line says `just test` ran at eb5dbd6, but the log's note at that head names only `just check` and `eval-dry-run`. Bound by claim 5 and 6.
8. Gates: no long-gate pass at eb5dbd6 (ship `off=` says so); CI (incl. `just scenario (ubuntu-latest)`) was pending at my check. Not a pass yet.

## Not done
Evidence before/after pairs not re-captured; the Driver's speed.md is the only measure.

## Re-verification at eb5dbd66a823fca7335769e175b954d420cc98d0 (same head)

Verdict: VERIFIED

- Claim 6 fixed: `chantier log 419` note "review approved at eb5dbd6 ... committed as 23734dbb ... docstring only" names eb5dbd6. PASS.
- Claim 5 fixed: PR body line 76 states `just test` 72.5 s at base a391c1e vs 72.6 s at head (my own run: 72.62 s). PASS.
- Claim 7 fixed: test-plan line now cites `just check` (its suite) and `eval-dry-run`, matching the log. PASS.
- CI at head: `gh pr checks 394`: check macos/ubuntu/windows pass, eval-dry-run pass; scenario (ubuntu) pending, listed in the PR's Known gaps as UNVERIFIED. Claims 1-4 carried unchanged (head did not move).
