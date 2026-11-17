# T19 implementation — round 3

STATUS: DONE

## Summary
Round-2 finding 1 fixed: both `radial-gradient` shadow layers in the overflow rule now use
`var(--vscode-editor-foreground, var(--vscode-foreground, CanvasText))` (35%, 1rem unchanged), so the
cue no longer falls back to black in the visual harness. The dark capture now shows a clear lighter
band at the right edge. Nothing else changed.

## Files changed
- src/preview/previewStyles.ts — foreground variable chain in both radial layers
- test/webview/previewStyles.test.ts — second regex of the T19 test now ends with `color-mix\(in srgb, var\(--vscode-editor-foreground, var\(--vscode-foreground`

## Tests written first (failing before the fix)
- overflowing content tables keep short cells whole and show scroll shadows — unit gate failed (exit 1) with the tightened regex before the CSS edit (log was overwritten by the passing run; the failing line was `✖ overflowing content tables keep short cells whole and show scroll shadows`)

## Tests added or changed
- same test: regex tightened (not weakened) to require the editor-foreground-first chain.

## Existing assertions changed
- None beyond the T19-own regex above.

## Verification
- `gate.sh T19-impl unit types trusted visual` → compile/unit/types/trusted PASS; visual PASS vs baseline (0 new failure lines) (logs/T19-impl-*.log)

## Evidence for reviewers
- Screenshots: .agents/changes/requests/deep-UX-analysis/fix-plan/logs/visual-T19-impl/code-dark-table-narrow.png and code-light-table-narrow.png
- Pixel samples (grayscale, 1x of the 1280-wide capture, body rows y=2280/2360/2440, x from 1110 to 1174 in steps of 4, approaching the right edge; cell background first):
  - Dark: y=2360: 31 … 31, 32, 40, 49, 57, 66, 74, 82 (background 31, edge 82, difference 51). y=2280 peaks 67 (36), y=2440 peaks 76 (45).
  - Light: y=2360: 255 … 255, 254, 244, 234, 224, 215, 205, 196 (background 255, edge 196, difference 59). y=2280 peaks at 214 (41), y=2440 at 203 (52).
  - At the cell rows with the strongest cue (y=2360, 2440) both themes exceed 40 levels; y=2280 dark is 36, light 41.
- Pillow was not fetchable via `uv run --with pillow` (offline); used the cached Pillow from the uv cache with python3.13.

## Feedback addressed (rounds 2–3)
- Finding 1 (MAJOR): done as written, with test first and pixel evidence above.
- Finding 2 (MINOR, carried): not addressed, follow-up only as the review stated.

## Open points / STOP reason
- Sample y=2280 in dark is 36 levels (just under 40) at the very first body row sampled; rows 2360 and 2440 exceed 40.
