## Summary

The heavy CI run (the real VS Code `integration` job) failed intermittently on correct code. The
trusted VS Code launch needed about 92 % of its 900 s deadline when healthy, so a slower runner
pushed it over, and one step also failed on a frame lookup that never returned. This change runs
the trusted suite as two launches, and the Studio frame lookup and the open-at-line marked-line
count no longer ask anything but its URL of a frame that cannot be the Studio frame.

## Deliverables

Every step that ran before still runs. The trusted suite is now two VS Code windows, each with its
own 900 s deadline, CDP port, user-data directory and heartbeat file:

```mermaid
flowchart LR
  A[untrusted] --> B["trusted-suite.js part 1/2<br/>setup, preview-smoke,<br/>13 steps, then edit-keys<br/>to workspace-disposal"]
  B --> C["trusted-suite.js part 2/2<br/>setup, preview-smoke,<br/>real-input, preview-editing"]
  C --> D[standalone]
```

Part 1 holds 53 steps and part 2 holds 4; `setup` and `preview-smoke` run in both. A unit test
hard-codes the 55 step names of the former single launch and checks that the two parts hold each
of them exactly once, in order, with those two exceptions.

Durations read from the job logs of heavy runs, before (one trusted launch) and after (two parts).
A launch or part lasts from its `setup` step to its last step.

| Duration | Before: run 45476952370 at `63ef752` | Before: run 45713440510 at `17b779d` | After: run 45729384181 at `5e7b4a3` |
| --- | --- | --- | --- |
| Single trusted launch (deadline 900 s) | 834 s | 831 s | none |
| Part 1 (deadline 900 s, bar 600 s) | none | none | 428 s |
| Part 2 (deadline 900 s, bar 600 s) | none | none | 502.5 s |
| `real-input` step | 404 s | 405 s | 462 s |
| `open-at-line-probe` step | 178 s | 178 s | 182 s |
| Whole `just ci-integration` step (limit 1200 s) | 1011 s | 1002 s | 1128 s |

The frame lookup now chooses its candidates from `frame.url()` alone, before any call that needs
the frame's document:

```ts
// test/shared/webviewFrames.ts
// undefined for a "vscode-webview://" URL, else why the frame is skipped
// ("" = no document yet, about:blank, any other scheme)
export function frameUrlSkipReason(url: string): string | undefined { ... }

// a skipped frame receives no call but url(); `inspect` only sees webview frames
const scan = await scanWebviewFrames(page.frames(), async (frame) => ...);
frameLookups.record(scan);   // listed by waitFor if it times out
return scan.found;
```

A timeout on a webview frame still fails the step (the 10 s bound is unchanged). When a wait for
the Studio frame times out, the message now lists every frame seen, with why each was skipped.

## Changes

- `test/shared/trustedParts.ts` (new): the steps of each part, the part read from
  `STUDIO_TRUSTED_PART` (an unknown or missing value fails at once), and the two launch
  descriptions. The single-scenario runs (`STUDIO_REAL_INPUT_SCENARIO`, used by `ci-stress`,
  `ci-toc-loop` and the probe) stay one launch.
- `test/integration/trusted-suite.ts` runs the steps of the received part and logs
  `TRUSTED LAUNCH: <name>`; `test/integration/run-tests.ts` starts part 1, then part 2. The
  frontmatter evidence is written after part 2, the part that produces it, so its recorded suite
  result now covers part 2 only (serializer and workspace disposal run in part 1).
- `test/shared/launchWatchdog.ts`: the dump folder of a launch timeout or hang names the trusted
  part.
- `test/shared/webviewFrames.ts` (new), `test/integration/realInput/harness.ts` and the marked-line
  count of `openAtLine.test.ts`: the URL filter and the frame list in the timeout message.
- `CONTRIBUTING.md` describes the two launches. No deadline, step budget or `timeout-minutes`
  value changes, and no test assertion changes.

### What the failed frame lookup showed

