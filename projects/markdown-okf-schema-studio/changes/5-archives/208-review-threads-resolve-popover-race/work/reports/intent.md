# Review threads: the comment popover closes itself after a successful Resolve (product race)

Merged item (owner decision 2026-10-31): the former P1 `review-threads-resolve-popover-stress-flake`
and the former P2 `comments-post-hash-before-staleness`, now ONE item at P2. Queued after the three
CI flake CRs; not urgent.

## Status of the merged parts

- DONE: post-hash ordering. `CommentsController.post()` now records `textHash` only after the last
  staleness check (`src/session/features/comments.ts`, "Recorded only now, after the last staleness
  check"), covered by the unit test "a post overtaken while it checks the anchors leaves the newer
  post free to show the new thread" in `test/session/reviewReqComments.requirements.test.ts`
  (PR #202). Verified on main 6a2cb9d8 on 2026-10-31.
- REMAINING: the product race. After a successful Resolve, two comment posts arrive (commentPosts
  2 -> 4 in the stress dump) and the page closes the popover itself ("re-apply without threads").
  1. Unit test that replays 2 posts after Resolve (fails today).
  2. Fix the popover re-apply so a resolved thread keeps its popover open.

## History (former P1 item)

## Stress flake: the review-threads comment popover's Resolve button does not appear

Type: fix (test or product) · Priority: P1 · Filed 2026-10-28 by the Foreman from the 1.0.0 heavy
gate · No CR now (user decision via the Chief of Staff): the post-CR-168 heavy gate on main
decides; if `review-threads` fails again, the user chooses between a fix before 1.0.0 and a release
with a known flake.

## Evidence

- Failing run: heavy on main `b71fac7c`,
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732349085, `stress` job,
  round 9 of 20, scenario `review-threads`:
  `locator.textContent: Timeout 30000ms exceeded` waiting for
  `[data-okf-comment-popover] [data-okf-comment-resolve]`
  (`out/test/integration/realInput/run.js:93`, `runStress`). Rounds 1–8 of the scenario passed.
  Log: `stress-b71fac7c.log` (this folder).
- Earlier heavy runs, `stress` green:
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40728621051 (`2577039e`)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40723757734 (`620c640a`, Edit figure fix)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40716533723 (`ff9f9c1e`, five-row toolbar)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700884217 (`59f0c329`)
- Suspect range `2577039e..b71fac7c`: PR #175 (toolbar and tooltip motion, incl. the shared
  tooltip slide-in) and PR #178 (table menu: clear the toolbar before revealing). Lead (unproven):
  a motion transition delays the popover or its Resolve button becoming visible.

## Expected

- Reproduce in the stress job (CI only; no local real-window runs), find the cause, fix product or
  test wait per `.agents/guidelines/ci.guidelines.md` rule 12 (record host/page state on failure;
  never a blind retry or a longer timeout alone), and prove it with a green stress run.

## Update 2026-10-28 (PR #189, merged)

Diagnostics only: the popover records its close reason and the scenario dumps sidecar, host and
page state on failure. The flake is NOT fixed; wait for the next failure dump, then fix.

## Status after CR 186 (2026-10-29, PR #200 — test hardening + dumps, cause not proven)

- Not the alert-dropdown window-blur cause: both failure logs predate #189's diagnostics and show only
  the 30 s timeout waiting for the Resolve button; Resolve had already succeeded (sidecar
  `resolved: true`); the popover has no window-blur handler.
- Candidates left: a window/OS blur swallowing input, or a page replacement during the Resolve round
  trip.
- PR #200: re-asserts state before/after each critical click; redoes a step once only when the trace
  proves a real VS Code window blur or a page replacement the host did not cause; otherwise fails with
  a full dump (host counters, window state, page witness, trace).
- Two heavy runs green (40 rounds), no redo fired. Close only when a dump explains a failure or many
  more rounds stay clean.

## First dump with cause (2026-10-29, top-of-stack heavy 40811480230, stress round 20/20)

`/private/tmp/claude-502/top-heavy2-stress.log` line 3244. Resolve succeeded (sidecar `resolved:true`,
host result ok, mark `data-okf-comment-resolved=true`), then the page traced
`comment popover closed: re-apply without threads, thread t_d94a2289` at 2602 ms. Host `commentPosts`
went 2 → 4 during the step (two posts), no page reload (`pageLoads` 4 → 4), no content patch, window
focused. The verdict correctly refused a redo. So the popover is closed by the page's own re-apply
logic finding no thread for the open holder although the thread exists and is resolved — likely a
product race between two comment posts (one apparently without the thread, or the holder lookup
filtering resolved threads). This is now a product lead, not a focus issue. Next: unit test replaying
two posts after Resolve (first without / second with the resolved thread) against the popover re-apply.

## Open question (Chief of Staff, 2026-10-29)

Did #202's change to how the extension posts the comment list make this race more likely?
The flake predates #202, so it is not the root cause, but it may have widened the window.
To answer: write a unit test that replays two comment-list posts right after a successful
Resolve (the order seen in the stress dump: commentPosts 2→4, then "re-apply without threads")
and run it on main and on #202. Plan: open a CR for this race on 2026-10-29 (daytime), not
during the night batch. Impact is minor: the popover closes, no data is lost.

## Related (2026-10-29)

P2 `comments-post-hash-before-staleness` (an overtaken post can make a newer post skip) is in
the same post() path; check it in the same CR.
