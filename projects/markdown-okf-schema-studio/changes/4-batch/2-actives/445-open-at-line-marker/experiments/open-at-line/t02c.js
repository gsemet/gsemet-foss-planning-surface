// T2c: variance of the selection kind of a search click against the stored view state.
const { launch, sleep, fs } = require("./lib");
(async () => {
  const s = await launch("t02c", { port: 9413, settings: { "markdownOkfSchemaStudio.open.searchResultsInStudio": false, "markdownOkfSchemaStudio.open.markdownFilesInStudio": false } });
  const { page } = s;
  await sleep(5000);
  let mark = 0;
  const events = (label) => {
    const lines = fs.readFileSync(s.logF, "utf8").trim().split("\n");
    const fresh = lines.slice(mark); mark = lines.length;
    const out = [];
    for (const l of fresh) { const o = JSON.parse(l); if (o.ev === "selection" || o.ev === "visible" || (o.ev === "tabs" && o.opened.length)) out.push(JSON.stringify({ dt: o.t, ev: o.ev, kind: o.kind, sel: o.sel, eds: o.eds?.map((e) => e.sel), opened: o.opened?.length, preview: o.opened?.[0]?.preview })); }
    s.note(`CASE ${label}\n    ` + out.join("\n    "));
  };
  const closeTab = async () => { await page.keyboard.press("Control+W"); await sleep(1200); events("close"); };
  const searchClick = async (row, label) => { await s.search("zebrafish"); await page.locator(".search-view .monaco-list-row").nth(row).click(); await sleep(2000); events(label); };
  events("startup");
  await searchClick(1, "search click doc.md line 30, never opened (no stored state)");
  await closeTab();
  await searchClick(2, "search click doc.md line 40, stored state = line 30 range");
  await closeTab();
  await searchClick(1, "search click doc.md line 30, stored state = line 40 range");
  await closeTab();
  await searchClick(4, "search click other.md line 30 never opened");
  await closeTab();
  // plain reopening, stored cursor (empty) at line 30 of other.md: reopen via Explorer
  await page.keyboard.press("Control+Shift+E"); await sleep(700);
  await page.locator(".explorer-viewlet .monaco-list-row", { hasText: "other.md" }).first().click(); await sleep(2000); events("explorer click other.md, stored = line 30 range from search (plain reopening)");
  await closeTab();
  // a plain reopening with the stored view state of an empty cursor at line 30 (from Quick Open)
  await s.quickOpen("other.md:35"); events("quickopen other.md:35");
  await closeTab();
  await page.keyboard.press("Control+Shift+E"); await sleep(700);
  await page.locator(".explorer-viewlet .monaco-list-row", { hasText: "other.md" }).first().click(); await sleep(2000); events("explorer click other.md, stored = empty cursor line 35");
  await closeTab();
  await s.close();
})().catch((e) => { console.error(e); process.exit(1); });
