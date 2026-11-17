# CR 264, round 2 inspection (2026-11-06)

Head `1f94f56d`. One inspector (Opus). Verdict: FIX-REQUIRED. A0 and A1 code verified correct.

- 1 major: commit subjects over 71 characters; `docs(requirements)` scope not allowed (scopes only on fix/feat); bodies describe internals.
- 2 major: A5 flush in `previewManager.ts` `replaceEach` has no test (lifeReq/host test with `edits.lock.pageEditorOpen`; state it in TRUST-001/LIFE-143 with a marker).
- 3 minor: `replaceEach` computes the target folder before the flush; recompute inside `replace` after the flush.
- 4 minor: `blockReq.requirements.test.ts:235` adds `.filter(error !== undefined)` to TRUST-065 with no reason: revert or explain.
- 5 minor: `inlineThread.test.ts:85` title and REVIEW-171:83 quote still say read-only; capture id `r01-untrusted-read-only` and stress scenario `untrusted-read-only` kept (rename or record why).
- 6 minor: TRUST-001 Verification lists `reviewReqComments.requirements.test.ts` among read-only-file tests (wrong); `tiers/log.md` round 2 verification claims unverifiable runs.
- 7 minor: no test asserts `preview.edits.pastedImages` records the saved image (`pasteImageWrite.test.ts`).
