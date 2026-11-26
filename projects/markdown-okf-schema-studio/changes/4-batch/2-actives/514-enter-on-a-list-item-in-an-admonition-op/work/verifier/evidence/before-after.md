# CR-514 before and after

- Before: base `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f` (same tree as the restacked base
  `223a8c49a47f8af786412e7cff748860b18d3782`).
- After: `a5550c32100a24e646efdf293db93cdac30e3cba` (same tree as the restacked pull request head
  `4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e`). At the next head
  `739f9e3ecd771efce1938ebdb0685f324a6cf0a2`, the five "after" scenarios below were captured again
  against base `223a8c49` and the five images are byte-identical to the `after-*.png` here.

## Screenshots (visual harness, dark theme, 900 px)

How to reproduce, after: in the worktree at the head, `fnm exec -- npm.cmd run visual:render`,
then `.venv/Scripts/python.exe test/visual/capture.py --scenario <id>`.

How to reproduce, before: `git worktree add --detach out/vbase cd3b8e6a`; in `out/vbase` take the
head's `test/` files (the scenarios and fixtures are new), leave every existing file under `src/`
at the base, then run the same two commands there. The two source files that only the head has were
present in `out/vbase` as well; no base code imports them (the compiled base renderer holds no
`mapBoxSourceLines`).

| Gesture | Scenario | Before | After |
| --- | --- | --- | --- |
| Click the second paragraph of a note alert | `gfm/v14-alert-body-opens-pointed-paragraph-dark-900` | `before-alert-body-click.png`: one editor holds the whole alert (the scenario's checks fail) | `after-alert-body-click.png`: the editor holds that quoted paragraph, inside the alert, which stays rendered (checks pass) |
| Click the second paragraph of a `{note}` | `block-editing/v57-admonition-body-opens-pointed-paragraph-dark-900` | `before-admonition-body-click.png`: whole directive (checks fail) | `after-admonition-body-click.png`: that paragraph only (checks pass) |
| Down, Down, Right, Down, Right, Enter into a note's list | `block-editing/v59-admonition-keyboard-opens-first-item-dark-900` | `before-admonition-keyboard-enter.png`: whole directive, lines 3-8 (checks fail) | `after-admonition-keyboard-enter.png`: the first item only, line 6 (checks pass) |
| Click the title of the alert | `gfm/v15-alert-title-opens-whole-alert-dark-900` | `before-alert-title-click.png`: whole alert | `after-alert-title-click.png`: whole alert, pixel-identical (unchanged behaviour, checks pass on both) |
| Click the title of the `{note}` | `block-editing/v58-admonition-title-opens-whole-directive-dark-900` | `before-admonition-title-click.png`: whole directive | `after-admonition-title-click.png`: whole directive, pixel-identical (unchanged, checks pass on both) |

No screenshot shows a user name or a home folder.

## Text evidence for the failed claims at 739f9e3

Run from the build root, with `<build>` the worktree at the head (after) or
`<worktree>/out/vbase` at `223a8c49` (before). `<r2>` and `<repro>` stand for the full paths of the
`r2` and `repro` folders beside this one; `<node>` is
`fnm exec -- node --import ./scripts/register-myst-patches.mjs`.

### A. Enter on a formula held by a list item of a box

`<node> <repro>/gesture.js <build> <r2>/shapes/dollar-one-blank.md "y = 2" enter erase`

Source: `":::{note}\n- Text\n  $$\n  y = 2\n  $$\n\n- next\n:::\n"`.

| | Enter on the formula opens | Editor text | After erasing it and committing |
| --- | --- | --- | --- |
| Before | the whole box, lines 1-8 | the whole directive | the document is emptied (the whole box was open) |
| After | lines 2-2 | `- Text` | the text of the item is gone, the formula stays |

### B. The move chord on a callout written as a `{div}` directive

`<node> <r2>/calloutdiv.js <build>`

Source: `":::{div}\n:class: callout-tip\n\nBefore.\n\n---\n\nAfter.\n:::\n"`.

| | Chord down on "Before." | Document | Preview of the callout |
| --- | --- | --- | --- |
| Before | no inner move exists on the base page | unchanged by any inner move | "Tip", "Before.", rule, "After." |
| After | accepted | `":::{div}\n:class: callout-tip\n\n---\n\nBefore.\n\nAfter.\n:::\n"` | "Tip" only |

## Text evidence of the earlier verdict (a5550c32), both fixed at 739f9e3

A captioned `{table}` and a `{figure}` in a list of a box no longer get a fence line cut by Enter,
and the chord that moved a thematic break first in the body of a note or an alert is now refused:
see `<r2>/firstplace-head.log` and `verify.md`. The earlier commands are in
`verify-a5550c3.md`.

## Not captured

- No real VS Code window and no new take of the clip: the brief forbids both. The clip was judged
  from its committed files.
- No screenshot of the move chord, of a refused move or of an erased alert block: their effect is a
  document change, shown by the tests and by session probes (text), see `verify.md`.
- No screenshot of the failures above: the evidence is the document text and the rendered HTML.
