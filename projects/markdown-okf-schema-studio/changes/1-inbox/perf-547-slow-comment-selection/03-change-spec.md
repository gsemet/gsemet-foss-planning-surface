# Comment creation no longer restyles the whole document, measured in a real window (issue 547)

On a large document, creating a review comment is slower the larger the document is. This change
removes the costs the reproduction found, handles the other points the issue names, and measures
selection and comment creation in a real VS Code window before and after.

## Base and place in batch-09

The owner asked for this fix as soon as possible (`02-answers.md`, item 1). It needs no other CR of
the batch: place it so that it does not wait for CR-514 or CR-507 to be merged, unless its files
conflict with theirs. `perf-kpi-real-window-tests` sits above it and builds on the measure it adds.

## Baseline

`intake/request.md` holds the measures at 5f0746d (headless Chromium, not a real window), with the
generator and scripts in `experiments/`. In short: comment creation, Save to highlight, 45 ms on a
small document, 65 ms on the issue's shape, 114 ms on one four times larger (164 and 488 ms with the
CPU slowed four times on the last two). A comment's DOM change restyles 1893 elements on the issue's
shape; 16 with the `:has()` rules removed. Slow selection was not reproduced there, nor on the
reporter's own document (`intake/reporter-document.md`).

## Part 1: measure first, in a real window

First commit, before any fix:

- A generator in `test/probe/` for a document of the issue's shape (about 464 lines and 52 KB, 22
  tables with about 197 rows, 11 SVG images of 1100 x 560, 9 comment threads, some inside cells),
  deterministic, adapted from `experiments/gen.mjs`. The reporter's gist is third-party content: it
  does not enter the repository.
- A real-window scenario, beside `test/integration/performanceProbe.ts`, that on that document, with
  real mouse input: drags a selection over running text and across table cells, releases it, and
  creates a comment from the Comment button, timed from the save action to the highlight shown.
- It writes a JSON report under `out/reports/probe/` with every sample and the median per
  interaction. It sets no limit.
- It runs by a local command and by a manual CI run (a `workflow_dispatch` input, as `toc_loop` has);
  it does not run on pull requests or on every push.

Then three runs in CI on that commit (the "before"). Local runs on a real desktop are added when the
conditions of `.agents/guidelines/local-worktree.guidelines.md` for window tests are met; when they
are not, say that they were not run.

The reporter's document (the issue's gist, downloaded on the owner's word, `02-answers.md` item 2)
was measured without a window at intake (`intake/reporter-document.md`): no stall at normal speed,
longest task in a selection 12 ms at worst, but about 3160 elements in the page against 1873 for the
first generated document, and a comment restyling 3222 elements. The generator therefore aims at that
density (inline code and bold in the cells, some blockquotes), about 3000 elements.

## Part 2: the fixes

1. The three `:has()` rules on the content root (`src/core/preview/styles/contentLayoutStyles.ts`,
   two rules; `contentBlockStyles.ts`, one) are replaced by a test whose cost does not follow every
   DOM change, for example a class or attribute on the content root that says whether the content
   holds an aligned float (the selector `ALIGNED_FLOAT`). The layout stays the same in every case
   those rules cover, on every surface that carries these styles (find them all: preview, content
   patches, runtime changes of the content, and any export or standalone page with no page script),
   including after a change that adds or removes the document's last aligned float.
2. When the threads arrive again, the page changes only what changed: a thread whose anchor and
   content are the same keeps its highlight elements. Work that is the same for every thread (the
   lookup of the `[data-line]` elements) is done once per update, and the scroll measure is not run
   when nothing that moves a line changed. Every comment behaviour stays: orphans and their return,
   resolved threads, badges, an open popover, overlapping highlights.
3. The refresh of the Comment button on `selectionchange` runs at most once per animation frame; a
   scroll only moves the button and does not read the selection again. The button appears and
   disappears in the same situations as today.
4. The git author name: measure in the real window how long a comment write waits for it when
   `comments.authorName` is empty. Over 10 ms, Save no longer waits for the lookup, without ever
   using a name older than the preview session; the setting, when set, still wins at once. At 10 ms
   or less, leave it and say so.
5. Selection: if the "before" runs show a drag or a release on the document blocking the page for
   more than 50 ms, find the cause and fix it here. Otherwise change nothing more than point 3 and
   say that the slowness was not reproduced in a real window.

## Done when

- A test without a VS Code window, in `just check` or in the visual stage, fails if adding one comment
  on the generated document restyles more than 100 elements, and passes after the change.
- Tests cover the layout with and without an aligned float, and the switch between the two after the
  content changes.
- A test shows that creating a comment keeps the highlight elements of the unchanged threads.
- Three CI runs of the real-window scenario after the fix, against the three before: the pull
  request's body and the CR's evidence give each run and the medians per interaction, and the number
  of elements restyled by a comment creation in the real window, which drops. Hosted runners vary:
  when the two sets of medians overlap, "not separable from runner noise" is an accepted result,
  said as such. Any interaction that got slower beyond that spread is explained. No target time is
  set here: the maximums belong to `perf-kpi-real-window-tests`.
- The new manual CI job follows `.agents/guidelines/ci.guidelines.md` (a `just ci-<name>` target,
  `timeout-minutes`, its line in rule 13's on-demand jobs). The "how we test" page of CR-507 lists
  every job of `ci.yml`: whichever of the two changes is higher in the stack adds this job to
  `docs/how-we-test.md`.
- Requirements: every behaviour changed or added has its SwRS and markers (project rules). No StRS
  is changed.
- `just preflight` passes and a heavy CI run of the head is green.
- The pull request references https://github.com/gsemet/markdown-okf-schema-studio/issues/547; it
  closes it by keyword only if the measures show both reported symptoms fixed or absent in a real
  window. Nothing is posted on the issue.

## Out of scope

KPI scores, maximums, the Pages site (`perf-kpi-real-window-tests`); typing, scrolling and first
render performance; reply to the reporter.
