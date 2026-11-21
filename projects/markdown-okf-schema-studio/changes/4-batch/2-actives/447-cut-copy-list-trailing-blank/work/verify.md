# Verify CR-447

Head: 15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b

Verdict: VERIFIED

## Claims, all judged at 15a0ef09

1. Unit proof re-run at 15a0ef09: `npm run compile`, then
   `node --test out/test/core/edits/sourceEdits.test.js out/test/core/mapping/blockRange.test.js out/test/core/edits/blocksDelete.test.js out/test/session/dropFiles.requirements.test.js`
   Output: `tests 88, pass 88, fail 0`.
2. Claims 1 to 5 of the previous pass (trim for LF, CRLF, lone CR and refusals; paste anchor; the new
   tests fail on base 5a84db8b with 15 failures; requirements lint and update clean; code against spec)
   carried from 15a0ef0: the head is the same (`git rev-parse HEAD` = 15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b,
   tree clean), no code moved since that pass.
3. Gate: `work/gates/20261121-121839.log`, first line
   `gate CR-447 branch ... head 15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b`; `$CHANTIER log` shows
   `gate result=pass head=15a0ef09... command=just preflight`.
4. Real VS Code steps, judged from heavy CI run 44898480884: `gh run view 44898480884 --json headSha,conclusion`
   gives headSha 15a0ef09..., conclusion success (integration, stress, visual, static, static-windows,
   report, checks all success). Its integration log holds
   `PASS real-input screenshot: block-editing/r25-cut-list-trailing-blank` and
   `PASS real-input screenshot: block-editing/r26-paste-after-list-trailing-blank`.
5. Review box: `$CHANTIER log` note "r3 approved at b39e99d2..., committed as 15a0ef09..." matches
   "Review: approved at 15a0ef0".

## Description (as posted on PR 458, `gh pr view 458 --json body,headRefOid`, headRefOid 15a0ef09...)

- Renders (sections, table, fold); no image. No stale SHA: every SHA is 15a0ef0 (the earlier 150ee65 is gone).
- Summary, Deliverables, Changes match the diff (`git diff 5a84db8b HEAD --stat`: 15 files: src,
  requirements, changelog, capture registries, tests). Known gaps names the heavy-only real scenario,
  now proved by the CI log above. Role names: none outside Internal references.
