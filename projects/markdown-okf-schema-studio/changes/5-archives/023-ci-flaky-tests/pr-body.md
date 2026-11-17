## Summary

Removes the root causes of three tests that failed at random on Linux CI. They blocked PR #12
and the `main` run after PR #11, but had nothing to do with those changes. Two causes were real
product bugs.

| # | Flaky test | Root cause | Kind |
| --- | --- | --- | --- |
| F1 | visual first-gap: `[read:properties] 1 control(s) … sit under the toolbar` | the page never re-measured the leading properties table after its final layout (inset stayed 0 instead of 84 on CI): its own resize, late page/font load and updates skipped in a busy second were not handled; the test also compared readings without a rendered frame between them | product + test |
| F2 | `previewEditing`: `Timed out waiting for linked target metadata to refresh` | a linked target saved in the editor refreshed only through the file watcher, which can miss the write | product |
| F3 | `realInput`: `the user's lock survived: Quick Open from the locked group opened elsewhere` | closing a locked preview could focus a stale group position, which makes VS Code create a new empty group | product |

## Changes

- **F1** `src/webview/firstClearance.ts`: a ResizeObserver on the leading properties section
  (re-armed when it is replaced), updates on `load` and `fonts.ready`, and one trailing update
  after the burst limiter skipped some. `test/visual/capture.py`: each settle reading waits for
  fonts and two animation frames, and a toolbar-overlap failure now dumps the layout (rects, CSS
  variables, load/font state) so a CI-only failure is diagnosable. No tolerance changed.
- **F2** `src/extension.ts`: saving a linked target schedules the link enrichment of the previews
  that link to it. Only the enrichment runs, so an include is not rendered twice. The test now covers
  both paths without a retry loop:
  - a save in the editor;
  - an external write (as git would make), done once after a deterministic "watcher armed" signal.
- **F3** `src/extension.ts` + new `src/navigation/groupFocus.ts`: the unlock code remembers the
  `TabGroup` objects instead of their columns. It waits (event-based, bounded) for the unlocked
  group to close before it restores focus, and never focuses a position past the last group.
- CHANGELOG: three user-facing bullets (F1, F2, F3).

No visual change, so no screenshot. The visual campaign output is unchanged.

## Test plan

- [x] Unit: new `test/navigation/groupFocus.test.ts` (3) and 3 new `firstClearance` tests (fail on
  the old code); `just check` green.
- [x] `just visual` (255 scenarios) green; F1 pages re-run 6× at CPU throttle 1 and 8.
- [x] Sonnet review: round 1 asked for fixes (F2 external-write coverage, save refresh scope);
  round 2 approved; round 3 (F1 product fix after CI run 39787841817) approved.
- [ ] CI `just preflight` green, then re-run a few times to confirm F2/F3 are stable.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
