# 06-table-padded-edit

Edit mode on; the padded table cell `second` gained ` X` and Enter saved it. The buffer changed only the line `| first    | second X |`; the alignment padding is kept.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Table document

| Column A | Column B |
|----------|----------|
| first    | second X |

Between the tables.

| Step | Owner |
|---|---|
| Plan | Ana |
| Ship | Bo |

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
