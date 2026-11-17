# Split `src/page/modules/commentThreads.ts` (787 of 800 lines)

Type: refactor · Priority: P3 · Filed 2026-11-01 from CR 224 reviews (round 1 nit 5, round 3)

## Today

`src/page/modules/commentThreads.ts` is 787 lines, 13 under the 800-line `check-limits` cap. The
next feature in that file will break the gate.

## Expected

Split by responsibility (for example the thread view, the chips visibility and the host messages) into
sibling modules. No behaviour change.

Proof: `just check` passes; the existing `commentThreads` tests pass unchanged; the file is well under
the cap.
