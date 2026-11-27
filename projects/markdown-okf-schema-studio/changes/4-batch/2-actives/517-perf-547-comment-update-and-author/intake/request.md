# A comment updates only its highlights and does not wait for Git

Second part of the fix of https://github.com/gsemet/markdown-okf-schema-studio/issues/547, split from
`perf-547-slow-comment-selection` on the owner's word (that CR's `02-answers.md`, item 3). Filed on
2026-11-26 from the Chief of Staff session of batch-09.

The owner, verbatim: "A. Deux CR (reco.)", to: "does the fix go as one CR or two? Two: 1) measure,
`:has()` rules, comment button; 2) changed threads only and the Git author name, stacked above, in
batch-09".

The two points, from the reproduction (that CR's `intake/request.md`):

- When a comment is created, every thread's highlight is torn down and anchored again, and the scroll
  measure runs over all lines (about 1.7 ms to set the threads and 3 ms to measure on the issue's
  shape, besides the restyle the first CR removes).
- When the `comments.authorName` setting is empty, the Git user name is asked for on every comment
  write (`src/session/features/comments.ts`, `src/host-vscode/headBaseline.ts`); its cost through VS
  Code's git extension was not measured.
