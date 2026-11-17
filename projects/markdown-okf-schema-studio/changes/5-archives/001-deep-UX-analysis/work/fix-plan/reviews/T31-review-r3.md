# T31 review — round 3 (base fed90bd)

## A. Scope
- Round-3 changes: `src/extension.ts` (test counter) and `test/integration/realInput.test.ts`
  (additions in RI-T31 case A and RI-T31b). Both files are allowed. No frozen behaviour touched.

## B. Correctness
- `restoreCalls` is a field on `ActivePreview`, set to 0 in `createPreview`, incremented as the first
  statement of `restorePreviewState`, and read only by `getActivePreviewForTests()`
  (`restorePreviewStateCalls`). Nothing branches on it: a pure test hook, no behaviour change.
- The counter lives on the preview object, which is reused across re-renders (re-renders do not call
  `createPreview`), so it does not reset between the "before" read and the assertion.
- Callers of `restorePreviewState`: the `becameVisible` branch of `onDidChangeViewState`, and
  `restorePreviewStateForTests()`, which neither RI-T31 nor RI-T31b calls.

## C. Tests (failing power, by code reading)
- RI-T31b: opening `other.txt` creates no preview, so `activePreview` is still the test's preview
  when the counter is read before and after `panel.reveal`. The only path that can raise it is the
  hidden → visible branch. Without that branch, the `waitFor(... >= before + 1)` times out. This
  closes round-2 finding 1.
- RI-T31 case A: at base, the handler called `restorePreviewState` whenever `panel.visible` was
  true (verified with `git show fed90bd`). Clicking into the editor changes the panel's `active`
  state, which fires `onDidChangeViewState` while the panel stays visible. So the old code raises
  the counter and `strictEqual(count, before)` fails. This guards H1 directly. There is a single
  preview, so the assertion cannot pass vacuously by reading another preview's counter.
- No existing assertion was modified or weakened.

## D. Regressions
- Gates T31r3 compile, unit, types and full all PASS. In `T31r3-full.log`, case A has
  Y0=Y1=Y2=1200, case B moves 0.4 px, and RI-T31b has an anchor distance of 1.
- P-N1 is now guarded by RI-T31b. P-N2 and R7/D-18 are unchanged since round 1.

## Findings
- [NIT] An untracked `src/extension.ts.orig` exists in the working tree. It is not part of the
  diff, but it should not be committed.

VERDICT: PASS
