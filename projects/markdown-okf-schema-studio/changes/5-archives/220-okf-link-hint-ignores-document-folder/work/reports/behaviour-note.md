# Behaviour note — 220 x-okf-link list editor hint

## Cause (analysis)

The `related` field is a `filename-stem` link list. The table resolves each item against the full
Markdown stem index of the workspace roots (`resolveFilenameStem`, src/core/frontmatter/fileLinks.ts).
The editor gets its "known" stems from the row attribute `data-okf-link-suggestions`, filled by
`filenameStemSuggestions(options, limit = 500)`: the same index, but sorted alphabetically and cut
at 500. The list editor (src/page/features/frontmatterListEditor.ts) treats that truncated list as
the complete set and warns on any value outside it.

The QA workspace holds 1125 unique stems; `related-target` sorts around position 848, so it is cut
off. Book chapters (`00-…`, `01-…`) sort first, which is why the suggestions show only `book/`.
So it is not a different root: it is the same index, truncated. The intent's "document folder"
wording is a symptom reading; filename-stem resolution is workspace-wide, not document-relative.

## Today

Editing an item of a filename-stem link list in a workspace with more than 500 Markdown stems
warns `No Markdown file named "related-target.md" was found` for a target the table resolves;
the suggestion list shows the first 500 stems alphabetically (book chapters), not the document's
neighbours.

## After

The warning appears only for a value that matches no stem of the full index (the one the table
uses), so `related-target` gives no warning and `zzz` still warns. The suggestions start with the
stems nearest the document (same folder first, then by folder distance, then alphabetical),
still capped for the dropdown.

## Requirements touched (all proposed)

- SwRS-MDOKFSTUDIO-FMEDIT-010 (proposed): suggestion and warning scenarios, known issue text.
- SwRS-MDOKFSTUDIO-FMSCHEMA-055 (proposed): only if the suggestion order is written there.
- No approved requirement changes.

## Choices left open (with proposals)

1. Known set for the warning: send the full stem list to the page (second attribute, no cap), the
   dropdown keeps a cap. Proposal: yes; alternative for very large vaults is a "list incomplete"
   flag that suppresses the warning instead of a false one.
2. Suggestion order: same folder, then by folder distance, then alphabetical. Proposal: yes.
3. Dropdown cap: keep 500. Proposal: yes.
4. Ambiguous stems (same name in two folders): unchanged, the editor treats them as known; the
   table keeps its "ambiguous" error. Proposal: out of scope.
5. Tests: the intent ticks "No test", but the batch rule requires a test that fails before the
   fix. Proposal: a core unit test (a file beyond 500 stems is known; siblings come first) and a
   page test (no warning for a stem in the known set but outside the dropdown list). No real-input
   E2E: no click, key or focus change.
