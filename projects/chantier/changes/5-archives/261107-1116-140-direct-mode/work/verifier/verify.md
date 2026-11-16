# verify.md - CR-140

Head: f83b3ab4c97415f8f1f74dda01409d9718317564 (pushed). Verdict: VERIFIED (see evidence/before-after.md).

Claims proven by command and output (files in evidence/):
1. preflight --direct passes P1 on any Claude Code entry point and omits P2 - after-1-open-claim.txt.
2. open --direct records steering direct; shown in status line 1, brief.md, STATUS.md; next line "steer it yourself".
3. Direct batch priced with one "Chief of Staff (steering)" row; "Chief of Staff" line excludes the window; Total has nothing counted twice - after-2-cost.txt.
4. order add / order qa exit 2 on a direct batch; order slots-type orders unaffected - after-4-orders.txt.
5. close not blocked by the Chief's own fresh transcript, still blocked by a fresh Driver file - after-4b-close.txt.
6. A later epoch from another transcript sets steering foreman, logs it, old epoch exits 3, order add then passes, costs split correctly - after-3*.txt.

Observations (do not change the verdict):
- brief.md keeps "Steering: direct" after a switch to Foreman (written once at open); status/STATUS.md/batch.json are right.
- cost --summary prints "Driver chief-of-staff with its workers: $2.00" for the steering row's group; the steering session is listed as a Driver type there (cosmetic; the Foreman case prints the same pattern with "foreman").
- Copilot direct run unproved; pytest not run by the Verifier.
