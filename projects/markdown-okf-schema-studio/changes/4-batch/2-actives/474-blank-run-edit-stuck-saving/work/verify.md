# Verify CR-474

Head: 466a9c062d361e37ad1ad46ac73920f0d76d4d14

Claims, all judged at 466a9c06 (full SHA above).

1. Fix: `applyContentPatch` closes a blank-run editor once `finishing`; otherwise unchanged.
   Command: `git diff origin/main...HEAD -- src` -> one condition (`blankRunEdit = replaceBlankRun && !finishing; if (!blankRunEdit) closeBlockEdit(false)`), comment says both halves, BLOCK-268 marker kept. Matches spec section 1.
2. Page tests pass at head.
   Command: `npm run compile` then `node scripts/node-test.mjs unit "out/test/page/runtimeBlankLines*.test.js" "out/test/session/blankRunHost.test.js"`
   Output: tests 83, pass 83, fail 0. Includes new "Done in a blank-lines block's editor: the patch of its final save closes the editor", "Done in the editor of a run inside a list: the patch closes the editor", "an error answer to Done keeps the editor open across a patch, and a second Done then a patch closes it", the kept fix-7 quote-run test, and the session test "a final save that writes text asks for a render and posts no done: the patch closes the editor" (LF and CRLF).
3. Requirements: `just requirements-lint` ran (diagram check passed: 94 StRS parse); log.md entry dated 2026-11-23 and BLOCK-268 change present in diff stat.
4. Gate: work/gates/preflight-466a9c06.log first line "head 466a9c062d361e37ad1ad46ac73920f0d76d4d14"; CI per brief green at this head.
5. PR body (draft, gh pr view 491): headRefOid equals the head; Summary/Changes match the diff (contentPatch.ts, two test files, requirements, changelog). Known gaps names the Cancel follow-up.

Not run: the new test against the base code (spec says it fails first; I cannot edit code, so this rests on the Coder's record, not on my run); no real VS Code editor run; the PR body's unchecked boxes (tests, requirements, changelog, CI) are drafts to tick.

NOT carried: nothing.

VERIFIED

## Description pass at 466a9c062d361e37ad1ad46ac73920f0d76d4d14

Command: `gh pr view 491 --repo gsemet/markdown-okf-schema-studio --json body,headRefOid` (headRefOid = 466a9c0, no stale SHA); `git diff --stat origin/main...HEAD` (7 files: CHANGELOG, requirements x3, contentPatch.ts, two tests); `gh pr checks 491` (checks, report, static, static-windows, viewer-graph, visual pass; integration, stress skipped); `chantier log CR-474` (r3 inspector approved at 73037bd, committed as 466a9c06; preflight pass at 466a9c06).

Judged true: Summary, Deliverables table, Changes list match the diff; CI and gate boxes backed; Review box backed by the log notes; Known gaps lists the unverified fails-first and no real run/capture.

Failed: role names as the doer of the work, outside Internal references (pr-template, "The rules", internal-reference bullet):
- Test plan: "(Verifier ran them; ... it rests on the Coder's record)"
- Known gaps: "(they fail there, per the Coder's record only)"
- Test plan Review: "inspector approved at 466a9c0"
Reword without roles (e.g. "passing at 466a9c0; that they fail on the previous code is UNVERIFIED"; "Review: approved at 466a9c0").

Note (not a failure): "Fixes #485" closes the issue while the PR is "part 1 of 3"; confirm that is intended.

NOT VERIFIED

## Description pass, second start, at 466a9c062d361e37ad1ad46ac73920f0d76d4d14

Command: `gh pr view 491 --repo gsemet/markdown-okf-schema-studio --json body,headRefOid` (headRefOid = 466a9c0); `git diff --stat origin/main...HEAD` (same 7 files as above, unchanged).
Output: the body no longer names Coder, Verifier or inspector as the doer; "the author's own run" and "Review: approved at 466a9c0" are plain wording. Summary, Deliverables, Changes match the diff; Known gaps lists the unverified fails-first and no real run or capture; no image attached. "Fixes #485" is intended (specification, Decisions carried: this CR closes the issue).

VERIFIED
