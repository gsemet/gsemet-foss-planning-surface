# 32-save-keeps-list-in-place

Edit mode on; `Frozen goods` was added with Enter and committed with Mod+Enter in a list whose top was 39.609375 px below the preview top (reading line at 81.80000000000001 px). List top after Save T1=39.609375, after a second render T2=39.609375, 700 ms later T3=39.609375.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# Pinned list

Before paragraph 1 of filler text.

Before paragraph 2 of filler text.

Before paragraph 3 of filler text.

Before paragraph 4 of filler text.

Before paragraph 5 of filler text.

Before paragraph 6 of filler text.

Before paragraph 7 of filler text.

Before paragraph 8 of filler text.

Before paragraph 9 of filler text.

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- n/a `identifier-split`: no identifier cell
- n/a `status-two-lines`: no status with a strong line and message
