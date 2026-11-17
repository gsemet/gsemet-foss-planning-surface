## Summary

Inserting a figure from the palette and choosing an image used to leave a bare `figure` directive in
the editor; the user then had to find and open the figure form by hand. The figure form now opens
right after the image is chosen, with the caret on the Caption field and Source and Alt already
filled in, like other editors that open their properties dialog on insert.

## Deliverables

```text
Insert figure -> pick image -> figure inserted -> "Edit figure" form opens on Caption
                                                   Apply: caption written   Cancel: default figure kept
```

Before (directive only, no form) and after (form open on Caption), cream and dark themes:

| | Cream | Dark |
|---|---|---|
| Before | ![before cream](reports/shots/before-cream.png) | ![before dark](reports/shots/before-dark.png) |
| After | ![after cream](reports/shots/after-cream.png) | ![after dark](reports/shots/after-dark.png) |

(Screenshot files are attached by the stack step; local copies are in `reports/shots/`.)

- `editPalette.ts`, `figurePanel.ts` and the page wiring: open the figure form after the pick and
  focus the caption.
- Tests: a runtime test (fails on the old code) and a real-window scenario (image dialog stubbed,
  caption typed, Apply, save).
- Requirements PALETTE-150 and PALETTE-153, user docs and CHANGELOG updated.

## Autonomous decisions

- The form opens focused on the Caption field.
- Cancel keeps the inserted figure with its default values.
- The new real-window scenario is not yet in the stress plan or capture registry.

## Internal references

CR 117 (`117-insert-figure-opens-editor`), backlog item `bug-edit-figure`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
