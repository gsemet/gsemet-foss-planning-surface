# 22-editor-frame-and-buttons

A paragraph editor is open and ` R` was typed: framed editor, monospace text, hint line, Done and Revert.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Affordance document

- outer one
  - inner a
  - inner b
- outer two

Alpha paragraph. R

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- n/a `identifier-split`: no identifier cell
- n/a `status-two-lines`: no status with a strong line and message
