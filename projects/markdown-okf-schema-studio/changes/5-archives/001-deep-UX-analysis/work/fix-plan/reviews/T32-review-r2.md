# T32 review — round 2

Base: 29a3df8 · Reviewed diff: 5 files, +375/-2

## Gates
- compile, unit, types, contracts: PASS (logs/T32r2-*.log).
- full: PASS (logs/T32r2-full.log), which makes three clean full runs (T32-impl2-full, T32-impl2c-full,
  T32r2-full). The RI-T21 failure from round 1 did not come back.
- visual: PASS vs baseline, 0 new. The `failed:` lines in the log are the known baseline entries.
- Base measurement: RI-T32 list **fails at 29a3df8** (drift 22 px, logs/T32-base-29a3df8-trusted.log).
  With this branch the drift is 0.

## Done-when
- [x] unit, trusted and scroll gates pass. Evidence: the gate logs above.
- [x] RI-T32 passes, with before and after drift recorded. List: 22 px before, 0 after. Second
  render: T2 drift 0, and T3 1.5 s later within 3 px. Table: drift -0.39 against Tcommit.
- [x] R7 holds across the save render and a later render with no pin. Evidence: unit test
  "previewReady reports the pinned anchor only when the load restored a pin", plus the RI-T32
  T2/T3 checks.

## Protected features checked
- P-N1 R6 (initial anchor with no save): unchanged. The pin branch runs only when `initialPin` is
  set. `previewReady` adds `anchorLine` only when `pinApplied` is true, so loads without a pin send
  the same message as before. The unit test asserts this, and the existing restore tests pass.
- P-N1 R4 (source-led scrolling): untouched.
- Echo guard: the pin restore uses `programmaticScroll`. OK.
- P-S2: edit version checks are unchanged. The pin is now stored only on accepted paths:
  `handlePreviewEditSave` stores it when `final` is true, and `handleFrontmatterSave` stores it after
  `applyEdit` returns true. The round-1 read-only NIT is resolved.
- P-E8: no new controls.
- Webview template rules (§2): the added runtime code has no backtick, no `${` and no global
  `setTimeout`. OK.
- Message validation: `validPin` is unchanged since round 1 and is correct.

## Round-1 findings
1. `previewReady` anchor: resolved. Unit test added, and the E2E re-measures T2 and T3 give drift 0.
   There is no red-first run, but the E2E second render is direct behavioural evidence. The unit
   test cannot pass on the r1 tree, because `anchorLine` was absent there. Accepted.
2. `minVersion`: implemented. I checked the claim in `refreshPreview` (extension.ts ~2433). It skips
   change events while `activeBlockEdit.applying` is true. `applyEdit` fires the change event before
   its promise resolves, so the preview's own autosaves do not start a render while the editor is
   open. The guard can only matter for a render that was already in flight or was started from
   outside. That makes it a cheap defensive guard: it never consumes the pin early, and the 5 s
   expiry bounds it. Accepted without a test (see finding 2).
3. List case: resolved. The reading line is inside the list, and the test fails at base with 22 px.
4. Table case: resolved for R7. See the note below.
5. RI-T21: three clean full runs. Resolved.
6. Pin store location: resolved.

## Orchestrator notes, answered
- **Table case.** T0=299 and Tcommit=38.5 come from the separate typing-jump issue. The R7 check
  compares Tcommit (38.5) with T1 (38.1), and the table stays inside the viewport. That still proves
  R7 across the save render. The short document gives only about 260 px of scroll room. With the
  table near the end of the document, clamping to `maxScrollTop` could hide a drift if the save
  render were short of room. Here Tcommit sits at the clamp boundary, so the table case is weaker
  evidence than the list case. The list case, which fails at base, carries the main proof. MINOR
  follow-up (finding 3).
- **`takePendingPin` comment vs code.** The code is right. A render of an older version must not
  pin, because the edited text is not in it yet. The comment is wrong (finding 1).
- **No red-first for finding 1.** The T2/T3 E2E is enough, see above.

## Findings
1. [NIT] src/extension.ts: the `takePendingPin` doc comment says an older-version render "gets it
   without consuming it". The function returns `undefined` for such a render and keeps the pin. Fix:
   change the sentence to "A render of an older document version (for example an in-flight autosave
   build) does not get the pin and does not consume it".
2. [MINOR] src/extension.ts: `takePendingPin`. The `minVersion` branch has no test, because no unit
   seam exists. Log in followups.md: if an extension-host unit seam is added later, cover three cases
   (older version keeps the pin, current version consumes it, expired pin is dropped).
3. [MINOR] test/integration/realInput.test.ts: RI-T32 table. Once the typing-jump issue is fixed,
   move the table to mid-document with filler below it, so the drift check does not sit at the
   scroll clamp. Assert |T1 − T0| ≤ 3 instead of measuring against Tcommit. Log in followups.md.
4. [NIT] `src/extension.ts.orig` is an untracked leftover. It is not in the diff. Delete it before
   the commit, and do not commit it.

## Existing assertions changed
None. `git diff 29a3df8 -- test/` has no removed lines. OK.

VERDICT: PASS
