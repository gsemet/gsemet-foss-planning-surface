## Summary

A Chief of Staff could open a batch and forget to start the watcher that wakes its session on a merge; started by hand, it was given a flag `watch` does not take. Now each output that makes a batch run ends with one line naming the exact command to start in the background when no watcher of this session runs, and the Chief of Staff's cards make it a step done at once, written where it is read.

## Deliverables

Each watcher now holds a per-session lock, so the CLI can tell whether the current session's watcher runs:

```
chantier/watch-<project>/<session>.lock     (OS lock, held while the watcher runs, never removed)
watch: not running: for the Chief of Staff, start in the background: <cli> watch --after <n>
watch: <batch> still running: for the Chief of Staff, start again in the background now: <cli> watch --after <n>
```

- The line ends `open` (batch running), the `take` or `order qa` that sets a paused batch running, the switch to direct mode, and `status`; a watcher of another session is named in one `watch: session <id> runs a watcher too` line.
- The watcher's own end prints the restart command with the batch name; a batch with no running batch still ends with no restart.
- The ten-line output cut keeps a last `watch: not running:` line.
- Cards: a Startup core line, a numbered "Start the watcher" step, an Entry points row, and the host rows, all with one sentence: run the printed command as is: no flag added.
- The startup reading limit stays 12,544 (cuts in the Chief of Staff's skill file pay for the additions).

## Blast radius

Grade: 2. A new lock file in the git folder and a changed last line of several outputs and of the watcher's end; a revert restores the previous behaviour.

## Autonomous decisions

- The session id helper moved to `plugin_files.py` and the watch lines to `hub/lines.py`, to avoid an import cycle and keep a file under its size limit.
- With no detectable host, the session key is `none` instead of an error, so `status` works in a bare terminal.

## Known gaps

- The "open with no CR prints no line" case holds by hand at `fe2c215` (the empty-batch change is below this PR), but no test asserts it.
- Only the `surface-board` and `direct` scenario units were run on GitHub by the coder; the full scenario and the Windows run come with the long gate.

<details>
<summary>Details</summary>

## Changes

- `hub/lock.py`: `WatcherLock`, `watchers()`; `hub/watch.py`: the watcher takes its lock, new end line; `hub/lines.py`: the helpers and status lines.
- `open`, `take`, `order qa`, the direct-mode switch and `status` end with the helper's line; `cli.py` keeps it through the cut.
- Cards, `AGENTS.md`, `CONTRIBUTING.md`, `scenario/README.md` updated; tests and scenario checks added.

## Human decisions

- The CLI never starts the watcher itself: its end must wake the Chief of Staff's own session, so the trigger is a printed line.
- Detection is per session, by a lock file per project and session; a watcher of another session does not count.
- One fixed sentence everywhere: run the printed command as is: no flag added.
- The startup reading limit does not rise; cuts in the Chief of Staff's skill file pay for the added line.
- The step is written where the Chief of Staff reads it: startup core, a numbered step, an Entry points row.

## Impacts

The Chief of Staff sees a start line at each moment a watcher is due. No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `4b111a1`: `just check` pass, `just eval-dry-run` pass; at `fe2c215` the same two jobs are green in CI
- [x] Evidence: none, no visible change
- [x] Review: approved at `4e0de99`, carried to `fe2c215` (clean rebase, no conflict: the commit's hunks only follow the base's own edits to the same files)
- [x] Verified at `fe2c215`
- [x] CI green at `fe2c215`

## Internal references

CR-375 watcher-autostart.

</details>
