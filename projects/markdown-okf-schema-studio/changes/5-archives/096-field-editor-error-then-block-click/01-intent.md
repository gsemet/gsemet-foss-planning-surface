# A refused field value stays open next to a block editor

User decision (2026-10-24): P3, cancel the field and open the block.

Current behaviour (SwRS-MDOKFSTUDIO-BLOCK-041 (was SwRS-MDOKFSTUDIO-FMEDIT-002) and FMEDIT-073, Known issue): with a frontmatter
field editor open, clicking a block or a "+" insert point still opens a block editor:
`openBlockEditor` (`src/page/features/blockEditor.ts`) checks only `activeBlockEdit`. The click
blurs the field, which posts a plain save (`src/page/features/frontmatterValueEditor.ts`).

- Valid value: the save succeeds and the field closes; no visible problem.
- Refused value (invalid YAML such as `[review`, or a value the schema refuses): the field stays
  open in its error state and the block editor opens too. Two editors are open, and the field in
  error keeps blocking every other field until Escape.

## Expected

- When the plain save of a field is refused and the user has clicked a block or a "+" insert
  point, the field editor is cancelled (the field shows its saved value again) and the block
  editor opens. The refused text is discarded.
- A valid value keeps today's behaviour: saved, then the block editor opens.
- Page test for both cases; update FMEDIT-002 and FMEDIT-073 in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
