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

Measured heights, before and after, and the before/after captures: **UNVERIFIED:** not yet measured
on the real site at the pushed head.

<!-- screenshots go here at the closing -->

## Changes

- `layout.ts`: `buildMetroMap` (joined nodes, one edge per state-behaviour-state triple listing its
  paths, rows, columns, packing) and `metroSvg` (strokes, pills, joins and splits, start discs,
  outcomes, size).
- `pages.ts`, `urls.ts` usage: full IDs on every link text; `mapSection` carries the one-line
  reading help and the legend.
- `viewer.css`, `siteTheme.ts` (`--p3` from the extension's yellow token), `viewer.js` (Play colour
  and marker).
- Requirements: SwRS CORE-080, -081, -082, -083 updated, new CORE-091 (Play), StRS CORE-008 note, the
  project guideline (one to three paths per use case), a dated entry in the requirements log.
- Tests: `metroMap.test.ts`, `metroMap.browser.test.ts`, `metroShapes.ts`, updated `pages.test.ts`
  and fixture, pinned KaTeX fonts for the layout checks; `npm run test:viewer-graph`, run by
  `just ci-visual` after `just requirements-report`.

## Impacts

Visible on every use case page of the requirements site: a smaller, joined map and full IDs in
link texts. The before/after captures are in Deliverables once taken.

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
- **UNVERIFIED:** the heights and captures on the real site, and the first CI run of the browser test.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `metroMap.test.ts`, `pages.test.ts`,
      `metroMap.browser.test.ts`
- [ ] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `just check`, `npm run test:viewer-graph` on the real report: pass before the
      commit; the head's gates to come
- [ ] Review
- [ ] CI green

## Internal references

CR-441 path-graph.
