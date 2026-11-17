## Summary

The preview skips file events below build and tool folders (`tmp`, `out`, `output`, `dist`,
`public`, ...). The check read every segment of the absolute path, so a workspace stored under
such a folder (for example `/home/me/tmp/book`) never refreshed when an included file, an image,
a sibling file or a `conf.py` changed. The check now reads only the part of the path below the
workspace root.

## Deliverable showcase

```text
root /home/me/tmp/book
  include.md        before: ignored (tmp above the root)   after: refreshes
  out/include.md    before: ignored                        after: ignored (out is below the root)
```

## Changes

- `src/session/hostEvents.ts`: `isIgnoredWatchPath` takes the session's workspace root and checks
  the relative path; a path outside the root is still read whole. A `conf.py` event is filtered
  per session.
- SwRS lifecycle-sync 044 states the new behaviour; its Known issue line is removed.
- Test: a root under `/home/me/tmp/book` refreshes, `out/` below it is still ignored.

## Impacts

No visual change. Workspaces under `tmp`, `out`, `dist`... now refresh like any other.

## Blast radius

Grade: 1. One helper in the watcher event handler; `git revert` restores the old behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated, markers unchanged, `okfreq update-coverage` and `lint` regenerated
- [x] Local gates: `just check` (2594 unit tests, 31 Python tests, requirements 1010 with 0 errors)
- [ ] Review
- [ ] CI green

## Internal references

- Change request 064 (watcher-ignore-absolute-path), SwRS-MDOKFSTUDIO-LIFE-044.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
