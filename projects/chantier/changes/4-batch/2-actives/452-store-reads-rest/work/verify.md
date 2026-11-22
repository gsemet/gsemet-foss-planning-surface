# Verify CR-452

Head: d7154f8397f022a56f4f3299ace5facaedec1252

Gate pass cited: `work/gates/20261122-055156.log`, first line `gate CR-452 branch chantier/batch-30/cr-452-the-last-readers-onto-the-store-run-time head d7154f8397f022a56f4f3299ace5facaedec1252`, last line `result: pass at d7154f8397f022a56f4f3299ace5facaedec1252`.

Second pass at the same head (no move). Claims 1 to 5 carried from d7154f8 (first pass, same head; nothing moved). Re-checked now: `git rev-parse HEAD` = d7154f8397f022a56f4f3299ace5facaedec1252, `git status --short` empty, `gh pr checks 424`: just check macos/ubuntu/windows, eval-dry-run, scenario (ubuntu) all pass.

## Claims

1. Pushed head is the verified head. d7154f8: re-run, as above. VERIFIED.
2. Structure test and run-time proof pass. carried from d7154f8 (same head): `pytest test_store_reads.py test_store_runtime.py test_gate_queue_order.py test_leases.py -q` -> `56 passed in 12.50s`. VERIFIED.
3. Moved modules listed in `tests/test_store_reads.py`. carried from d7154f8 (same head). VERIFIED.
4. CI at d7154f8: pass on all five jobs (re-run `gh pr checks 424`, above); local long gate pass (log above). The macOS fix is proved only by the CI pass; the body now says its cause was not reproduced. VERIFIED.
5. Docs: CONTRIBUTING.md sentences. carried from d7154f8 (same head). VERIFIED.
6. Speed (spec 7). Not re-measured (not cheap: no prepared 200+ CR folder kept, per-run times were not kept). The body now marks the speed line UNVERIFIED in the Test plan and has a Known gaps bullet: that narrowing is honest and is accepted. VERIFIED as a narrowed claim, EXCEPT one clause, see claim 7.
7. PR description consistency and proof. Renders; Summary, Deliverables, Changes match the diff (carried from d7154f8); Known gaps names the 20 modules / 60 calls, the speed UNVERIFIED and the macOS cause. NOT VERIFIED: the Known gaps bullet says "The head is measurably slower (13 of 14 pairs), within the rule." That is stated as fact with no proof: the per-run times were not kept (the bullet itself says so), and `grep "13 of 14"` over the CR folder finds it only in `work/pr-body.md`. Fix: delete that sentence, or mark it part of the UNVERIFIED claim (for example "the Driver's note says 13 of 14 pairs were slower; UNVERIFIED").

## Third pass (description only), head d7154f8397f022a56f4f3299ace5facaedec1252

8. Claim 7 re-judged at d7154f8. Command: `grep -rn "13 of 14\|measurably slower" <CR folder>` (excluding this file) -> no output: the sentence is deleted from `work/pr-body.md`. Known gaps now holds the 20 modules / 60 calls, the speed UNVERIFIED, the macOS cause, the unobserved push loop/watch, the docs search; no unproved fact remains. Other claims carried from d7154f8 (same head, nothing moved). `git rev-parse HEAD` = d7154f8397f022a56f4f3299ace5facaedec1252, `git status --short` empty. VERIFIED.

Verdict: VERIFIED (claims 7 and 8 now pass; all others carried at d7154f8).

## Fourth pass (posted description only), head d7154f8397f022a56f4f3299ace5facaedec1252

9. Posted body read with `gh pr view 424 --repo gsemet/chantier --json body -q .body`, judged against pr-template.md's audit at d7154f8. Sections, order, fold (blank lines, nothing after `</details>`), Blast radius one grade, SHAs on proofs, UNVERIFIED speed claim with its Known gaps bullet, Review box vs the note "r2 approved at e4171908... committed as 9d3ff72e", and Changes vs `git diff --stat origin/main...HEAD` (30 files, listed modules match): all pass. FAIL: Known gaps bullet 2 says "no verifier re-measured it": a role name as the doer of the work outside Internal references (pr-template, "The rules", internal references bullet; the product-term exception does not apply, the PR changes no role). Fix: say "the speed was not re-measured". NOT VERIFIED.

Verdict: NOT VERIFIED (claim 9).

## Fifth pass (posted description only), head d7154f8397f022a56f4f3299ace5facaedec1252

10. Posted body re-read (`gh pr view 424 --repo gsemet/chantier --json body -q .body`) at d7154f8. The role name is gone; sections, fold, Changes vs diff (30 files), SHAs, UNVERIFIED speed with its Known gaps bullet: pass. Review box vs note "r3 approved at 9d3ff72... committed as d7154f83": matches. FAIL: Test plan item "Review: approved at 9d3ff72 (the last round's change, committed as d7154f8)" uses "round", an internal process term, outside Internal references (pr-template audit 3 lists "round"). Fix: "(the last change, committed as d7154f8)". NOT VERIFIED.

Verdict: NOT VERIFIED (claim 10).

## Sixth pass (posted description only), head d7154f8397f022a56f4f3299ace5facaedec1252

11. Posted body re-read at d7154f8; "round" and role names gone; fold, SHAs, Review box (note "r3 approved at 9d3ff72... committed as d7154f83"), CI (`gh pr checks 424`: 5 pass), UNVERIFIED speed bullet: pass. FAIL (diff consistency): Deliverables table lists `rails.py` under "Modules moved onto the store", but `git diff --stat main...HEAD | grep -c rails` -> 0: rails.py is not changed (only listed in tests/test_store_reads.py with an exempt entry). Fix: drop it from the moved list, say it is checked and exempt. FAIL (minor, unmentioned delivered change): tests `test_gate_queue_order.py`, `test_leases.py`, `test_outside_poller.py` change in the diff and Changes names none. Minor wording: Known gaps says "as the specification asks" and "the 10 % rule" (internal rule, undefined to an outside reader). NOT VERIFIED.

Verdict: NOT VERIFIED (claim 11).