The job log of the failed attempt (run 45706313890, attempt 2) shows
`TIMEOUT: locator.count did not return within 10000 ms (frame )` 12.6 s into the open-at-line
step: a bounded call hung on a frame whose URL was empty. The report that attempt uploaded
(`e2e-integration-attempt-2`) holds only the integration manifest, the campaign file, a process
list taken after the step ended and the screenshots of earlier launches: no in-window dump. So
neither shows which frame it was, why it had no URL, or the other frames of the window. An earlier
`CodeWindow: failed to load (code: -3)` line in the same run is not evidence: passing runs log it
too. The empty-URL observation is consistent with a frame that never loaded a document.

The Studio content frame has a `vscode-webview://.../fake.html` URL (seen in an earlier real
window run on Windows). On the CI runner, the browser target lists saved with the two timed-out
launches of the same run hold only webview service workers, so they confirm the
`vscode-webview://` scheme and not the content frame's URL. The filter therefore keeps every
`vscode-webview://` URL.

## Impacts

No visual change: only tests, CI behaviour and contributor documentation change. A full local or
CI integration run now opens one more VS Code window.

## Blast radius

Grade: **2**. Test code and contributor documentation only, nothing shipped in the extension
changes, but the frame lookup is shared by most real-window steps and the launches belong to the
CI job that releases depend on. A `git revert` restores the single trusted launch and the former
frame lookup; it needs one heavy run to confirm.

## Autonomous decisions

- The cause is fixed rather than hidden: no deadline, budget or time limit is raised, no test is
  skipped, and a re-run until green does not count.
- The bar for each part is 600 s, two thirds of its 900 s launch deadline, in each of two heavy
  runs on the same commit: that leaves 300 s, four times the spread seen between passing and
  failing runs. The long `real-input` step is not split, because the two parts reach the bar
  without it.
- The whole integration step only has to stay under its 1200 s limit: parallel CI jobs would
  change the report and release jobs, and shortening the open-at-line probe's fixed pauses is a
  separate change (see Known gaps).
- No new stress scenario for the frame lookup: it failed once and the open-at-line steps are not
  stress scenarios, so this change adds the URL filter and the frame list in the failure message
  only.
- The last group of steps (`edit-keys` to `workspace-disposal`) moved to part 1 rather than
  keeping a contiguous split: reading the code found no state it takes from the two steps it no
  longer follows, and the contiguous split would leave part 2 over 600 s on a slow runner. One
  difference remains: `preview-editing` leaves the preview theme dark, so `edit-keys`, `save-key`
  and `grid-card-editor-blur` now run under the `current` theme instead (none of them asserts a
  theme).
- Each launch logs its name in the extension host, so a passing log also says which part ran.
- Beyond the shared Studio frame lookup, the URL filter also covers the second frame scan of the
  open-at-line step and the frame dump written when the current preview frame is not found. The
  other frame scans of the test suite are left as they were (see Known gaps).

## Known gaps

- The whole integration step has a thin margin under its 1200 s limit: it took 1128 s on the heavy
  run measured above, about 6 % under, so a slower runner could still stop the step. Running
  integration as parallel CI jobs, or replacing the fixed pauses of the open-at-line probe (about
  180 s) with readiness signals, would widen it.
- The frame lookup is not proven fixed: one failure in many runs cannot be shown gone by two green
  runs, and the open-at-line steps are not stress scenarios, so the repetition proof the project's
  CI rules ask for a flaky test is not provided. The URL filter and the frame list in the failure
  message are what make a next failure explain itself.
- Other test steps still scan every frame without the URL filter (block actions, edit toolbar,
  find in preview, table empty column, tall block scroll, preview editing helpers, render patching,
  reload and scroll-sync suites, window focus), so a frame without a document could still stall one
  of them.
- No real-window run of these changes was made locally: on the Windows development machine the
  local gates skip the real VS Code stage. Only the CI runs exercise the two launches and the
  filter in a real window.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test/build/trustedParts.test.ts`,
      `test/build/webviewFrames.test.ts`
- [ ] Requirements: no behaviour change; `just requirements-lint` and `just requirements-update`
- [ ] Changelog: no user-facing change
- [ ] Local gates
- [ ] Heavy CI: two runs in a row on the same head
- [ ] Review
- [ ] Verified
- [ ] CI green

## Internal references

CR-509 heavy-ci-trusted-suite-timeout.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
