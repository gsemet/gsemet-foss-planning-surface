status: done · PR merged by the user 2026-10-23T14:21Z (rebase, main 98195d9) · F done
head: 20a2d43 (PR head 2e62d6b = merge of main) · branch test/real-window-t2-final · worktree ../markdown-okf-schema-studio-wt-043
PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/36 · runs: PR 39965946197 (checks success), heavy 39966448771 (all jobs success, gallery success)
next: none (follow-ups in followups.md: 6 removed captures, local macOS undo failure, README refresh)

## Log
- Local full integration (2 runs) and origin/main local run: checkbox "one undo" fails on this Mac (pre-existing, VS Code 1.143.0 local vs 1.143.1 CI): see followups.md.
- Local: full real-input suite stops at the existing undo step (17 captures passed before it); the 4 new scenarios in stress mode: 5/5 each, untrusted capture passed in the full run.
- CI stress run 39963915074 (bc414d4): all 16 scenarios 20/20. Heavy 39966448771 (20a2d43): 9 trusted + untrusted 20/20.

- F: gallery from heavy run (new captures present); README: committed = B0, CI Linux differs (fonts), local macOS 12/15 match, 3 changed by the toolbar comment button (main); images/ not committed; inventory.md regenerated (old kept as inventory-b0.md), 110/110 real PNGs found.
