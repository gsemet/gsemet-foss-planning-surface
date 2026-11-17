# In a narrow side preview the expanded toolbar covers the first lines of text

Severity Medium · Reproduced · Verdict Gap · Requirements: none found · Area Chrome, width and layout · Side preview · QA210-09 · Replay `scenarios/c7-1-toolbar-covers-first-lines-narrow.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![393 px pane: toolbar over the first paragraph](evidence/currently.jpg) | ![Same document in a 566 px pane: text clear of the toolbar](evidence/expected.jpg) |
| *Currently: at 393 px the expanded toolbar covers the end of the first paragraph lines (replay `c7-1` on b9118506).* | *Expected: the same document after dragging the sash to a wider pane, text and toolbar do not overlap; at 380-440 px the text must reserve the toolbar width.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author who keeps the preview in a narrow column and has expanded the view controls (the state
persists) cannot read the first two lines of the first paragraph: words such as "harness" and
"coding agents be..." are hidden under the toolbar. The h1 already wraps around the toolbar, so the
page knows how, and the same document is clear in a wider pane. The layout requirements keep the
toolbar off the first editor, button and properties table (LAYOUT-011 to 016), but none covers
plain body text, so nothing guards this.

## Steps to reproduce

1. Open `book/chapters/08-research-plan-implement.md`, run "Open Preview to Side" (pane about
   393 px).
2. Click "Show view controls" (the toolbar expands to 102 x 166 px) and scroll to the top.
3. Read the first paragraph: its first two lines run under the toolbar (toolbar rect 322-424,
   y 12-178; content `padding-inline-end` is 35 px).

## Impact

Unreadable words at the top of every document in the narrow layout while the controls are open.
A collapsed toolbar covers one line only when text scrolls under it, which is expected for an
overlay.

## Where it comes from

`src/core/preview/styles/contentLayoutStyles.ts` around lines 581-585: the toolbar-width reserve
uses `--sphinx-preview-toolbar-width`, which is empty on `documentElement`.

## Suggested direction

Set the toolbar-width variable when the toolbar expands, or float the first lines around it as for the h1. Done when: no text sits under the expanded toolbar at 380-440 px; replay `c7-1` passes.

Uncheck to disagree: [x]

## Requirement to write or change

Write a new SwRS (Gap): "Body text keeps clear of the expanded toolbar" - When the floating toolbar is expanded in a pane narrower than 440 px, the extension SHALL keep the text of the first blocks outside the toolbar rectangle.

Uncheck to disagree: [x]

## Test to add

No test: a layout measure at one width is brittle and cosmetic; the requirement and the replay `c7-1` are the check.

Uncheck to disagree: [x]

Sources: sheet [c7-1](../../../210-qa-campaign-2026-10-31/work/07-layout-and-width/c7-1-toolbar-covers-first-lines-narrow.md),
replay [c7-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c7-1-toolbar-covers-first-lines-narrow.json),
[campaign index](../../../210-qa-campaign-2026-10-31/work/00-index.md).
