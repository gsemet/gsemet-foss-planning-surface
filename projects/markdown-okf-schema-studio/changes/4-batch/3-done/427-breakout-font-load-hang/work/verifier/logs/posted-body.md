## Summary

The table breakout tests draw their pages in a pinned font. When that font did not load, the
test run did not fail: it hung. The helper that opens a test page started Chromium, then the font
check threw, and nothing closed the browser, so the open Chromium process kept Node alive and
`npm run test:unit`, `just check` and `just preflight` never ended. The helper that opens the
chart and Mermaid test pages had the same gap. Both helpers now close the browser when their page
setup fails, so the run fails with the real error message and ends.

## Deliverables

Each helper wraps everything after a successful Chromium launch in one `try`; the `catch` closes
the browser and throws the original error again:

```ts
try {
  browser = await chromium.launch();
} catch {
  return undefined; // no Chromium here: the tests skip
}
options.launched?.(browser);
try {
  // newPage, goto, theme variables, pinTestFonts(page, options.fonts), wait for Auto ...
  return { browser, page, close: async () => { await browser.close(); } };
} catch (error) {
  await browser.close().catch(() => undefined); // never hides the setup's error
  throw error;
}
```

| Run, on Windows, with the pinned font made to fail | Before | After |
| --- | --- | --- |
| Font folder missing (`ENOENT`) | still running after 120 s, then stopped | exits by itself in about 3 s, code 1 |
| Font files that are not fonts | still running after 120 s, then stopped | exits by itself in about 3 s, code 1, "the pinned test font did not load" |

## Changes

- `test/page/tableBreakout.test.ts`: the page-opening helper closes Chromium when its setup
  throws; an optional options argument (`fonts`, `launched`) lets a test make the font fail and
  watch the browser. A new test feeds it font files that are not fonts and checks that the error
  names the font and that the browser is closed.
- `test/page/pinnedFont.ts`: `pinTestFonts` takes the fonts folder as an optional argument
  (default unchanged).
- `test/page/chartPage.ts`: `openPreviewPage` (and so `openChartPage`) closes Chromium when its
  setup throws, with an optional `launched` callback.
- `test/page/chartCsp.test.ts`: a new test opens a chart page with an unknown theme, a real setup
  failure after the launch, and checks that the browser is closed.

## Impacts

No visual change: test harness only. A broken pinned font now fails the run quickly with its
message instead of hanging it. No product code changes.

## Blast radius

Grade: 1. Test helpers only; the existing tests and their callers are unchanged. A `git revert`
restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): each new test is red with its
      helper's `browser.close()` removed and green with it restored, on Windows, at ebfb7f2
- [x] Requirements: No behaviour change (test harness only; existing markers unchanged)
- [x] Changelog: No user-facing change
- [x] Local gates: `just check` and `just preflight` (its static stage on Windows) pass at
      ebfb7f2
- [x] Review: approved at ebfb7f2
- [ ] CI green

## Known gaps

- CI does not run the table breakout tests: its machines have no Chromium they can start there,
  so those tests skip, and the breakout fix is proven only by the local runs on Windows.
- Linux and macOS were not run locally (no machine available): UNVERIFIED there.

## Autonomous decisions

- The fix also covers the chart and Mermaid test-page helper, which had the same gap.
- The fix closes the browser instead of adding a forced exit or a timeout to the test runner, so
  a leak is not hidden.

## Internal references

- Found while making the table breakout tests independent of the installed fonts (#429).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

