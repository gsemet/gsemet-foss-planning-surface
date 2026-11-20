# Verify CR-344 (second pass, round 6 move)

Head: 13a8545aa54a6ed206e93a6e87efe5d4c6f3cecc

Move judged: c13b511..13a8545 (one commit: `links.ts` marker split, `links.ts` dropped from `scripts/marker-baseline.json`). Claims 1-9 of the first pass (work/verifier-first-pass.log) are carried from c13b511: the move touched only two files, neither a requirement, the commentStyles split, the supersessions or the approved StRS. Items 10-11 are judged again.

10. Spec evidence 3 and 4 at 13a8545. `git diff c13b511 HEAD`: `links.ts` now carries FMSCHEMA-073 alone on the blocked-link warning branch (line 238), BLOCK-205, TOOLBAR-117, TOOLBAR-059, TOOLBAR-077 each on their own branch; `src/session/features/links.ts` removed from the baseline. `grep FMSCHEMA-073 src test` shows `@implements_req` at links.ts:238 and `@tests_req` in previewEditing.test.ts, diagReq.links.requirements.test.ts, links.test.ts. `node scripts/check-marker-companions.mjs` -> `check-markers: 5 companion file(s), 418 in-force SwRS marked, 39 files on the marker baseline` (pass). A script with the checker's own `markerBlocks` over every baseline file, printing over-3 blocks naming REVIEW/FMEDIT/FMSCHEMA IDs, lists exactly: commentAnchors.test.ts, commentWrite.test.ts, inlineThread.test.ts, reviewComments.test.ts, capture_export_html.py and exportHtmlScenarios.ts (FMSCHEMA-091), scenarioDefinitions1.ts (FMSCHEMA-001/006/029) - only the accepted deviation files (O-27/O-28). Nothing else remains. VERIFIED.
11. `work/pr-body.md` against the code at 13a8545. Known gaps names the deviation exactly (the same seven files and IDs as above) and says FMSCHEMA-073 has a focused marker (true). Test plan: Local gates `13a8545` (gate log work/gates/20261118-145021.log first line `gate CR-344 ... head 13a8545aa54a...`, `just preflight`), Review box `13a8545` backed by Driver note "r6 approved at c13b511 ... committed as 13a8545a", CI box backed by heavy run 44317812898 success at 13a8545 and `gh pr checks 416` pass (reported in the brief). Unchecked boxes (failing-once, evidence none, Verified) are consistent. Note: the PR as posted on the forge still carries the older body (`gh pr view 416` shows `927f540` boxes); the Driver must post this draft. VERIFIED for the draft.

## Verdict

VERIFIED

## Description pass (posted body of PR 416)

Head: 13a8545aa54a6ed206e93a6e87efe5d4c6f3cecc

12. `gh pr view 416 -R gsemet/markdown-okf-schema-studio --json body` diffed with work/pr-body.md: identical except a trailing newline. Test plan boxes (gate `13a8545` preflight, Review `13a8545`, Verified `13a8545`, CI `13a8545`) match claim 11 above; `gh run view 44317812898 --json conclusion,headSha` -> `success 13a8545aa54a...`; `gh pr checks 416` -> static, static-windows, visual, report, checks pass (others skipping). Known gaps names the seven deviation files exactly (commentAnchors, commentWrite, inlineThread, reviewComments tests, scenarioDefinitions1.ts, capture_export_html.py, exportHtmlScenarios.ts). CR-344 and batch-06 appear only under Internal references. No images. VERIFIED.

## Verdict (description pass)

VERIFIED
