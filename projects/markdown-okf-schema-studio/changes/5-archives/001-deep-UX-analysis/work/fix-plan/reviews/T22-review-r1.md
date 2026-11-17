# T22 review — round 1

Base: 43e1711 · Reviewed diff: 11 files (6 source, 5 test), ~+290/-2

## Gates
compile PASS; unit PASS (logs/T22-unit.log); types PASS (logs/T22-types.log); contracts PASS
(logs/T22-contracts.log); trusted PASS incl. RI-T22 (logs/T22-trusted.log); visual PASS vs T00
baseline, 0 new failure lines (logs/T22-visual-failures-normalized.txt). No new failures.

## Done-when
- [x] unit and trusted gates pass; RI-T22 passes — logs above; pre-fix failure of RI-T22 shown in
  logs/T22-impl-pre-trusted.log (`the datalist offers StRS-B: []`).
- [x] `stems` sorted and limited — stemIndex.test.ts "T22: stems returns the indexed stems sorted and limited".
- [x] suggestions only for filename-stem fields (property or `items`), absent with `inspectLinks:false`
  — okfFrontmatter.test.ts "T22: linkSuggestions ...".
- [x] attribute escaped — propertiesTable.test.ts "T22: link suggestions are rendered as an escaped row attribute".
- [x] datalist on existing and new inputs, warning set/cleared, unknown value still saves — four
  scrollSync.test.ts T22 tests.

## UX-22 frozen (explicit)
- `fileLinks.ts`: only an appended export `filenameStemSuggestions`; `resolveFrontmatterLinkRoots`,
  `inspectFrontmatterLinks`, messages untouched (diff shows no other hunk).
- `stemIndex.ts`: only `stems(limit)` added; it reads `candidatesByStem` keys, copies them into a
  new array before sorting, and does not touch `pathsByStem`, the cache, or the file system.
  `get`/`lookup`/`build`/`visit` unchanged.
- `okfFrontmatter.ts`: the new block runs after `fieldsFromYaml(... linkResults)`, only assigns
  `field.linkSuggestions`; `linkInspectionOptions` (line ~1323) is reused as is, so the roots are
  the resolver's own. `inspectLinks !== false` gate for link inspection is unchanged.

## inspectLinks === true reaches users
`extension.ts:732` (link-enrichment render, `scheduleLinkEnrichment`) and `extension.ts:1469`
(fresh analysis for navigation) pass `inspectLinks: true`; the fast renders (553, 995, 2521) pass
`false`, so suggestions appear after enrichment, as specified. RI-T22 confirms end to end.

## Cost
`filenameStemSuggestions` is called lazily via `??=` at most once per analysis and only if some
field matches `fieldUsesFilenameStemLinks`; otherwise zero calls. It uses the cached index
(`getCachedMarkdownStemIndex`), cap 500. No per-keystroke host work; webview builds one datalist
per editor open.

## Protected features checked
- P-N6 / UX-22: see above; `fileLinks.test.ts` unchanged and passing.
- P-R7 / UX-24: value display untouched; only an extra row attribute when suggestions exist.
- P-E7: list editor creation, save path unchanged; T21 list tests and RI list scenario still pass.
- P-S4: suggestions reach the DOM via `escapeHtml` attribute, `JSON.parse`, `option.value`/
  `textContent`; no `innerHTML`.
- P-E8: suggestions only attach inside the list editor, which exists only in edit mode.
- §2 template rules: new runtime code has no backticks or `${`; uses `'...'` strings; compiled
  contract gate PASS.

## Findings
1. [MINOR] src/webview/scrollSync.ts:`refreshLinkWarning` — when the status already shows a
   validation error (`data-state="error"`), typing an unknown stem overwrites that error text with
   the warning. Fix: at the start of the "unknown" branch, return without changing `status` when
   `status.getAttribute("data-state") === "error"` (still set `aria-invalid`). Test: in
   scrollSync.test.ts set status `data-state="error"` and text "E", type unknown value, assert text stays "E".
2. [MINOR] src/webview/scrollSync.ts list editor — removing the only unknown item (remove button)
   does not call `refreshLinkWarning`, so the warning lingers until the next input. Fix: call
   `refreshLinkWarning()` after an item row is removed when `linkStems` is set. Test: unknown item
   warns, click its remove button, assert `data-state` is null.
3. [NIT] Existing unknown items are not flagged when the editor opens (only on input). Acceptable
   per task text.

## Existing assertions changed
None. `openListEditor` helper gained an optional parameter (additive) — OK.

VERDICT: PASS
