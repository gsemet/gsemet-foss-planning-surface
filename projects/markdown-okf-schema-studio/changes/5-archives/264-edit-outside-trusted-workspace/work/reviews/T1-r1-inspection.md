# CR 264, round 1 inspection (2026-11-06)

Head `19a97e04` on `e20c6432`. Three read-only inspectors (Opus), one slice each. Verdict of each:
fix-required. Nothing was run by them; `just check` on this head exits 0. Round 2 fixes the items below.

## Decisions of the main session

- A1: fix the code, do not narrow the requirements. The owner's decision is "stays read-only, with its
  existing reason", and approved StRS REVIEW-015 says the writer is told.
- C4: keep the REVIEW-003 text, correct the log and the PR wording so the owner reviews what changed.

## Blocker

- A0 Security. `src/session/features/sourceEdits.ts:541` and `describe` below it: a dropped `.md` is read
  (up to 64 KiB, first heading) with no `ResourcePolicy`, in a preview with restricted reads. The removed
  `preview.readOnly` gate was the only guard. With `preview.restrictedReads`, skip the title read or go
  through the policy; write the link without a title. Test it with a `.md`:
  `test/session/dropFiles.requirements.test.ts` only drops a `.png`.

## Major

- A1 `READ_ONLY_FILE` exists only at `sourceEdits.ts:128` (toggles). Every other write path answers
  success on a file VS Code holds read-only: label rename `:180`, thread reply and delete `:232`, find
  replace `:308`, move `:358`, cut `:451`, paste `:497`, drop `:569`, `frontmatter.ts:356`,
  `blockEdits.ts:324`. `handlePasteImage` leaves an orphan image. Move the written check into
  `SourceEditController.apply` and the frontmatter and block paths. Tests on each family, including with
  restricted reads, with `@tests_req` TRUST-001. Requirements affected: TRUST-001, TRUST-005, REVIEW-015,
  BLOCK-025. VS Code's behaviour is known from the code comment and `test/integration/radioChoice.test.ts`.
- B1 `test/integration/blockClipboard.test.ts:177`: the Copy in `runUntrusted` has no retry after the move
  undo; it can be dropped as stale in the heavy run. Retry until the clipboard changes.
- B3 `test/integration/commentWrite.test.ts:226-238`: reply, resolve and delete lost their restricted
  coverage, here and in `test/session/reviewReqComments.requirements.test.ts:326`. Restore all three.
- C1 StRS BLOCK-001 (`:52`, also `:6-9`, `:37`) still says no Edit button in an untrusted workspace.
- C2 StRS FMEDIT-008 (`:80`, `:10`) still refuses a metadata edit in an untrusted workspace.
- C4 StRS REVIEW-003 `:69` deleted the reason, while `tiers/log.md:22-23` and the PR text in
  `reports/T1-r1.md` say it was replaced. REVIEW-015 `:51` also adds "Every preview offers the thread
  controls": say so in the same place.

## Minor

- A3 Drop on a standalone file is refused (`sourceEdits.ts:541`, `folderOf`), against TRUST-005.
- A4 `package.json:38` and `docs/user/editing.md`: images also come from the workspace folder (TRUST-002).
- A5 `previewManager.ts:448`: promotion closes an open editor with no flush; flush as at `:392`.
- A6 `hostRequests.ts:72`: orphaned doc comment.
- A7 `pageChromeStyles.ts:457`: dead CSS, wrong comment.
- B4 `blockClipboard.test.ts:163-190`: Cut no longer tested with restricted reads.
- B5 `commentsEnabled` has no unit test since `editingBootState` was deleted.
- B6 `test/security/readOnlyRoot.requirements.test.ts:125-131`: use the production root, cover a non-image
  file, assert the refusal codes of TRUST-002.
- B7 `test/visual/scenarioIds.ts:595`: the v02 lock describes a click that v02 does not do.
- B8 Stale wording: `lifeReq.requirements.test.ts:437,507,528,538,570`, `toolbarReq.requirements.test.ts:57`,
  `workspaceDisposal.test.ts:65,70`, `readOnlyLocalRoots.test.ts:1`, `realInput/harness.ts:426`,
  `r01-untrusted-read-only`, `scenarioUntrustedReadOnly`, `inlineThread.test.ts:85`.
- C5 SwRS PALETTE-192 `:43`, `:6`: "for a trusted, saved document".
- C6 SwRS PALETTE-213 `:59`: "including a read-only one".
- C7 SwRS TRUST-001 `:104` cites superseded DIAG-025; use DIAG-024.
- C8 `tiers/log.md:12,20`: heading wrong for superseded and draft ids; `:26` gives no results.
- C9 Follow B8 in the requirements that quote those titles (REVIEW-171 `:83`, LIFE-143 `:99`, TRUST-001);
  "writable preview" in REVIEW-038, TOOLBAR-001, TRUST-007.

## Not covered by this inspection

Nothing executed. Real VS Code behaviour on a read-only file; `src/host-vscode/activation.ts`; `test/site/*`;
`renderReq.codeCopy` and `renderReq.labelRename`; line-by-line meaning of proposed SwRS outside TRUST-001, 002,
005, 006; `08-okf-schema` yielding 5 edit cells; the dirty document left by the standalone suite.
