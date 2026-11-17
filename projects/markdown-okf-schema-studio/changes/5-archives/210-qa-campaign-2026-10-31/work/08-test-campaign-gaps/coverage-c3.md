# Coverage note, charter C3 (admonitions and the alert type dropdown)

Used 38 of 40 driver calls, 3 screenshots opened.

Exercised (real input, diff against mark, errors check):
- Alert type change through the palette Alert button and its type list, keyboard only after the
  list opens (ArrowDown, Enter): first alert and the alert inside a list item (fixtures-visual/71);
  menu inViewport, focus returns to the text box, menu closed, one-line diff, no console error.
- Type change with the caret in an alert body line, on an alert with a lazy continuation, on a
  lowercase head with trailing spaces (picking the same type is a no-op, by design).
- Nested MyST admonition: body edit (one-line diff), title block editor opens the right line range.
- Plain blockquote lazy line renders correctly (control for c3-1).

Observations, not findings:
- The type list does not preselect the current type: the first ArrowDown lands on Note.
- Opening the list needs the mouse (Alert button); no keyboard route was found in the 40 calls.

Not exercised: dropdown while scrolling, dropdown after a re-render (external rewrite), MyST
admonition type change (ADMONITION_TYPES), real book chapters with admonitions, vault notes,
alerts with code fences and lists in the body, keyboard-only route to open the list.
Harness notes: `--var nth=3` is passed as a string and clicks the first match; use a literal
number in the scenario. `Meta+ArrowUp` in the block editor textarea did not move to the start.
