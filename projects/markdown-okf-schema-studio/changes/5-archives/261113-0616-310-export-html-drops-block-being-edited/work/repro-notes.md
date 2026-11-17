# Reproduction notes, CR-310

Test: `test/page/exportWhileEditing.test.ts` (the real editors of the page runtime on the runtime
harness, the Export button, `buildHtmlExport` on the snapshot the page sent). Run on the unfixed
code (`origin/main`, `cb968299`) with
`npx tsc -p . && node scripts/node-test.mjs unit out/test/page/exportWhileEditing.test.js`.

| Case | Unfixed code |
| --- | --- |
| paragraph under the block editor | passes (exported, nothing hides it) |
| block editor opened inside a card | passes |
| `{list-table}` edited as raw Markdown | passes |
| table cell under the cell editor | FAILS: `<span data-sphinx-table-cell-content aria-hidden="true">` kept around the cell content |
| front matter value under the value editor | FAILS: `hidden` kept on `[data-okf-value-display]` |
| front matter key under the key editor | FAILS: `hidden` kept on `.okf-name-cell` |

So the Known issue of TOOLBAR-137 was wrong for a block (it is exported); the real losses are the
table cell and the two front matter editors. The fix in `removeChrome` covers the three failing cases.
