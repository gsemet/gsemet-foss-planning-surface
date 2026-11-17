# T14 implementation — round 2

STATUS: DONE

## Summary
Addressed review r1. RI-T14 now asserts the exact first line. The editing-element choice is factored
into one helper `editingElementFor(target)` (returns `{ element, sourceRange }`) used by both
`openMappedEditor` and `clickCaretContext`; it returns the list only when `sourceRangeForList`
yields a range, else the target, so both always agree. Added the fenced-code mapper unit case.

## Files changed
- src/webview/scrollSync.ts — `editingElementFor`; used by `openMappedEditor` and `clickCaretContext`.
- test/integration/realInput.test.ts — RI-T14 single exact assertion.
- test/webview/textEditing.test.ts — fenced code case.

## Tests written first (failing before the fix)
- Not applicable this round (review fixes: stricter assertion, refactor, documenting case). The stricter RI-T14 assertion passes against the existing behaviour.

## Tests added or changed
- RI-T14: `assert.match(firstLine, /^Alpha (?:Xbravo|bXravo|brXavo|braXvo|bravXo|bravoX) charlie$/u, ...)` replaces the two loose assertions.
- mapRenderedCaret "fenced code with underscore": `foo_b` before-context maps to `foo_b|ar = 1`, no crash.

## Existing assertions changed
- RI-T14 assertions from round 1 (my own new test) tightened as per finding 1. No other existing assertion changed.

## Verification
- `gate.sh T14-impl unit types trusted visual` -> compile/unit/types/trusted PASS; visual PASS vs baseline, 0 new failure lines (logs/T14-impl-*.log)

## Evidence for reviewers
- Real-input screenshot `20-caret-at-click`.

## Feedback addressed (rounds 2–3)
- Finding 1: exact regex as written; trusted gate passes with RI-T14.
- Finding 2: `editingElementFor` shared helper, including the undefined-range case.
- Finding 3: unit case added; no source change needed.

## Open points / STOP reason
None.
