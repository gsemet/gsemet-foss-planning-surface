# Report — 281-frontmatter-click-lost-below-open-editor

Status: **done** (2026-11-11, branch `change-requests/281-frontmatter-click-lost-below-open-editor`, PR #352, merge commit `2e9cf0b9`; no GitHub issue).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A click on a front matter field below an unchanged open editor is no longer lost | `2e9cf0b9` |
| T2 (round 2) | Visual scenario `frontmatter-editing/v09-click-field-below-open-editor-light-900` (fails on the base: no editor opens), SwRS FMEDIT-019; squashed into one commit by the Chief of Staff | `2e9cf0b9` |

## Proof of completion

- Two rounds (2/3). Heavy CI run 43002096151 at head `f86cae43` green, stress included; earlier run 42997949782 green at the pre-squash head.
- Light-only before/after screenshots on branch `change-requests/281-frontmatter-click-lost-below-open-editor-assets`.
- The Chantier repository was not touched.

## Open items

- Remote branches `change-requests/281-frontmatter-click-lost-below-open-editor` and its `-assets` branch are left for the owner to delete.
