# Verify CR-476 One blank-line block per extra blank line

Head: 58c9f1e679e8b89e2c0da54a16edfefb1ea3c23b

Base: origin/main dcc84def8b331e323fb3b91ef89941f9ca7dbb13. All commands run in the CR worktree at the head above.

## Claims

1. One block per extra blank line, text + three blank lines, six blank lines, one-newline document (58c9f1e).
   Command: `npm run visual:render` then `uv run --no-sync --group docs python test/visual/capture.py --group block-editing --group layout-width`.
   Output: every blank-line scenario passed (v44, v45, v54, v86, v87 PNGs written); the group run ended with one failure, `08-okf-schema--dark--sticky-3--default.html: paragraph editor caret is not at the clicked word`, a paragraph editor caret check unrelated to blank lines (not in these scenarios; CI visual is green at this head, `gh pr view 494`: visual SUCCESS). Not re-run on the base, so not proved to fail there either.
   Images (evidence/): after-v44 shows two "Blank line" blocks between the paragraphs; after-v54 shows "Text." then six stacked "Blank line" blocks; before-six shows one "Blank lines (6)" block; before-v44 one block for the run.
   Judged: PASS.
2. One-newline document shows one block at the top, then Start writing 40 px below (58c9f1e).
   Output (out/reports/visual/first-gap/layout-width/v39-first-gap-empty-edit-dark-900.json): block `gap` 3.6 viewportTop 3.6; Start writing viewportTop 65.0 (block bottom + 40, check FIRST_ELEMENT_GAP). after-v86 image shows both. PASS.
3. Typing, delete, selection, arrows, paste act on one line (58c9f1e).
   Commands: `node scripts/node-test.mjs unit "out/test/page/runtimeBlankLines*.test.js"` -> tests 69, pass 69, fail 0; `node scripts/node-test.mjs unit "out/test/{core,page,session}/**/*lank*.test.js"` -> tests 374, pass 374; `node scripts/node-test.mjs unit "out/test/core/{mapping,edits}/**/*.test.js"` -> tests 501, pass 501, fail 0.
   Byte-for-byte restore: test/session/blankRunInListHost.test.ts line 90 and blankRunInContainerHost.test.ts line 114 (in the 374 run). PASS.
4. StRS-MDOKFSTUDIO-BLOCK-011 `verified:` block (58c9f1e).
   Command: `git diff origin/main...HEAD -- requirements/tiers/strs/block-editing/StRS-MDOKFSTUDIO-BLOCK-011.md`.
   Output: `req_lifecycle: proposed` -> `approved`, `approved_by: gaetan@xeberon.net`, `approved_at: '2026-11-23T14:00:00+01:00'`, `verified: by: human:gaetan@xeberon.net, at: '2026-11-23T14:00:00+01:00'`; the added sentence and Path 3 are verbatim the spec's section 5 text (compared by reading); spec answers Q10 and Q11 (02-answers.md) approve the text and the `approved` state dated 2026-11-23. The verified date equals the approval date, and approval is the owner's answer, so the block is correct. `okfreq validate/lint` ran: `0 indexes would change`, `0 requirement OKF projections would change`; only W2 broken-cross-link warnings on PALETTE-264 (not touched by this CR). PASS.
5. Gate and CI (58c9f1e).
   `work/gates/preflight-r4.log` first line `58c9f1e679e8b89e2c0da54a16edfefb1ea3c23b`, ends `ci-static: passed`. `gh pr view 494 --json statusCheckRollup`: static, static-windows, visual, viewer-graph, report, checks SUCCESS; integration, stress, gallery SKIPPED (PR). Review: `chantier log`: "r4 inspector approved at e1882e8..., committed as 58c9f1e6", ship at the head. PASS.
6. PR description (posted body equals work/pr-body.md bar one blank line) (58c9f1e).
   - Summary, Deliverables, Changes match the diff in substance. FAIL on cleanliness: the Deliverables line "Screenshots of the new look are attached below once captured at the pushed head." is a placeholder, and no image is attached. Replace it with the captured images (evidence/after-v54..., before-six...) or delete it.
   - Known gaps is stale: the bullet "A document made only of whitespace now shows blank-line blocks; its interaction with the Start writing button is not verified" is now proved (claim 2); the bullet "browser captures are not run locally; they run in CI" is out of date (CI visual passed at this head). Narrow both. The integration and stress runs are skipped on a PR; keep that gap.
   Judged: NOT VERIFIED until the body is fixed.

## Verdict

NOT VERIFIED (the code, tests, captures and the StRS-BLOCK-011 block are proved at 58c9f1e; only the PR description fails: placeholder screenshot line, stale Known gaps).
