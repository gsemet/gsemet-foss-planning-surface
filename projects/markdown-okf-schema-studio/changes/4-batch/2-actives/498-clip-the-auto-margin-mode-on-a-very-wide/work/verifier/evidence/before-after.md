# Before and after, CR-498

- Base (before): af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea
- Head (after): 37ef61b338b3ca56d1cb428983c78ebdb54684f0

No before/after pair was captured: the change adds a new clip, and the base holds none of it
(`git ls-tree -r --name-only af4a4aa6 -- docs/demo-video/clips/wide-table-auto-width` lists 0
files). The extension does not change (no `src/` file in the diff).

The comparison the clip itself shows is in its committed key frames at the head:
`docs/demo-video/clips/wide-table-auto-width/frames/margin.png` (the table cut at the column) and
`frames/auto.png` (the table broken out, centred, the paragraph unmoved). To reproduce the checks,
see `work/verify.md`.
