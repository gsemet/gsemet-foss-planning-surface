# Before and after

- After (head 4e0de99c2d9513b3464e238f45c12b201ce84f62): `direct-box.png`, the direct box of `docs/batch-lifecycle.svg`, 3x crop. Reproduce: headless Chrome `--screenshot` of an HTML page that shows the SVG as an `<img>` cropped to the box (left -50px, top -516px, 1310px wide, window 340x130, scale 3). It shows the title "direct mode: while running" and two lines, all inside the box; no path or username.
- Before (base): not captured. The old box text ("strict while running") is read from the diff; a before image adds nothing to the claim, which is the new text's fit. Not a failure.
