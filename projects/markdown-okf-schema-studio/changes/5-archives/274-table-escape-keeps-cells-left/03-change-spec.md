---
title: "CR 274: Escape in a table cell keeps the cells left with Tab"
description: QA271-01 (High), Escape in the next cell drops the text typed in the cells already left while the preview still shows it.
status: open
date: 2026-11-10
---

# CR 274: Escape in a table cell keeps the cells left with Tab

> [!NOTE]
> Source: QA campaign 271, finding QA271-01 (High, reproduced, replayed). Sheet:
> `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/03-table-cell-editing/c2-1-escape-after-tab-drops-previous-cells.md` (read it: steps, variants,
> code pointers). Owner's answers: `02-answers.md` (authoritative). No GitHub issue.

## What ships

- In a table cell edit session, Escape cancels only the text typed in the cell it is pressed in. The
  cells left earlier in the session with Tab, an arrow key or a click keep their typed text in the
  buffer, and the page shows it.
- The shown text of every cell equals the buffer after Escape (no cell shows text the buffer lost).
- Escape in the first and only cell of a session behaves as today (TABLE-025 nominal scenario).
- Enter, blur, Tab and the IME composition rules are unchanged.

## Requirements

`SwRS-MDOKFSTUDIO-TABLE-025` (stable, not approved: no recorded agreement needed) is amended: Escape
drops the text typed in the open cell only, keeps the cells already left in the session, and the
preview shows what the buffer holds. Check `TABLE-013` (one session across cells) and `TABLE-035` (the
cell left shows its text) stay true; add a scenario rather than change their intent. If an
**approved** requirement must change, stop with `status: blocked` and the exact sentence.

## Tests

- Unit (`test/page/runtimeTableCellEditor.test.ts` or its neighbour): type in cell A, Tab, type in
  cell B, Escape: the saved table holds A's text and not B's; same after ArrowRight and after a click.
  Must fail on the unchanged code.
- A real-input scenario in `test/integration/realInput/` promoting the QA replay
  `271-c2-1-escape-after-tab-reverts-previous-cell.json` (branch `qa/271-table-campaign-replays`, local
  commit 87307e8f, not pushed: read it there with `git show`; do not merge that branch): type, Tab,
  Escape; the buffer line and the shown cell agree. CI runs it (heavy run).

## Done when

- The variants of the sheet (Tab, Tab Tab, ArrowRight, click) all keep the text of the cells left.
- `just check`, `just requirements-update`, a dated log entry, a `CHANGELOG.md` `## Unreleased` line.
- PR opened as a draft, marked ready only when CI (PR and heavy run) is green and the Inspector approved.
