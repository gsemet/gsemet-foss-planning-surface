# Before and after, CR-462

Before: base 58b4c302 (detached worktree, with the fixture 95 and the v51-v53 scenario files copied in, since the base has neither). After: head fc7c67ac8f4225020b526976d99e1a3f0dc5a8ee (the v51-v53 images retaken at this head are byte-identical to the ones kept here; the full-page pairs are carried from bb49b02, same fixture and render).

Fixture: test/visual/fixtures/95-blank-lines-in-containers.md. The spec said v44-v53; the CR's own scenarios are v51, v52, v53 (v44-v50 are CR-444/448).

| Pair | Files | Shows |
| --- | --- | --- |
| Edit mode, light, 900 px, full page | before-edit-light.png / after-edit-light.png | Before: only the footnote run shows a block (placed as a top-level run); quote, alert, admonition, panel, definition show none. After: six blocks, each inside its container. |
| Edit mode, dark, 900 px, full page | before-edit-dark.png / after-edit-dark.png | Same, dark. |
| Scenario captures at head | after-v51-edit-light-bar.png, after-v52-reading-dark.png, after-v53-typing-light.png | v51 six blocks in edit mode; v52 reading mode shows none; v53 editor open inside the quote after typing "More". |

Reproduce: `npm run visual:render`, then `python test/visual/capture.py --scenario block-editing/v51-blank-lines-in-containers-light-900 ...` (v51, v52, v53); the full-page pairs open out/reports/visual/pages/95-blank-lines-in-containers--{light,dark}--sticky-3--default.html at 900x1000, click `[data-sphinx-preview-edit-toggle]` and take a full-page screenshot. Counts printed: before 1 block (LI), after 6 (BLOCKQUOTE, ASIDE note simple, ASIDE note, ASIDE myst-context-admonition, DD, LI), both themes.

The images show no username or home folder (opened and checked).
