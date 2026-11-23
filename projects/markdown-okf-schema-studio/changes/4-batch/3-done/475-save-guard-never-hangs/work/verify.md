# Verify CR-475

Head: 8aeae06bb16554aa77c93c80c3da1ce3ef06c9d4

Verdict: VERIFIED (real-window step UNVERIFIED, stated in the PR's Known gaps)

## Claims (all judged at 8aeae06b)

1. The code compiles. `npm run compile` (tsc -p .): no error.
2. The new and touched tests pass at the head. `node scripts/node-test.mjs unit "out/test/page/runtime{DetachedSave,SaveEnds,EditInFlight,FrontmatterSaveEnds}*.test.js" "out/test/session/detachedSave.test.js"`: tests 112, pass 112, fail 0.
3. Wider set (page runtime*, blockReq*, pageMessages, previewManager, session detachedSave, core/protocol, host fmtableReq): tests 1265, pass 1265, fail 0. It includes the Cancel/Escape close, reopen with the typed text, Q13/Q16 outside change, "reopened: false" Copy text, retry after reopen, host decision 1 (a)(b)(c), Cancel-before-Done restore, and the protocol validators.
4. Fail-on-previous-code: not re-derived; taken from the PR's Known gaps (44 of 95 fail on previous src; gesture-guard tests pass there by design, stated).
5. PR description (draft #492) against the diff (63 files): Changes list matches (detachedSave*.ts, blockEditor/tableCellEditor, gesture guards, session detachedEdits/blockEdits/hostEvents/rendering, frontmatter unchanged, protocol, HostUi.showWarning, requirements, glossary, rewritten BLOCK-053 test). `detached: true` on previewEditClosed is present in src/core/protocol/pageToHostMessages.ts:423, as the Autonomous decisions say. Known gaps lists the UNVERIFIED real-VS Code step and the changelog PR number.
6. UNVERIFIED: real-VS Code step test/integration/detachedSaveWindow.ts never ran (heavy run stops at preview-smoke, also red on main). No real VS Code locally. Stated in Known gaps, so it does not alone change the verdict.

No before/after images: no UI capture; before-after evidence not captured (no real window available).

## Description pass at 8aeae06bb16554aa77c93c80c3da1ce3ef06c9d4

Command: gh pr view 492 --json body; git diff origin/main...HEAD; chantier log 475. Result: VERIFIED. No internal reference outside the last section; proofs carry SHAs (8aeae06, 466a9c0 with the log note of the approval at 466a9c06 and the clean-rebase carry); the UNVERIFIED real-window claim, the missing changelog PR number, the render-never-arrives gap and the 44 of 95 note each have a Known gaps bullet (44 of 95 matches the Driver note of the base run); Summary, Deliverables and Changes match the diff (protocol messages, HostUi.showWarning actions, MAX_PAGE_TEXT_LENGTH shared, unchanged frontmatter answer). Minor, not failing: the test-only hook holdBlockEditAppliesForTests is not named in Changes.
