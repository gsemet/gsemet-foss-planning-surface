# 24-table-tab

Edit mode on; Tab moved from `one` to `beta` (typed `X`) and `two`, on to a new third row where `gamma` and `three` were typed; Enter saved. The buffer holds the new row.

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
| betaX | two |
| gamma | three |

- item one
- item two

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
