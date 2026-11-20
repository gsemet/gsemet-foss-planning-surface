# Verify CR-436

Head: 9091f929c83ae559fb6b8c4731aba7c29d58f026

Gate: work/gates log first line "gate CR-436 branch chantier/batch-07/cr-436-block-editor-stuck-on-saving-markdown-af head 9091f929c83ae559fb6b8c4731aba7c29d58f026", `just preflight`.

Claims (all judged at 9091f929):

1. New unit/page/host tests fail on base, pass at head. Base (7c88b89c, tests copied in): `node scripts/node-test.mjs unit ...` gave "tests 20, pass 4, fail 16" (exit 1; matchLineEndings test: Cannot find module lineEndings; "exactly one done" assertion failures). Head: 6 related test files, "tests 70, pass 70, fail 0". Logs: verifier/evidence/before-unit.log, after-unit.log.
2. Real window `STUDIO_REAL_INPUT_SCENARIO=line-ending-leave npm run test:integration -- --trusted-only`: head exit 0 (STEP done: real-input); base (scenario copied in) exit 1, "Timed out waiting for the editor to close (CRLF file, paragraph, left by Done)". Logs: verifier/evidence/*-integration.log. Run one at a time.
3. Line-ending rule: at head `node scripts/node-test.mjs unit` on lineEndingPreservation, lineEndingSave, lineEndingFixtures tests: tests 8, pass 8, fail 0 (fixtures in test/fixtures/markdown-line-endings read as raw bytes); real-window scenario also checks the bytes unchanged and a real change in CRLF stays CRLF.
4. PR description (read with gh pr view 446 at head 9091f929): matches diff. BLOCK-234 mixed-endings row refined in diff and declared in Autonomous decisions; BLOCK-263 added with markers in src (lineEndings, blockEditor, blockSourceEditor, blockEdits) and tests; markers on 042 and 130 are test-file additions; CHANGELOG line present; `just requirements-lint` passes (92 StRS, 581 SwRS citations valid). Known gaps "None": no UNVERIFIED claim, all evidence captured. No images, no role names, no STALE mark. Draft PR leaves "Local gates", "Review", "CI green" unchecked, expected for a draft.

Review box check not applicable (draft, no box).

VERIFIED

## Description-only pass (head 9091f929c83ae559fb6b8c4731aba7c29d58f026)

Command: `gh pr view 446 --json body,headRefOid` -> headRefOid 9091f929c83ae559fb6b8c4731aba7c29d58f026.
- Clean render: template sections in order, one mermaid block, one ts block, no images, no fold (none in template), no STALE mark.
- Consistent with `git diff --stat origin/main...HEAD` (23 files): lineEndings.ts new, blockEditor, blockEdits, blockSourceEditor, hostToPage done field, BLOCK-263 and markers, CHANGELOG all present in the diff and the body.
- Test plan proofs each name `9091f92`; Local gates match gate log `just preflight` pass at 9091f929.
- Review box `approved at 9091f92`: `chantier log CR-436` has "r2 approved at 7c88b89c, committed as 9091f929" (round committed as the cited SHA): proves it.
- Known gaps "None": no UNVERIFIED, no uncaptured evidence, no accepted failure.
- Internal references: "CR-436 stuck-saving" only inside the Internal references section; none in the body text; no role names.

VERIFIED
