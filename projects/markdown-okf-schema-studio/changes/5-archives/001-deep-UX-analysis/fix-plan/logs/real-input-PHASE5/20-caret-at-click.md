# 20-caret-at-click

Edit mode on; clicking the word `bravo` placed the caret there, and the typed `X` landed in line one.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Caret document

Alpha Xbravo charlie
delta echo foxtrot
golf hotel india.

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- n/a `identifier-split`: no identifier cell
- n/a `status-two-lines`: no status with a strong line and message
