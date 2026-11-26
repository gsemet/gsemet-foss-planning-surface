# Fix slow comment creation and selection on large documents (issue 547)

https://github.com/gsemet/markdown-okf-schema-studio/issues/547: on a large document with many
tables and SVG images, selecting text and creating a review comment in the preview are reported
sluggish. The reproduction (see `intake/request.md`) measured comment creation growing with the
document, mainly through the root `:has()` style rules, and did not reproduce the slow selection in a
windowless browser.

Wanted (`02-answers.md`, item 1): the fix in batch-09 as soon as possible, with a performance
analysis in a real VS Code window, run two or three times for stability, before and after.

This CR is the lower of two: `perf-kpi-real-window-tests` builds the KPI campaign (maximums, scores,
Pages) on top of the real-window measure this one adds, so the fix can merge without waiting for the
campaign.
