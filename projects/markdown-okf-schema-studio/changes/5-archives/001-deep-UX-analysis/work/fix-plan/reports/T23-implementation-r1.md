# T23 implementation — round 1

STATUS: DONE

## Summary
Frontmatter field actions (Add field / Remove field / picker + Add) now render inside the editing
cell, in normal flow after the control and status (`edit.editor.appendChild(menu)`), with text
labels. `positionMenu`, its scroll/resize listeners and the CSS custom-property writes are gone.
The pseudo-tooltip is disabled for this menu (`content: none`); native titles/aria-labels stay.
Text values open a one-row textarea (`rows = 1`, CSS min-height 1.6em).

## Files changed
- src/webview/scrollSync.ts — createFrontmatterMenu inside editor, labels, no positioning; closeFrontmatterEditor drops listener removal; text field rows=1
- src/preview/previewStyles.ts — static wrapping menu, labelled buttons, picker min-width 0, frontmatter selectors removed from shared tooltip rules + `content: none`, textarea min-height
- test/webview/scrollSync.test.ts, test/webview/previewStyles.test.ts — tests (below)
- test/visual/scenarios.ts — machineChecks on the 5 frontmatter editTarget scenarios
- test/visual/capture.py — placement checks (inside editor, static, not clipped, labels), "floating" wording removed
- test/integration/realInput.test.ts — RI-T23 added; selectors narrowed (see below)

## Tests written first (failing before the fix)
- "frontmatter field actions render inside the edited row" — `AssertionError: name` (menu.parentElement not the editor)
- "frontmatter text values open a one-row textarea" — `actual: 2, expected: 1` (rows)
- "field toolbar adds and removes fields" (placement assertion) — `actual: 'below', expected: null`
- RI-T23 and the previewStyles test were not run against the old code (no stash/checkout allowed); the old menu was `position: fixed`, so RI-T23's `static` assertion cannot pass on it.

## Tests added or changed
- scrollSync: inside-editor (name + value editors), labels `Add field`/`Remove field`/`Add`, no position props after scroll/resize; one-row textarea.
- previewStyles: static menu rule, no fixed/z-index, labelled buttons, `content: none`, no hover tooltip selectors, textarea min-height.
- RI-T23 (1100x900 viewport, frame width asserted 480-620 px): value editor of `scope`, then Add field; both captures with required overlay-covers-text and overlay-clipped (PASS).

## Existing assertions changed
- scrollSync.test.ts: "frontmatter floating bar follows the active field…" — old: floating placement/`--sphinx-preview-frontmatter-menu-*` → new: renamed "frontmatter field actions render inside the edited row" (listed).
- scrollSync.test.ts: "frontmatter field toolbar adds and removes fields" — old: `data-placement` "below", top "38px", left "8px" → new: placement null, top "" — required by: removal of floating placement (same behaviour change, not listed explicitly).
- previewStyles.test.ts: "control tooltips retain their offset…" — old: `.sphinx-preview-frontmatter-menu {… flex-wrap: nowrap}` → removed; new rule asserts `flex-wrap: wrap` in the new test (menu now wraps).
- realInput.test.ts (RI-T05/T06): `[data-okf-frontmatter-editor] select|input` → `> select|input` — the menu now lives inside the editor and its picker contains an input/select, which made the `count()===1` selector ambiguous. Same target element, no weakening.
- capture.py: "frontmatter editor still has action buttons" (`editor.locator("button").count() != 0`) → buttons outside `[data-okf-frontmatter-menu]` must be 0 — required by menu now inside the editor.

## Verification
- `gate.sh T23-impl unit types trusted visual` → compile/unit/types/trusted PASS, visual PASS vs baseline (0 new failures, 4 baseline lines now passing). Logs in PLAN/logs/T23-impl-*.log.
- An earlier trusted run failed once in RI-T21 ("Timed out waiting for StRS-A.md to become the active text editor", link-open focus; unrelated to the menu); rerun and the final full gate passed.

## Evidence for reviewers
- Visual: logs/visual-T23-impl/edit-frontmatter-value-dark.png (actions under the status select, inside the row, labels readable), edit-frontmatter-key-dark.png (menu below the key input; the native datalist popup overlaps it while open).
- Real input (540 px frame): .artifacts/real-input-kxxpOS/30-frontmatter-actions-value.png and 31-frontmatter-actions-picker.png — nothing covers another row; at 540 px the buttons and picker stack vertically inside the row, all machine checks PASS. I viewed the 31 capture and the two visual captures above; list/boolean captures were gated by machine checks only.

## Open points
- Visual `machineChecks` were added also to list and boolean scenarios (all five editTarget frontmatter scenarios); they pass.
