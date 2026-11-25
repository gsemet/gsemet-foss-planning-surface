# CR-504 round 2, group 2b: sweep entries with a weak keyword match (to review)

| File:line (before the sweep) | SwRS | Chosen | Score | Test title |
|---|---|---|---|---|
| test/build/integrationEditModeRestore.test.ts:9 | SwRS-MDOKFSTUDIO-BLOCK-004 | S1,S2 | 0.35 | CR 152: every top-level integration scenario that turns edit mode on turns it off again |
| test/build/test_table_bar_flow.py:33 | SwRS-MDOKFSTUDIO-TABLE-064 | S1,S2 | 0.58 | test_wrong_z_index_fails |
| test/core/edits/blocksDelete.test.ts:83 | SwRS-MDOKFSTUDIO-BLOCK-264 | S1 | 0.0 | ${name}: stale lines give no removal |
| test/core/edits/sourceEdits.test.ts:289 | SwRS-MDOKFSTUDIO-BLOCK-124 | S2,S4 | 1.3 | ${name}: a selection ending on a no-break-space line is refused, not shortened |
| test/core/mapping/blankRunContainer.test.ts:99 | SwRS-MDOKFSTUDIO-BLOCK-268 | S1 | 1.22 | ${name}: the indent of ${row.name} |
| test/core/mapping/blankRunContainer.test.ts:122 | SwRS-MDOKFSTUDIO-BLOCK-268 | S1,S6 | 0.82 | a footnote label after a tab is no footnote label: it is refused |
| test/core/mapping/blankRunInList.test.ts:112 | SwRS-MDOKFSTUDIO-BLOCK-268 | S6 | 0.71 | ${name}: "More" after a tab marker and after a second marker takes four spaces |
| test/core/mapping/imageReference.holes.test.ts:8 | SwRS-MDOKFSTUDIO-PALETTE-192 | S1 | 0.71 | Windows path rules apply when either path holds a backslash, and POSIX rules when neither does |
| test/core/mapping/listItemIndent.test.ts:29 | SwRS-MDOKFSTUDIO-BLOCK-268 | S5 | 0.41 | ${name}: a tab after the marker runs to the next tab stop of 4 |
| test/core/mapping/listItemIndent.test.ts:47 | SwRS-MDOKFSTUDIO-BLOCK-268 | S5 | 0.41 | ${name}: five spaces or more after the marker, or none, put the content column after one space |
| test/core/mapping/pastedImage.holes.test.ts:19 | SwRS-MDOKFSTUDIO-PALETTE-196 | S1 | 0.0 | the pasted-image caps are 10 MiB of pixels and 14 million base64 characters |
| test/core/mapping/pastedImage.holes.test.ts:27 | SwRS-MDOKFSTUDIO-PALETTE-196 | S1 | 0.0 | each image type is saved with its own extension and announced with its own MIME type |
| test/core/mapping/pastedImage.holes.test.ts:34 | SwRS-MDOKFSTUDIO-PALETTE-196 | S4,S5 | 0.3 | sniffImage accepts input exactly as long as the signature and refuses one byte less |
| test/core/mapping/pastedImage.holes.test.ts:48 | SwRS-MDOKFSTUDIO-PALETTE-196 | S1 | 0.0 | a WebP needs both the RIFF tag at the start and the WEBP tag at offset 8 |
| test/core/mapping/pastedImage.holes.test.ts:55 | SwRS-MDOKFSTUDIO-PALETTE-196 | S1 | 0.0 | each announced MIME type maps to its own type, and anything else maps to none |
| test/core/mapping/pastedImage.holes.test.ts:67 | SwRS-MDOKFSTUDIO-PALETTE-196 | S4,S5 | 0.3 | isBase64 refuses a foreign character anywhere in a string of valid length |
| test/core/mapping/quoteBlankRuns.test.ts:103 | SwRS-MDOKFSTUDIO-BLOCK-267 | S2 | 0.45 | ${name}: checkBlankLine accepts every line of a quote run but its first |
| test/core/mapping/quoteBlankRuns.test.ts:117 | SwRS-MDOKFSTUDIO-BLOCK-267 | S1 | 0.0 | ${name}: checkBlankLine refuses a line that is not a shown blank line of a quote run |
| test/core/paste/htmlToMarkdown.test.ts:85 | SwRS-MDOKFSTUDIO-PALETTE-229 | S1 | 0.0 | T1: htmlToMarkdown,  |
| test/core/protocol/hostToPage.test.ts:95 | SwRS-MDOKFSTUDIO-BLOCK-003 | S1,S2 | 0.88 | the payload checks refuse what the page used to refuse |
| test/core/protocol/pageToHost.test.ts:255 | SwRS-MDOKFSTUDIO-PALETTE-196 | S7 | 1.01 | T38: previewPasteImage caps the size and accepts plain base64 of an allowed type only |
| test/core/render/blankRunsList.test.ts:99 | SwRS-MDOKFSTUDIO-BLOCK-266 | S1 | 0.0 | an alert holds its run up to its edges |
| test/core/render/blankRunsList.test.ts:107 | SwRS-MDOKFSTUDIO-BLOCK-266 | S2 | 0.45 | an admonition, a closed dropdown and a context-tag panel hold their run, with their mapped paragraph |
| test/integration/blockClipboard.test.ts:84 | SwRS-MDOKFSTUDIO-BLOCK-166 | S2,S6 | 1.34 | run |
| test/integration/editToolbarCover.test.ts:87 | SwRS-MDOKFSTUDIO-PALETTE-021 | S1,S3 | 1.22 | run |
| test/integration/emptyBlocks.test.ts:82 | SwRS-MDOKFSTUDIO-BLOCK-265 | S4,S5 | 1.15 | run |
| test/integration/imagePaste.test.ts:29 | SwRS-MDOKFSTUDIO-PALETTE-196 | S6,S7 | 0.71 | run |
| test/integration/imagePaste.test.ts:32 | SwRS-MDOKFSTUDIO-PALETTE-217 | S2,S8 | 0.89 | run |
| test/integration/imagePicker.test.ts:29 | SwRS-MDOKFSTUDIO-PALETTE-192 | S1,S2 | 1.41 | run |
| test/integration/inlineThread.test.ts:101 | SwRS-MDOKFSTUDIO-BLOCK-058 | S5 | 1.41 | run |
| test/integration/listItemMoves.ts:138 | SwRS-MDOKFSTUDIO-BLOCK-262 | S1,S3 | 1.15 | scenarioSubListDrag |
| test/integration/listItemMoves.ts:160 | SwRS-MDOKFSTUDIO-BLOCK-262 | S1,S3 | 1.15 | scenarioDropOverAnotherList |
| test/integration/mystPickers.test.ts:10 | SwRS-MDOKFSTUDIO-PALETTE-178 | S4 | 0.71 | run |
| test/integration/mystPickers.test.ts:11 | SwRS-MDOKFSTUDIO-PALETTE-183 | S1,S2 | 0.71 | run |
| test/integration/previewEditing.test.ts:630 | SwRS-MDOKFSTUDIO-BLOCK-014 | S8,S9 | 1.34 | stepBodyEdits |
| test/integration/previewEditing.test.ts:631 | SwRS-MDOKFSTUDIO-BLOCK-216 | S1,S6 | 1.0 | stepBodyEdits |
| test/integration/previewEditing.test.ts:661 | SwRS-MDOKFSTUDIO-BLOCK-058 | S4 | 0.89 |  |
| test/integration/previewEditing.test.ts:714 | SwRS-MDOKFSTUDIO-BLOCK-191 | S7,S11 | 0.63 |  |
| test/integration/previewEditing.test.ts:731 | SwRS-MDOKFSTUDIO-BLOCK-053 | S2,S4 | 1.41 | stepTableAndInsert |
| test/integration/realInput/lineEndingLeave.ts:26 | SwRS-MDOKFSTUDIO-BLOCK-263 | S1,S3 | 1.15 |  |
| test/integration/realInput/textEditing.ts:449 | SwRS-MDOKFSTUDIO-BLOCK-069 | S6 | 1.34 | scenarioShortcuts |
| test/integration/realInput/textEditing.ts:622 | SwRS-MDOKFSTUDIO-PALETTE-031 | S1,S4 | 1.34 | scenarioPalette |
| test/page/modules/cardGridDirectives.test.ts:76 | SwRS-MDOKFSTUDIO-PALETTE-270 | S2 | 0.3 | the registry lists Card and Grid, with their panel, in the MyST palette only |
| test/page/modules/cardGridDirectives.test.ts:77 | SwRS-MDOKFSTUDIO-PALETTE-271 | S2 | 0.3 | the registry lists Card and Grid, with their panel, in the MyST palette only |
| test/page/modules/codeBlockDirective.test.ts:120 | SwRS-MDOKFSTUDIO-PALETTE-272 | S3,S4 | 0.3 | the form refuses a bad language, emphasized lines, or a multi-line caption or name |
| test/page/modules/dropFiles.test.ts:24 | SwRS-MDOKFSTUDIO-PALETTE-004 | S1 | 0.0 | the insertion bar nearest to the pointer is chosen |
| test/page/modules/editActions.test.ts:149 | SwRS-MDOKFSTUDIO-PALETTE-001 | S8 | 1.34 | the registry lists the actions with metadata and indexes them by id |
| test/page/modules/editActions.test.ts:344 | SwRS-MDOKFSTUDIO-PALETTE-050 | S1 | 0.0 | editActions rule  |
| test/page/modules/editCommandKey.test.ts:6 | SwRS-MDOKFSTUDIO-BLOCK-003 | S1,S2 | 0.76 | CR 119: the VS Code default keys map to undo, redo, select all and delete line |
| test/page/modules/editPalette.test.ts:264 | SwRS-MDOKFSTUDIO-PALETTE-078 | S3 | 0.71 | T24: the Table button opens a 9 x 9 grid of 81 cells |
| test/page/modules/editPalette.test.ts:1050 | SwRS-MDOKFSTUDIO-PALETTE-238 | S5,S6 | 0.3 | CR038: the slash menu offers the conversion only inside a table of the other form |
| test/page/modules/editPalette.test.ts:1051 | SwRS-MDOKFSTUDIO-PALETTE-263 | S2,S3 | 0.3 | CR038: the slash menu offers the conversion only inside a table of the other form |
| test/page/modules/listItemMove.test.ts:61 | SwRS-MDOKFSTUDIO-BLOCK-262 | S1,S7 | 0.8 | a tight list stays tight and a loose list keeps its gaps in place |
| test/page/modules/markdownTablePreservation.test.ts:117 | SwRS-MDOKFSTUDIO-TABLE-094 | S1,S4 | 0.41 | round trip preserves the source: ${entry.name} |
| test/page/modules/pasteUrl.test.ts:39 | SwRS-MDOKFSTUDIO-PALETTE-264 | S1,S3 | 0.88 | CR 145: only http, https and mailto addresses are links |
| test/page/modules/pasteUrl.test.ts:50 | SwRS-MDOKFSTUDIO-PALETTE-264 | S1 | 0.0 | CR 145: a destination with parentheses is written in angle brackets |
| test/page/modules/slashMenu.test.ts:761 | SwRS-MDOKFSTUDIO-PALETTE-240 | S3,S5 | 1.06 | P11 r2: in MyST the MyST entry ranks before its GFM equivalent; GFM and exact labels are unchanged |
| test/page/modules/structuralCursor.test.ts:55 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1 | 1.34 | CR 157: the arrows move cell to cell without wrapping, and a short row clamps the column |
| test/page/modules/structuralCursor.test.ts:84 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1 | 0.89 | CR 157: a position that names nothing in the tree stays |
| test/page/modules/tableInContainer.test.ts:96 | SwRS-MDOKFSTUDIO-TABLE-121 | S3 | 0.3 | Windows line endings stay and the closing line break is kept or absent as in the source |
| test/page/modules/textEditing.test.ts:206 | SwRS-MDOKFSTUDIO-BLOCK-003 | S1 | 0.0 | CR 119: deleteLine removes the caret line with its break and keeps the column on the next line |
| test/page/modules/textEditing.test.ts:214 | SwRS-MDOKFSTUDIO-BLOCK-003 | S1 | 0.38 | CR 119: deleteLine on the last line takes the break before it and moves the caret up |
| test/page/modules/textEditing.test.ts:222 | SwRS-MDOKFSTUDIO-BLOCK-003 | S2 | 0.3 | CR 119: deleteLine removes every line a selection touches, not the line it ends at the start of |
| test/page/modules/tocAction.test.ts:18 | SwRS-MDOKFSTUDIO-PALETTE-003 | S1 | 0.0 | the Table of contents action writes [TOC] set apart after the line, the caret after it |
| test/page/modules/tocAction.test.ts:28 | SwRS-MDOKFSTUDIO-PALETTE-003 | S2 | 0.3 | the action is a block-scope palette button and a /toc entry in every mode |
| test/page/runtimeBlankLinesContainers.test.ts:200 | SwRS-MDOKFSTUDIO-BLOCK-266 | S2 | 0.89 | a run in a loose definition shows in its dd; a run between two entries ends the dd above |
| test/page/runtimeBlankLinesContainers.test.ts:221 | SwRS-MDOKFSTUDIO-BLOCK-266 | S2 | 0.89 | a footnote run shows in the footnote: in its body, after a label alone, and between two footnotes |
| test/page/runtimeBlankLinesContainers.test.ts:239 | SwRS-MDOKFSTUDIO-BLOCK-266 | S2 | 0.89 | a run between a footnote and the body after it shows in the body, after the block above it |
| test/page/runtimeBlankLinesContainers.test.ts:303 | SwRS-MDOKFSTUDIO-BLOCK-266 | S1,S3 | 0.58 | a run in a closed dropdown shows when it opens and goes when it closes |
| test/page/runtimeBlankLinesContainers.test.ts:316 | SwRS-MDOKFSTUDIO-BLOCK-266 | S2 | 0.89 | an insertion editor opened in a dropdown stays when the dropdown closes |
| test/page/runtimeBlockEditor.test.ts:1035 | SwRS-MDOKFSTUDIO-BLOCK-003 | S1 | 0.38 | CR 119: undo and redo keys of the table cell editor cancel the native action and reach VS Code |
| test/page/runtimeBlockEditorLineEndings.test.ts:111 | SwRS-MDOKFSTUDIO-BLOCK-263 | S1 | 1.22 | a block of an LF file posts LF, as before |
| test/page/runtimeCodeBlockPanel.test.ts:78 | SwRS-MDOKFSTUDIO-PALETTE-272 | S4 | 0.8 | Apply without a change writes nothing |
| test/page/runtimeEditPalette.test.ts:308 | SwRS-MDOKFSTUDIO-PALETTE-021 | S3,S8 | 1.22 | measure |
| test/page/runtimeEditPalette.test.ts:445 | SwRS-MDOKFSTUDIO-PALETTE-083 | S1,S4 | 0.88 | T22: Cmd+K on macOS opens the panel and Ctrl+K there does not |
| test/page/runtimeFileDrop.test.ts:32 | SwRS-MDOKFSTUDIO-PALETTE-004 | S1 | 0.38 | files dragged over the page mark the nearest insertion bar and the drop posts their addresses |
| test/page/runtimeFileDrop.test.ts:67 | SwRS-MDOKFSTUDIO-PALETTE-004 | S1 | 0.38 | leaving the window takes the marker away |
| test/page/runtimeListItemMove.test.ts:224 | SwRS-MDOKFSTUDIO-BLOCK-262 | S1,S3 | 1.15 | a drop in place, outside the list or over another list requests nothing |
| test/page/runtimeListItemMove.test.ts:291 | SwRS-MDOKFSTUDIO-BLOCK-262 | S2,S6 | 1.0 | a refused source, a source that does not read as the items or a lost answer leaves the document alon |
| test/page/runtimePaletteActions.test.ts:936 | SwRS-MDOKFSTUDIO-PALETTE-270 | S1 | 1.15 | CR245: the slash menu opens the card and the grid forms and removes the typed query |
| test/page/runtimePaletteActions.test.ts:937 | SwRS-MDOKFSTUDIO-PALETTE-271 | S1 | 1.15 | CR245: the slash menu opens the card and the grid forms and removes the typed query |
| test/page/runtimeStructuralNavigation.test.ts:107 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1,S2 | 1.34 | CR 157: the four arrows move cell to cell and stop at the edges |
| test/page/runtimeStructuralNavigation.test.ts:145 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1,S2 | 1.15 | CR 157: Enter on a selected cell opens the cell editor like a click |
| test/page/runtimeStructuralNavigation.test.ts:204 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1 | 0.45 | CR 157: Enter on an inner block opens that block's editor |
| test/session/alertBlockEditOpen.test.ts:172 | SwRS-MDOKFSTUDIO-BLOCK-014 | S10 | 1.15 | each of several consecutive alerts opens only its own lines |
| test/session/dropFiles.requirements.test.ts:102 | SwRS-MDOKFSTUDIO-PALETTE-004 | S1 | 0.76 | files outside the workspace, other addresses and unreadable files are handled without touching the s |
| test/session/heldEditSource.test.ts:24 | SwRS-MDOKFSTUDIO-BLOCK-255 | S2 | 1.45 | CR 188: a held block source reaches the page only when the queue runs, unchanged |
| test/session/listItemEditOpen.test.ts:92 | SwRS-MDOKFSTUDIO-BLOCK-014 | S8,S9 | 0.89 | a wrapped item of a tight list opens on all its lines |
| test/session/listItemEditOpen.test.ts:124 | SwRS-MDOKFSTUDIO-BLOCK-014 | S8,S9 | 0.89 | the list itself, outside its items, opens the whole list |
| test/session/listItemEditOpen.test.ts:134 | SwRS-MDOKFSTUDIO-BLOCK-254 | S3 | 0.71 | from the keyboard, an item opens on its lines and a block inside it opens on its own lines |
| test/session/paletteReq.requirements.test.ts:330 | SwRS-MDOKFSTUDIO-PALETTE-196 | S6 | 1.01 | an image paste is refused for an unsaved document or one that is not the previewed document |
| test/session/paletteReq.requirements.test.ts:357 | SwRS-MDOKFSTUDIO-PALETTE-196 | S6 | 0.71 | an image paste is saved next to a standalone file and in Restricted Mode |
| test/visual/admonitionTypePickerScenarios.ts:55 | SwRS-MDOKFSTUDIO-PALETTE-269 | S1,S2 | 0.71 |  |
| test/visual/admonitionTypePickerScenarios.ts:67 | SwRS-MDOKFSTUDIO-PALETTE-269 | S1,S2 | 0.71 |  |
| test/visual/alertEditingScenarios.ts:15 | SwRS-MDOKFSTUDIO-BLOCK-014 | S3,S8 | 1.34 | gfm/v09-alert-body-opens-whole-alert-dark-900 |
| test/visual/capture_edit_checks.py:205 | SwRS-MDOKFSTUDIO-PALETTE-031 | S3,S5 | 0.89 | check_edit_palette |
| test/visual/cardGridFormScenarios.ts:56 | SwRS-MDOKFSTUDIO-PALETTE-270 | S1,S2 | 0.58 |  |
| test/visual/cardGridFormScenarios.ts:71 | SwRS-MDOKFSTUDIO-PALETTE-271 | S1 | 0.58 |  |
| test/visual/gridCardEditingScenarios.ts:54 | SwRS-MDOKFSTUDIO-BLOCK-257 | S1,S2 | 1.41 |  |
| test/visual/linkEditModeScenarios.ts:42 | SwRS-MDOKFSTUDIO-BLOCK-014 | S4,S5 | 1.13 |  |
| test/visual/optionListScenarios.ts:37 | SwRS-MDOKFSTUDIO-BLOCK-061 | S3,S5 | 1.22 |  |
| test/visual/releaseShowcaseScenarios.ts:47 | SwRS-MDOKFSTUDIO-PALETTE-269 | S2 | 1.15 | rendering-core/v27-release-1-3-showcase-cream-1200 |
| test/visual/scenarioDefinitions1.ts:296 | SwRS-MDOKFSTUDIO-BLOCK-234 | S1,S2 | 0.41 |  |
| test/visual/scenarioDefinitions1.ts:859 | SwRS-MDOKFSTUDIO-BLOCK-033 | S7,S10 | 0.82 | edit-paragraph-dark |
| test/visual/scenarioDefinitions1.ts:1414 | SwRS-MDOKFSTUDIO-PALETTE-002 | S1 | 1.41 |  |
| test/visual/scenarioDefinitions1.ts:1415 | SwRS-MDOKFSTUDIO-BLOCK-014 | S5,S10 | 1.15 |  |
| test/visual/scenarioDefinitions1.ts:1434 | SwRS-MDOKFSTUDIO-BLOCK-004 | S1 | 1.41 |  |
| test/visual/scenarioDefinitions1.ts:1456 | SwRS-MDOKFSTUDIO-BLOCK-254 | S1 | 0.89 |  |
| test/visual/scenarioDefinitions3.ts:147 | SwRS-MDOKFSTUDIO-TABLE-002 | S1,S5 | 1.15 |  |
| test/visual/scenarioDefinitions3.ts:192 | SwRS-MDOKFSTUDIO-TABLE-048 | S1,S7 | 1.41 |  |
| test/visual/slashAdmonitionScenarios.ts:12 | SwRS-MDOKFSTUDIO-PALETTE-238 | S1,S5 | 1.41 |  |
