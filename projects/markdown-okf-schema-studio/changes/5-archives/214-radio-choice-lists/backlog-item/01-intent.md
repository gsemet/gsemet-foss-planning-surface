# Radio choice lists: `- ( )` and `- (x)`, clickable in the preview

Feature · P2 · Owner request 2026-10-31 · Next CR after 213

:::{important}
**Owner decisions, 2026-10-31.**
- Syntax: a list item that starts with `( )` or `(x)`, like a task list with parentheses.
- Clicking an option in the preview writes the change to the file.
- In the same CR, the writing skill and the QA bug template learn to use it.
:::

## Intent (owner, verbatim French)

> est ce que des choix multipes existent en markdown ? … ah tu peux rajouter le support de input
> radio en CR ?

The trigger: QA bug tickets need "pick one" sections, such as a fix direction with several
approaches. Task lists allow two ticks, so an agent cannot trust them as a single choice.

## Syntax

````markdown
Fix direction:

- (x) A click in the margin around the block opens its editor
- ( ) Alt+click on the link opens the editor
- ( ) Leave as is: edit link-only blocks in the source
````

| Rule | Behaviour |
| --- | --- |
| Group | Consecutive radio items of the same list form one group; a blank line, a heading or another list ends it |
| Marker | `( )` unselected, `(x)` or `(X)` selected; a space after the marker |
| Mix | A list that mixes `[ ]` and `( )` items: each item keeps its own kind; a radio group is the run of `( )` items |
| No selection | Allowed; rendered as an unselected group |
| Two `(x)` in the source | Rendered as written (both selected); the first click normalises the group |
| Nested | Nested lists form their own groups |
| Elsewhere | On GitHub and in plain editors the list stays readable as `( )` and `(x)` text |

## Click in the preview

- A click on an option moves the `x`: the old option becomes `( )` and the clicked one `(x)`. The
  diff touches at most two lines, and one undo step reverts it.
- It follows the same path, guards and read-only rules as the clickable task-list checkboxes
  (trust, read-only roots, an open block editor, a stale document).
- Keyboard: the arrow keys inside a focused group, and Space to select, as a native radio group
  does.
- Accessibility: `role="radiogroup"` and `role="radio"` with `aria-checked`.

## Same CR: the writing skill and the QA bug template

- `skills/writing-for-markdown-okf-schema-studio/SKILL.md`: one row in "What renders", plus one
  example rendered by its own pipeline in a test, like the other examples.
- `.agents/skills/markdown-studio-exploratory-qa-claude/references/qa-bug-template.md` (after
  CR 213 lands): a proposal section that offers several approaches uses a radio group, with the
  recommended option preselected. A single proposal keeps `Uncheck to disagree: [x]`. An agent that
  reads a ticket checks for exactly one `(x)`; if there is none, or more than one, it asks the
  owner.

## Done when

- [ ] Parser and renderer, with unit tests for the group rules above.
- [ ] The click writes a minimal diff, with a real-input E2E test (click, diff, undo).
- [ ] Visual scenarios in Cream and Dark, plus before/after screenshots in the PR.
- [ ] A new SwRS (proposed) and the user documentation.
- [ ] The writing skill and the QA bug template are updated.
