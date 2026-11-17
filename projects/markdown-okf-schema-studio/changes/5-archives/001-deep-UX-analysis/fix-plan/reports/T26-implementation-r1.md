# T26 implementation — round 1

STATUS: DONE

## Summary
Invalid or unavailable frontmatter link values now show an icon plus a plain label (`✖ File not found`)
instead of `[E10]`. The span is keyboard-focusable and keeps its full-message `title`, which the
custom tooltip shows on hover and on focus (the tooltip selector now covers non-anchor link spans and
excludes pending ones). The header badge is a `<button>` that scrolls to and focuses the first issue
row and highlights it for 1.5 s. Diagnostic messages, resolution (UX-22) and value display (UX-24)
are untouched.

## Files changed
- src/frontmatter/propertiesTable.ts — `linkStatusLabel` (exported), icon+label span, `tabindex="0"`, badge as button with aria-label
- src/webview/scrollSync.ts — `linkTooltipSelector` replaces `a.okf-frontmatter-link` (3 uses); badge click handler (registered before the mapped-block click handlers, uses stopImmediatePropagation)
- src/preview/previewStyles.ts — button reset + focus-visible outline for the badge, `data-okf-issue-highlight` outline
- test/frontmatter/propertiesTable.test.ts — new tests
- test/webview/scrollSync.test.ts — new tests; harness extended (see below)
- test/webview/previewStyles.test.ts — new CSS test
- test/integration/realInput.test.ts — RI-T26

## Tests written first (failing before the fix)
(Compile failed first on the missing `linkStatusLabel` export; after adding only a stub export the unit run gave:)
- linkStatusLabel maps every diagnostic family to a plain label — `AssertionError: {"message":"target 'a.md' does not resolve to a file"}`
- invalid links show an icon and a plain label instead of the error code — `expected to not match /\[E10\]<\/span>/` (markup had `<span class="okf-link-status">[E10]</span>`)
- unavailable links use the warning icon — did not match `⚠ Link root unavailable`
- the header badge is a button that goes to the first issue — markup had `<span data-okf-badge …>`
- the issue badge is a plain button and a clicked badge highlights its row (CSS) — no `button[data-okf-badge]` rule
- an invalid link span shows its full message in a tooltip on keyboard focus — `TypeError: Cannot read properties of undefined (reading 'getAttribute')` (no tooltip created)
- the badge click scrolls to and focuses the first issue row and highlights it briefly — falsy `prevented`
- RI-T26 was written before the fix but not run red (trusted needs the whole bundle; it was run only after the fix).

## Tests added or changed
- the unit tests above, plus "a pending link never opens a tooltip" (guard for the new selector)
- RI-T26 (`scenarioReadableLinkDiagnostics`, screenshot `34-link-diagnostic-tooltip`): text has `File not found` and no `[E10]`; Tab reaches the invalid span and a `[role=tooltip]` containing `does not resolve` appears; clicking the badge after scrolling away brings the row into view with focus inside it
- Harness-only edits in scrollSync.test.ts: `RuntimeElement.closest` knows the new link selector and `[data-okf-badge]`; `RuntimeElement.querySelector` knows `[data-okf-edit-cell="value"]`; `document.querySelector` returns the frontmatter row for the issue-row selector only when the row has an issue class. No existing assertion changed.

## Existing assertions changed
- none. (No existing test asserted `[E10]`/`[W15]` text or a `span` badge; `data-okf-link-code` assertions still hold.)

## Verification
- `PLAN/scripts/gate.sh T26-impl unit types contracts trusted visual` → all PASS (unit 559/559; visual "PASS vs baseline", 0 new failures) — logs in `PLAN/logs/T26-impl-*.log`
- Red run log: `PLAN/logs/T26-impl-red-unit.log`

## Evidence for reviewers
- Screenshot from RI-T26: `34-link-diagnostic-tooltip` in the real-input evidence folder (see `T26-impl-trusted.log`)
- Visual screenshots: `PLAN/logs/visual-T26-impl`

## Open points / STOP reason
- Deviation 1: the tooltip selector is `.okf-frontmatter-link:not([data-okf-link-status="pending"])` (no `[data-okf-link-status]` presence requirement) because existing tooltip tests build links with only the class and I may not change them; real rendered links always carry the attribute, so behaviour is identical.
- Deviation 2: RI-T26 uses `resolution: document-relative` instead of project-relative, because project/bundle roots may be unavailable in the fixture (would give W15 "root unavailable" rather than "does not resolve").
- The label for a "was not found" filename-stem message is also `File not found`; "ambiguous" maps to `Several files match`.
- No nowrap added to `.okf-link-status` to avoid overflow at narrow widths.
- Reviewer should look at a screenshot with an invalid link in each theme (not captured per theme by me).
