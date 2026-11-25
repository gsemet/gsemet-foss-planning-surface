## Summary

With the Width button on Auto, a code block whose longest line is a little wider than the text column still showed a horizontal scroll bar. The widened block was 2 px too narrow (its two borders were not counted), and a code block with a caption was never widened at all. In Auto a code block now widens until its longest line fits, as a wide table does.

## Deliverables

| Code block in Auto width | Before | After |
| --- | --- | --- |
| Longest line a little wider than the column | Widened, still scrolls by 2 px | Widened, no scroll bar |
| Overflow of up to 3 px | Not widened, scrolls | Widened, no scroll bar |
| With a caption (`:caption:`) | Never widened, scrolls | Widened with its caption bar |
| Line wider than the space left of the table of contents | Capped, scrolls | Capped, scrolls (unchanged) |
| Inside a list, admonition, quote, tab or card | Keeps its container's width, scrolls | Unchanged |

The width a code block needs is now measured on its whole box:

```ts
// code = the `pre`, or the direct `pre` child of a captioned figure
const codeNeed = box - code.clientWidth + code.scrollWidth;
```

## Changes

- `src/page/modules/widthMode.ts`: a code block is measured through its `pre` (borders included, and the figure around a captioned one). A code block whose code really overflows is widened from a gain of 1 px; every other block, and a code block that fits, keeps the 1 px rounding tolerance.
- `test/page/runtimePageControls.test.ts`: unit tests of the measure.
- `test/page/codeBlockBreakout.test.ts` (new): the rendered page and the shipped stylesheet in Chromium, across the dark background and line number settings, at 125 % display scaling and with the table of contents open. `npm run test:breakout` runs it, so the visual CI job does.
- `test/build/test_workflows.py`: the check of the `test:breakout` script now expects both files.
- Requirement `SwRS-MDOKFSTUDIO-LAYOUT-023`, `docs/user/wide-tables.md` and the changelog describe the rule.

## Impacts

In Auto width, code blocks a little wider than the column no longer show a scroll bar. Margin and Full width are unchanged, and so is the measure of tables, images and diagrams. No setting changes.

## Blast radius

The change is confined to the Auto width measure of the preview page, and only for code blocks. A plain `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

- A 1 px tolerance is dropped only for a code block whose code overflows; keeping it for blocks that fit avoids marking every code block under display scaling, where box widths are fractional.
- A figure counts as a captioned code block only when the `pre` is its direct child, so Mermaid diagrams are measured as before.
- Code blocks nested in a container are left as they are: only top-level blocks widen, as for tables.

## Known gaps

- A code block inside a list, admonition, quote, tab or card still scrolls inside its container in Auto width.

## Test plan

- [x] New or changed tests (they fail on the previous code): the 1 px, border and caption unit tests fail before the fix; all 6 real-browser tests fail before it and pass after
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `npm run test:breakout` 14 passed with Chromium required; `just check` passed (unit 5221 passed, 21 skipped; pytest 205 passed); `just preflight` passed (static stage on Windows)
- [ ] Review
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)
