Before: d05934da (CR-500 head, detached worktree, removed). After: f7b74e64be590ce2650b03f5209dbc7b00b040cd.
Pair: briefs-base.txt / briefs-head.txt: 360 `brief` calls (2 hosts x 18 roles x 5 units x epoch or not), identical. Reproduce: in-process `chantier.cli.main(["brief", ...])` from each tree's src, brief file hashed with the root path normalised.
