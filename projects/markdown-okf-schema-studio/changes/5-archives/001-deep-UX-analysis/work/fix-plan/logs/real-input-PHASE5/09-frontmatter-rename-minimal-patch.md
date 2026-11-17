# 09-frontmatter-rename-minimal-patch

Edit mode on; the name cell `summary` was renamed to `abstract` by select-all, typing and Enter. The buffer changed only the line `abstract: When export ...`; the continuation line `  as CSV.` is untouched.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
---
type: req
title: Write CSV output
status: draft
tags:
- alpha
- beta
abstract: When export is requested, the service SHALL write the report
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
