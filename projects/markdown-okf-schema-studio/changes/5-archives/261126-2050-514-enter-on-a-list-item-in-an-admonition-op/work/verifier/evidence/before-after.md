# CR-514 before and after

All ten images below hold at the head `f9dc2c630b852635e8bffcd0b00b42cc886b293c`.

- Before: base `5f0746d79ca28e564841daa19288075aa7823776` of the pull request. The images were
  captured on `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f`, whose tree
  (`e6f6894de333c24969709306715c4f3c06d06418`) is the tree of this base and of
  `223a8c49a47f8af786412e7cff748860b18d3782`: not captured again.
- After: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c`. The images were captured on
  `a5550c32100a24e646efdf293db93cdac30e3cba`; the five scenarios were captured again at
  `739f9e3ecd771efce1938ebdb0685f324a6cf0a2` and at `f9dc2c63`, and the five new images are
  byte-identical to the `after-*.png` here.

## Screenshots (visual harness, dark theme, 900 px)

How to reproduce, after: in the worktree at the head, `fnm exec -- npm.cmd run visual:render`,
then `.venv/Scripts/python.exe test/visual/capture.py --scenario <id>`; the images are written to
`out/reports/e2e/screenshots`.

How to reproduce, before: `git worktree add --detach out/vbase 5f0746d7`; in `out/vbase` take the
head's `test/` files (the scenarios and fixtures are new) and the source files that only the head
has (no base code imports them), leave every existing file under `src/` at the base, run the same
two commands there, then `git worktree remove --force out/vbase`.

| Gesture | Scenario | Before | After |
| --- | --- | --- | --- |
| Click the second paragraph of a note alert | `gfm/v14-alert-body-opens-pointed-paragraph-dark-900` | `before-alert-body-click.png`: one editor holds the whole alert (the scenario's checks fail) | `after-alert-body-click.png`: the editor holds that quoted paragraph, inside the alert, which stays rendered (checks pass) |
| Click the second paragraph of a `{note}` | `block-editing/v57-admonition-body-opens-pointed-paragraph-dark-900` | `before-admonition-body-click.png`: whole directive (checks fail) | `after-admonition-body-click.png`: that paragraph only (checks pass) |
| Down, Down, Right, Down, Right, Enter into a note's list | `block-editing/v59-admonition-keyboard-opens-first-item-dark-900` | `before-admonition-keyboard-enter.png`: whole directive, lines 3-8 (checks fail) | `after-admonition-keyboard-enter.png`: the first item only, line 6 (checks pass) |
| Click the title of the alert | `gfm/v15-alert-title-opens-whole-alert-dark-900` | `before-alert-title-click.png`: whole alert | `after-alert-title-click.png`: whole alert, pixel-identical (unchanged behaviour, checks pass on both) |
| Click the title of the `{note}` | `block-editing/v58-admonition-title-opens-whole-directive-dark-900` | `before-admonition-title-click.png`: whole directive | `after-admonition-title-click.png`: whole directive, pixel-identical (unchanged, checks pass on both) |

No screenshot shows a user name or a home folder (all ten opened). For the pull request, the three
changed pairs are enough; the two title pairs are the same image before and after.

## Clip of the branch

`docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif` at the head: the keyboard walk
into a note, down to a nested sub-list item, which Enter opens alone. It has no "before" take.

## Not captured

- No real VS Code window and no new take of the clip: the brief forbids both. The clip was judged
  from its committed files.
- No screenshot of the move chord, of a refused move or of an erased alert block: their effect is a
  document change, shown by the tests and by session probes (text), see `verify.md`.
- No screenshot of the failed claim (a card body): a browser capture of the card pages is in
  `../r3/cardpages/`, with `../r3/cards-browser-f9dc2c6.log`. Those pages use the preview style
  sheets without the webview shell; they are probe evidence, not images for the pull request.
