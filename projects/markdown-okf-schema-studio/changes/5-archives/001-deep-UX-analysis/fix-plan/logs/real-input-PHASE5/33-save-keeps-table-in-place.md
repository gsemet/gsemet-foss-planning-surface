# 33-save-keeps-table-in-place

Edit mode on; the cell `Ana` gained `-Lee` and Enter committed it in a visible table. Table top 299.125 before the click, 38.515625 at Enter and 38.125 after Save.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Pinned table

Before paragraph 1 of filler text.

Before paragraph 2 of filler text.

Before paragraph 3 of filler text.

Before paragraph 4 of filler text.

Before paragraph 5 of filler text.

Before paragraph 6 of filler text.

| Step | Owner |
|------|-------|
| Plan | Ana-Lee |
| Ship | Bo    |

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
