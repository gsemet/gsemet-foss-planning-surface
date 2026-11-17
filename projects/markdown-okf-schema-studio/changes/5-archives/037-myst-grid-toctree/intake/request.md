# 037 — myst-grid-toctree

From backlog `P3/grid-support` (files copied here as `backlog-*` / images).

## Problem

MyST {grid} and {toctree} directives are not rendered.

## Decisions (user grill, 2026-10-22 night plan)

1. Decision {grid}: responsive columns per the `1 1 2 2` breakpoints argument, with grid-item and grid-item-card (title, body, footer, link); both ``` and ::: fences, nesting with colon fences.
2. Decision {toctree}: a list of clickable links to the referenced documents; label = the target's H1 when readable, else the file name; :caption: renders as a heading; :hidden: hides the list; globs: list matching files sorted; missing target: entry shown with a warning style. Links use the existing link navigation (open in preview).
3. Readable in all themes; narrow pane collapses to one column.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
