// Run D: T13 jump after the rule 5 fix, T4 preview tab, T10 links.
const { launch, sleep, STUDIO, fs, path } = require("./lib");
(async () => {
  const s = await launch("td-rerun", { port: 9451 });
  try {
    const { page } = s;
    await sleep(6000);
    const OPEN = "markdownOkfSchemaStudio.open";
    const set = async (a, b) => { await s.rpc({ op: "config", section: OPEN, key: "searchResultsInStudio", value: a }); await s.rpc({ op: "config", section: OPEN, key: "markdownFilesInStudio", value: b }); await sleep(500); };
    const clickRow = async (needle) => { const rows = page.locator(".search-view .monaco-list-row"); const n = await rows.count(); for (let i = 0; i < n; i++) { const l = (await rows.nth(i).getAttribute("aria-label")) || ""; if (l.includes(needle)) { await page.mouse.move(900, 500); await sleep(300); await rows.nth(i).click({ force: true }); return l; } } s.note("  row not found " + needle); };
    const explorerOpen = async (file) => { await page.keyboard.press("Control+Shift+E"); await sleep(700); await page.mouse.move(900, 500); await sleep(300); await page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first().click({ force: true }); await sleep(3500); };
    const closeAll = async () => { await s.rpc({ op: "exec", command: "workbench.action.closeAllEditors" }); await sleep(800); };
    fs.writeFileSync(path.join(s.ws, "links.md"), "# Links\n\nGo to [the other file heading](other.md#other-file) now.\n\nOr [plain link](other.md).\n");
    await s.rpc({ op: "exec", command: "markdown-okf-schema-studio.showFeatureIntroductionsAgain" }); await sleep(2500);
    await set(true, true);
    s.note("T13 files on");
    await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(5000);
    await s.facts("T13 setup Studio tab doc.md group 1");
    await s.rpc({ op: "exec", command: "workbench.action.newGroupRight" }); await sleep(1000);
    await s.rpc({ op: "exec", command: "workbench.action.focusSecondEditorGroup" }); await sleep(500);
    await s.search("zebrafish"); await clickRow("Line 40 of doc"); await sleep(5000);
    await s.facts("T13 jump to 40 with group 2 focused (expect group 1 Studio revealed, no new tab, no text tab)");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    await closeAll();
    await s.rpc({ op: "exec", command: "workbench.action.editorLayoutSingle" }); await sleep(500);
    s.note("T4 preview tab, files off");
    await set(true, false);
    await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(5000);
    await s.facts("T4 preview Studio tab at 30");
    await s.search("zebrafish"); await clickRow("Line 40 of doc"); await sleep(5000);
    await s.facts("T4 second click line 40 on the preview Studio tab");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    await closeAll();
    s.note("T10 files on: link");
    await set(true, true);
    await explorerOpen("links.md");
    await s.facts("T10 Studio tab links.md");
    for (const fr of await s.studioFrames()) {
      try { const el = await fr.frameElement(); if (!(await el.isVisible())) continue; const hrefs = await fr.evaluate(() => [...document.querySelectorAll("a")].map((a) => a.getAttribute("href"))); s.note("  anchors: " + JSON.stringify(hrefs)); await fr.locator("a", { hasText: "the other file heading" }).first().click(); s.note("  clicked"); } catch (e) { s.note("  link click failed " + String(e).slice(0, 150)); }
    }
    await sleep(5000);
    await s.facts("T10 after link with files on (expect Studio of other.md, no text tab)");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    await s.snap("t10-link-files-on");
  } finally { await s.close(); }
})().catch((e) => { console.error(String(e).slice(0, 600)); process.exit(1); });
