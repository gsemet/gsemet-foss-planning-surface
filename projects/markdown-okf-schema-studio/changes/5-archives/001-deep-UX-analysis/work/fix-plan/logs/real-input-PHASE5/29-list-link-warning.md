# 29-list-link-warning

`StRS-BX` typed in a new list item: the datalist offered the known stems and the warning is shown.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: Linked list
derives_from:
- StRS-A
---

# Requirement

Body text.

```

## Machine checks

- PASS `overlay-covers-text`: no overlay covers preview text
- PASS `overlay-clipped`: every overlay is inside the viewport
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
