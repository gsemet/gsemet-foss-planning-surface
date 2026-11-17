# Block edit toolbar covers the text being edited

User report (2026-10-26), seen on the after-screenshot of the edit-toolbar tooltip fix:
when the toolbar wraps to two rows (narrow preview), it overlaps the block editor and hides the
lines being edited (red arrow: the first text lines under the second toolbar row). The user
cannot tell what they will see under it.

![image.png](image.png)

Evidence: [after-cream-cr112.png](after-cream-cr112.png).

Expected: the toolbar never covers the edited text. Options to weigh: reserve its height above
the editor (push the editor down), place it above the block when there is room, or collapse
the second row into an overflow menu at narrow widths.

## Second case: the figure edit panel (2026-10-26)

The same overlap hides the top of the figure edit panel: the second toolbar row covers its
title ("Figure") and top edge (red arrow).

![image-figure-modal.png](image-figure-modal.png)

Evidence: [after-cream-cr117.png](after-cream-cr117.png). The fix must cover every panel opened
inside the block editor (figure, table, admonition…), not only the text area.
