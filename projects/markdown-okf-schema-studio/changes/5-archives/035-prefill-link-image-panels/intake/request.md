# 035 — prefill-link-image-panels

From backlog `P3/edition-link` (files copied here as `backlog-*` / images).

## Problem

In edit mode with the caret inside a link, the toolbar link button opens an empty panel and inserts a new link.

## Decisions (user grill, 2026-10-22 night plan)

1. Decision: with the caret (or selection) inside an existing Markdown link, the link panel opens pre-filled (text + URL + title if any) and Save REPLACES that link; same for images (alt + path + title) with the image panel.
2. All block and cell editors that offer these panels (src/webview/linkPanel.ts, figurePanel.ts, editActions.ts...). Reference-style links: pre-fill from the definition when resolvable, else insert inline (note it).
3. Undo restores the previous link in one step; no change when the caret is outside any link/image.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
