# Before and after, CR-463

After: pushed head 1dd3e76829b3e7711ee0890e1f4f946f7f615205 (captures v31 to v36 here, light and dark).
Before: base 58b4c302 (origin/main). The scenarios v31 to v36 do not exist at the base (they are added by this CR) and the base renders no tooltip, no removed marker and no single card, so no before capture is possible with them: the before state is the same page with only the green bars (the unchanged part of each after image). Not captured separately.

Reproduce the after: `npm run visual:render`, then
`uv run --no-sync --group docs python test/visual/capture.py --scenario review-annotations/v31-change-bar-tooltip-light-900 ...` (v31 to v36).

- v31/v32: green bar tooltip "Changed line 7 since last commit" (light/dark).
- v33/v34: red marker with tooltip "Removed lines 21-23 since last commit" (light/dark).
- v35/v36: single side-by-side card (last commit left, now right) over the changed heading, red marker still shown (light/dark).
Paths: none on screen.
