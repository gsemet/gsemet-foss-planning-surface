# 31-frontmatter-actions-picker

Same row after clicking Add field: the picker and its Add button wrap inside the row, not over other rows.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: Requirement F1
status: draft
scope: Core
owner: platform
---

# Requirement

Body text.

```

## Machine checks

- PASS `overlay-covers-text`: no overlay covers preview text
- PASS `overlay-clipped`: every overlay is inside the viewport
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
