# T23 implementation — round 2

STATUS: DONE

## Summary
Addressed review finding 1: added the missing unit test that blur/focusout toward the field actions
does not save, for the value editor, the key editor and the list editor (focusout toward the
picker). No source change was needed: the blur guards in scrollSync.ts were already correct. The
test initially failed only because the fake DOM `closest` did not resolve `[data-okf-frontmatter-menu]`;
the harness was extended.

## Files changed
- test/webview/scrollSync.test.ts — new test; `RuntimeElement.closest` supports `[data-okf-frontmatter-menu]`

## Tests written first (failing before the fix)
- "frontmatter blur toward the field actions does not save" — failure excerpt: `1 !== 0` (saves posted on blur toward the Add button). Cause: harness `closest` lacked the menu selector, not a source bug (real DOM `closest` resolves it; the menu carries the attribute).

## Tests added or changed
- "frontmatter blur toward the field actions does not save" — value editor (text textarea), key editor, list editor `focusout`: with relatedTarget inside the menu/picker no `previewFrontmatterSave` is posted and the menu stays inside the editor; with relatedTarget null exactly one save is posted.
- Harness: `closest("[data-okf-frontmatter-menu]")` added (support code, no assertion changed).

## Existing assertions changed
- none in this round.

## Verification
- `gate.sh T23-impl unit types trusted visual` -> compile/unit/types/trusted PASS, visual PASS vs baseline (0 new failure lines). Logs: PLAN/logs/T23-impl-*.log.

## Evidence for reviewers
- Unit run: 533 pass, 0 fail.

## Feedback addressed (rounds 2–3)
- Finding 1: test added as described (all three editors); no save-on-blur bug found.
- Findings 2–4: no change, per instructions.

## Open points / STOP reason
- Finding 2 (list focusout now saves when focus leaves the picker for outside the row) should be recorded in followups by the orchestrator.
