# 17-enter-continues-list

Edit mode on; Enter after `Refrigerated goods` continued the list, and `Frozen goods` is a sibling at the same indentation while `Deduplication` kept its place.

Edit mode: on.

Real VS Code window; every action is a real mouse or keyboard event dispatched by Playwright through CDP. Buffer excerpt at capture time:

```markdown
# List document

- Intake
  - Dry goods
    - Refrigerated goods
    - Frozen goods
  - Deduplication

```

## Machine checks

- n/a `overlay-covers-text`: no visible overlay
- n/a `overlay-clipped`: no visible overlay
- n/a `identifier-split`: no identifier cell
- n/a `status-two-lines`: no status with a strong line and message
