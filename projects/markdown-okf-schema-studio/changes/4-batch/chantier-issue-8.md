Bug: a dangling junction in a done CR folder crashes serve; watcher ends after 2 h

## Problem

A Driver left a dangling directory junction (a node_modules link to a removed worktree) inside a done change request's work folder. `serve` then failed with "path must be inside the planning folder", so the watcher stopped and the board went down. Separately, the watcher ends after 2 h without an event and the board stops with it, so a long CI wait or an owner's merge pause takes the board down.

## Proposed fix

- `serve` tolerates (skips) links that leave the planning folder.
- Moving a change request to done removes junctions and symlinks from its work folder.
- The watcher stays alive on a heartbeat while the batch runs, rather than ending after 2 h.

chantier 0.15.1, Claude Code desktop app (Windows). From a batch retro.
