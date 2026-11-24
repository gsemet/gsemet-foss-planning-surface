## Summary

Copying a selection in the preview puts the exact Markdown source under it on the clipboard. When the selection starts or ends inside a construct (a bold word, an admonition, a table, a list item, a heading), that verbatim cut is broken Markdown: `rld** again`, an admonition body with a closing fence and no opening, table rows without their header.

This adds an opt-in setting, `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges` (off by default). With it on, a selection entirely inside a construct copies that construct's content only, and a selection crossing a construct's boundary gets the missing delimiters added. With it off, the copy is unchanged. An edge the alignment cannot place now snaps to its whole element instead of leaving the copy native, with the setting off or on.

## Deliverables

Source `Hello **world** again`:

| Selection | Setting off | Setting on |
| --- | --- | --- |
| from "r" to the end of the line | `rld** again` | `**rld** again` |
| from "o" to "l" | `orl` | `orl` |
| `## Hello`, from "llo" | `llo` | `## llo` |

New modules, all pure code in `src/core/mapping`:

```text
rawCopyEdges.ts   balanceRawCut: snap, then verbatim (off) or balanced (on)
rawCopyScan.ts    scans the source for the constructs enclosing an offset
rawCopyBalance.ts block rules: containers, code, tables, lists, headings, definitions, HTML, footnotes
rawCopyInline.ts  inline rules: emphasis, code, links, roles, inline HTML
```

A selection starting in a bold word of an admonition and ending in a table row (setting on): the admonition's opening line, `**rld**` and the rest of the paragraph, the table's header and delimiter rows, and the touched row whole. Off: the verbatim cut. A word inside a code block copies the word alone (on) or the same verbatim text (off); a selection leaving the code block gets its fences (on).

The setting `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges` defaults to `false`.

## Blast radius

Grade: **1**. The setting is off by default, so the copy only changes for an edge the alignment could not place. A plain revert restores the previous behaviour.

## Autonomous decisions

- The enclosing constructs are found by a scan of the source lines, with the frames used only to snap an unplaced edge.
- The code block's line numbers no longer count as page chrome, so a selection edge in a code block is placed instead of left native; this also applies with the setting off.
- The list-marker helper moved out of `listItemIndent.ts` into `listMarker.ts` to keep files under the size limit.

## Known gaps

- The real VS Code window step (`test/integration/realInput/rawCopy.ts`) is written but not run locally (no VS Code on this machine); it runs in the heavy CI (`ci.yml` with `heavy=true`).
- Visual scenarios other than the raw copy ones were not re-run locally.

<details><summary>Details</summary>

## Changes

- `rawMarkdownForSelection` takes `options?: { balanceEdges?: boolean }`, fed into the cut.
- `balanceRawCut` snaps unplaced edges and balances when the setting is on.
- The setting is a startup setting in the registry; the page handler reads it once from the boot context.
- Fix found on the way: the code block's line numbers counted as chrome, so an edge in a code block left the copy native; they no longer do.
- Docs (`docs/user/settings.md`), glossary entry, changelog line.
- Requirements: nine new SwRS in the block-editing scope; the raw copy SwRS 272 and 273 and the StRS are updated.

## Impacts

No visual change. The clipboard text differs only with the setting on, or for a formerly unplaceable edge.

## Tests

- Requirements: SwRS-MDOKFSTUDIO-BLOCK-278 to 286 added; SwRS-MDOKFSTUDIO-BLOCK-272 and 273 and StRS-MDOKFSTUDIO-BLOCK-027 updated. Sources: `src/core/mapping/rawCopyEdges.ts`, `rawCopyScan.ts`, `rawCopyBalance.ts`, `rawCopyInline.ts`, `src/core/configuration/settingsRegistry.ts`, `src/page/features/rawCopy.ts`.
- Tests: `test/core/mapping/rawCopyBalance*.test.ts`, `rawCopy.test.ts`, `test/core/configuration/*.test.ts`, `test/page/runtimeRawCopy.test.ts`, `test/security/package-contract.test.ts`, `test/visual/capture_raw_copy.py`, `capture_raw_copy_balanced.py`, `test/integration/realInput/rawCopy.ts`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): core balancing tests, registry tests, page handler test, browser capture page
- [ ] Requirements: SwRS added and updated, markers in code and tests, `just requirements-update`
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `just preflight`
- [ ] Review
- [ ] CI green

## Internal references

- Builds on the raw copy change, already merged.

</details>
