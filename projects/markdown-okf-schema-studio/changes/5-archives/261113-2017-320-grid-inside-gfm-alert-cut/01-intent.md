# A grid inside a GitHub alert is cut

Type: fix. Filed 2026-11-12 by the grill advisor of batch-02; grilled 2026-11-13 by the Chief of
Staff.

## Owner's words

> grillons les tous de suite

## Problem

A `::::{grid}` written inside a GitHub alert (`> [!NOTE]`, or the bold form `> **Note**`) renders
cut: the grid and the cards after its first inner fence fall out of the note.

## Cause (read at `main`)

`expandGithubAlertsWithLines` in `src/core/render/mystGithubAlerts.ts` rewrites the alert as a
three-colon admonition (`:::{note}`) when it is not itself inside a colon container. A colon fence
closes at the first colon line at least as long as its own, so the grid's inner `:::` closing line
(a card's) closes the note, and the four-colon grid cannot nest inside a three-colon note anyway.
The backtick form is used only when the alert sits inside a colon container.

## Scope

- The rewritten admonition's fence is longer than every colon fence opened in the alert's quoted
  body (for example `:::::{note}` around a `::::{grid}`), so no inner line closes it; with no inner
  colon fence it stays `:::`, so the common case does not change. The existing backtick choice
  inside a colon container stays.
- The line map (`sourceLines`, `alertLines`) keeps mapping every line back to the document.
- A test, written first and failing on `main`: a grid with two cards inside `> [!NOTE]` and inside
  `> **Note**` renders as one note holding the whole grid, and a click on a card maps to its line.
- SwRS-MDOKFSTUDIO-GFM-009 gains the nested-container case.
- Visible change: the grid now shows inside the note, as GitHub users expect.
