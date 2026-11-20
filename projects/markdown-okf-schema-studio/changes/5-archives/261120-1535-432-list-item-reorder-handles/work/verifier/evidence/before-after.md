# Before and after: list item handles

Before: base `cdf286fe0ac649a300de63c789895092665cad86` (main), from the project's visual job of CI
run 44752621641 (push on main at that SHA, artifact `e2e-visual-attempt-1`).
After: pushed head `cb618b15a6eb668929001f964cb091aeb7511e05`, from the visual job of the heavy CI
run 44756125693 (workflow_dispatch at that SHA, artifact `e2e-visual-attempt-1`).

Reproduce: `gh run download <run> -n e2e-visual-attempt-1`, then take
`e2e/screenshots/visual/block-editing/<scenario>.png`; or `just ci-visual` (Linux) at each SHA.

Every image was opened and given the look: no local path, no username, no home folder shows.

## Pairs

| Pair | Before (cdf286f) | After (cb618b1) | What it shows |
| --- | --- | --- | --- |
| Bullet list, light, 900 px (scenario `block-editing/v17-block-selection-light-900`) | `before-bullet-list-light-900-cdf286f.png` | `after-bullet-list-light-900-cb618b1.png` | Same page in edit mode. Before: the three-item bullet list under "Depot topology" has no handle. After: a six-dot handle sits left of each item, centred on its line; nothing else on the page changes (the alerts have no list and get none). |
| Ordered list, dark, 460 px (scenario `block-editing/v12-list-item-opens-item-dark-460`) | `before-ordered-list-dark-460-cdf286f.png` | `after-ordered-list-dark-460-cb618b1.png` | Same page with a list item editor open. Before: no handle. After: each item of the "Run order" ordered list has its handle, and the bullet list whose item is being edited keeps a handle on its other item; the item editor itself is unchanged. |

## After only (new fixture, no before)

The fixture `test/visual/fixtures/90-list-item-handles.md` is new in this change, so the base has no
capture of it (see "Not captured").

| File | Scenario | What it shows |
| --- | --- | --- |
| `after-handles-containers-light-900-cb618b1.png` | `v36-list-item-handles-light-900` | Light: handles on the bullet, ordered (from 3, with a nested list whose handles sit left of the sub-list), task, GitHub alert and nested-admonition lists; the alert's and the admonitions' handles sit left of the outermost box. |
| `after-handles-containers-dark-900-cb618b1.png` | `v37-list-item-handles-dark-900` | The same in the dark theme. |
| `after-handles-pushed-light-360-cb618b1.png` | `v39-list-item-handles-pushed-light-360` | Light, 360 px pane: blocks pushed right, every handle inside the pane. |
| `after-drag-held-light-900-cb618b1.png` | `v40-list-item-drag-light-900` | Light: after a first drag (first bullet item moved last, list now second, third, first), a second drag held down: dragged item dimmed with a dashed outline, the drop line under the third item. |
| `after-drag-held-dark-900-cb618b1.png` | `v41-list-item-drag-dark-900` | The same in the dark theme. |

## Not captured

- **Before of the new fixture (lists in an alert and in nested admonitions, the drag line):** the
  detached worktree of the base could not be created in the scratch folder:
  `git worktree add --detach <scratch>/b cdf286fe...` failed with
  `error: unable to create file .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json: Filename too long`
  then `fatal: Could not reset index file to revision 'HEAD'.` (Windows path length). The base's own
  CI visual run has no capture of this fixture (it is new). The two pairs above stand in for "a list
  in edit mode, before and after".
- **An ordered list before and after a move (screenshots):** no visual scenario moves an ordered
  list; the visual drag scenario moves a bullet list (v40/v41 show the list after the move, second,
  third, first). The ordered renumbering after a move is proven by tests and by the real-window run
  (see verify.md), not by a screenshot.
