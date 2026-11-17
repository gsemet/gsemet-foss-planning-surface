# 047 — initial-defaults

New request (user, 2026-10-23): define the initial state of the extension and the default
settings, in a dedicated PR.

## Decisions (user grill, 2026-10-23)

1. Fresh state (workspace with nothing stored), as built-in defaults, NOT new settings:
   - preview theme: `cream` (today `current`; `src/state/previewTheme.ts`, webview fallback in
     `src/webview/scrollSync.ts`);
   - floating toolbar collapsed (rows 2-3 hidden): `DEFAULT_VIEW_PREFERENCES.toolbarCollapsed = true`
     (`src/state/previewViewPreferences.ts`, `src/webview/toolbarCollapse.ts`);
   - editing palette mode `gfm`: `editing.defaultPaletteMode` default `myst` → `gfm` in
     `package.json` and `src/configuration/editingConfiguration.ts`.
2. Existing users keep what they chose: a theme, toolbar state or palette mode already stored for
   a workspace is used as is; the new defaults apply only where nothing is stored. Test it.
3. Every other default is kept as is (reviewed one by one with the user): scroll sync both ways,
   markEditorSelection off, doubleClickToSwitchToEditor off, incrementalUpdates on,
   maxContentWidth 960 + width mode margin, stickyHeadingDepth 3, TOC closed, zoom 100,
   showComments on, showIncomingChanges on, propertiesTable on, strictAdditionalProperties off,
   allowOutsideWorkspaceLinks off, path settings and authorName empty.
4. Settings UI: organise `contributes.configuration` into ordered categories (Preview, Editing,
   Frontmatter, Comments, PlantUML), most used first (`order`), descriptions proofread. Setting keys
   never change. CR 045 adds `plantuml.useJar` in parallel: whoever lands second rebases and puts it
   in the PlantUML category.
5. Tests: unit tests for the new defaults and for "stored choice wins". Visual: existing scenarios
   must not change PNGs because of the new defaults — scenarios that relied on the implicit
   default pin their previous theme / toolbar state explicitly (the assertion intent is unchanged);
   add one scenario "fresh workspace" showing cream + collapsed toolbar (light/dark host). README
   images regenerated only if intended (decide and say so in the PR).
6. Docs: CHANGELOG (user-visible change of defaults), README settings section in the new order.
7. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green. Rounds: 3.
8. PR written for an external reader.

## Decision 9 (user, 2026-10-23 ~18:00)

"Tu peux merger 42 quand elle sera valide et rebase les autres restantes dessus après": the main
session merges PR #42 (rebase merge) once the required `checks` is green, the PR mergeable and the
review approved; then it rebases the remaining CRs (048) on the new main. The main session
rebased #42 on 7149d6d itself (b04834f): package.json settings categories now include
`plantuml.useJar` in the PlantUML category; scenario count 312; README PlantUML section merged.
