# CR-312 Change Specification: Cmd+S saves the document from the preview

✅ merged · batch-02 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/383)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/383.
**Next:** Nothing.

## Progress

- [x] Round 1: Implement the whole specification: protocol, host command, session handler, page handlers, requirement, docs, changelog, unit/session/page tests, integration test file
- [x] Round 2: Inspector: add bounded host fallback when the page posts OK but never sends previewSaveRequest (timer FLUSH_WAIT_MS, cleared on request, never double save) + test that fails on current code
- [x] Long gate fail: 9abd4bc6
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/383
- [x] Note: Local preflight: static and visual passed; ci-integration failed in the existing palette real-input scenario (no focus, locked screen); heavy run 43334982738 dispatched as proof
- [x] Round 3: Heavy run: save-key frontmatter step times out waiting for [data-okf-frontmatter-editor] textarea; fix the real-window test (block and cell steps passed)
- [x] Note: Heavy run 43340259932 at 7570feb: block, cell, frontmatter save-key steps pass; custom-editor step (decision 5) times out waiting for the saved text; stress, visual, static green; needs round 4 to add activeCustomEditorId clause or fix the test
- [x] Blocked: rounds: save-key custom-editor step fails on heavy run 43340259932 (head 7570feb), decision 5 not settled; draft PR 383; needs a 4th round
- [x] Round 4: round 4: save-key binding gains the activeCustomEditorId clause (done by the Driver, small); heavy run 43344012200 green at aed1a0a
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/383
- [x] Note: round 4: Inspector FIX-REQUIRED (SwRS-173 custom editor scenario, test comment, PR body native-check result) fixed by the Driver in 92137829 (docs/comments only, no new round); Verifier VERIFIED at aed1a0a; heavy run 43347118035 green at 92137829. No local long gate: ci-integration cannot run on the locked-screen machine; CI heavy run is the proof
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/383
- [x] Handed back
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/383
- [x] Note: Restacked 305..312 in order, linked as gh stack #384; just check green at fb7b57f; no per-CR preflight at new heads (owner order: just check at top + heavy run 43353161466 on top + PR CI).
- [x] Note: PR CI green on all eight restacked heads (checks/report/static/static-windows/visual); heavy run 43353161466 on top pending.
- [x] Note: Heavy run 43353161466 green at fb7b57f: static, static-windows, visual, integration, stress, report, checks success.
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/383

## Documents

- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [conflicts](work/conflicts.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261113-001446.log)
- [evidence](evidence)
- [.agents/constitution.md](../../../constitution.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [docs/user/editing.md](../../../../docs/user/editing.md)
- [requirements/tiers/log.md](../../../../requirements/tiers/log.md)

## Where

- Branch: `chantier/batch-02/cr-312-change-specification-cmd-s-saves-the-doc`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-02-CR-312`
- Driver: `-`

## Decisions and open questions

- Local preflight: static and visual passed; ci-integration failed in the existing palette real-input scenario (no focus, locked screen); heavy run 43334982738 dispatched as proof
- Heavy run 43340259932 at 7570feb: block, cell, frontmatter save-key steps pass; custom-editor step (decision 5) times out waiting for the saved text; stress, visual, static green; needs round 4 to add activeCustomEditorId clause or fix the test
- back to a Driver: round 4 granted (O-2). Add the activeCustomEditorId == 'markdown-okf-schema-studio.editor' clause to the binding in package.json and test/security/package-contract.test.ts; check runSaveCommand finds the custom editor's session; push; re-dispatch the heavy run on the exact new head; integration and stress must be green there. Fill the PR body (RESULT_PLACEHOLDER, preflight line, boxes), then gh pr ready. Log keep-or-drop of the clause in 02-answers.md for the owner's morning review.
- round 4: Inspector FIX-REQUIRED (SwRS-173 custom editor scenario, test comment, PR body native-check result) fixed by the Driver in 92137829 (docs/comments only, no new round); Verifier VERIFIED at aed1a0a; heavy run 43347118035 green at 92137829. No local long gate: ci-integration cannot run on the locked-screen machine; CI heavy run is the proof
- Restacked 305..312 in order, linked as gh stack #384; just check green at fb7b57f; no per-CR preflight at new heads (owner order: just check at top + heavy run 43353161466 on top + PR CI).
- PR CI green on all eight restacked heads (checks/report/static/static-windows/visual); heavy run 43353161466 on top pending.
- Heavy run 43353161466 green at fb7b57f: static, static-windows, visual, integration, stress, report, checks success.

## Cost

$5.43.
