## Summary

On the published requirements site, the page of a use case draws its main paths as a map (the
"path graph"). The map was far too big (readers zoomed out to half size to see it) and hard to read:
side-branch labels, test counts and captions overlapped each other and the dashed lines, and a
state shared by two paths was drawn again, in grey, on every row.

This change redraws the map as a joined, metro-style map drawn at its own size: a state shared by
several paths is one circle, the paths join into it and split out of it, each in its own colour, and
no text or pill overlaps another. Every link to a requirement on these pages now shows its full ID
(`StRS-MDOKFSTUDIO-BLOCK-014`, not `BLOCK-014`).

## Deliverables

- **A joined map.** One circle per distinct state; a step shared by two paths is drawn once, with one
  stroke per path side by side. A path that shares nothing with the others sits apart, on the right
  of an earlier row, so it never reads as the continuation of another path. A path that starts on
  another path's state shows its number in a disc of its colour.
- **Drawn at its own size.** The SVG has its natural `width`, shrinks to 85 % of it at most before the
  page scrolls sideways, and is never stretched to the page.
- **Readable.** Pills hold the full ID on one line and the test count on the next; captions are
  wrapped and kept clear of the lanes; a second behaviour between the same two states hangs under the
  first one's caption; the other outcomes of a state hang on a dotted stem as dashed pills.
- **One line to read it.** The old hint paragraph is replaced by one short line (use case reached by
  one or more paths, each step a behaviour with its own tests, paths can share steps) and the legend.
- **Play** walks the path in its own colour and lights its states.
- **A guard in CI.** A browser test loads every real use case page of the generated report at 1280
  and 800 px and fails on any overlap or text past the map, plus six frozen map shapes.

```ts
// test/site/requirementsViewer/layout.ts
export function buildMetroMap(paths: readonly MainPath[]): MetroMap; // joined nodes + edges per path
export function metroSvg(model: MetroMap, paths: readonly MainPath[], fromDir: string): string;
```

Map height in px on six real use case pages, before (base `8d99cd1e`) and after (head `d94b5ec`; the later commit only moves CI jobs, no site code), measured by the verifier on the generated report; overlaps are 0 on all twelve captures and the page never scrolls sideways at 800 px.

| Use case | 1280 px before | 1280 px after | 800 px before | 800 px after | Captures |
| --- | --- | --- | --- | --- | --- |
| StRS-MDOKFSTUDIO-BLOCK-003 | 1041 | 589 | 770 | 616 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-BLOCK-003-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-BLOCK-003-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-BLOCK-003-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-BLOCK-003-narrow.png) |
| StRS-MDOKFSTUDIO-FMSCHEMA-014 | 791 | 699 | 616 | 747 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-FMSCHEMA-014-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-FMSCHEMA-014-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-FMSCHEMA-014-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-FMSCHEMA-014-narrow.png) |
| StRS-MDOKFSTUDIO-BLOCK-014 | 1183 | 861 | 901 | 909 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-BLOCK-014-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-BLOCK-014-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-BLOCK-014-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-BLOCK-014-narrow.png) |
| StRS-MDOKFSTUDIO-MYST-006 | 910 | 402 | 675 | 429 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-MYST-006-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-MYST-006-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-MYST-006-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-MYST-006-narrow.png) |
| StRS-MDOKFSTUDIO-REVIEW-012 | 1582 | 858 | 1190 | 819 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-REVIEW-012-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-REVIEW-012-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-REVIEW-012-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-REVIEW-012-narrow.png) |
| StRS-MDOKFSTUDIO-MYST-009 | 949 | 770 | 731 | 812 | [before 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-MYST-009-desktop.png), [after 1280](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-MYST-009-desktop.png), [before 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/before-MYST-009-narrow.png), [after 800](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/bf652330c09832c1f2b32a1821d2051be7429a2b/after-MYST-009-narrow.png) |

At 1280 px all six maps are shorter. At 800 px three maps are taller than before (FMSCHEMA-014 616 to 747, BLOCK-014 901 to 909, MYST-009 731 to 812): the map is drawn at its own size and scrolls inside its box instead of being squeezed, and the size bound of this change is the 1280 px one.

## Changes

