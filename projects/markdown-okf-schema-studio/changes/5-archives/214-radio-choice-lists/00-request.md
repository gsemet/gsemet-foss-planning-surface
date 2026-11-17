# 214 — Radio choice lists: decide in the page

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** A **differentiating feature**: multiple choice in
Markdown, for plans. An agent proposes two or three approaches with the recommended one preselected,
and the owner switches the choice with one click in the preview. Stacked on the QA template CR (213),
which provides `qa-bug-template.md`. One clean commit, one ready PR, never merge.
:::

The full intent is in [backlog-item/01-intent.md](backlog-item/01-intent.md).

## Syntax and rules (owner-approved)

````markdown
Fix direction:

- (x) A click in the margin around the block opens its editor
- ( ) Alt+click on the link opens the editor
- ( ) Leave as is: edit link-only blocks in the source
````

| Rule | Behaviour |
| --- | --- |
| Group | **At least 2** consecutive radio items of the same list; a lone `( )` or `(x)` item stays plain text |
| Marker | `( )` unselected, `(x)` or `(X)` selected; a space after the marker |
| End of group | A blank line, a heading, another list, or a non-radio item ends the run |
| Mix | A list that mixes `[ ]` and `( )` items: each item keeps its own kind |
| No selection | Allowed, rendered unselected |
| Two `(x)` in the source | Rendered as written; the first click normalises the group |
| Nested | Nested lists form their own groups |
| Label | No label syntax: the paragraph just above the list is the label (`aria-labelledby`) |
| Modes | Renders in every palette mode (Strict, GFM, MyST, Full); no insert button in this CR (P3 `radio-list-palette-button`) |
| Elsewhere | On GitHub and in plain editors the text `( )` / `(x)` stays readable |

## Interaction (owner-approved)

| Input | Effect |
| --- | --- |
| Click an unselected option | Old option becomes `( )`, the clicked one `(x)`: **at most two lines change, one undo step** |
| Click the selected option | Nothing: no write, no deselect |
| Arrow keys in a focused group | Move the focus only |
| Space or Enter | Select the focused option and write; one undo step |

- Same path, guards and read-only rules as the clickable task-list checkboxes: trust, read-only roots,
  an open block editor, a stale document. Reuse them, do not duplicate them.
- Accessibility: `role="radiogroup"`, `role="radio"` with `aria-checked`, roving `tabindex`.

## Showcase

> [!TIP]
> This is the feature to show first: "decide in the page".

- **README:** a section near "Review with comment threads", for example
  `### Decide in the page: choices in your plans`. A short plan with a radio group (two or three
  approaches, the recommended one preselected) and the owner switching the choice with one click.
  Screenshot from a visual scenario, in **Cream and Dark**, captured like the other README images.
- **Demo fixture:** a plan document with one or two radio groups and a task list, reused by the README
  shot and by the demo video (CR 170 adds the video part).
- **Writing skill** (`skills/writing-for-markdown-okf-schema-studio/SKILL.md`): one row in "What
  renders", and a **plan** as the tested example, not a generic list.
- **QA bug template** (`references/qa-bug-template.md`): a proposal section that offers several
  approaches uses a radio group with the recommended option preselected; a single proposal keeps
  `Uncheck to disagree: [x]`. An agent that reads a ticket checks for exactly one `(x)`, and asks the
  owner if there is none or more than one.

## Done when

- [ ] Parser and renderer, with unit tests for every rule in the table (including the 2-item minimum
      and the mixed list).
- [ ] Real-input E2E: click writes at most two lines, undo reverts in one step, clicking the selected
      option writes nothing, Space and Enter select, arrows only move the focus.
- [ ] Visual scenarios in Cream and Dark; before/after screenshots in the PR.
- [ ] A new SwRS, `--lifecycle proposed`, and the user documentation.
- [ ] README section with Cream and Dark images, the demo fixture, the writing skill example and the QA
      template updated.
- [ ] `just check` green, normal CI green.
