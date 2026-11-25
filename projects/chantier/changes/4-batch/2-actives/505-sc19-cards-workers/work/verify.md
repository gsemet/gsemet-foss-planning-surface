# Verify (description-only pass) CR-505

Head: 5be593b7486739c435eaf3db8922ce1f0d490637

Verdict: NOT VERIFIED

Claims judged at 5be593b (full SHA above). Base used for diffs: f08cf41f (merge-base with origin/main).

## Held
- Files: `git diff --name-only f08cf41f..HEAD` lists 71 files, all under skills/chantier/cards-next/ (none outside); 2 commits. Matches body.
- floor.md: `git show HEAD:.../cards-next/floor.md | cmp - <(git show HEAD:.../references/floor.md)` no difference.
- Card sizes (`git show HEAD:<path> | wc -c`): coder 1417, conflict-resolver 1378, debugger 1165, investigator 1370, demo-explorer 1496, spec-writer 1493, spec-critic 1499, retro-critic 1492, inspector 1999, verifier 2996, griller 1758 (old section 2198), cr 3280, stack 3321, qa 1337, release 3277. Old sizes at f08cf41f equal the table (4609, 3893, 3682, 3554, 3422, 3254, 3729, 2901, 6044, 14581); old driver.md 54955. All match.
- 54 topic files; 23 over 1536 (worst release-merged 2845, cr-ship 2413, stack-changes 2354, retake 2328, release-ship 2306); worker topics max 1492. topics.json has 55 entries (old names kept as rows). Match.
- `git grep -n cards-next HEAD -- . ':(exclude)skills/chantier/cards-next'`: no line. Forbidden phrases / `chantier board` / version line: none in cards-next.
- Driver role-only briefs via staging folder (driver.md copy, floor, topics): cr 7541, stack 7582, release 7538, qa 5598; body says 7442/7483/7439/5499 (constant +99 bytes, the longer path of my staging folder). Accepted as the same.
- retro-critic 4225->2816, demo-explorer 4746->2820 reproduced exactly.
- Inventory: 374 rows (W-001..W-374), walk method stated; Known gaps content agrees with the log's gaps.
- Spec items spot-checked in the cards: stack never "loop or script over branches", release never "undo half-done irreversible work", lead 1 wait form, background-shell wait, rules by section.

## Failed
1. Review box. The body says "Review: approved at 5be593b (Inspector round 4 ...)". `$CHANTIER log CR-505 --batch batch-31` (47 lines) has no note of an approved pass at 5be593b: the only approvals are "r2 inspector approved at f08cf41f" and "PART 1 approved at f08cf41f, committed as 5f1905a3"; round 3 is FIX-REQUIRED at 5f1905a3; the last events are leases (15:17:59Z). No round-4 note. By the card, a Review box without such a note is NOT VERIFIED. Fix: the Driver notes the round-4 approval with its head (or the Review line is unticked/narrowed).
2. Worker brief sizes (minor, not alone failing). `brief <role> CR-505 --batch batch-31` at this head gives coder old 9662 / new 6470, verifier 19634 / 8049, inspector 11097 / 7052, against the body's 7549/4357, 17521/5936, 8984/4939. The difference is a constant +2113 bytes on both sides (the CR's facts block grew since the earlier run; savings identical, e.g. 3192 for coder). The body does not say these were measured earlier; re-measure at the head or say when.
3. Forward-link count (minor). Body: "`../pr-template.md` and `../concepts.md` (2 and 4 uses)". At head: pr-template.md 2, concepts.md 5 (`grep -rn "concepts.md" skills/chantier/cards-next`: inspector-audit, spec-writer-extras, trouble-worker, verifier-delta-matrix, verifier-description). Fix to 5.

## Not run
Quiz, real run, `just check`, CI: not part of this pass; the body marks quiz and real run UNVERIFIED in Known gaps, consistent with the log.
