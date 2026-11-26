# CR-514 before and after

- Before: base `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f` (same tree as the restacked base
  `223a8c49a47f8af786412e7cff748860b18d3782`).
- After: `a5550c32100a24e646efdf293db93cdac30e3cba` (same tree as the restacked pull request head
  `4e4eeb4eb548fc4a8f05838f6d0257b76d6b9f0e`).

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

## Failed claim: a block of a box that cuts a fence (text evidence)

Reproduce, from the worktree, with `<build>` the worktree (after) or `out/vbase` (before) and the
files of `../repro/`:

```
fnm exec -- node --import ./scripts/register-myst-patches.mjs ../repro/gesture.js <build> ../repro/gap-note.md "Step one" enter erase
```

(`gap-alert.md` with the same text; `gap-fig.md` with `"Caption text"`.) `../repro/` stands for
the full path of that folder.

Source `gap-note.md`:

````markdown
::::{note}
- Step one

  ```{table} Caption
  | a | b |
  | - | - |
  | 1 | 2 |
  ```
::::

After.
````

| | Enter on "Step one" | Editor text | After erasing it and committing |
| --- | --- | --- | --- |
| Before | the whole box, lines 1-9 | the whole directive | not run (the whole box is open) |
| After | the paragraph, lines 2-4 | `- Step one`, a blank line, the opening fence line of the `{table}` | the `{table}` directive and its caption are gone; its closing fence is left alone and opens an empty code block |

`gap-fig.md` (a `{figure}` inside a list of a note): after, Enter on "Caption text" opens lines 5-7
(the caption and the closing fence of the figure); erasing it leaves the figure's opening fence
unclosed and the figure disappears. Before, the whole box opens (lines 1-9).

## Not captured

- No real VS Code window and no new take of the clip: the brief forbids both. The clip was judged
  from its committed files.
- No screenshot of the move chord, of a refused move or of an erased alert block: their effect is a
  document change, shown by the tests and by session probes (text), see `verify.md`.
- No screenshot of the fence cut above: the evidence is the document text.
