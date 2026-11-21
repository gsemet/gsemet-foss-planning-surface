# CR-455 debugger, round 4: T2 "Timed out waiting for the cursor in the real original side" (runs 44916057996, 44917868136)

Repro: `gh workflow run ci.yml --ref chantier/batch-07/cr-455-... -f heavy=true`, job `integration`, step `diff-preview`.
No local run is possible (no xvfb VS Code test host here); the proof below is VS Code's own code, read from the
installed VS Code 1.147.0 (`%LOCALAPPDATA%/Programs/Microsoft VS Code/8a14f0cc1b/resources/app/out/vs/workbench/workbench.desktop.main.js`)
plus the two CI logs.

## Cause (proven, test bug): the test uses the wrong side command

`workbench.action.compareEditor.focusPrimarySide` is registered as `focusInDiffEditor(args, 1)` and
`...focusSecondarySide` as `focusInDiffEditor(args, 0)`; the handler does:
`case 0: getOriginalEditor().focus(); case 1: getModifiedEditor().focus()`.
So PRIMARY = MODIFIED (right), SECONDARY = ORIGINAL (left). The test assumed primary = original (left).

- T2 diff = (original: real b.md file, modified: virtual `studio-diff-test`). `focusPrimarySide` focuses the
  modified = virtual side, so `activeTextEditor.document.uri.scheme === "file"` is never true: timeout after the
  10 s default of `waitFor` (log: step 14357 ms = ~4 s of T1/T2 setup + 10 s wait; same in r2 and r3).
- T3 (original virtual, modified file) would also fail with the same wrong command: it waits for SCHEME after
  `focusPrimarySide`, which gives the file side. T5 does not depend on the side. T6 (both virtual) passes only by
  accident (modified = virtual index).

## The webview-focus hypothesis is false

`getActiveTextDiffEditor` iterates `[activePane, ...visibleEditorPanes]` and returns the first text diff pane, so
the focus command works even while the preview webview holds the focus. `refocusDiff` (vscode.diff reopen) and
`focusFirstEditorGroup` are not needed for the command to act; (round-2 note that the webview stole the focus
was a reasonable but unneeded step; keeping `refocusDiff` is harmless, dropping it is cleaner). The
windowFocus.ts l.112 comment (focusFirstEditorGroup adds a focus move of its own, lands on whichever group is
first) is valid: do not use that command.

## Fix (test only, test/integration/diffPreview.test.ts)

1. l.112 (T2), l.143 (T6 keep either): to focus the ORIGINAL side use `workbench.action.compareEditor.focusSecondarySide`.
   - T2: `focusSecondarySide`, wait scheme === "file", `cursorBottom` (the `refocusDiff` call before it may stay).
   - T3 l.124: `focusSecondarySide` (original = virtual, wait SCHEME) .
   - T5 l.133 and T6 l.143: either command (T6: `focusSecondarySide` gives virtual head, also SCHEME). Prefer
     `focusSecondarySide` everywhere "original" is meant, and say in the comment "primary = modified".
2. Layout robustness: `diffEditor.useInlineViewWhenSpaceIsLimited` (default true, threshold 900 px) can turn a
   side-by-side diff inline in a small CI window; set it to `false` in `withLayout` for `sideBySide === true`
   (and restore) so the original editor really exists. Cheap and removes one unknown.
3. Inline T2: keep as is (no scroll assert); inline has no separate original editor, `getOriginalEditor().focus()`
   there is not meaningful. Inline T1 (file on the modified side) should pass like side-by-side T1 (T1
   side-by-side passed in run 44914183706); unproven in inline.

## Prediction

- T2 side by side: ~80% to pass with `focusSecondarySide` (focus is then provably on the file's original editor;
  `cursorBottom` scrolls it, the visible-range event of that real editor reaches `syncEditorToPreview`, the same
  path T1 proved on the modified side). Residual 20%: original-side visible-range reporting in the ext host,
  CI window size (fix 2).
- T3 ~85%, T5 ~85% (follows the active diff, independent of the side), T6 ~85% (vacuity now excluded since
  the cursor is in a diff editor and the check asserts the scheme).
- Inline T1 ~75%, inline T2 (open-only asserts) ~90%.
- Least provable in CI if it still fails after this fix: the T2 side-by-side original-side scroll assertion, and
  inline T1 (layout-dependent). Per the fallback, drop those two first; keep side-by-side T1, T4 (manifest), T3, T5,
  T6 (they need no scroll of the original side) and the unit tests.
