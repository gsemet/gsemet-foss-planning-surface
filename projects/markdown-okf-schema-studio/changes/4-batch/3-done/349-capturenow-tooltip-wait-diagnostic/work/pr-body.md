## Summary

The real-window tests take screenshots through a shared capture helper. Before each capture it
moves the pointer off the preview toolbar, blurs the toolbar buttons and waits for every toolbar
tooltip to hide. That wait used Playwright's 30 s default and, when it ran out, its error said only
that the wait timed out. The CI `stress` job (which repeats the real-window scenarios) hit this
timeout three times in the incoming-changes scenario, on intermediate commits of a branch since
merged (PR #402), and nobody could tell which toolbar button kept its tooltip; the stress runs have
not reproduced it since.

This PR is a diagnostic only: it fixes no flake and changes no product behaviour. The wait now
fails after 10 s, and its error names each toolbar button still showing its tooltip and why
(hovered or focused).

## Deliverables

One helper in `test/integration/realInput/harness.ts` replaces the inline wait of the capture
helper. The wait and the error report read the same page-side probe, `shownToolbarTooltips`, so
the condition is defined once and is the same as before: a capture that passed before passes now.

```ts
const TOOLTIP_HIDE_TIMEOUT_MS = 10_000;

function shownToolbarTooltips(): ShownTooltip[] { ... } // runs in the webview

async function waitForToolbarTooltipsHidden(frame: Frame, id: string): Promise<void> {
  try {
    await frame.waitForFunction(`(${shownToolbarTooltips.toString()})().length === 0`,
      undefined, { timeout: TOOLTIP_HIDE_TIMEOUT_MS });
  } catch (error) {
    // TimeoutError only: probe again, throw a one-line Error with the original as `cause`
    ...
  }
}
```

The message a stuck tooltip now gives, on one line so the stress job's
`stress round N/M, scenario <name>: ` prefix keeps it whole:

```text
capture review-annotations/r03-incoming-change-bars: toolbar tooltip still shown after 10000 ms: "<tooltip text>" (hover: yes, focus-visible: no, ::after content "...", visibility visible, opacity 1)
```

Choices made:

| Case | Before | After |
| --- | --- | --- |
| Wait bound | Playwright default, 30 s | 10 s (`TOOLTIP_HIDE_TIMEOUT_MS`): the toolbar tooltip has `transition: none`, so one still shown after 10 s is stuck, not slow |
| Tooltip stuck | Playwright timeout error | capture id, tooltip text, hover and focus-visible state, `::after` content, visibility, opacity of each shown tooltip |
| Tooltip hid just after the deadline | Playwright timeout error | `capture <id>: toolbar tooltips hid only after the 10000 ms wait timed out` |
| Second probe fails (frame gone) | not applicable | the original timeout error, unchanged, so the detached-frame retry still sees it |
| Any other error | rethrown | rethrown unchanged |

The new messages do not match the harness's detached-frame pattern, so a stuck tooltip is never
retried as a detached frame.

## Changes

- `test/integration/realInput/harness.ts`: the page-side probe `shownToolbarTooltips`, the
  constant `TOOLTIP_HIDE_TIMEOUT_MS`, the helper `waitForToolbarTooltipsHidden` called by the
  capture helper, and one sentence in the capture helper's doc comment.
- Not changed: the other copies of this wait, in `test/integration/checkboxToggle.test.ts` and
  `test/integration/previewEditingHelpers.ts` (used by `previewEditing.test.ts`); `src/`; the
  requirements; CI.

## Impacts

No visual change and no product change. Developers reading a failed real-window run see which
toolbar tooltip stayed shown, after 10 s instead of 30 s.

## Blast radius

Grade: 1. Test-harness code only, on the capture path of the real-window tests; a plain
`git revert` restores the previous wait.

## Autonomous decisions

- The message keeps every tooltip on one line even if a tooltip text or computed value held a line
  break: the text and `::after` content are JSON-quoted, and whitespace runs in the visibility and
  opacity values are folded to one space. Reason: the stress job's prefix must keep the message
  whole.

## Known gaps

- The timeout path has not run: a stuck tooltip cannot be forced in a real window without the very
  instability this diagnoses, so it is shown by the code only and is proven on the next real
  recurrence.

## Test plan

- [ ] New or changed tests (they fail on the previous code): no new test; the timeout path is not
      forced (see Known gaps)
- [x] Requirements: No behaviour change (test-harness code with no requirement markers)
- [x] Changelog: No user-facing change
- [x] Local gates at `eabbe0f` (carried from `52c0488` through clean rebases, Windows):
      `just check` pass; `just preflight` pass (its static stage on Windows; the real-window
      stages run in CI)
- [x] Review: approved at `eabbe0f` (carried from `52c0488` through clean rebases)
- [x] Verified at `eabbe0f` (carried from `abeb761`: clean rebase onto `main`, same patch): the
      change meets its specification; the timeout path is judged by reading the code only (see
      Known gaps)
- [x] CI green at `eabbe0f`: pull-request checks pass (static, static-windows, visual, report,
      checks); before the rebase onto `main` (same patch), heavy dispatch run 44639811161 passed its `integration` and `stress` jobs, which
      run the changed capture helper in a real VS Code window (gallery, toc-loop and release jobs
      skipped by the workflow)

## Internal references

- Change request CR-349 `tooltip-wait-diag` (batch-06); background: the investigation of CR-337
  (stress incoming-changes wait timeout).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
