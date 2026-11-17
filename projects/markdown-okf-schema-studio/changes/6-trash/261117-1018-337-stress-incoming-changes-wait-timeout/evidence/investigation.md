# CR-337 investigation: incoming-changes frame.waitForFunction timeout

Date: 2026-11-17. Read-only: GitHub run logs of gsemet/markdown-okf-schema-studio, no code change.

## Runs found (CR-328 branch, workflow_dispatch, job `stress`)

| run | head | scope | failure |
| --- | --- | --- | --- |
| 43596868562 | 0a15412 | all 19 scenarios x12 | round 2/12 incoming-changes: frame.waitForFunction 30000 ms |
| 43601502967 | 836054d | all 19 x12 | round 2/12 incoming-changes: same |
| 43603384558 | 836054d | readme-html,toc,myst-blocks,find-in-preview,palette,checkbox-toggle,incoming-changes x6 | round 1/6 incoming-changes: same |
| 43604526837 | 0ed8a5e (merged head) | all x12 | round 5/12 palette "Heading 2 to prefix the line" (different, known family) |

So it repeated: 3 times, not once. The request's "round 2 of a scoped run" matches 43596868562 / 43601502967 (an empty scope means all scenarios).

## The condition waited for

The only `frame.waitForFunction` on the incoming-changes path is the tooltip wait in `captureNow`
(test/integration/realInput/harness.ts line ~622, no explicit timeout, so Playwright's 30 s default),
reached by `scenarioIncomingChanges` at the r03 and r07 captures: every
`[data-sphinx-preview-toolbar] button[data-tooltip]` must have its `::after` content none/normal,
visibility hidden or opacity 0, after the pointer was moved to the frame's bottom-left corner and the
toolbar buttons blurred. In the failing log the webview iframe blurred ~31 s before the failure and
only the workbench regained focus ~1 s before it: the wait ran the whole 30 s with no signal naming
which button's tooltip stayed shown (the Playwright stack is cut to `runStress`). That attribution is
inferred from the code path; the logs do not name the button.

## Does it repeat

- Never on main: stress succeeded on the push runs 43598582117, 43607815697, 43619406747 (earlier 43567601653, 43500084136) and 44056200079; the two I read in full (44056200079, 43607815697) passed incoming-changes 12/12.
- Never at the merged head 0ed8a5e (PR #402 merged 2026-11-14T15:00Z); only at the intermediate heads 0a15412 and 836054d, which are not in the repository (squashed).
- Passing on those same heads: incoming-changes alone x60 (43598104427), and short scopes (43603962284/5/7, 43602660201), so it needs a longer sequence before it.
- No incoming-changes timeout in the other 22 failed runs of the repository since 2026-11-11.

## Conclusion

Seen 3 times, only on intermediate heads of CR-328's branch (which changed the side-bar handling of
the steps around it), 0 times in the 7 later main/merged-head runs (more than 80 rounds). Not
reproduced on the code now on main; no fix is warranted. Optional hardening, outside this scenario
(the helper is shared harness code, `captureNow`): give that wait an explicit timeout and report which
toolbar button's tooltip is still visible, so a recurrence names its cause. To the owner to decide.
