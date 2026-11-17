# Some MyST labels show an anchor icon but cannot be renamed

Current behaviour (specified as such in the myst SwRS for F-MYST-044, flagged "Known issue"):

- A label whose name starts with `_`, `.` or `-` is valid for the anchor icon
  (`src/core/render/mystInlineTransforms.ts`, `ANCHOR_LABEL` = `^[A-Za-z0-9_.:-]+$`).
- In edit mode, a click on its icon is swallowed: `src/page/modules/labelRename.ts` calls
  `preventDefault`/`stopPropagation` before testing the name against a pattern that requires a
  letter or digit first (`src/core/mapping/labelRename.ts`, `LABEL_NAME`). No editor, no
  popover, no message.
- Related (F-MYST-038): a rename for a stale revision is dropped by the `render` gate with no
  answer, so the field ends with the 6 s "did not answer" text instead of the stale-line refusal.

## Expected

- One label pattern shared by the renderer, the page and the host, or the page tests the name
  before swallowing the click and shows why a label cannot be renamed.
- The host answers a stale rename with the stale-line refusal.
- Tests: unit (pattern parity), page (click on `_label`), integration (stale rename answer).
  Update the SwRS in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
