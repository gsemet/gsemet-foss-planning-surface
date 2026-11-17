# 34-link-diagnostic-tooltip

The invalid `missing.py` value reads `File not found` and its explanation shows on keyboard focus.

Edit mode: off.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: Broken link
implemented_in_files:
- missing.py
---

# Requirement

Paragraph 1.

Paragraph 2.

Paragraph 3.

Paragraph 4.

Paragraph 5.

Paragraph 6.
```

## Machine checks

- FAIL `overlay-covers-text`: 1 covered text excerpt(s): "Requirement"
- PASS `overlay-clipped`: every overlay is inside the viewport
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
