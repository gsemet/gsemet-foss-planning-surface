// T2b: selection kind and extent of each opening, plain reopening with a non-empty stored selection.
const { launch, sleep, fs } = require("./lib");
(async () => {
  const s = await launch("t02b", { port: 9412, settings: { "markdownOkfSchemaStudio.open.searchResultsInStudio": false, "markdownOkfSchemaStudio.open.markdownFilesInStudio": false } });
  const { page } = s;
  await sleep(5000);
  let mark = 0;
  const events = (label) => {
    const lines = fs.readFileSync(s.logF, "utf8").trim().split("\n");
    const fresh = lines.slice(mark); mark = lines.length;
    s.note(`CASE ${label}`);
    for (const l of fresh) { const o = JSON.parse(l); if (o.ev === "selection" || o.ev === "visible" || (o.ev === "tabs" && o.opened.length)) s.note("  " + JSON.stringify({ t: o.t, ev: o.ev, kind: o.kind, sel: o.sel, eds: o.eds?.map((e) => e.sel), opened: o.opened?.length })); }
  };
  const explorerOpen = async (file) => { await page.keyboard.press("Control+Shift+E"); await sleep(700); await page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first().click(); await sleep(2000); };
  events("startup");
  await s.quickOpen("doc.md:30"); events("quickopen doc.md:30");
  await page.keyboard.press("Shift+End"); await sleep(500); events("select the line (shift+end), a user selection in an open editor");
  await page.keyboard.press("Control+W"); await sleep(1200); events("close");
  await explorerOpen("doc.md"); events("plain reopening with a stored NON-EMPTY selection");
  await page.keyboard.press("Control+W"); await sleep(1200); events("close");
  await s.search("zebrafish");
  await page.locator(".search-view .monaco-list-row").nth(1).click(); await sleep(2000); events("search click, first match doc.md (range 28..35)");
  await page.keyboard.press("Control+W"); await sleep(1200);
  await s.rpc({ op: "open", file: s.ws + "/doc.md", line: 30 }); await sleep(1500); events("vscode.open selection line 30 (stored: select-all line 30)");
  await page.keyboard.press("Control+W"); await sleep(1200);
  // Open from the Problems-like command: workbench.action.gotoLine is in-editor only; use the Explorer double click as a pinned plain open
  await page.locator(".explorer-viewlet .monaco-list-row", { hasText: "other.md" }).first().dblclick(); await sleep(2000); events("explorer double click other.md (never opened)");
  await s.close();
})().catch((e) => { console.error(e); process.exit(1); });
