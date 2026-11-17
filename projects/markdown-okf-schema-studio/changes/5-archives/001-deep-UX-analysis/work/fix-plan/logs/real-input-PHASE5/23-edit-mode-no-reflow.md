# 23-edit-mode-no-reflow

Edit mode on; hard-wrapped paragraphs (about 40 characters per source line) keep their reading flow.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Reflow document

alpha bravo charlie delta echo foxtrot
golf hotel india juliet kilo lima mike
november alpha bravo charlie delta echo
foxtrot golf hotel india juliet kilo

delta echo foxtrot golf hotel india
juliet kilo lima mike november alpha
bravo charlie delta echo foxtrot golf
hotel india juliet kilo lima mike

golf hotel india juliet kilo lima mike
november alpha bravo charlie delta echo
foxtrot golf hotel india juliet kilo
lima mike november alpha bravo charlie

| Name | Value |
|------|-------|
| alpha | one |
```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- PASS `identifier-split`: identifier cells stay on one line
- n/a `status-two-lines`: no status with a strong line and message
