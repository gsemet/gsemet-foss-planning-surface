# 16-undo-stays-side

Typed ` abc` and ` def` inline (side); Cmd/Ctrl+Z undid typing inside the textarea and Cmd/Ctrl+Shift+Z restored it; the inline editor stayed open and focused.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Smoke document

First paragraph line one
continues on line two.

Second paragraph. abc 

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
