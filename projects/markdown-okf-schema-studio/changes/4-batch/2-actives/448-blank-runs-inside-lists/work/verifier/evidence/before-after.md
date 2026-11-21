# Before and after: blank-lines blocks inside lists (CR-448)

Before: `e0c7836c24254840cab8ac58ac82b52ee538ed1d` (base, parent of the CR's commit), detached worktree, with the
head's visual fixture `93-blank-lines-in-lists.md`, scenarios and capture script copied onto it (the base has
none of them), removed after the run.
After: `8ecec6bb8d1d497ecb23c191a71313bae00919cf` (pushed head).

Reproduce (in either tree): `npm run visual:render`, then
`python test/visual/capture.py --workers 1 --scenario block-editing/v47-blank-lines-in-lists-light-900 --scenario block-editing/v48-blank-lines-in-lists-selected-dark-900 --scenario block-editing/v49-blank-lines-in-lists-reading-light-900 --scenario block-editing/v50-blank-lines-in-lists-typing-light-900`.

| Pair | Shows |
|---|---|
| `before-v47-no-blocks.png` / `after-v47-between-items-and-in-item.png` | Edit mode. Before: the runs between items 1 and 2 and between the paragraphs of item 2 show nothing. After: two "Blank lines (3)" blocks, one at the end of item 1, one between the paragraphs of item 2; none in the fence of item 3. |
| `after-v48-selected-delete-button.png` | Dark theme. The block of item 1 is selected by the arrows; its Delete block button sits at its left edge, clear of the list item handles. |
| `after-v49-reading-mode.png` | Reading mode: no blank-lines block. |
| `after-v50-typing-editor-in-item.png` | After clicking the block, typing "More" and an autosave: the editor frame is still open inside item 1 of the re-rendered list. |

Before run output (base): v47, v48, v50 `failed` ("blank lines in lists: 0 blocks (0 in the fence), expected 2 and none in the fence"), v49 passed (reading mode shows none, as expected).
After run output (head): all five blank-lines scenarios (v44, v47-v50) `passed`.

Not captured: a before of v48 and v50 images (the base run failed before producing a distinct step image; the failure text above is the before). Not captured: LF/CR LF integration screenshots (the integration step has none).

All images were opened and looked at: the fixture's text is made-up; no username or home folder shows.