- `layout.ts`: `buildMetroMap` (joined nodes, one edge per state-behaviour-state triple listing its
  paths, rows, columns, packing) and `metroSvg` (strokes, pills, joins and splits, start discs,
  outcomes, size).
- `pages.ts`, `urls.ts` usage: full IDs on every link text; `mapSection` carries the one-line
  reading help and the legend.
- `viewer.css`, `siteTheme.ts` (`--p3` from the extension's yellow token), `viewer.js` (Play colour
  and marker).
- Requirements: SwRS CORE-080, -081, -082, -083 updated, new CORE-091 (Play), the StRS CORE-008 links, the
  project guideline (one to three paths per use case), a dated entry in the requirements log.
- Tests: `metroMap.test.ts`, `metroMap.browser.test.ts`, `metroShapes.ts`, updated `pages.test.ts`
  and fixture, pinned KaTeX fonts for the layout checks; `npm run test:viewer-graph`, run by the new
  `just ci-viewer-graph` target in its own CI job (`viewer-graph`), after a JSON-only
  `just requirements-report-json`.
- CI: the `visual` job already used about 90 % of its 15 minute limit (its healthy runs last 11m45 to
  14m05; the test step alone is 11 to 13 minutes). Putting the report and the map tests in it added
  75 to 90 s and got it cancelled twice, in the last seconds, just as the map test started. Nothing was
  hung or waiting: `test:viewer-graph` takes 18.5 s in CI (17 s locally) in the green run, and the report it needs took 56 s in the `visual` job (59 s locally, 14 to 18 s of it
  a status print the test does not use, 22 s a Markdown copy it does not read). The cause is the job's
  budget: the unchanged visual test step alone takes 11 to 13 minutes. The report step is now JSON only
  (about 23 s locally instead of 60 s), and the map tests and report
  now run in a job of their own (1m24 in CI), in parallel; `visual` is back to what it ran before,
  and no timeout is raised.

## Impacts

Visible on every use case page of the requirements site: a smaller, joined map and full IDs in
link texts. Heights and captures are in Deliverables: six maps are 12 to 56 % shorter at 1280 px; three are taller at 800 px.

## Blast radius

Grade: **1**. Only the generated requirements site's viewer and its tests change, nothing under
`src/`. A plain `git revert` restores the previous map.

## Autonomous decisions

- Third path colour comes from a site token `--p3` built on the extension's cream yellow, not a raw
  colour, because the site takes every colour from the cream block.
- Play gets its own new requirement (CORE-091) rather than an item of CORE-081, so its test and
  marker stay apart.
- Map size bound is "shorter than before at 1280 px"; at 800 px one map was already taller in the
  prototype.
- A missing requirements report fails the browser test in CI and skips it locally.

## Known gaps

- Numbered badges at every path start, a two-colour border on shared pills and a stronger scroll hint
  are not part of this change.
- The `visual` job still takes 12 to 14 minutes of its 15 minute limit without this change's additions (its test step is the slow part); it is a separate follow-up, not changed here.
- **UNVERIFIED:** the CI timing figures of the `visual` job and of the report step (about 90 % of its limit, 11m45 to 14m05, cancelled twice, 17 to 19 s, 43 s locally) come from the author's own measurements and logs; the durations 13m05 and 1m24 of the green run are verified.
- At 800 px three of the six measured maps are taller than before (listed under Deliverables); the bound is the 1280 px one.

## Test plan

- [x] New or changed tests (they fail on the previous code): `metroMap.test.ts`, `pages.test.ts`,
      `metroMap.browser.test.ts`
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates at `d20b0bf`: `just check` pass, `just preflight` pass, `just ci-viewer-graph` pass
      (43 s), `npm run test:viewer-graph` 4 of 4 pass on the real report
- [x] Evidence: before at `8d99cd1`, after at `d94b5ec` (carried to `d20b0bf`, the move touches no site code); twelve captures in Deliverables
- [x] Review: approved at `d20b0bf` (round 4, the CI job split; earlier rounds approved at 5abb7af and d94b5ec)
- [x] Verified at `d20b0bf` (map claims carried from `d94b5ec`; CI split and job durations proved at `d20b0bf`)
- [x] CI green at `d20b0bf`: static, static-windows, visual (13m05), viewer-graph (1m24), report pass

## Internal references

CR-441 path-graph.
