# 14-escape-keeps-table-cell

Edit mode on; the cell `two` gained `2` and Escape closed the editor. The buffer contains `| beta | two2 |`.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Smoke document

First paragraph line one
continues on line two.

Second paragraph. KEEP ME PLEASE. B

| Name | Value |
|------|-------|
| alpha | one |
| beta | two2 |

- item one
- item two

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
