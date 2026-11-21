# Verify CR-455 at 61737fd

Head: 61737fd33b34967ff26837a87506c6e28d191186

Scope: the pushed head. The PR body is not posted yet; the candidate work/pr-body.md was checked against the diff
(description pass on the posted body still to do by the Driver). Accepted gaps are those in pr-body.md Known gaps.

## Claims

1. Host tests of the real-file rule, openPreview from a diff (no text editor, either side), staged stand-in and refusal,
   other-file URI keeps its path, follow switch (no switch for a stand-in), scroll of the real side only, reveal on the
   real side (61737fd).
   Command: `node scripts/node-test.mjs unit out/test/host/diffPreview.requirements.test.js` after `npm run compile`.
   Output: 7 tests, pass 7, fail 0.
2. Package contract pins the editor/title clause (61737fd).
   Command: `node scripts/node-test.mjs security out/test/security/package-contract.test.js`. Output: 13 tests, pass 13, fail 0.
   `git show HEAD:package.json` shows `resourceExtname == .md && (activeEditor == workbench.editors.files.textFileEditor || activeEditor == workbench.editors.textDiffEditor)`.
3. Real-window proof (61737fd): `gh run view 44925814982 --json ...` headSha 61737fd; jobs integration, stress, visual,
   static, static-windows success; the integration job log has `STEP start: diff-preview` then `STEP done: diff-preview (9709 ms)`.
   PR run 44925818134 headSha 61737fd conclusion success; `gh pr checks 466`: static, static-windows, visual, viewer-graph, report pass.
4. Gate: `chantier log` has `gate result=pass head=61737fd33b34967ff26837a87506c6e28d191186 command=just preflight`.
5. Review box `approved at 61737fd`: the log has only inspector approvals at e153886 (r4 fallback B) and 7121260 (r4 openDiff fix);
   no note names 61737fd as approved. 61737fd is the test-only follow-up commit (test: wait for the requested diff to be the active tab).
   The body claims "Review: approved at 61737fd (rounds 1 to 4)": the Driver must record an approved note at 61737fd or reword the box.
   Not a code failure; flagged for the description pass.
6. Body vs diff: diffRealFile.ts (new, rule as stated), activation.ts (openPreview + tab-change follow), hostEvents.ts
   (onActiveDocumentChanged), scrollSync.ts (reveal only for `file:` document ids), package.json, tests, 4 SwRS, docs,
   changelog, glossary all present in `git diff --stat origin/main...HEAD`. Matches.
7. Known gaps cover the dropped T6, inline layout not asserted, title button by manifest, palette not Ctrl+K Shift+V, out-of-scope
   editors, no screenshots. The two inbox items (multi-file/merge, scroll limitation) are not filed per the Driver's note; spec decision 10 asks for one.

## Verdict

VERIFIED (code and behaviour at 61737fd); the Review-box wording in item 5 is for the description pass.
