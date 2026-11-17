# 38-anchor-enabled

A text editor now shows the file beside the Open With editor: the anchor button is enabled.

Edit mode: off.

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
