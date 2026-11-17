Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: theme-zoom inventory (P10.1 critic)

Scope `theme-zoom` (THEME). Checked `inventory/theme-zoom.md` against the checklists
(`checklists/*.md`, scope column), `tools/scope-map.json` and the worktree
`markdown-okf-schema-studio-wt-059`.

## Missing rows

None. The checklists hold 24 rows with scope `theme-zoom` (exact or `?`); all 24 are cited in the
inventory table (scripted `comm` of the scope's C- ids against all C- ids in the inventory: empty
difference). None is listed as moved out, so no target-scope check applies. Related rows owned by
other scopes (C-CL-080, C-AR-141 review-annotations/toolbar-navigation; C-CL-057 code-blocks;
C-CL-101 diagrams; C-CL-002, C-MSG-003 toolbar-navigation) are each cited by their owner's
inventory; the cream default and Cream-in-the-loop halves are covered here by F-THEME-001/003.
Optional: the "Checklist corrections" section could say that C-CL-057 (Cream added to the button
loop) is guessed `code-blocks?` but is behaviourally F-THEME-001/016; the owner inventory already
claims it, so this is a note, not a gap.

## Missing behaviours

Minor (none of substance on its own; two together are worth one added row):

1. No workspace storage (`WorkspaceChoices.storage` undefined, e.g. no workspace state available):
   `setPreviewThemeMode` and `setViewPreference` keep the choice for the session only and skip
   persistence silently (`src/session/workspaceChoices.ts`, early `return`). F-THEME-033 covers only
   the failed write, not the absent storage.
2. `resetPreviewThemeMode` / `clearPreviewThemeMode` (`previewTheme.ts`) forget the stored theme
   (session and workspace); used by test hooks only, no reader-visible path. Worth one line
   ("not user reachable") so the exported function is accounted for.
3. Page-side normalisation of a saved or initial zoom (`viewControls.ts:normalize`: non-number and
   NaN are ignored, other values rounded to 10 and clamped) is only implied by F-THEME-028/029,
   which describe the host side; the page-side fallback chain (saved state, then initial
   preference, then 100 %) is stated, the rounding of a page-side value is not.
4. Zoom buttons mirror the tooltip into `data-tooltip` as well as `title` (themeMode.ts does the
   same for the theme button); and both features are null-safe when the toolbar is absent.
   Trivial.

Checked and already covered: unknown mode falls back to Cream, precedence host > saved state >
default, read-only acceptance, reduced motion, themeChanged deferral, no-op zoom at limits,
`previewReady` re-sync, persistence failure.

## Wrong/unverifiable evidence

Spot-checked 34 claims. All 29 test titles listed below exist verbatim in the cited file (grep -F):
`runtimeScroll` cycle test; `creamTheme` (6 titles); `previewTheme.test` (4); `runtimePageControls`
(5); `pageStateMessages` frozen validators; `motion.test` CR 046; `runtimeContentPatch` CR 046;
`themeTokens.test` (4); `mermaidCache` PERF-07 (2); `previewStyles` T08; `contentPatch` T08;
`pageToHost` per-preference validation; `previewViewPreferences` (2). Source symbols found:
`themeSwitch`/`endSwitch` (motion.ts), `themeVariable`/`initializedTheme` (mermaidPreview.ts),
`diagramKey` (mermaidCache.ts), `deferWhileEditing(..., "theme-render")` (viewState.ts),
`onThemeChanged` (hostEvents.ts, activation.ts), `PAGE_MESSAGE_GATES` entries
(`previewThemeModeChanged: "page-state"`, `previewViewPreferenceChanged: "render"`),
`keepReadingLine` (runtime.ts), lifecycle.test posts `previewThemeModeChanged`, reload-suite asserts
zoom 130 survives reload, `captureRegistry` r01-r08 with r03 `capture: false`. Coverage states
(host handler untested at session level: only `test/integration/lifecycle.test.ts` mentions the
messages under test/session|integration; F-007, 030, 031, 032, 033 untested) match what grep shows.

One imprecise claim:

- F-THEME-032 / F-THEME-008 "the only dedicated rule is `@media (forced-colors: active)` for the
  warning banner": true for `pageChromeStyles.ts`, but the preview CSS has other forced-colors
  rules (`contentBlockStyles.ts` diff lines, `editPaletteStyles.ts` slash menu). Reword to "the only
  theme-level rule" or "no rule for the page palette; forced-colors rules exist for the warning
  banner, diff lines and the slash menu".

Not verified (no tool use of VS Code allowed): visual scenario assertions (`v01-v13`) and the
`data-sphinx-preview-theme` "no CSS reads it" claim was confirmed only for src/core and src/page
(only themeMode.ts writes it).

## Count check

Table has 33 rows (F-THEME-001 to 033). Untested 6 (007, 011, 030, 031, 032, 033) so tested 27;
doc-only 0; the "Undocumented" list names 14 ids and the count says 14. Checklist rows 24/24
matches the scripted count. Counts table is consistent.

## Verdict

Real gaps: none (no uncited row, fewer than 3 substantive missing behaviours, no false test or
symbol evidence). Suggested polish: add the no-storage and `resetPreviewThemeMode` notes (F-033 or a
new row), and reword the forced-colors claim in F-THEME-032.

Verdict: APPROVE
