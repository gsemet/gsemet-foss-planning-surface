# 25-table-toolbar

Edit mode on; the cell `one` is open. The toolbar sits in the flow above the table with text labels, and the selected cell is outlined.

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

- PASS `overlay-covers-text`: no overlay covers preview text
- PASS `overlay-clipped`: every overlay is inside the viewport
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
