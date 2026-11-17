# `{doc}` and `{download}` without a label render an empty link

User decision (2026-10-24): P3, fix the empty link only.

Current behaviour (SwRS-MDOKFSTUDIO-MYST-017 (was SwRS-MDOKFSTUDIO-MYST-095), Known issue; read from the code, no test yet):
``{doc}`other/page` `` and ``{download}`schema/m.json` `` written without a label render a link
with no text, so the reference disappears from the preview.

## Expected

- Without a label, the link text is the written target: `other/page` for `{doc}`, the file name
  (`m.json`) for `{download}`. With a label, unchanged.
- Out of scope (user decision): checking that targets exist, and `{numref}` (stays the inert
  "reference role unhandled" placeholder).
- Render test for both roles with and without a label; update MYST-095 in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
