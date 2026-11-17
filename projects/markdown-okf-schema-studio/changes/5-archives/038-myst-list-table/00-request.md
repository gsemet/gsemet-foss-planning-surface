# 038 — myst-list-table

From backlog `P3/list-table-support` (files copied here as `backlog-*` / images).

## Problem

MyST {list-table} (https://mystmd.org/guide/tables) is not rendered and there is no table conversion.

## Decisions (user grill, 2026-10-22 night plan)

1. Render {list-table} with :header-rows:, :widths:, :align: and a title argument, consistent with existing table styles.
2. Decision: a button in the table-level toolbar converts pipe table → list-table and list-table → pipe table; a simple HTML table converts to either; never produce HTML. A conversion that would lose content (multi-line cells or block content to pipe) shows a message and changes nothing.
3. Conversion is one undo step; round trip pipe → list-table → pipe is lossless for simple tables (unit tests with src/webview/markdownTable.ts helpers).

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
