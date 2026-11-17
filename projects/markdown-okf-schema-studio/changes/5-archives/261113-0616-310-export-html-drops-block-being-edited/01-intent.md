---
title: Export to HTML drops the block being edited when a block editor is open
description: Known issue found by CR 288 (single HTML export), recorded in SwRS TOOLBAR-137.
status: inbox
date: 2026-11-11
---

# Export to HTML while a block is being edited

When the reader exports the page to a single HTML file while a block editor is open, the exported
file lacks that block. CR 288 recorded it as a Known issue in SwRS-MDOKFSTUDIO-TOOLBAR-137. Fix:
export the block's rendered content (or its last saved state) even while it is being edited, and
remove the Known issue.
