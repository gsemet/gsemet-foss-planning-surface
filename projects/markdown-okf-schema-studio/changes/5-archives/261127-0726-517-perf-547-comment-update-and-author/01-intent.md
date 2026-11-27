# A comment updates only its highlights and does not wait for Git (issue 547)

Second part of the fix of https://github.com/gsemet/markdown-okf-schema-studio/issues/547, stacked
above `perf-547-slow-comment-selection` in batch-09 (that CR's `02-answers.md`, item 3).

Wanted: creating, replying to, resolving or deleting a review comment no longer rebuilds every
thread's highlight, and saving a comment does not wait for the Git user name when that wait is
measurable. Both are measured in a real VS Code window with the scenario the lower CR adds.
