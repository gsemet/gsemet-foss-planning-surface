# 254 — Release 1.3: report

Shipped as **1.3.2** on 2026-11-03. 1.3.0 and 1.3.1 were merged but never tagged or published.

| Item | Value |
| --- | --- |
| Tag | `v1.3.2` at `42cd340a` |
| GitHub release | https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.3.2 (notes replaced with `release-notes.github.md`) |
| Marketplace | GaetanSemet.markdown-okf-schema-studio v1.3.2, published by the release job, listed by the public gallery a few minutes later |
| Release run | 41711901580 (integration re-run once after a window focus flake, then tag, release, pages green) |
| Change count | 40 changes since 1.2.0 (version commits excluded) |

## What happened

1. #303 (1.3.0) merged; its release run 41686091727 failed two real VS Code jobs: the wide table
   cell editor left the box after the table left its breakout, and a stress helper waited for a
   stored edit mode that is no longer written. Fixed in #306 (with a page test, TABLE-035).
2. #306 was merged by the owner's auto-merge before two more stale scenario fixes were pushed to
   its branch (toolbar reopen, window switch keys tab route), so #308 (1.3.1) failed on them in run
   41704023642. They landed in #309.
3. #310 (1.3.2): integration failed once on the alert type list scenario (CI window lost the focus
   during the click, no mousedown reached the page); the re-run passed and the release shipped.

## Follow-ups

- P3 `stress-alert-dropdown-flake`: the scenario's redo rule misses a text box blur that comes a
  few ms before the page blur (seen twice).
- Lesson: on a branch with the owner's auto-merge, push every fix before the PR goes green, or
  open a new PR for late fixes.
- Repository merges are rebase only (no squash): a version PR must hold a single commit.
- Open VSX publication: P1 backlog, waiting for the owner's registration.
- The announcement thread in `tweet.md` is ready for the owner to post.
