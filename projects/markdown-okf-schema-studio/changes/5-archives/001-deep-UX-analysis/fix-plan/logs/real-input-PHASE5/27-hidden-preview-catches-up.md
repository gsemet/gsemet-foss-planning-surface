# 27-hidden-preview-catches-up

The preview was hidden behind another tab, the editor scrolled about 200 lines, and the revealed preview shows the editor's top line.

Edit mode: off.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
## Section 0

Paragraph 0 line one
continues on line two.

## Section 1

Paragraph 1 line one
continues on line two.

## Section 2

Paragraph 2 line one
continues on line two.

## Section 3

Paragraph 3 line one
continues on line two.

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- n/a `identifier-split`: no identifier cell
- n/a `status-two-lines`: no status with a strong line and message
