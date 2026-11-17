# Verify CR-311

Head: 42d9718d0c8cdaaf290c2e58abf12b251c1b1cb0

Claims, all judged at d3a37e75fe14d60def7ee99882b2e91849e6dc74:

1. Diff scope. `git diff --stat main...HEAD`: chief-of-staff.md, driver.md, foreman.md, verifier.md only (4 files, 63+/9-). `grep -n "^## "` shows every hunk lies outside the `## Startup core` sections (driver.md:1031, verifier.md:147, foreman.md:663; hunks are in Your means, QA driver, Release driver, Your part, ask bullets). The foreman.md clause is the settled open question, named in the PR's Autonomous decisions. PASS.
2. Driver items 1-4 present: rule and terms in "The evidence:" (look, keeping, upload, user's screenshot not uploaded with Known gap kept and note + report, post-upload leak replaced and reported, user's own removed and gap put back), pointer in the archive bullet, QA driver, both Release driver bullets. PASS (read in the diff).
3. Verifier items 1-2: third condition on the description ("fails any of the three"), terms and capture rule, description-pass look naming the failing image in verify.md. PASS.
4. Chief of Staff two acts (plain ask and stack ask) and the Foreman relay clause present. PASS.
5. `just check` at head (clean tree): ruff, mypy, biome, uv lock check, `369 passed in 96.21s`, `release-notes ... ok`. PASS.
6. CI: Driver's note records all 5 jobs green at d3a37e7 incl. `just scenario (ubuntu-latest)` (task brief confirms); not re-run by me.
7. PR description (gh pr view 263, headRefOid d3a37e7): renders (sections, fold, no images, no local links); Summary, Deliverables, Changes match the diff; Known gaps "None" with no UNVERIFIED claim, no uncaptured evidence pair (none required); no STALE mark; no role name misuse (only product terms). Review box `approved at d3a37e7` matches `$CHANTIER log`: "r1 inspector approved at 3df17b9" then "r1 committed as d3a37e7". Remaining `<sha7>` boxes are the Verified/CI boxes, filled after me. PASS.
8. No images in the PR or CR evidence: nothing to give the look.

VERIFIED

## Description pass at 42d9718d0c8cdaaf290c2e58abf12b251c1b1cb0 (after the rebase onto CR-310)

- Patch unchanged: `git range-diff d3a37e7~1..d3a37e7 42d9718~1..42d9718` prints `1: d3a37e7 = 1: 42d9718`; `git patch-id --stable` of both commits is 236e487d83786752175d7091ad54a948d4844cae. All earlier claims carried from d3a37e7 (clean rebase, patch identical).
- Description (gh pr view 263 body at head 42d9718): clean, sections and fold render, no image attached, so none shows the username or home folder.
- Consistent with the diff: `git diff --stat <CR-310 branch> 42d9718` = chief-of-staff.md, driver.md, foreman.md, verifier.md (4 files), as the Changes list names; Foreman clause listed under Autonomous decisions.
- Proofs name SHAs: gates, review and verdict "carried from d3a37e7"; CI at 42d9718: `gh pr checks 263` all 5 jobs pass.
- Review box: log shows `r1 inspector approved at 3df17b9...` then `r1 committed as d3a37e7`; carried SHA d3a37e7 matches the round's committed-as note.
- Known gaps "None": no UNVERIFIED claim, no uncaptured evidence pair (Evidence line "none, no visible change").

VERIFIED
