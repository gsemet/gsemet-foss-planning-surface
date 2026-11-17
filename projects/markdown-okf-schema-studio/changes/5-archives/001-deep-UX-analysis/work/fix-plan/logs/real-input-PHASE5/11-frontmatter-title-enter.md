# 11-frontmatter-title-enter

Edit mode on; the title was replaced and Enter saved it as a one-line scalar.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: 'Write CSV output: with quotes "and" colons'
status: draft
tags:
- alpha
- beta
summary: When export is requested, the service SHALL write the report
  as CSV.
derives_from:
- StRS-CORE-001
---

# Requirement

Body text.

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
