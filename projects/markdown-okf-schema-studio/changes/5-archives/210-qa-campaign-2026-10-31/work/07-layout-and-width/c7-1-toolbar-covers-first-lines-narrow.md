# c7-1 — In a narrow side preview the expanded toolbar covers the first lines of the document

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (2 runs) |
| Area | Chrome, width / layout |
| Modes | Side preview (about 393-438 px wide) |
| Evidence | [c7-1-toolbar-covers-text.jpg](../../evidence/c7-1-toolbar-covers-text.jpg) |
| Related | none |
| Replay | `scenarios/c7-1-toolbar-covers-first-lines-narrow.json` |

## Use case

An author keeps the preview in a narrow column beside the editor and has expanded the view
controls (the state persists across sessions).

## Steps to reproduce

1. Open `book/chapters/08-research-plan-implement.md`, run "Open Preview to Side" (pane about 393 px).
2. Click "Show view controls" (toolbar expands to 102 x 166 px), scroll to the top.
3. Read the first paragraph.

## Expected

The h1 wraps around the toolbar; body text should also keep clear of it (the content reserves
`padding-inline-end` for the toolbar width).

## Observed

The h1 avoids the toolbar, but the first two lines of the first paragraph run under it: words such
as "harness" and "coding agents be..." are hidden. Content padding-inline-end is 35 px while the
toolbar is 102 px wide (toolbar rect 322-424, y 12-178; text rects overlap it).
A collapsed toolbar still covers 1 text line when text scrolls under it (expected for an overlay).

## Impact

Unreadable words at the very top of every document in the narrow layout while controls are open.

## Where it comes from

`src/core/preview/styles/contentLayoutStyles.ts` around line 581-585: the `max()` of the
toolbar-width reserve is only effective when `--sphinx-preview-toolbar-width` is set; it is empty
on `documentElement` (read as "" in the page).

## Suggested direction

Set the toolbar-width variable when the toolbar expands, or float the first lines around it as for
the h1.

## Test to add

Page-level test: at 400 px, no text client rect of the first paragraph intersects the expanded
toolbar rect.

## Done when

The replay scenario passes.
