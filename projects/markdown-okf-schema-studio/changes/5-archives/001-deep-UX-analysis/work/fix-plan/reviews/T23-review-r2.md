# T23 review — round 2

Base: cf66e90 · Round-2 delta: test/webview/scrollSync.test.ts only (new test plus a one-line harness `closest` selector)

## Gates
compile/unit/types/trusted: PASS. Visual: PASS vs baseline (0 new failure lines), per the orchestrator.
Reviewer rerun: scrollSync.test.js 119 pass, 0 fail.

## Done-when
- [x] All round-1 items still hold. The source is unchanged since round 1.
- [x] Unit test "frontmatter blur toward the field actions does not save" (round-1 finding 1). It covers the value editor (textarea blur), the key editor (input blur) and the list editor (focusout toward the picker). Each case checks: no save while `relatedTarget` is inside the menu or picker, the menu stays in the editor, and exactly one save once `relatedTarget` is null.

## Mutation evidence (compiled out/ JS, restored afterwards; cmp verified)
For each mutation, `closest?.("[data-okf-frontmatter-menu]")` was replaced with a selector that never matches.
- Value-editor guard (scrollSync.ts:1027): the new test FAILS with `1 !== 0`.
- Key-editor guard (scrollSync.ts:1543): the new test FAILS with `1 !== 0`.
- List-editor guard (scrollSync.ts:1535): the test still passes. The picker is inside the editor, so the `editor.contains(relatedTarget)` clause on line 1534 already catches it, and the menu clause is redundant for this path. This is not a test defect: the behaviour is protected either way.

## Harness `closest` extension
The extension matches only elements that carry `data-okf-frontmatter-menu`. In the source, `[data-okf-frontmatter-menu]` is used with `closest` only in the three blur/focusout guards above. So the extension can only make those guards return early (fewer saves). No existing test asserts "no save" in a way that this change could satisfy vacuously: the suite passes, and the assertions that expect a save still observe it.

## Protected features checked
- P-E7 blur-save: the guard is now locked by a test for the value and key editors. Saving on blur outside the row is still asserted (one save each).

## Findings
- None blocking. Round-1 finding 2 (list focusout now saves when focus leaves the picker for somewhere outside the row) still needs to go in followups, as the report notes.

VERDICT: PASS
