# 03-arrow-navigation

Edit mode on; ArrowDown at the end of the paragraph moved the raw Markdown editor to the table, whose textarea starts with `| Name | Value |`.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Smoke document

First paragraph line one
continues on line two.

Second paragraph.

| Name | Value |
|------|-------|
| alpha | one |
| beta | two |

- item one
- item two

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
