# Before / after (CR-459)

Before: base dce2c644 (detached worktree, removed). After: a2a083af9e92e5949c683fae754752999b542618.
Reproduce: `uv run --with playwright python -I verifier/probe.py.txt <checkout> <tag> <outdir>` (copy it to probe.py first; it uses
scripts/docs_screenshots.py of the checkout: demo copy, board on loopback, clock fixed). Data in before.json / after.json is in verify.md.

| Pair | Shows |
| --- | --- |
| before-desktop-folded.png / after-desktop-folded.png | Graph tab, 1600x900, demo batch-03 (before has no chip, scrolls sideways 1502 > 886; after fits) |
| after-desktop-hover.png | CR-148 hovered: its waits' cards lit, 2 lit arrows into it |
| after-desktop-unfolded.png | chip on, CR-141 back in level 0 |
| before/after-desktop-closed.png | closed record batch-01 of mobile-app: no chip, same |
| before/after-phone.png | 375x812 |
