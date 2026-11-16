# Retro: points the retro critic dropped

## 2026-11-16, batch-21: CR-296 (PR 247)

- Merged into the kept point: batch-20's record stays `running`; `pause` refused on an unmerged, stopped CR; the worktree branch named from the batch while the PR kept batch-20's branch.
- [chantier] The Driver was started and recorded before `take`, so its `writes:` line named the 1-pending folder: dropped, one 40-second unset and set, never seen by the user.
- [project] test_startup_manifest.py measured raw bytes and failed on a Windows CRLF checkout: dropped, fixed in round 1 (LF measure); `just check` on Windows already covers it.
- [project] The new surface-board scenario check raced; `runs()[-2]` can still raise IndexError after the 10 s poll: dropped, fixed in round 2; the leftover only changes the failure's message.
- [project] The startup reload margin is 30 bytes: dropped, nothing broke; `just check` catches an overrun before any PR, and the PR's Known gaps name it.
