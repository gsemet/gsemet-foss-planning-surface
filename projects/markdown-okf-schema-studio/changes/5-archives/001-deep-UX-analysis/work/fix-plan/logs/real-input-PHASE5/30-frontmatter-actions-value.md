# 30-frontmatter-actions-value

Window 1100 px wide, preview frame 521 px. The `scope` value editor is open; Add field / Remove field sit under the one-row textarea inside the row and cover no other row.

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
