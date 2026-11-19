# Retro of release 1.9.3

- **What cost time.** The version push `integration` job failed twice on `paste-url`, which forced
  two re-runs (about 40 min).
- **Root cause, diagnosed but not fixed.** #424 makes a block commit render at once, which moves the
  stage request id forward immediately. The host drops a `page-state` message whose request id is
  no longer the stage's (`matchesCurrent`), and that includes `previewEditModeChanged`. Leaving
  edit mode right after a commit can therefore leave the workspace choice unsaved. The same gate
  applies to the theme, palette and anchor choices. The heavy run on a0821ac5 passed by timing.
- **Process fix.** A fix PR lets workspace-choice messages through the render staleness gate
  (they do not depend on the render shown), with a regression test. To be filed as a follow-up of
  #423.
- **Missed step.** PR #424 first landed without its CHANGELOG line, and the line was added before
  the merge. The coder checklist must include the changelog line for every `perf`/`fix`/`feat` PR.
