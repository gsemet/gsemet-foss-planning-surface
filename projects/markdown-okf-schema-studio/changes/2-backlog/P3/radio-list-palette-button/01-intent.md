# Radio list palette button

Feature · P3 · Owner decision 2026-10-31 (CR 214 scope review)

:::{note}
CR 214 adds radio choice lists (`- ( )` / `- (x)`) without an insert button: they render in every
palette mode, and authors type them. This item is the follow-up button, if wanted.
:::

## Intent

A palette button (and a slash-menu entry) that inserts a radio group of two options, the first one
preselected, at the caret, like the task-list button does.

## Done when

- [ ] The button inserts a two-item `( )` / `(x)` group with a minimal diff and one undo step.
- [ ] It appears in the palette modes that show the task-list button.
