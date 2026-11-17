# 26-boolean-one-click

Edit mode on; one click on the annotation_exemption checkbox saved `true`. No editor stays open.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: Boolean field
annotation_exemption: true
---

# Requirement

Body text.

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
