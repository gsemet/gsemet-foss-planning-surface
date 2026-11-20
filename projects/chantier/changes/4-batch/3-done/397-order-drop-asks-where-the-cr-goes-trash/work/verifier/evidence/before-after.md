# Before / after: `order drop` and its destination

Before: base `9ff16d56355e5af44f639b093c9db9b43bad587d` (CR-396's branch), a detached worktree's source (removed at the end).
After: head `a872a662c025bd2ca2c1808abade5fe1134a6e18`.
Both run in a throwaway scratch repository (`work/scratch/p0`, `p1`, removed), a batch of CRs opened with `chantier open`.

## Pair 1: a drop with no destination, then with `--note P2`

Reproduce: file and open a batch, `chantier foreman set f --epoch 1`, then
`chantier order drop CR-101` and `chantier order drop CR-102 --note P2`.

Before (9ff16d56):
```
[chief-of-staff->foreman] order O-1: drop CR-101
dropped CR-101: 6-trash/261120-0327-101-one-item        exit=0
[chief-of-staff->foreman] order O-2: drop CR-102 P2
dropped CR-102: 6-trash/261120-0327-102-two-item        exit=0   (P2 ignored: trash)
```

After (a872a662): see verify.md claims 1, 3: no `--note` exits 1 and records nothing;
`--note p2` gives `dropped CR-103 to 2-backlog/P2: 2-backlog/P2/103-gamma-item`.

## Pair 2: the label in STATUS.md

Before (9ff16d56): both cancelled CRs read `[dropped]` (the trash was the only exit).
After (a872a662): `[dropped to 2-backlog/P2]`, `[dropped to 1-inbox]` and `[dropped]` (trash), verify.md claim 7.

No screenshots or videos: the pane screenshot is a named Known gap of the PR.
Note: a base worktree under the scratch folder failed ("Filename too long" on the repository's demo files); it was made at a short path
inside the CR worktree instead, and removed.
