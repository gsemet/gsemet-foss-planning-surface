# T19 implementation — round 2

STATUS: DONE

## Summary
Fixed review finding 1. The two radial-gradient edge shadows in `previewStyles.ts` now use
`color-mix(in srgb, var(--vscode-foreground, CanvasText) 35%, transparent)` instead of black at 0.28,
and are `1rem` wide instead of `0.75rem`. The regex test was extended first, and it failed. A light
counterpart scenario `code-light-table-narrow` was added. Everything else from round 1 is unchanged.

## Files changed
- src/preview/previewStyles.ts — theme-aware, wider shadows
- test/webview/previewStyles.test.ts — regex also asserts the color-mix right shadow
- test/visual/scenarios.ts — new `code-light-table-narrow` (fixture 04, 640 px, light, full page, `identifier-split`)

## Tests written first (failing before the fix)
- overflowing content tables keep short cells whole and show scroll shadows — failed on the new regex (unit gate FAIL, logs/T19-impl-unit.log from the first run, overwritten by the passing run)

## Tests added or changed
- the test above (regex tightened, not weakened); visual scenario `code-light-table-narrow`: PASS

## Existing assertions changed
- previewStyles.test.ts: "overflowing content tables keep short cells whole and show scroll shadows" — old: `radial-gradient\(farthest-side at 100% 50%/` → new: `…at 100% 50%, color-mix\(in srgb, var\(--vscode-foreground/` — required by: review finding 1 (T19 own test, added in round 1)

## Verification
- `gate.sh T19-impl unit types trusted visual` → compile, unit, types, trusted PASS; visual PASS vs baseline (0 new failure lines, 4 baseline lines now passing). Logs: logs/T19-impl-*.log, logs/visual-T19-impl/

## Evidence for reviewers
- logs/visual-T19-impl/code-dark-table-narrow.png and code-light-table-narrow.png (both read). Zoomed crops of the right edge: the light theme shows a clear grey shadow at the right edge of the body rows. The dark theme shows a visible lighter band at the same place. It is subtler than in light, but now perceptible. The header row cells have their own background, so the shadow shows mainly on body rows.

## Feedback addressed (rounds 2–3)
- Finding 1: theme-aware colour, 1rem width, test regex, light scenario, both screenshots checked.
- Finding 2: follow-up only, untouched.

## Open points / STOP reason
- None. The dark cue is subtle; raise the 35% if the reviewer wants it stronger.
