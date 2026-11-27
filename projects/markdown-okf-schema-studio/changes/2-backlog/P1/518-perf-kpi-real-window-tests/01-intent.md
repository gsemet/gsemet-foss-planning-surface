# Real-window performance KPI campaign with maximums, shown on GitHub Pages

Performance measured in a real VS Code window on a complex rendering case, given as KPI scores,
published on the project's GitHub Pages site, with requirements that set the maximum each score must
meet (`intake/request.md`; decisions in `02-answers.md`, items 3 to 6).

First scope: the document of issue 547 (https://github.com/gsemet/markdown-okf-schema-studio/issues/547),
selection and comment creation. The campaign runs in GitHub CI, which carries the maximums (an
exceeded maximum turns the heavy job red), and by a local command for comparison. Each score is a
median time in milliseconds and its ratio to the maximum. The site shows the latest run only.

This CR sits above `perf-547-slow-comment-selection`, which fixes the issue and adds the real-window
measure of selection and comment creation on that document, with its generator; this CR builds on
that measure and does not repeat it.

formerly CR-518 of batch-09
