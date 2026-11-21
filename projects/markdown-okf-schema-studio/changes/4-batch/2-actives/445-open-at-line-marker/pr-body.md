## Summary

Studio opens a Markdown file at a searched line and marks it with an arrow and a light band (CR-445). Work in progress, rounds 1 and 2 of 3 so far.

- Round 1 (545b910a): two settings (`open.searchResultsInStudio`, `open.markdownFilesInStudio`), one-time migration of a `*.md` editor association (the setting is written before the association is removed, the reverse of spec 4.4), feature introductions, lazy activation on `onLanguage:markdown`, "Open as Text" command.
- Round 2: `previewRevealLine` host-to-page message, the page marker (`lineMarker.ts`), pending line for a new Studio tab, `studioTargetFor`, `showDocumentInStudio` and Studio's own link and history navigation, SwRS LIFE-178 to 183.
- Round 3 (not done): opening watcher and policy, real VS Code trials, docs.

Decisions 12 to 33 of the specification were decided by the Griller under the owner's autonomy rule; the owner may change them at review. "On by default" is read as: "Open search results in Studio" on, "Open Markdown files in Studio" off until migration turns it on.

## Known gaps

- Visual scenarios, integration stage and real VS Code trials do not run on Windows; they run on Linux CI.
- The "most recently active Studio tab" is approximated; `putStudioInPlace` has no host test yet (round 3).

## Review

- [ ] Inspector, round 2
