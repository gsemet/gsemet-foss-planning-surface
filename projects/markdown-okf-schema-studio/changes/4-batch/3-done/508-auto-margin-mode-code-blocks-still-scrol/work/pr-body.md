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

The screenshots show that in Auto width the widened code blocks lose their scroll bar, captioned ones included, and that Margin looks the same.

Auto width, a numbered Python block and the same block with a caption (688 px column):

| Before (`4a47151`) | After (`09e8acf`) |
| --- | --- |
| ![Before, Auto: both blocks show a scroll bar](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/base-auto-cream-1100.png) | ![After, Auto: both blocks are widened and show no scroll bar](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/head-auto-cream-1100.png) |

Margin width, same page (unchanged, the two captures are identical):

| Before (`4a47151`) | After (`09e8acf`) |
| --- | --- |
| ![Before, Margin: both blocks keep the column and scroll](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/base-margin-cream-1100.png) | ![After, Margin: both blocks keep the column and scroll](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/head-margin-cream-1100.png) |

A real page in the VS Code preview, Auto width:

| Before (`4a47151`) | After (`09e8acf`) |
| --- | --- |
| ![Before, VS Code: the widened block still shows a scroll bar](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/base-vscode-auto-planning-page.png) | ![After, VS Code: the block fits, no scroll bar](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/62364df7aaf8a35a3735dbd349915fa6e39316e9/head-vscode-auto-planning-page.png) |

## Blast radius

The change is confined to the Auto width measure of the preview page, and only for code blocks. A plain `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

- A 1 px tolerance is dropped only for a code block whose code overflows; keeping it for blocks that fit avoids marking every code block under display scaling, where box widths are fractional.
- A figure counts as a captioned code block only when the `pre` is its direct child, so Mermaid diagrams are measured as before.
- Code blocks nested in a container are left as they are: only top-level blocks widen, as for tables.

## Known gaps

- A code block inside a list, admonition, quote, tab or card still scrolls inside its container in Auto width.
- In a widened code block the longest line ends flush against the block's right border: the browser leaves the block's right padding out of the code's scroll width, before this change as after, so the measured width does not include it. It is left because the change keeps the block's look as it is; adding that padding to the measured width would close it.

## Test plan

- [x] New or changed tests (at `09e8acf`; they fail on the previous code, `4a47151`): the unit tests of the border, the caption and the 1 px overflow, and all 6 real-browser tests
- [x] Requirements: `SwRS-MDOKFSTUDIO-LAYOUT-023` updated (still proposed) at `09e8acf`, markers in code and tests, `just requirements-update`
  - Source: `src/page/modules/widthMode.ts`, `src/page/features/scrollCore.ts` (unchanged)
  - Tests: `test/page/runtimePageControls.test.ts`, `test/page/codeBlockBreakout.test.ts` (new); unchanged: `test/core/preview/previewStyles.test.ts`, `test/page/diagReq.layout.requirements.test.ts`, `test/page/runtimeScroll.test.ts`, `test/page/tableBreakout.test.ts`, `test/page/widthModeScenarios.test.ts`, `test/visual/capture_layout_checks.py`, `test/visual/capture_width_scroll.py`, `test/visual/widthScrollScenarios.ts`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md` at `09e8acf`
- [x] Local gates at `09e8acf`: `npm run test:breakout` 14 passed with Chromium required; `just preflight` passed (static stage on Windows: unit 5221 passed, 21 skipped; pytest 205 passed)
- [x] Review: approved at `09e8acf`
- [x] CI green at `09e8acf`

Unit tests of the measure, run before the fix (source at `4a47151`, tests at `09e8acf`):

```text
✖ a code block that breaks out is widened by its border too            '60px' !== '62px'
✖ a captioned code block breaks out through its inner code             null !== ''
✖ a code block that overflows by 1 px still breaks out, a table ...    null !== ''
✔ the 4 cases that must not change (fits, capped, in a list, Mermaid)
tests 7, pass 4, fail 3
```

After the fix, at `09e8acf`: `tests 7, pass 7, fail 0`.

In the real browser on Windows (688 px column, 1100 px pane, Auto), `box width, clientWidth/scrollWidth` of the code:

| Block, line length | Before (`4a47151`) | After (`09e8acf`) |
| --- | --- | --- |
| Numbered Python, 97 | 696 px, 694/696 | 698 px, 696/696 |
| Plain, 100 | 688 px, 686/689 | 691 px, 689/689 |
| Captioned, 103 | 688 px, 686/709 | 711 px, 709/709 |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
