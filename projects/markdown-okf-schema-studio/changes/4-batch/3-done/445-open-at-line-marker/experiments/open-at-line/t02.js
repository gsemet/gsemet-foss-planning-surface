// T2: does a signal tell a jump from a plain reopening? Pure observation: both settings off, Studio replaces nothing.
const { launch, sleep, fs } = require("./lib");
(async () => {
  const s = await launch("t02", { port: 9411, settings: { "markdownOkfSchemaStudio.open.searchResultsInStudio": false, "markdownOkfSchemaStudio.open.markdownFilesInStudio": false } });
  const { page } = s;
  await sleep(6000);
  let mark = 0;
  const events = (label) => {
    const lines = fs.readFileSync(s.logF, "utf8").trim().split("\n");
    const fresh = lines.slice(mark); mark = lines.length;
    s.note(`CASE ${label}`);
    for (const l of fresh) s.note("  " + l.slice(0, 330));
  };
  const explorerOpen = async (file) => {
    await page.keyboard.press("Control+Shift+E"); await sleep(700);
    await page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first().click(); await sleep(2000);
  };
  events("startup");
  // 1. put the cursor on line 30 via Quick Open doc.md:30, then close the tab
  await s.quickOpen("doc.md:30"); await sleep(1500);
  events("quickopen doc.md:30 (first time, a jump into a never-opened file)");
  await s.facts("after quickopen:30");
  await page.keyboard.press("Control+W"); await sleep(1200);
  events("close doc.md");
  // 2. plain reopening from the Explorer (restored view state)
  await explorerOpen("doc.md"); await sleep(1500);
  events("explorer click doc.md after close with cursor at line 30 (plain reopening, restored view state)");
  await s.facts("after explorer reopen");
  await page.keyboard.press("Control+W"); await sleep(1000);
  events("close");
  // 2b. plain reopening, cursor at 1:1 (other.md never opened)
  await explorerOpen("other.md"); await sleep(1500);
  events("explorer click other.md never opened (plain opening, no state)");
  await page.keyboard.press("Control+W"); await sleep(1000);
  events("close other");
  // 3. Quick Open doc.md:40 on a closed tab (cursor state at 30)
  await s.quickOpen("doc.md:40"); await sleep(1500);
  events("quickopen doc.md:40 (closed tab, stored state at 30)");
  await page.keyboard.press("Control+W"); await sleep(1000);
  events("close");
  // 4. vscode.open with a selection
  await s.rpc({ op: "open", file: s.ws + "/doc.md", line: 50 }); await sleep(1500);
  events("vscode.open selection line 50 (closed tab, stored state at 40)");
  await page.keyboard.press("Control+W"); await sleep(1000);
  events("close");
  // 4b. vscode.open with a selection at line 30 exactly like the stored one? stored 50 -> jump 50 (same line as the restored state)
  await s.rpc({ op: "open", file: s.ws + "/doc.md", line: 50 }); await sleep(1500);
  events("vscode.open selection line 50 again (stored state is already 50)");
  await page.keyboard.press("Control+W"); await sleep(1000);
  events("close");
  // 5. search view click
  await s.search("zebrafish"); await sleep(1000);
  s.note("search rows: " + JSON.stringify(await s.searchRows()));
  events("search ran");
  const rows = page.locator(".search-view .monaco-list-row");
  // expand: rows are [doc.md, match, match, other.md, match]
  const n = await rows.count();
  for (let i = 0; i < n; i++) { const l = (await rows.nth(i).getAttribute("aria-label")) || ""; if (/Found in|match/i.test(l) && /doc\.md/.test(l)) { s.note("clicking row: " + l.slice(0, 100)); } }
  await rows.nth(1).click(); await sleep(2000);
  events("search view click on first match of doc.md (line 30; stored state is 50)");
  await s.facts("after search click");
  await s.snap("search-click");
  await s.close();
})().catch((e) => { console.error(e); process.exit(1); });
