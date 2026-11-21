## Summary

Studio opens a Markdown file at a searched line and marks it with an arrow and a light band (CR-445).

- Settings `open.searchResultsInStudio` (on) and `open.markdownFilesInStudio` (off, on after migration), a one-time migration of a `*.md` editor association (the setting is written before the association is removed, the reverse of spec 4.4), feature introductions with a reset command, lazy activation on `onLanguage:markdown`, an "Open as Text" command.
- `previewRevealLine` host-to-page message, the page marker (`lineMarker.ts`), the pending line for a new Studio tab, `studioTargetFor`, `showDocumentInStudio` for Studio's own link and history navigation.
- The opening watcher and policy truth table. Placement differs from spec 4.1: the watcher lives in `src/host-vscode/openingWatcher.ts` and `studioPlacement.ts`, not `openInStudio.ts`.
- SwRS LIFE-178 and following, docs, CHANGELOG, glossary.

Decisions 12 to 33 of the specification were decided by the Griller under the owner's autonomy rule; the owner may change them at review. "On by default" is read as: "Open search results in Studio" on, "Open Markdown files in Studio" off until the migration turns it on.

## Known gaps

- Known issues from the real VS Code trials (details in `docs/known-limitations.md`): T4 (a pinned or preview Studio tab ignores a new line), T3b (a dirty document gives a save dialog on Open as Text), T3d (Open With > Text Editor is replaced), T1 (brief text editor flash), the opening that triggered activation is never replaced.
- Trials T5, T6, T7, T11 and T10 Back/Next were not run; `openAtLineCampaign.ts` was cut; `test/integration/openAtLine.test.ts` compiles but was not run in the real harness. Visual scenarios, integration stage run on Linux CI only.

## Review

- [ ] Inspector, round 4
