# SC19 evidence: bytes of the new cards, topics and floor (round 1)

Measured with `wc -c` on LF files, no BOM, at the worktree `batch-31-CR-505`, under `skills/chantier/cards-next/`.

| File | Bytes | Budget | Within |
| --- | --- | --- | --- |
| coder.md | 1434 | 1500 | yes |
| conflict-resolver.md | 1378 | 1500 | yes |
| debugger.md | 1165 | 1500 | yes |
| investigator.md | 1370 | 1500 | yes |
| demo-explorer.md | 1487 | 1500 | yes |
| spec-writer.md | 1498 | 1500 | yes |
| spec-critic.md | 1499 | 1500 | yes |
| retro-critic.md | 1492 | 1500 | yes |
| inspector.md | 1985 | 2000 | yes |
| verifier.md | 2991 | 3000 | yes |
| griller.md (the whole file is the section) | 1630 | 2000 | yes |
| floor.md | 554 | copy | byte-identical (`cmp` empty) |
| topics/worker-shell.md | 1219 | 1500 | yes |
| topics/verifier-scratch.md | 1385 | 1500 | yes |
| topics/verifier-description.md | 1325 | 1500 | yes |
| topics/verifier-review-box.md | 461 | 1500 | yes |
| topics/verifier-delta-matrix.md | 1492 | 1500 | yes |
| topics/verifier-before-after.md | 1172 | 1500 | yes |
| topics/verifier-images.md | 1328 | 1500 | yes |
| topics/inspector-audit.md | 1123 | 1500 | yes |
| topics/spec-writer-extras.md | 954 | 1500 | yes |

Cards over budget: none. No card goes in Known gaps for size.

Old card bytes at HEAD, for the cut: coder 4609, conflict-resolver 3893, debugger 3682, investigator 3554, demo-explorer 3422, spec-writer 3254, spec-critic 3729, retro-critic 2901, inspector 6044, verifier 14581, griller.md 10757 (its "Started from the board" section 2198).
