# 07-table-compact-edit

Edit mode on; the compact table cell `Ana` gained ` Lee` and Enter saved it. The buffer changed only the line `| Plan | Ana Lee |`; the compact `|---|---|` delimiter is untouched.

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
| Plan | Ana Lee |
| Ship | Bo |

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
