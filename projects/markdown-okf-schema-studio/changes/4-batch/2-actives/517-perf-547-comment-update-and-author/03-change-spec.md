# A comment updates only its highlights and does not wait for Git (issue 547)

After a comment is created, answered, resolved or deleted, the page tears down every thread's
highlight and anchors all of them again, and saving a comment asks Git for the user name each time.
This change updates only what changed and removes a measurable wait for Git.

## Base and place in batch-09

Directly above `perf-547-slow-comment-selection`, which adds the real-window scenario `perf-547`, its
report `out/reports/probe/perf-547.json` and the first part of the fix. As soon as possible, like it
(`02-answers.md`, item 1). `perf-kpi-real-window-tests` also builds on the lower CR.

## Fixes

1. Highlights, badges and the orphan list (`src/page/modules/commentThreads.ts`): when the page
   receives the threads again, only the threads that were added, changed or removed are touched. The
   highlight elements of the other threads stay the same DOM elements. An update reads the
   document's `[data-line]` blocks once, not once per thread. The scroll measure that follows
   (`src/page/features/hostHandlers.ts`) runs only when the update can have moved a block of the
   content.
2. The result is the same as today in every case: where each highlight, badge and orphan entry sits
   (threads that share a block or overlap included), the resolved state, the focus colour, the open
   popover with its typed draft and pending confirmation, hidden comments, and the behaviour after a
   content patch or a new render, which anchors the threads again as today.
3. Git author name (`src/session/features/comments.ts`): measure first, in the real-window scenario,
   the time a comment write waits for the Git user name, with `comments.authorName` empty and the
   test folder a Git repository with `user.name` set. The scenario adds the samples to its report as
   `authorWait`, and the report says the folder is such a repository. Measured in CI (`02-answers.md`,
   item 3).
   - Median above 10 ms: a save no longer waits for Git once a name has been read in the same preview
     session; the name is read again in the background so that the next write has the current one.
     A name older than the preview session is never used, the `comments.authorName` setting still
     wins, and a write with no name read yet waits as today.
   - Median at 10 ms or under: change nothing for the author and say so with the figures.

## Measure: what the thread index costs

4. The owner suspects review comment threads cause needless load on large documents, because the
   document is indexed to anchor them (`02-answers.md`, items 4 and 5). Measure that cost on its own,
   in Node, on `src/core/comments/anchoring.ts`: indexing the document (`createDocumentIndex`) and
   re-anchoring all its threads (`reanchorThreads`, which indexes it too).
   - Two generated documents: the issue-size one of the lower CR's generator
     (`test/probe/perf547Document.ts`, 9 threads) and one four times as large with 36 threads. The
     generator's default output stays byte for byte what the lower CR's runs measured.
   - The `perf-547` CI job runs the measure and adds it to its report as `threadIndex`: per document,
     lines, bytes, thread count, and the samples and median of both times.
   - Report only: no limit asserted, nothing changed in how threads are indexed, anchored or stored.

## Done when

- The reports of the three CI runs hold `threadIndex` for both documents. The pull request's body and
  the CR's evidence give the medians beside the `commentCreate` median of the same runs, and say, as
  read in the code, on which user actions the extension host runs these two functions.
- Tests show that adding one comment leaves the highlight elements of the other threads in place and
  reads the `[data-line]` blocks once.
- A test compares, after create, reply, resolve and delete (orphaned and overlapping threads
  included), the page updated in place with the page anchored from nothing: the same highlights,
  badges and orphan entries.
- The restyle test of the lower CR still passes.
- Three CI runs of the real-window scenario on this change, against the three "after" runs of the
  lower CR: the pull request's body and the CR's evidence give each run, the medians per interaction
  and the `authorWait` samples. "Not separable from runner noise" is an accepted result, said as
  such; an interaction that got slower beyond that spread is explained. No target time is set here.
- If the author wait is changed, tests cover the setting, the name read in the session, the first
  write and a changed Git name.
- Requirements: every behaviour changed has its SwRS and markers (project rules;
  `SwRS-MDOKFSTUDIO-REVIEW-065` states which Git name a write may use, if that changes). No StRS is
  changed.
- `just preflight` passes and a heavy CI run of the head is green.
- The pull request references https://github.com/gsemet/markdown-okf-schema-studio/issues/547; it
  closes it by keyword only if the real-window runs show both symptoms of the issue fixed or absent.
  Nothing is posted on the issue.

## Out of scope

The measure harness itself, the `:has()` rules, the comment button, hover and scroll listeners (the
lower CR); inline thread comments written in the Markdown source; KPI scores and the Pages site; a
reply to the reporter; making the thread index faster, disabling review comment threads or storing them
elsewhere (the owner decides, on the figures).
