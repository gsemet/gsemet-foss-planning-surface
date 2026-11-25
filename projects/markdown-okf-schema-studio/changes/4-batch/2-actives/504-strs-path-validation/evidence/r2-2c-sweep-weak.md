# CR-504 round 2, group 2c: sweep entries with a weak keyword match (to review)

| File:line (before the sweep) | SwRS | Chosen | Score | Test title |
|---|---|---|---|---|
| test/build/checkUseCaseDiagrams.test.ts:49 | SwRS-MDOKFSTUDIO-CORE-090 | S1,S2 | 1.3 | refusal: a participant named Box used in a message is reported at its line with Mermaid's message |
| test/build/checkUseCaseDiagrams.test.ts:110 | SwRS-MDOKFSTUDIO-CORE-090 | S1,S2 | 1.15 | walk |
| test/build/checkUseCaseDiagrams.test.ts:126 | SwRS-MDOKFSTUDIO-CORE-090 | S1,S3 | 1.41 | words |
| test/build/mystSourcePatches.test.ts:205 | SwRS-MDOKFSTUDIO-CORE-070 | S1 | 0.5 | no integration test imports the MyST engine unbundled |
| test/build/test_changelog_refs.py:99 | SwRS-MDOKFSTUDIO-CORE-094 | S1 | 0.0 | test_two_bullets_get_their_own_commit |
| test/build/test_changelog_refs.py:111 | SwRS-MDOKFSTUDIO-CORE-094 | S1 | 0.0 | test_a_second_run_changes_nothing |
| test/build/test_changelog_refs.py:152 | SwRS-MDOKFSTUDIO-CORE-094 | S1 | 0.5 | test_an_empty_section_changes_nothing |
| test/build/test_plugin_manifests.py:18 | SwRS-MDOKFSTUDIO-CORE-074 | S1 | 0.89 |  |
| test/build/test_plugin_manifests.py:19 | SwRS-MDOKFSTUDIO-CORE-075 | S1 | 0.89 |  |
| test/build/test_workflows.py:185 | SwRS-MDOKFSTUDIO-CORE-076 | S5,S6 | 0.5 | test_every_job_after_a_skippable_job_opts_out_of_the_implicit_success |
| test/build/test_workflows.py:694 | SwRS-MDOKFSTUDIO-CORE-076 | S1,S2 | 0.45 | test_every_xvfb_screen_is_wider_than_the_emulated_viewports |
| test/build/test_workflows.py:707 | SwRS-MDOKFSTUDIO-CORE-076 | S2 | 0.89 | test_stress_dispatch_inputs_reach_the_stress_recipe_through_env |
| test/build/test_workflows.py:721 | SwRS-MDOKFSTUDIO-CORE-076 | S1 | 0.0 | test_ci_stress_recipe_quotes_and_validates_repeat |
| test/build/test_workflows.py:730 | SwRS-MDOKFSTUDIO-CORE-076 | S1 | 0.0 | test_ci_stress_recipe_defaults_to_11_rounds_and_leaves_the_deadline_computed |
| test/build/test_workflows.py:1056 | SwRS-MDOKFSTUDIO-CORE-076 | S2 | 0.89 | test_toc_loop_inputs_reach_the_recipe_and_leave_the_deadline_computed |
| test/core/comments/anchoring.test.ts:157 | SwRS-MDOKFSTUDIO-REVIEW-107 | S2,S3 | 0.3 | T45: a quote that changed by more than 20 percent is orphaned, not guessed |
| test/core/comments/commentEditing.test.ts:78 | SwRS-MDOKFSTUDIO-REVIEW-044 | S1 | 0.0 | T43: normalizeBody trims and enforces 1 to 10000 characters |
| test/core/comments/commentModel.holes.test.ts:40 | SwRS-MDOKFSTUDIO-REVIEW-004 | S2 | 1.22 | a comment date is an ISO 8601 date-time with a zone, to the minute or finer, naming a real instant |
| test/core/comments/commentModel.holes.test.ts:79 | SwRS-MDOKFSTUDIO-REVIEW-004 | S6,S7 | 1.3 | a sidecar is refused over 2 MiB of text or of UTF-8, and accepted at exactly 2 MiB |
| test/core/comments/commentModel.holes.test.ts:153 | SwRS-MDOKFSTUDIO-REVIEW-004 | S6,S7 | 0.58 | an anchor sent by the page holds at most 500 characters of quote and 32 of prefix and suffix |
| test/core/comments/commentModel.holes.test.ts:154 | SwRS-MDOKFSTUDIO-REVIEW-001 | S2,S3 | 0.71 | an anchor sent by the page holds at most 500 characters of quote and 32 of prefix and suffix |
| test/core/comments/inlineThread.holes.test.ts:14 | SwRS-MDOKFSTUDIO-REVIEW-167 | S4 | 1.45 | a reply is accepted at exactly 10,000 characters and refused at 10,001 |
| test/core/comments/sha256.test.ts:8 | SwRS-MDOKFSTUDIO-REVIEW-054 | S10,S11 | 0.88 | the synchronous sha256 equals node:crypto on empty, ASCII, multibyte, long and block-boundary inputs |
| test/core/configuration/editorAssociationMigration.test.ts:16 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | an object without *.md gets the entry and keeps every other entry in its order |
| test/core/configuration/editorAssociationMigration.test.ts:26 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | an object whose *.md already names Studio has nothing to write |
| test/core/configuration/editorAssociationMigration.test.ts:36 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | the legacy array form gets the Studio item appended and keeps its items |
| test/core/configuration/editorAssociationMigration.test.ts:43 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | the legacy array form with a *.md item, Studio's or another editor's, has nothing to write |
| test/core/configuration/previewConfiguration.test.ts:87 | SwRS-MDOKFSTUDIO-LIFE-044 | S3,S5 | 0.88 | incremental updates can be turned off and default to on |
| test/core/edits/findReplace.test.ts:106 | SwRS-MDOKFSTUDIO-TOOLBAR-012 | S1,S2 | 0.58 | link titles, angle-bracket targets and targets with parentheses are left out too |
| test/core/edits/findReplace.test.ts:167 | SwRS-MDOKFSTUDIO-TOOLBAR-012 | S2 | 1.3 | no link inside a link: the outer target after an inner link is visible text |
| test/core/export/htmlExport.test.ts:116 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S3 | 0.3 | a paragraph under the block editor is exported, its editor is not |
| test/core/export/htmlExport.test.ts:272 | SwRS-MDOKFSTUDIO-TOOLBAR-136 | S2,S3 | 0.5 | the token rule follows the preview sheet and names every resolved token |
| test/core/export/htmlExport.test.ts:296 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S3 | 0.3 | a THREAD chip with its popover, a TODO chip, source-mapping attributes and the tabindex of mapped bl |
| test/core/mapping/lineDiff.test.ts:37 | SwRS-MDOKFSTUDIO-REVIEW-195 | S7 | 0.88 | T16: a base without a trailing newline matches one with it |
| test/core/mapping/lineHunks.test.ts:17 | SwRS-MDOKFSTUDIO-REVIEW-009 | S7 | 0.58 | CR147: added lines have an empty base side and removed lines an empty current side |
| test/core/mapping/lineHunks.test.ts:83 | SwRS-MDOKFSTUDIO-REVIEW-009 | S1,S5 | 0.58 | CR234: a removal is never merged across a heading or a text line |
| test/core/mapping/wordDiff.test.ts:42 | SwRS-MDOKFSTUDIO-REVIEW-009 | S5,S6 | 0.8 | CR147: an empty side marks all of the other |
| test/core/navigation/jumpSignal.test.ts:24 | SwRS-MDOKFSTUDIO-LIFE-190 | S2 | 0.3 | keyboard, mouse and kindless selection changes are never jumps |
| test/core/navigation/pendingLine.test.ts:15 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a pending line is taken once, and only for its own URI |
| test/core/navigation/pendingLine.test.ts:25 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a pending line past the window is dropped, and one at the window is still taken |
| test/core/navigation/pendingLine.test.ts:38 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a second request for the same URI replaces the first, and drop forgets it |
| test/core/navigation/pendingLine.test.ts:49 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a line delivered to a live session is not left pending, and one nobody takes is recorded |
| test/core/navigation/pendingLine.test.ts:64 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a live delivery replaces an older pending line of the same file instead of leaving it |
| test/core/navigation/previewNavigation.holes.test.ts:137 | SwRS-MDOKFSTUDIO-TOOLBAR-090 | S1 | 0.0 | a link is trimmed before it is classified |
| test/core/navigation/previewNavigation.holes.test.ts:166 | SwRS-MDOKFSTUDIO-TOOLBAR-090 | S2 | 1.01 | only http, https and mailto links are external, and never behind wiki: |
| test/core/preview/commentContrast.test.ts:62 | SwRS-MDOKFSTUDIO-REVIEW-002 | S2,S3 | 0.3 | the comment popover and boxes never dim their text with opacity |
| test/core/preview/commentStyles.test.ts:10 | SwRS-MDOKFSTUDIO-CORE-008 | S1 | 0.0 | the comment stylesheet joined from its parts equals the former single constant |
| test/core/preview/previewStyles.test.ts:772 | SwRS-MDOKFSTUDIO-CORE-034 | S1 | 0.0 | overflowing content tables keep short cells whole and show scroll shadows |
| test/core/protocol/hostToPage.test.ts:130 | SwRS-MDOKFSTUDIO-LIFE-181 | S1 | 0.0 | previewRevealLine needs a 1-based safe integer line and addresses its render |
| test/core/protocol/pageStateMessages.test.ts:224 | SwRS-MDOKFSTUDIO-TOOLBAR-079 | S7 | 0.5 | the page-state validators accept exactly what the frozen validator accepted |
| test/core/protocol/pageToHost.test.ts:474 | SwRS-MDOKFSTUDIO-REVIEW-006 | S3,S4 | 0.58 | CR147: previewSideBySideChanged carries a boolean and names the current render |
| test/core/render/blockTagTitle.test.ts:21 | SwRS-MDOKFSTUDIO-REVIEW-003 | S1,S4 | 0.71 | a long opening tag is shortened with an ellipsis and keeps its closing bracket |
| test/core/render/frontmatterValue.test.ts:54 | SwRS-MDOKFSTUDIO-CORE-079 | S1 | 0.5 | a list shows its items joined with commas |
| test/core/render/frontmatterValue.test.ts:60 | SwRS-MDOKFSTUDIO-CORE-079 | S1 | 0.5 | an object shows as its YAML on one line |
| test/core/render/frontmatterValue.test.ts:171 | SwRS-MDOKFSTUDIO-CORE-079 | S3,S4 | 1.01 | an empty object counts as missing, like an empty list |
| test/core/render/gridToctree.test.ts:157 | SwRS-MDOKFSTUDIO-CORE-022 | S2,S5 | 0.5 | a toctree lists links labelled by the target H1, the file name or an explicit title |
| test/core/render/markerLines.test.ts:65 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.75 | a pipe table in a blockquote marks its rows and itself |
| test/core/render/markerLines.test.ts:75 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.58 | a pipe table in a GitHub alert marks its rows |
| test/core/render/markerLines.test.ts:81 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.58 | a pipe table in a {note} and in an {admonition} marks its rows |
| test/core/render/markerLines.test.ts:91 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.58 | a pipe table in a list item marks its rows |
| test/core/render/markerLines.test.ts:97 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.58 | a pipe table in a tab item marks its rows, and a click on the item still edits the whole item |
| test/core/render/markerLines.test.ts:226 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.58 | a pipe table with aligned columns (written through the HTML pass) marks its rows too |
| test/core/render/mystRawHtml.test.ts:124 | SwRS-MDOKFSTUDIO-CORE-071 | S2,S6 | 1.41 | raw HTML keeps no script, event handler, style, class or script URL |
| test/core/render/mystToc.test.ts:18 | SwRS-MDOKFSTUDIO-CORE-072 | S1 | 1.41 | [TOC] renders the headings as a nested list of links to their ids |
| test/core/render/mystToc.test.ts:39 | SwRS-MDOKFSTUDIO-CORE-072 | S2 | 0.3 | the marker is replaced by the list and is not rendered as a wiki link |
| test/core/render/mystToc.test.ts:46 | SwRS-MDOKFSTUDIO-CORE-072 | S1 | 0.0 | [[_TOC_]] and any case of both markers render the same list, titled as written |
| test/core/render/mystToc.test.ts:82 | SwRS-MDOKFSTUDIO-CORE-072 | S2 | 0.3 | repeated heading text gets distinct ids and a skipped level nests under the previous heading |
| test/core/render/mystToc.test.ts:93 | SwRS-MDOKFSTUDIO-CORE-072 | S1 | 0.0 | headings are collected as plain text and the list follows the headings of the source |
| test/core/state/headingFold.test.ts:43 | SwRS-MDOKFSTUDIO-TOOLBAR-004 | S1 | 0.0 | the key tells two headings with the same text apart by their occurrence |
| test/host-vscode/openExternal.test.ts:22 | SwRS-MDOKFSTUDIO-TOOLBAR-090 | S2,S3 | 0.3 | only http, https and mailto URIs reach openExternal |
| test/host/lifeReq.requirements.test.ts:1006 | SwRS-MDOKFSTUDIO-LIFE-024 | S2 | 0.89 | an Open With tab is titled with the bare file name |
| test/host/openAtLine.test.ts:22 | SwRS-MDOKFSTUDIO-LIFE-001 | S2,S4 | 1.45 | an activation with no preview starts no service, the first preview starts them once, a second one do |
| test/host/openAtLine.test.ts:23 | SwRS-MDOKFSTUDIO-LIFE-004 | S2,S3 | 0.3 | an activation with no preview starts no service, the first preview starts them once, a second one do |
| test/host/studioLine.test.ts:46 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a Studio tab that opens with a pending line asks its page to reveal it, once; without one it asks no |
| test/host/studioLine.test.ts:63 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a line delivered to the live Studio tab of a revealed file is gone afterwards, so a later opening re |
| test/host/studioLine.test.ts:77 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a link from a Studio tab that opens as text reports other and drops the line, and closes no tab |
| test/host/studioLine.test.ts:90 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a link from a Studio tab that opens a new Studio tab reports studio-created and the new tab reveals  |
| test/host/studioLine.test.ts:104 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a link, Back or Next to a file whose Studio tab is open in another group reveals that tab in its gro |
| test/host/studioLine.test.ts:124 | SwRS-MDOKFSTUDIO-LIFE-198 | S2 | 0.3 | Open in Studio at This Line opens the Studio view type in the text editor's group at the caret's lin |
| test/host/studioLine.test.ts:138 | SwRS-MDOKFSTUDIO-LIFE-198 | S1 | 0.0 | Open in Studio at This Line reveals the Studio tab of the file already open in another group and giv |
| test/host/studioLine.test.ts:153 | SwRS-MDOKFSTUDIO-LIFE-198 | S2 | 0.3 | Open in Studio at This Line tells the reader and opens nothing on a Studio tab, with no editor and o |
| test/host/studioSelections.test.ts:9 | SwRS-MDOKFSTUDIO-LIFE-186 | S1 | 0.0 | an expected selection is taken once, with its purpose, by uri and line |
| test/host/studioSelections.test.ts:23 | SwRS-MDOKFSTUDIO-LIFE-186 | S1 | 0.0 | an expected selection expires after the window |
| test/integration/commentAnchors.test.ts:38 | SwRS-MDOKFSTUDIO-REVIEW-219 | S2,S4 | 1.41 | run |
| test/integration/dirtySnapshots.test.ts:116 | SwRS-MDOKFSTUDIO-LIFE-039 | S8 | 1.15 |  |
| test/integration/dirtySnapshots.test.ts:131 | SwRS-MDOKFSTUDIO-LIFE-044 | S1 | 1.41 |  |
| test/integration/dirtySnapshots.test.ts:176 | SwRS-MDOKFSTUDIO-LIFE-049 | S1,S2 | 0.89 |  |
| test/integration/exportHtml.test.ts:73 | SwRS-MDOKFSTUDIO-TOOLBAR-135 | S3 | 1.41 |  |
| test/integration/exportHtml.test.ts:96 | SwRS-MDOKFSTUDIO-TOOLBAR-135 | S2 | 0.41 |  |
| test/integration/findInPreview.test.ts:274 | SwRS-MDOKFSTUDIO-TOOLBAR-010 | S1,S2 | 0.58 |  |
| test/integration/incomingChanges.test.ts:17 | SwRS-MDOKFSTUDIO-REVIEW-195 | S3,S10 | 1.06 | run |
| test/integration/inlineThread.test.ts:152 | SwRS-MDOKFSTUDIO-REVIEW-171 | S3,S4 | 0.89 | runUndo |
| test/integration/lifecycle.test.ts:46 | SwRS-MDOKFSTUDIO-LIFE-170 | S2,S4 | 1.0 | run |
| test/integration/lifecycle.test.ts:47 | SwRS-MDOKFSTUDIO-LIFE-169 | S6,S11 | 1.41 | run |
| test/integration/lifecycle.test.ts:64 | SwRS-MDOKFSTUDIO-LIFE-003 | S3,S7 | 1.41 |  |
| test/integration/lifecycle.test.ts:76 | SwRS-MDOKFSTUDIO-LIFE-024 | S2 | 1.34 |  |
| test/integration/lifecycle.test.ts:122 | SwRS-MDOKFSTUDIO-LIFE-125 | S1,S6 | 0.71 |  |
| test/integration/lifecycle.test.ts:136 | SwRS-MDOKFSTUDIO-LIFE-026 | S1,S3 | 1.0 |  |
| test/integration/lifecycle.test.ts:164 | SwRS-MDOKFSTUDIO-LIFE-032 | S5,S8 | 1.15 |  |
| test/integration/lifecycle.test.ts:196 | SwRS-MDOKFSTUDIO-LIFE-049 | S1,S2 | 0.89 |  |
| test/integration/lifecycle.test.ts:265 | SwRS-MDOKFSTUDIO-LIFE-143 | S3,S5 | 0.71 |  |
| test/integration/openAtLine.test.ts:12 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | run |
| test/integration/openAtLineProbe.test.ts:251 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | run |
| test/integration/openAtLineStudio.test.ts:77 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | run |
| test/integration/openAtLineStudio.test.ts:78 | SwRS-MDOKFSTUDIO-LIFE-197 | S1 | 0.0 | run |
| test/integration/openAtLineStudio.test.ts:79 | SwRS-MDOKFSTUDIO-LIFE-198 | S1 | 0.0 | run |
| test/integration/paletteMode.test.ts:40 | SwRS-MDOKFSTUDIO-LIFE-169 | S4,S6 | 1.41 | run |
| test/integration/paletteMode.test.ts:41 | SwRS-MDOKFSTUDIO-LIFE-169 | S4,S6 | 1.41 | run |
| test/integration/previewEditing.test.ts:81 | SwRS-MDOKFSTUDIO-LIFE-169 | S2,S12 | 1.0 | stepDescriptionColumn |
| test/integration/previewHistory.test.ts:43 | SwRS-MDOKFSTUDIO-TOOLBAR-054 | S2,S3 | 1.41 | run |
| test/integration/previewHistory.test.ts:47 | SwRS-MDOKFSTUDIO-TOOLBAR-077 | S4,S10 | 1.41 | run |
| test/integration/projectFeatures.test.ts:45 | SwRS-MDOKFSTUDIO-CORE-022 | S1,S5 | 1.0 | run |
| test/integration/projectFeatures.test.ts:46 | SwRS-MDOKFSTUDIO-CORE-043 | S1,S2 | 0.71 | run |
| test/integration/realWindowGaps.ts:101 | SwRS-MDOKFSTUDIO-REVIEW-008 | S1,S2 | 1.41 | sideBySideSteps |
| test/integration/reverse-migration-suite.ts:24 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.0 | run |
| test/integration/reviewComments.test.ts:39 | SwRS-MDOKFSTUDIO-REVIEW-001 | S1,S2 | 1.41 | run |
| test/integration/saveKey.test.ts:64 | SwRS-MDOKFSTUDIO-LIFE-173 | S1 | 1.22 | run |
| test/integration/scroll-sync-suite.ts:275 | SwRS-MDOKFSTUDIO-LIFE-100 | S2,S3 | 0.71 | run |
| test/integration/scroll-sync-suite.ts:276 | SwRS-MDOKFSTUDIO-LIFE-108 | S1,S9 | 0.45 | run |
| test/integration/scroll-sync-suite.ts:277 | SwRS-MDOKFSTUDIO-LIFE-119 | S1 | 0.0 | run |
| test/integration/serializer.test.ts:50 | SwRS-MDOKFSTUDIO-LIFE-127 | S4 | 0.82 |  |
| test/integration/serializer.test.ts:82 | SwRS-MDOKFSTUDIO-LIFE-062 | S2,S4 | 0.71 |  |
| test/integration/serializer.test.ts:113 | SwRS-MDOKFSTUDIO-LIFE-038 | S3,S4 | 1.15 |  |
| test/integration/serializer.test.ts:116 | SwRS-MDOKFSTUDIO-LIFE-024 | S2 | 1.34 |  |
| test/integration/sourceMapping.test.ts:44 | SwRS-MDOKFSTUDIO-LIFE-119 | S2,S7 | 1.22 |  |
| test/integration/stockCoexistence.test.ts:79 | SwRS-MDOKFSTUDIO-LIFE-059 | S5 | 1.41 |  |
| test/integration/stockCoexistence.test.ts:123 | SwRS-MDOKFSTUDIO-LIFE-001 | S2 | 1.15 |  |
| test/integration/stockCoexistence.test.ts:230 | SwRS-MDOKFSTUDIO-LIFE-049 | S4 | 1.41 |  |
| test/integration/tocWindow.ts:144 | SwRS-MDOKFSTUDIO-CORE-072 | S1,S3 | 1.41 | scenarioToc |
| test/integration/updateGlow.test.ts:137 | SwRS-MDOKFSTUDIO-LIFE-094 | S3,S5 | 1.34 |  |
| test/integration/workspaceDisposal.test.ts:64 | SwRS-MDOKFSTUDIO-LIFE-143 | S5 | 1.41 |  |
| test/node-services/build/buildQueue.test.ts:139 | SwRS-MDOKFSTUDIO-LIFE-044 | S5 | 0.58 | tracks referenced dependencies for refresh decisions |
| test/node-services/build/buildQueue.test.ts:233 | SwRS-MDOKFSTUDIO-LIFE-039 | S1,S8 | 0.88 | adapts the debounce to twice the last build time, within its bounds |
| test/node-services/build/buildQueue.test.ts:267 | SwRS-MDOKFSTUDIO-LIFE-039 | S4,S8 | 0.88 | an immediate request skips the adaptive wait, and still lets a running build finish |
| test/node-services/build/buildQueue.test.ts:357 | SwRS-MDOKFSTUDIO-LIFE-039 | S2,S3 | 0.3 | the adaptive wait uses the duration the result reports, and keeps its estimate without one |
| test/page/bootContext.test.ts:12 | SwRS-MDOKFSTUDIO-LIFE-156 | S5 | 0.71 | the boot context reads a JSON object and falls back to an empty one for anything else |
| test/page/exportWhileEditing.test.ts:86 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a paragraph under the block editor is exported, and its editor stays open |
| test/page/exportWhileEditing.test.ts:100 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a block editor opened inside a card exports the block of the card |
| test/page/exportWhileEditing.test.ts:145 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a table cell under the cell editor is exported shown, and its editor stays open |
| test/page/exportWhileEditing.test.ts:158 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a {list-table} edited as raw Markdown is exported with its table |
| test/page/exportWhileEditing.test.ts:177 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a front matter value under the value editor is exported shown, and its editor stays open |
| test/page/exportWhileEditing.test.ts:191 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | a front matter key under the key editor is exported shown, and its editor stays open |
| test/page/modules/commentCompose.test.ts:82 | SwRS-MDOKFSTUDIO-REVIEW-049 | S4 | 1.41 | T43: the quote is whitespace-collapsed and capped at 500, prefix and suffix at 32 |
| test/page/modules/commentEditorBehaviour.test.ts:306 | SwRS-MDOKFSTUDIO-REVIEW-217 | S1 | 1.22 | CR 265 r2: the popover is placed again after the Resolve / Delete row fills it |
| test/page/modules/commentThreads.test.ts:199 | SwRS-MDOKFSTUDIO-REVIEW-017 | S1,S2 | 1.15 | T42: re-applying is idempotent and survives replaced content |
| test/page/modules/commentThreads.test.ts:583 | SwRS-MDOKFSTUDIO-REVIEW-086 | S2 | 1.0 | T44: the pending question survives the threads being posted again |
| test/page/modules/contentMorph.test.ts:99 | SwRS-MDOKFSTUDIO-LIFE-069 | S7,S8 | 1.15 | P-07: the key leaves out the source-position attributes and a hash replaces the HTML |
| test/page/modules/exportSnapshot.test.ts:139 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S2,S3 | 0.71 | the snapshot records the shown tab of each tab set and the ticked task boxes |
| test/page/modules/exportSnapshot.test.ts:146 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 0.58 | taking a snapshot changes nothing on the page |
| test/page/modules/findIndex.test.ts:24 | SwRS-MDOKFSTUDIO-TOOLBAR-010 | S5 | 0.71 | text blocks follow the block elements; inline elements stay in their block |
| test/page/modules/findIndex.test.ts:34 | SwRS-MDOKFSTUDIO-TOOLBAR-010 | S1 | 0.0 | white space collapses as the reader sees it, code keeps its own |
| test/page/modules/tocColumn.test.ts:222 | SwRS-MDOKFSTUDIO-TOOLBAR-040 | S2,S3 | 1.0 | the TOC is rebuilt after the content is replaced, once per frame |
| test/page/modules/tocColumn.test.ts:253 | SwRS-MDOKFSTUDIO-TOOLBAR-033 | S1,S3 | 1.41 | the toggle opens the TOC, posts the preference, remembers it and builds the entries |
| test/page/modules/tocColumn.test.ts:320 | SwRS-MDOKFSTUDIO-TOOLBAR-040 | S6 | 0.71 | collapsing a parent hides its descendants, and a rebuild keeps it collapsed |
| test/page/modules/tocColumn.test.ts:340 | SwRS-MDOKFSTUDIO-TOOLBAR-040 | S6 | 1.01 | collapsing a middle parent hides only its own subtree |
| test/page/modules/tocColumn.test.ts:577 | SwRS-MDOKFSTUDIO-TOOLBAR-037 | S7 | 0.58 | a click on a tick goes to that heading |
| test/page/modules/toolbarCollapse.test.ts:92 | SwRS-MDOKFSTUDIO-TOOLBAR-037 | S6 | 0.71 | the layout is measured after the animation in both directions, once for quick clicks |
| test/page/modules/toolbarCollapse.test.ts:93 | SwRS-MDOKFSTUDIO-TOOLBAR-130 | S1 | 0.0 | the layout is measured after the animation in both directions, once for quick clicks |
| test/page/runtimeBlockEditor.test.ts:1401 | SwRS-MDOKFSTUDIO-LIFE-173 | S2 | 0.88 | CR 312: Cmd+S and Ctrl+S in the block text box are left to VS Code (not stopped, nothing posted) |
| test/page/runtimeContentPatch.test.ts:89 | SwRS-MDOKFSTUDIO-LIFE-100 | S1,S8 | 1.13 | T33: the startup sequence of effects and messages is stable |
| test/page/runtimeContentPatch.test.ts:894 | SwRS-MDOKFSTUDIO-CORE-025 | S1,S2 | 1.0 | T34: the patch rebuilds the status region from plain text |
| test/page/runtimeLineMarker.test.ts:99 | SwRS-MDOKFSTUDIO-LIFE-179 | S2 | 0.3 | the marker stays when the reader scrolls and is placed again after a layout change |
| test/page/runtimeLineMarker.test.ts:114 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | a pointer press, an edit or a new line removes or moves the marker |
| test/page/runtimeLineMarker.test.ts:130 | SwRS-MDOKFSTUDIO-LIFE-180 | S2 | 0.3 | in edit mode the marker opens no editor and the overlay is never an edit target |
| test/page/runtimeLineMarker.test.ts:143 | SwRS-MDOKFSTUDIO-LIFE-178 | S1 | 0.58 | a page with no mapped block draws nothing |
| test/page/runtimeLineMarker.test.ts:225 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | a re-render of the content places the marker again on its line |
| test/page/runtimeLineMarker.test.ts:236 | SwRS-MDOKFSTUDIO-LIFE-179 | S2 | 0.3 | opening a block editor removes the marker |
| test/page/runtimeLineMarker.test.ts:247 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | opening a table cell editor removes the marker |
| test/page/runtimeLineMarker.test.ts:257 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | a source edit the page posts removes the marker |
| test/page/runtimeLineMarker.test.ts:268 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | the editor selection mark and the line marker each keep their own aria-current |
| test/page/runtimeLineMarkerPlacement.test.ts:141 | SwRS-MDOKFSTUDIO-LIFE-178 | S2 | 0.89 | a tab set in a closed dropdown is opened, then its tab is selected |
| test/page/runtimeLineMarkerPlacement.test.ts:204 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | a re-render keeps the revealed tab and places the marker again |
| test/page/runtimeLineMarkerPlacement.test.ts:222 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | a tab shown by the keyboard hides the marker, and showing its tab again draws it again |
| test/page/runtimeLineMarkerPlacement.test.ts:240 | SwRS-MDOKFSTUDIO-LIFE-178 | S1,S2 | 0.75 | a later placement never selects a tab |
| test/page/runtimeLineMarkerPlacement.test.ts:382 | SwRS-MDOKFSTUDIO-LIFE-179 | S2 | 0.3 | a properties table the reader collapses again hides the marker, and a later placement never expands  |
| test/page/runtimeScroll.test.ts:1025 | SwRS-MDOKFSTUDIO-TOOLBAR-117 | S3,S4 | 0.88 | an escape left after four decoding rounds is refused, whatever its digits |
| test/page/sideBySideCards.test.ts:171 | SwRS-MDOKFSTUDIO-REVIEW-008 | S2 | 0.3 | CR147: toggling the diff off removes the cards and restores the default |
| test/security/package-contract.test.ts:457 | SwRS-MDOKFSTUDIO-LIFE-198 | S2 | 0.3 | CR-483: Open in Studio at This Line is a palette and title command for Markdown text editors, with n |
| test/security/resource-policy.test.ts:34 | SwRS-MDOKFSTUDIO-CORE-013 | S5 | 1.19 | canonicalizes local resources and rejects hostile paths |
| test/session/associationMigration.test.ts:117 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.0 | a fresh install writes nothing at all |
| test/session/associationMigration.test.ts:146 | SwRS-MDOKFSTUDIO-LIFE-195 | S1 | 0.5 | a second run writes nothing |
| test/session/associationMigration.test.ts:182 | SwRS-MDOKFSTUDIO-LIFE-195 | S2 | 0.3 | the state keys the 1.11.0 migration left are removed, and only when they exist |
| test/session/diagReq.viewState.requirements.test.ts:149 | SwRS-MDOKFSTUDIO-LIFE-002 | S1,S3 | 1.22 | a view preference that cannot be saved holds for the session and warns the reader once |
| test/session/htmlExport.test.ts:110 | SwRS-MDOKFSTUDIO-TOOLBAR-134 | S1,S2 | 1.0 | the save dialog proposes notes.html next to the file with the HTML filter, and the bytes written are |
| test/session/htmlExport.test.ts:127 | SwRS-MDOKFSTUDIO-TOOLBAR-134 | S1 | 0.5 | a document with no local folder proposes the first workspace folder |
| test/session/htmlExport.test.ts:213 | SwRS-MDOKFSTUDIO-TOOLBAR-135 | S2,S3 | 0.41 | a snapshot the host cannot read, or one of another document, is answered with a refusal and an error |
| test/session/previewManager.test.ts:206 | SwRS-MDOKFSTUDIO-LIFE-039 | S2,S3 | 0.3 | a stalled machine between two requests does not close the join window |
| test/session/previewNavigator.test.ts:188 | SwRS-MDOKFSTUDIO-TOOLBAR-094 | S1,S2 | 1.3 | blocks unsafe anchors, schemes, and paths |
| test/session/reviewReqComments.requirements.test.ts:549 | SwRS-MDOKFSTUDIO-REVIEW-119 | S4,S7 | 1.22 | an unrelated undo keeps a short-quote thread on its followed line, far beyond the search window |
| test/session/reviewReqIncoming.requirements.test.ts:316 | SwRS-MDOKFSTUDIO-REVIEW-006 | S2 | 1.3 | CR147: with preview.showIncomingChanges off nothing is read or posted |
| test/session/saveCommand.test.ts:156 | SwRS-MDOKFSTUDIO-LIFE-173 | S1 | 1.22 | CR 312: a page that is not ready, or cannot be reached, has nothing to flush: the document is saved  |
| test/session/studioTabNavigation.test.ts:146 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | a link with a heading anchor followed in a Studio tab hands the heading's line with the open |
| test/session/studioTabNavigation.test.ts:161 | SwRS-MDOKFSTUDIO-LIFE-196 | S2 | 0.3 | a link with a marker line and a link with neither hand their line, 1 for neither |
| test/session/studioTabNavigation.test.ts:175 | SwRS-MDOKFSTUDIO-LIFE-197 | S1 | 0.0 | a link that opens a new Studio tab records the move, and the new tab shares the source's history |
| test/session/studioTabNavigation.test.ts:204 | SwRS-MDOKFSTUDIO-LIFE-197 | S1 | 0.0 | a link to a Studio tab that is already open keeps its own history and appends the move to it |
| test/session/studioTabNavigation.test.ts:233 | SwRS-MDOKFSTUDIO-LIFE-197 | S1 | 0.0 | a link from a Studio tab that opens as text records nothing, in either history |
| test/session/studioTabNavigation.test.ts:252 | SwRS-MDOKFSTUDIO-LIFE-197 | S2 | 0.3 | a link to a file that is not Markdown opens without the Studio tab hand-off and without a history en |
| test/session/studioTabNavigation.test.ts:296 | SwRS-MDOKFSTUDIO-LIFE-196 | S1 | 0.0 | Back and Next from a Studio tab to a file whose Studio tab is open elsewhere ask the host to reveal  |
| test/session/toolbarReq.requirements.test.ts:833 | SwRS-MDOKFSTUDIO-LIFE-181 | S1 | 0.0 | a requested line waits for the page to be ready, is posted once and becomes the anchor |
| test/session/toolbarReq.requirements.test.ts:853 | SwRS-MDOKFSTUDIO-LIFE-181 | S1 | 0.0 | a requested line is posted at once when the page is already ready |
| test/session/toolbarReq.requirements.test.ts:889 | SwRS-MDOKFSTUDIO-LIFE-187 | S1 | 1.22 | a jump that arrives before the switch of document waits for the page of that document |
| test/session/toolbarReq.requirements.test.ts:907 | SwRS-MDOKFSTUDIO-LIFE-187 | S1 | 0.82 | the switch of document drops a line requested for another document and the old marker |
| test/session/toolbarReq.requirements.test.ts:925 | SwRS-MDOKFSTUDIO-LIFE-187 | S1 | 0.41 | a line past the window is dropped and a hidden page waits for its ready |
| test/session/toolbarReq.requirements.test.ts:1146 | SwRS-MDOKFSTUDIO-LIFE-187 | S1 | 0.82 | a jump before the switch is posted at the page ready of the switched render, not before |
| test/session/webview.priming.test.ts:35 | SwRS-MDOKFSTUDIO-CORE-013 | S4,S5 | 0.89 | an image the guess misses (an unquoted attribute) is found by the sanitizer and shown after a second |
| test/site/requirementsViewer/home.test.ts:19 | SwRS-MDOKFSTUDIO-CORE-069 | S1,S3 | 0.71 | home: layers, areas, sections and figures |
| test/site/requirementsViewer/home.test.ts:41 | SwRS-MDOKFSTUDIO-CORE-080 | S2 | 0.3 | home degrades without a report |
| test/site/requirementsViewer/home.test.ts:56 | SwRS-MDOKFSTUDIO-CORE-069 | S1 | 0.0 | marker snippets come from the repository files and fall back to the path |
| test/site/requirementsViewer/home.test.ts:63 | SwRS-MDOKFSTUDIO-CORE-069 | S3 | 0.58 | marker snippets come from the repository files and fall back to the path |
| test/site/requirementsViewer/metroMap.test.ts:174 | SwRS-MDOKFSTUDIO-CORE-081 | S1,S4 | 0.58 | metroSvg draws a fourth path in the third colour |
| test/site/requirementsViewer/model.test.ts:15 | SwRS-MDOKFSTUDIO-CORE-069 | S1 | 0.0 | the model separates active from retired by req_lifecycle and reads the older key |
| test/site/requirementsViewer/model.test.ts:32 | SwRS-MDOKFSTUDIO-CORE-069 | S1,S3 | 0.71 | the model counts the figures of active requirements and the areas |
| test/site/requirementsViewer/model.test.ts:52 | SwRS-MDOKFSTUDIO-CORE-087 | S2 | 1.0 | the model reads scenarios, files, parents, paths and known issues |
| test/site/requirementsViewer/pages.test.ts:37 | SwRS-MDOKFSTUDIO-CORE-080 | S1 | 0.0 | every relative link resolves from every depth |
| test/site/requirementsViewer/pages.test.ts:38 | SwRS-MDOKFSTUDIO-CORE-082 | S1,S2 | 0.71 | every relative link resolves from every depth |
| test/site/requirementsViewer/pages.test.ts:124 | SwRS-MDOKFSTUDIO-CORE-084 | S2 | 0.3 | without JavaScript the search and Play controls are hidden |
| test/site/requirementsViewer/pages.test.ts:125 | SwRS-MDOKFSTUDIO-CORE-086 | S1,S2 | 0.71 | without JavaScript the search and Play controls are hidden |
| test/site/requirementsViewer/pages.test.ts:188 | SwRS-MDOKFSTUDIO-CORE-082 | S1 | 1.41 | a full ID is the text of every link to a requirement |
| test/site/requirementsViewer/pages.test.ts:189 | SwRS-MDOKFSTUDIO-CORE-083 | S1 | 1.41 | a full ID is the text of every link to a requirement |
| test/site/requirementsViewer/search.test.ts:9 | SwRS-MDOKFSTUDIO-CORE-084 | S1,S2 | 1.41 | kinds |
| test/site/requirementsViewer/useCaseDiagram.test.ts:27 | SwRS-MDOKFSTUDIO-CORE-087 | S2 | 1.0 | chromiumStarts |
| test/site/requirementsViewer/write.test.ts:17 | SwRS-MDOKFSTUDIO-CORE-069 | S1 | 0.0 | the site navigation links requirements/ from the root and from nested pages |
| test/site/requirementsViewer/write.test.ts:31 | SwRS-MDOKFSTUDIO-CORE-069 | S1,S3 | 0.71 | requirements.html redirects to requirements/ and carries the tags of the index |
| test/site/requirementsViewer/write.test.ts:50 | SwRS-MDOKFSTUDIO-CORE-069 | S1,S3 | 0.71 | the viewer is written under requirements/ with its assets, index and redirect |
| test/site/requirementsViewer/write.test.ts:51 | SwRS-MDOKFSTUDIO-CORE-080 | S2 | 1.15 | the viewer is written under requirements/ with its assets, index and redirect |
| test/site/requirementsViewer/write.test.ts:83 | SwRS-MDOKFSTUDIO-CORE-085 | S6 | 1.15 | a missing report writes the home and the redirect only |
| test/site/requirementsViewer/write.test.ts:103 | SwRS-MDOKFSTUDIO-CORE-069 | S1 | 0.0 | the History checkbox sits inside the header landmark |
| test/site/siteClips.test.ts:39 | SwRS-MDOKFSTUDIO-CORE-095 | S1,S3 | 1.34 | everything |
| test/site/siteTheme.test.ts:73 | SwRS-MDOKFSTUDIO-CORE-086 | S3 | 0.71 | myst |
| test/visual/capture_export_html.py:27 | SwRS-MDOKFSTUDIO-TOOLBAR-135 | S2 | 0.82 | check_export_html |
| test/visual/capture_export_html.py:28 | SwRS-MDOKFSTUDIO-TOOLBAR-136 | S1,S2 | 1.34 | check_export_html |
| test/visual/capture_find_checks.py:12 | SwRS-MDOKFSTUDIO-TOOLBAR-010 | S1,S2 | 1.15 | check_find_bar |
| test/visual/capture_find_checks.py:13 | SwRS-MDOKFSTUDIO-TOOLBAR-010 | S1,S2 | 1.15 | check_find_bar |
| test/visual/capture_sbs_checks.py:11 | SwRS-MDOKFSTUDIO-REVIEW-008 | S1,S2 | 1.41 | check_side_by_side |
| test/visual/capture_toc_checks.py:73 | SwRS-MDOKFSTUDIO-TOOLBAR-033 | S1,S3 | 1.41 |  |
| test/visual/capture_toc_checks.py:95 | SwRS-MDOKFSTUDIO-TOOLBAR-037 | S1,S4 | 1.0 |  |
| test/visual/capture_toc_checks.py:107 | SwRS-MDOKFSTUDIO-TOOLBAR-040 | S1,S6 | 0.71 |  |
| test/visual/capture_toc_checks.py:159 | SwRS-MDOKFSTUDIO-TOOLBAR-045 | S4,S5 | 1.15 |  |
| test/visual/capture_toc_checks.py:193 | SwRS-MDOKFSTUDIO-TOOLBAR-040 | S6,S7 | 0.71 |  |
| test/visual/changeBarCardScenarios.ts:54 | SwRS-MDOKFSTUDIO-REVIEW-221 | S1,S2 | 1.15 |  |
| test/visual/changeBarCardScenarios.ts:67 | SwRS-MDOKFSTUDIO-REVIEW-222 | S1 | 1.15 |  |
| test/visual/exportHtmlScenarios.ts:16 | SwRS-MDOKFSTUDIO-TOOLBAR-135 | S1,S2 | 0.5 |  |
| test/visual/exportHtmlScenarios.ts:18 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S2 | 1.0 |  |
| test/visual/exportHtmlScenarios.ts:35 | SwRS-MDOKFSTUDIO-TOOLBAR-137 | S1 | 1.15 | toolbar-navigation/v44-export-html-edited-cell-light-900 |
| test/visual/lineMarkerScenarios.ts:197 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 |  |
| test/visual/lineMarkerScenarios.ts:210 | SwRS-MDOKFSTUDIO-LIFE-180 | S1 | 0.0 | lifecycle-sync/v06-line-marker-edit-mode-light-900 |
| test/visual/lineMarkerScenarios.ts:246 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | lifecycle-sync/v09-line-marker-folded-section-light-900 |
| test/visual/lineMarkerScenarios.ts:262 | SwRS-MDOKFSTUDIO-LIFE-179 | S1 | 0.0 | lifecycle-sync/v10-line-marker-closed-dropdown-dark-900 |
| test/visual/lineMarkerScenarios.ts:274 | SwRS-MDOKFSTUDIO-LIFE-180 | S1 | 0.0 | lifecycle-sync/v11-line-marker-edit-mode-list-dark-900 |
| test/visual/lineMarkerScenarios.ts:313 | SwRS-MDOKFSTUDIO-LIFE-192 | S1 | 1.0 | lifecycle-sync/v14-line-marker-delimiter-line-light-900 |
| test/visual/lineMarkerScenarios.ts:401 | SwRS-MDOKFSTUDIO-LIFE-180 | S1 | 0.0 | lifecycle-sync/v22-line-marker-edit-mode-property-row-dark-900 |
| test/visual/lineMarkerScenarios.ts:413 | SwRS-MDOKFSTUDIO-LIFE-180 | S1 | 0.0 | lifecycle-sync/v23-line-marker-edit-mode-tab-panel-dark-900 |
| test/visual/scenarioDefinitions1.ts:88 | SwRS-MDOKFSTUDIO-CORE-028 | S6 | 1.15 | handbook-dark-bottom |
| test/visual/scenarioDefinitions1.ts:1304 | SwRS-MDOKFSTUDIO-TOOLBAR-018 | S1,S6 | 1.0 |  |
| test/visual/scenarioDefinitions2.ts:575 | SwRS-MDOKFSTUDIO-REVIEW-207 | S3 | 1.15 | review-annotations/v21-readme-showcase-diff-cream-1000 |
| test/visual/tableRowColourScenarios.ts:17 | SwRS-MDOKFSTUDIO-CORE-077 | S1,S2 | 1.41 |  |
