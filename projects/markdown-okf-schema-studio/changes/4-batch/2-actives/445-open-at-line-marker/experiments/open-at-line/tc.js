// Run C: T3 (Reopen Editor With, Open With), T4 variants (preview and pinned Studio tab), rule 5 signal.
const { launch, sleep, STUDIO, fs, path } = require("./lib");
(async () => {
  const s = await launch("tc-reopen", { port: 9441 });
  try {
    const { page } = s;
    await sleep(6000);
    const OPEN = "markdownOkfSchemaStudio.open";
    const set = async (search, files) => {
      await s.rpc({ op: "config", section: OPEN, key: "searchResultsInStudio", value: search });
      await s.rpc({ op: "config", section: OPEN, key: "markdownFilesInStudio", value: files });
      await sleep(500);
    };
    const clickRow = async (needle) => {
      const rows = page.locator(".search-view .monaco-list-row");
      const n = await rows.count();
      for (let i = 0; i < n; i++) { const l = (await rows.nth(i).getAttribute("aria-label")) || ""; if (l.includes(needle)) { await page.mouse.move(900, 500); await sleep(300); await rows.nth(i).click({ force: true }); return l; } }
      s.note("  row not found: " + needle); return undefined;
    };
    const explorerOpen = async (file, dbl = false) => {
      await page.keyboard.press("Control+Shift+E"); await sleep(700); await page.mouse.move(900, 500); await sleep(300);
      const row = page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first();
      if (dbl) await row.dblclick({ force: true }); else await row.click({ force: true });
      await sleep(3500);
    };
    let mark = 0;
    const events = (label) => {
      const lines = fs.readFileSync(s.logF, "utf8").trim().split("\n");
      const fresh = lines.slice(mark); mark = lines.length;
      const out = [];
      for (const l of fresh) { const o = JSON.parse(l); if (o.ev === "tabs" && (o.opened.length || o.closed.length)) out.push(`${o.t} tabs opened=${JSON.stringify(o.opened.map((t) => [t.kind.slice(0, 8), t.label, t.g, t.preview ? "preview" : "pinned"]))} closed=${JSON.stringify(o.closed.map((t) => [t.kind.slice(0, 8), t.label, t.g, t.preview ? "preview" : "pinned"]))}`); else if (o.ev === "selection") out.push(`${o.t} selection kind=${o.kind} ${JSON.stringify(o.sel)}`); }
      s.note(`EVENTS ${label}\n    ` + out.join("\n    "));
    };
    const closeAll = async () => { await s.rpc({ op: "exec", command: "workbench.action.closeAllEditors" }); await sleep(800); };
    await s.rpc({ op: "exec", command: "markdown-okf-schema-studio.showFeatureIntroductionsAgain" }); await sleep(2500);
    events("setup");

    // T3c: Reopen Editor With > Text Editor from a Studio tab, files on
    s.note("T3c files on");
    await set(true, true);
    await explorerOpen("other.md");
    await s.facts("T3c Studio tab of other.md (preview tab)");
    events("T3c open");
    await s.palette("View: Reopen Editor With...", "Text Editor"); await sleep(4500);
    await s.facts("T3c after Reopen Editor With > Text Editor");
    events("T3c reopen as text");
    await closeAll();

    // T3d: Open With > Text Editor
    s.note("T3d files on: vscode.openWith default");
    await s.rpc({ op: "openWith", file: s.ws + "/other.md", viewType: "default", col: 1 }); await sleep(4500);
    await s.facts("T3d after openWith default");
    events("T3d openWith default");
    await closeAll();

    // T3c2: Reopen Editor With > Text Editor, files OFF (control)
    s.note("T3c2 files off, Reopen Editor With");
    await set(true, false);
    await s.rpc({ op: "openWith", file: s.ws + "/other.md", viewType: STUDIO, col: 1 }); await sleep(3500);
    await s.palette("View: Reopen Editor With...", "Text Editor"); await sleep(3500);
    await s.facts("T3c2 files off after Reopen as Text");
    events("T3c2");
    await closeAll();

    // T4 variants: a Studio tab (preview) then a search click on it; then pinned.
    s.note("T4 variants, files off, search on");
    await set(true, false);
    await s.rpc({ op: "openWith", file: s.ws + "/doc.md", viewType: STUDIO, col: 1 }); await sleep(4000);
    events("T4 pinned Studio tab opened by openWith");
    await s.facts("T4 pinned Studio tab of doc.md");
    await s.search("zebrafish"); await clickRow("Line 40 of doc"); await sleep(5000);
    await s.facts("T4 pinned: search click line 40");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    events("T4 pinned search click");
    await s.rpc({ op: "exec", command: "workbench.action.focusFirstEditorGroup" });
    await s.quickOpen("doc.md:55"); await sleep(5000);
    await s.facts("T4 pinned: Quick Open doc.md:55");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    events("T4 pinned quick open");
    await closeAll();
    s.note("T4 preview Studio tab: created by a jump");
    await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(5000);
    await s.facts("T4 preview Studio tab of doc.md (search click at 30)");
    events("T4 preview search 30");
    await s.search("zebrafish"); await clickRow("Line 40 of doc"); await sleep(5000);
    await s.facts("T4 preview: second search click line 40");
    s.note("  marker: " + JSON.stringify(await s.marker()));
    events("T4 preview search 40");
    await s.snap("t4-preview-second-click");
  } finally {
    await s.close();
  }
})().catch((e) => { console.error(String(e).slice(0, 600)); process.exit(1); });
