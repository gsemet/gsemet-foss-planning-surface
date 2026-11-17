## Summary

The preview now renders three MyST features it used to show as raw boxes or with a wrong title:
standalone `{card}`, `{tab-set}` / `{tab-item}`, and the `versionadded` / `versionchanged` /
`deprecated` directives (title without a trailing colon). The README shows them.

## Deliverables

- **Card**: `{card}` with `:header:`, `:footer:`, `^^^` / `+++` separators, `:link:`, `:class-card:`
  (plain class names only; reserved prefixes such as `okf-` or `vscode-` are dropped).
- **Tabs**: a tab bar with ARIA roles, one panel at a time, click, arrows (wrapping), Home/End,
  `:selected:`, `:sync:`. In edit mode each panel edits its own source lines.
- **Version titles**: `:::{versionadded} 0.47` reads "Added in version 0.47".
- README section "Version notes, cards and tabs" and `docs/user/editing.md`.

Before (raw directive boxes, titles with a colon) and after, cream and dark (headless captures of
the page bundle):

| Before (cream) | After (cream) |
| --- | --- |
| ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/48a3c6acf79902f68b9857bd24039d3aa2f9ec6c/headless-before-cream.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/48a3c6acf79902f68b9857bd24039d3aa2f9ec6c/headless-after-cream.png) |
| **Before (dark)** | **After (dark)** |
| ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/48a3c6acf79902f68b9857bd24039d3aa2f9ec6c/headless-before-dark.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/48a3c6acf79902f68b9857bd24039d3aa2f9ec6c/headless-after-dark.png) |

After a click, Home, ArrowRight and End on the tab bar:

![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/48a3c6acf79902f68b9857bd24039d3aa2f9ec6c/headless-after-tabs-keyboard.png)

## Changes

New `src/page/modules/tabs.ts`; card, tab and version transforms in `src/core/render/`; styles;
edit-mode and content-patch hooks so tab choices survive a patch. The HTML sanitizer is unchanged.

## Impacts

Preview rendering of the three directive families. Existing grid cards keep their order.

## Blast radius

2 (preview rendering and page runtime).

## Test plan

- 22 new unit tests (`test/core/render/cardsTabs.test.ts`, `test/page/modules/tabs.test.ts`), all
  failing on the previous code; three visual scenarios (`myst/v41`-`v43`).
- `just check` passes (unit 2882, security 66, 1034 requirements, 0 errors).
- A real VS Code window scenario (`test/integration/mystBlocksWindow.ts`) is written but was not
  run: the machine's screen was locked. Run it with the heavy CI before merging.

### Requirements traceability

| ID | Source | Tests |
| --- | --- | --- |
| MYST-097 (card) | `src/core/render/mystBlockTransforms.ts`, `mystGridToctree.ts` | `test/core/render/cardsTabs.test.ts`, `test/visual/cardsTabsScenarios.ts` |
| MYST-098 (tab set) | `src/core/render/mystBlockTransforms.ts`, `src/page/features/editMode.ts` | `test/core/render/cardsTabs.test.ts`, `test/integration/mystBlocksWindow.ts` |
| MYST-099 (tab keyboard) | `src/page/modules/tabs.ts` | `test/page/modules/tabs.test.ts`, `test/visual/cardsTabsScenarios.ts` |
| MYST-001 (version titles) | `src/core/render/mystBlockTransforms.ts` | `test/core/render/mystFeatures.test.ts` |

MYST-011 and CORE-061 (superseded) have updated wording.

## Autonomous decisions

- Placed on top of the stack. The `}::` typo in the reported source is not parsed leniently; only
  the valid form is supported.
- Screenshots are headless captures because the macOS session was locked; real-window run pending.
- `requirements-update` with the locked okfreq 0.13.0 also reordered file lists in DIAG-097,
  CORE-071 and REVIEW-003; kept because coverage check fails without them.

## Internal references

CR 148, stacked above CR 147.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
