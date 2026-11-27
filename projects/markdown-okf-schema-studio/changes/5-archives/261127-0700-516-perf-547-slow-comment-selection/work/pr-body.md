## Summary

Creating a review comment in the preview gets slower the larger the document is
(https://github.com/gsemet/markdown-okf-schema-studio/issues/547, reported on a document with many
tables and SVG images). The main cost found: three style rules made the browser restyle the whole
page after any change of its content. This change removes that cost, does the selection and hover
work of the page at most once per frame, and adds a measure in a real VS Code window to compare
before and after. The issue stays open: updating only the changed comment threads follows later.

## Deliverables

The three rules that asked "does the page hold an aligned image, figure or table?" with `:has()` now
read one attribute on the content root, written by whoever renders or changes the content:

```mermaid
flowchart LR
  find[core/preview/alignedFloat.ts<br/>selector and attribute] --> host[html-sanitizer.ts<br/>rendered page]
  find --> exp[exportContent.ts<br/>exported file]
  find --> page[page/modules/alignedFloat.ts<br/>content patches and runtime changes]
  host --> attr[main data-okf-aligned-float]
  exp --> attr
  page --> attr
  attr --> css[content styles<br/>no :has on the root]
```

| In the page | Before | After |
|---|---|---|
| Elements restyled by saving one comment (headless browser, page of 3072 elements) | 3125 | 26 |
| **Comment** button on a selection change | recomputed at every event | at most once per frame; the comment shortcut pressed before that frame reads it at once |
| **Comment** button on a scroll | selection read again | button moved only; the selection is read once more, at the next frame, only after the page changed under it |
| Hover outline and copy button | recomputed at every pointer event | at most once per frame |
| Selection text in scroll position reports | read at every report | read again only when it can have changed |
| Source line of a selection that ends at the very start of a block | every source line of the document listed | walks back from that block |

## Changes

- The content root carries `data-okf-aligned-float` exactly while it holds an aligned image, figure
  or table. The rules keep the same specificity and the page lays out as before, also in an exported
  file, which runs no page script. The attribute is left out of the page shell compared by content
  patches, so a patch stays a patch.
- The page's selection, hover and scroll handlers above.
- A test in a headless browser fails if saving one comment on a generated large document restyles
  more than 100 elements. It runs with the visual stage.
- A real-window scenario, `perf-547`, measures a generated document of the reported shape (about 464
  lines, 22 tables, 11 SVG images, 9 comment threads, about 3,100 elements): `just ci-perf-547`, and
  a CI job of the same name started only by a manual run with `perf_547=true`. The **How we test**
  page names it.

## Impacts

No visual change: the layout around aligned images and tables is the same, and the **Comment**
button, the hover outline and the copy button appear and disappear in the same situations, at the
next frame.

Real VS Code window on a Linux CI runner, three runs before (at 1fc9528, which adds the measure
only) and three after the change (at aeefa1b, carried from e52cd28: the later commit changes the
change log and a blank line of a test) on the same generated document. A run value is the median of
its samples:

| Measure | Before, 3 runs | After, 3 runs | Median of runs | Reading |
|---|---|---|---|---|
| Elements restyled by one comment creation | 3109, 3109, 3109 | 41, 41, 41 | 3109 to 41 | drops |
| Comment save to highlight drawn (ms) | 53.4, 51.0, 53.9 | 47.1, 45.9, 37.1 | 53.4 to 45.9 | faster, the runs do not overlap |
| Selection release to **Comment** button shown (ms) | 17.8, 18.45, 17.75 | 18.2, 17.65, 18.05 | 17.8 to 18.05 | not separable from runner noise |
| Longest task, drag over text (ms) | 2.65, 2.46, 2.66 | 2.72, 2.68, 2.62 | 2.65 to 2.68 | not separable from runner noise |
| Longest task, drag across cells (ms) | 2.64, 2.62, 2.69 | 2.54, 3.40, 2.71 | 2.64 to 2.71 | not separable from runner noise |
| Longest task, release over text (ms) | 2.28, 2.41, 2.17 | 2.41, 2.55, 2.92 | 2.28 to 2.55 | not separable from runner noise |
| Longest task, release across cells (ms) | 2.62, 2.79, 2.60 | 2.73, 2.92, 2.91 | 2.62 to 2.91 | not separable from runner noise |

The two release tasks have medians about 0.3 ms higher after the change; the two sets of runs touch
or overlap, and no longest task during a drag or a release exceeds 4.9 ms after the change. The
slowness of a text selection was not reproduced in a real window: before the change, no drag or
release blocked the page for more than 50 ms (largest sample 12.26 ms).

Runs before:
[1](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45895473044),
[2](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45895477080),
[3](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45896724578). Runs after:
[1](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45918715713),
[2](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45918718450),
[3](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45918721402).

## Blast radius

- **2**: several features of the preview page and the rendered and exported pages; a plain
  `git revert` restores the previous behaviour, no data or file format changes.

Grade: 2

## Autonomous decisions

- The pointer-move listener of the edit mode outline is not throttled: it only records that the
  pointer, not the keyboard, owns the hover actions, once per switch.
- The time limits of the manual `perf-547` job follow its measured duration (job 5 minutes, step 4).

## Known gaps

- No local real-window run: the real-window stages do not run on Windows.
- The real VS Code integration and acceptance jobs have not run at this head itself. They ran, with
  stress, at 44a2e93, the head of #550, which is stacked on this pull request and holds its commits,
  and passed there
  ([run 45951664534](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45951664534)).
  The CI checks of this pull request cover its simulated jobs only; the `perf-547` runs above are
  its own real-window evidence.

## Test plan

- [x] New or changed tests (they fail on the previous code): new tests for the restyle count, the
      layout with and without an aligned float and the switch between them, the once-per-frame
      handlers and the unchanged behaviours. On the previous code the new-behaviour tests fail and
      the unchanged-behaviour tests pass (the comment shortcut test was not run on it).
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just preflight` passes at aeefa1b (static stage on Windows: 5538 unit tests,
      5530 pass, 8 skipped; 298 Python tests). Carried from e52cd28 (the later commit changes the
      change log and a blank line of a test): 20 of 20 browser tests; the five timing-dependent test
      files pass 10 times in a row each, and once each while `just check` runs beside them;
      `just ci-visual` on Windows: 524 of 530 captures pass, the 6 failed captures fail the same way
      without this change
- [x] Review: the change approved at aeefa1b
- [x] CI green at aeefa1b: 7 checks pass (checks, report, static, static-windows, viewer-graph,
      visual, visual-2); the jobs started on demand or after merge are skipped, not run
- [x] Real VS Code jobs: the full CI run at 44a2e93 (the head of #550, which holds the commits of
      this pull request) passes, integration, acceptance and stress included
      ([run 45951664534](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45951664534))

## Internal references

- Change request CR-516 (perf-547).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
