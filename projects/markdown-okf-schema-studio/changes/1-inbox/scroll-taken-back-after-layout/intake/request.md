# A scroll made just after a height change is taken back

# A scroll made just after a height change is taken back

Found while CR-516 `perf-547-slow-comment-selection` was built (batch-09). Not asked by the owner
yet; filed so that it is not lost. Not part of CR-516.

## What was seen

A change of height starts a settling pass (`stabilizeLayout`, `scrollCore.ts`) at the frame after the
layout. A scroll that arrives before that pass is taken back to the earlier place, and the page
reports nothing. The window is about one frame.

## Source

- CR-516 folder, `work/coder/r4.md`, "B1, the flaky Chromium test" and open point 3.
- Reproduced with a temporary probe: scroll asked to 300, page back at 200, no report, 5 of 5
  (`evidence/local/r4-b1-race.txt` in the CR-516 folder).
- Foreman's note on ask A-66 (CR-516, pull request 549).

## Not established

- Seen in headless Chromium with CR-516's page script only; not run on the commit before it
  (1fc9528), so whether it is older than that change is not proved by a run.
- Not seen in a real VS Code window; no user report.
