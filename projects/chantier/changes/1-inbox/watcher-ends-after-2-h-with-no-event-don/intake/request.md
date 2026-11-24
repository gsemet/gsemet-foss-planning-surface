# Watcher ends after 2 h with no event; done move keeps junctions


## Problem

The watcher ends after 2 h without an event, and the board stops with it. A long CI wait or the owner's merge pause (hours between "ready" and "merged") takes the board down; the Chief of Staff restarted it by hand four times in batch-09, and a "forge saw merged" landing in the gap waits for the next start.

Also: moving a change request to done leaves its work folder's links in place. A Driver's dangling node_modules junction there crashed `serve`; that crash is already filed as `board-0-15-1-refuses-to-start-on-a-junct`. This item adds the other half: clean the links at the move.

## Proposed fix

- The watcher stays alive on a slow heartbeat while the batch runs (running or paused with open PRs), rather than ending after 2 h.
- Moving a change request to done removes junctions and symlinks from its work folder.

From the markdown-okf-schema-studio batch-09 retro (stack batch, 2026-11-24), chantier 0.15.1, Claude Code desktop app on Windows.
