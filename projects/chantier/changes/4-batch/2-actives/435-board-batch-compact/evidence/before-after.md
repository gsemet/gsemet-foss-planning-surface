# CR-435 before and after

Before: origin/main 33d10454 (detached worktree, removed). After: 2004e521db9acf1b8d752f0f5b7cb422d7939108. Demo from docs/demo copied by
scripts/docs_screenshots.py helpers (made-up paths via its fix routes, fixed clock). One-off Playwright
script: work/verifier/measure.py (batch shop-api, closed batch mobile-app batch-01); work/verifier/nocr.py.
Reproduce: uv run --with playwright work/verifier/measure.py <checkout> <before|after> <outdir> <tmp>.
Raw numbers: measure-before.json, measure-after.json.

| Pair | Shows |
| --- | --- |
| batch-pc-before.png / batch-pc-after.png (1400x860) | mode band and legend row gone; tab bar top 353 -> 263 (90 px higher); .bhead top 143 -> 143 |
| batch-phone-before.png / batch-phone-after.png (375x812) | Batch, navigator, then two pills on one line; hint and switch hidden; scrollWidth 375 = innerWidth |
| batch-pc-tip-mpill-after.png, batch-pc-tip-lgpill-after.png | each tip whole above the figures' tiles |
| batch-phone-tip-mpill-after.png, batch-phone-tip-lgpill-after.png | each tip opened by focus, inside the 375 px viewport |
| closed-pc-before.png / closed-pc-after.png | closed batch-01: mode and legend in the title row, figures, deps note, view switch |
| nocr-pc-after.png | scratch batch with no CR (open, no order add): mode only in the title row, figures, empty state |

No before for the tips and for the no-CR batch (no such element or page state to compare). Phone: .bhead top
moves 155 -> 176 (the pills take one new line in the title row); the spec's "figures do not move" is stated for
1400 px.
