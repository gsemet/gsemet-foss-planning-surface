# Verify CR-463

Head: 1dd3e76829b3e7711ee0890e1f4f946f7f615205

Claims, all judged at 1dd3e76829b3e7711ee0890e1f4f946f7f615205:

1. Unit tests (page, session, core/preview) pass. `npm run compile` then `node scripts/node-test.mjs unit "out/test/{core/preview,page,session}/**/*.test.js"`: tests 2747, pass 2745, fail 0, skipped 2. Includes "CR 463: the change bar tooltip shows on the bar only, in the tooltip look, never in edit mode or with the bars hidden" and "CR 463: the removed-lines marker is a red triangle in the diff's removed colour...". Code read: tooltip label from ranges (`changedLinesLabel`), removed label (`removedLinesLabel`), clicks ignored in edit mode (`editing()`), Escape and second click close the single card (`sideBySide.ts`).
2. Requirements: `just requirements-lint` -> "1202 requirements, 0 errors, 26 warnings", main paths valid. SwRS REVIEW-220/221/222 present, each derived from StRS-MDOKFSTUDIO-REVIEW-017, with `@implements_req` markers in src (incomingChanges.ts, sideBySide.ts, pageToHost.ts, viewState.ts, incomingChanges session) and tests; log entry in requirements/tiers/log.md.
3. Visual: `npm run visual:render` and `capture.py --scenario review-annotations/v31..v36` -> 6 passed, `{"status": "passed", "scenario_count": 6, "screenshot_count": 6}`. All six images opened: tooltip text, red removed marker with tooltip, single card (before left, after right), light and dark, legible, no username or home path. Copied to work/verifier/evidence/.
4. Long gate: gates/20261121-235149.log first line names CR-463 and head 1dd3e76829b3e7711ee0890e1f4f946f7f615205, last line `result: pass at 1dd3e76829b3e7711ee0890e1f4f946f7f615205`.
5. CI at head: `gh pr checks 474`: static, static-windows, visual, viewer-graph, report, checks pass (run 44958867063, the PR run).
6. Heavy run 44958907144 at the same head: static, static-windows, visual, viewer-graph, stress success; integration FAILURE at `STEP failed: diff-preview-scroll (21602 ms): Timed out waiting for the inline diff's editor to scroll.` (report and checks fail as a consequence). The same step fails identically on main at 58b4c302 (run 44957381296, `STEP failed: diff-preview-scroll (21535 ms)`), and the CR changes no integration test (`git diff --name-only origin/main...HEAD | grep -i integration|diff-preview` empty). So red on the default branch, not the CR's; reported, the real-window behaviour of the new bars is not proved by it. UNPROVED: the tooltip, marker and card in a real VS Code window (only simulated page and Chromium captures).
7. PR description (`gh pr view 474`, same text as work/pr-body.md): renders, sections complete, matches the diff (tooltip, removed marker, click card, host message `previewBaselineRequested`, `removed` payload, three SwRS, log, changelog line in diff). No images attached, no role name. Known gaps absent: acceptable only if the Driver adds a bullet for the unproved real-window behaviour (item 6); a check red on main is not an accepted failure of a claim. No claim is stated as fact without proof here.

Before/after: see work/verifier/evidence/before-after.md (before not capturable: scenarios new).

VERIFIED
