# Verify CR-419

Head: b3fbfa3cf1501478046e4d86a6abe41f45f8ca91

Verdict: NOT VERIFIED

Move judged: rebase onto CR-418 (58df3be3) plus journal.read caller fixes (868761b, b3fbfa3). Earlier VERIFIED at eb5dbd6 does not carry.

## Claims

1. Whole suite at b3fbfa3: `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests -q -x -n0` -> `1493 passed, 20 skipped in 312.13s` (serial, so not comparable to `just test`). Tree clean (`git status --short` empty). PASS.
2. CI at b3fbfa3: `gh pr checks 394` -> check macos/ubuntu/windows pass, eval-dry-run pass, `just scenario (ubuntu-latest)` pass. PASS.
3. Review box (`Review: approved at b3fbfa3`/restack fixes approved): `chantier log 419` holds no note of an approved pass naming b3fbfa3 (or 868761b); the only approval note names eb5dbd6 (line 17). The foreman take note asks for "inspector" on the caller fixes, none logged. FAIL.
4. PR description speed table: PR says board state `0.80 s -> 0.90 s (+5 %)`; 0.90/0.80 is +12.5 %, over the spec's 10 % limit. `evidence/speed.md` figures are 0.851/0.876 -> 0.895/0.902 (+5 %), measured at the old base a391c1e, not 0.80. The PR figure matches no evidence and contradicts its own percentage; also not re-measured at the new base/head. FAIL.
5. Other description claims (Deliverables, Changes, Known gaps) match the diff stat (134 files, store, readers, structure test, CONTRIBUTING). Not separately failed. Carried from eb5dbd6 for the speed-neutral parts of claims 1-3 of the prior note (store conformance, structure test) now covered by claim 1's full run.
6. Long gate: CI scenario (ubuntu) green at head (claim 2); local Windows scenario is the stack top's, not this CR's.

Not done: speed not re-measured by me; before/after evidence not re-captured.

## Re-verification at b3fbfa3cf1501478046e4d86a6abe41f45f8ca91 (same head)

Verdict: VERIFIED

- Claim 3 fixed: `chantier log 419` line 30 note "approved: inspector APPROVE on the restack's caller fixes (3e22340d, rebased as 868761b; head b3fbfa3 ...)" names b3fbfa3 and 868761b; PR box matches. PASS.
- Claim 4 fixed: `gh pr view 394` body table shows board state 0.833 -> 0.891 s (+7 %: 0.891/0.833 = 1.070), status 0.585 -> 0.590 s; `evidence/speed.md` "Re-measured at the restacked head" section gives the same figures. Driver's measure, consistent, under 10 %; not re-run by me.
- Claims 1, 2 carried unchanged (head did not move): 1493 passed; CI 5 checks pass.
