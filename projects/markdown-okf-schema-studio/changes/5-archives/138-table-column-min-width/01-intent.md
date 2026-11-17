# Table columns in the preview are too narrow: double the minimum width

Type: fix · Priority: P1 · Reported 2026-10-27 by the user with a screenshot

![A rendered table whose first columns are so narrow that "document", "parse" and "HTML out" wrap one or two letters per line](evidence/image-narrow-columns.png)

## Problem

In the rendered preview (read mode), a table with many columns squeezes some columns to a few
characters: words wrap letter by letter ("do / cu / me / nt", "pa / rs / e", "H / T / M / L").

## Expected

- The minimum width of a table column in the preview is **doubled** (user's words: "juste
  doubler"); a table wider than the column then uses the existing wide-table behaviour
  (break out of the text column in Auto width, horizontal scroll otherwise).
- Edit mode keeps its own cell minimum (CR 113) unless it shares the same rule; say which in the
  report.
- Proof: before/after real-window screenshots of the audit report's "Reference numbers" table
  (`.agents/changes/02-backlog/P3/audit-performance-security-maintainability/report.md`), cream
  and one dark theme; a webview test asserting the computed minimum column width.
