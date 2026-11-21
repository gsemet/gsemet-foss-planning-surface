// Run A, shipped defaults (search on, files off): T1, T9, T4, T8, T12 (side preview), T2 confirmation.
const { launch, sleep, STUDIO } = require("./lib");
(async () => {
  const s = await launch("ta-defaults", { port: 9421 });
  const { page } = s;
  await sleep(6000);
  const clickRow = async (needle) => {
    const rows = page.locator(".search-view .monaco-list-row");
    const n = await rows.count();
    for (let i = 0; i < n; i++) { const l = (await rows.nth(i).getAttribute("aria-label")) || ""; if (l.includes(needle)) { await rows.nth(i).click(); return l; } }
    s.note("  row not found: " + needle); return undefined;
  };
  const explorerOpen = async (file) => { await page.keyboard.press("Control+Shift+E"); await sleep(700); await page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first().click(); await sleep(2000); };
  const studioTabs = (st) => st.tabs.filter((t) => t.kind.startsWith("custom"));
  const textTabs = (st) => st.tabs.filter((t) => t.kind === "text");

  // ---- T1 + T2 confirmation: search click at line 30, with a frame-by-frame flash recorder.
  s.note("T1: search click on doc.md line 30");
  await s.search("zebrafish");
  await page.evaluate(() => {
    window.__flash = []; let last = "";
    const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 20 && r.height > 20; };
    const tick = () => {
      const monaco = [...document.querySelectorAll(".editor-instance .monaco-editor")].some(vis);
      const web = [...document.querySelectorAll("iframe.webview, .webview")].some(vis);
      const cur = `${monaco ? "text" : "-"}/${web ? "webview" : "-"}`;
      if (cur !== last) { window.__flash.push({ t: Math.round(performance.now()), s: cur }); last = cur; }
      requestAnimationFrame(tick);
    }; requestAnimationFrame(tick);
    window.__click = performance.now();
  });
  const clickedAt = await page.evaluate(() => performance.now());
  await clickRow("Line 30 of doc");
  await sleep(6000);
  const flash = await page.evaluate(() => window.__flash);
  s.note("  flash transitions (ms, performance.now; click at " + Math.round(clickedAt) + "): " + JSON.stringify(flash));
  await s.facts("T1 after click");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t1-studio-at-line-30");
  const evs = require("node:fs").readFileSync(s.logF, "utf8").split("\n").filter((l) => l.includes('"tabs"')).slice(-6);
  s.note("  last tab events: " + evs.join(" | ").slice(0, 1500));

  // ---- T4: Studio tab of doc.md active; search click at line 40.
  s.note("T4: Studio tab active, search click line 40");
  await s.search("zebrafish");
  const l4 = await clickRow("Line 40 of doc");
  await sleep(5000);
  await s.facts("T4 after search click line 40");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t4-search-click-line-40");
  s.note("T4b: Quick Open doc.md:40 with the Studio tab active");
  await s.rpc({ op: "exec", command: "workbench.action.focusFirstEditorGroup" });
  await s.quickOpen("doc.md:55"); await sleep(5000);
  await s.facts("T4b after quick open doc.md:55");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t4b-quickopen-line-55");

  // ---- T9: reused preview tab: search click doc.md then other.md
  await s.closeAll();
  s.note("T9: single click on doc.md result then other.md result");
  await s.search("zebrafish");
  await clickRow("Line 30 of doc"); await sleep(4000);
  await s.facts("T9 after doc.md click");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await clickRow("Line 30 of other"); await sleep(4000);
  await s.facts("T9 after other.md click");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t9-after-other");

  // ---- T8: dirty doc.md in a text editor of group 2, search click in group 1
  await s.closeAll();
  s.note("T8: doc.md dirty as text in group 2; search click in group 1");
  await s.rpc({ op: "config", section: "markdownOkfSchemaStudio.open", key: "searchResultsInStudio", value: false });
  await s.rpc({ op: "open", file: s.ws + "/doc.md", col: 2, preview: false }); await sleep(1500);
  await s.rpc({ op: "edit", file: "doc.md" }); await sleep(500);
  await s.rpc({ op: "config", section: "markdownOkfSchemaStudio.open", key: "searchResultsInStudio", value: true });
  await s.rpc({ op: "exec", command: "workbench.action.focusFirstEditorGroup" }); await sleep(500);
  await s.facts("T8 before");
  await s.search("zebrafish");
  await clickRow("Line 30 of doc"); await sleep(5000);
  const t8 = await s.facts("T8 after click");
  s.note("  doc state: " + JSON.stringify(await s.rpc({ op: "doc", file: "doc.md" })));
  s.note("  dialogs: " + t8.d.dialogs);
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t8-dirty-doc");

  // ---- T12 side preview open: defaults, side preview of doc.md, search click line 30
  await s.closeAll();
  s.note("T12 side preview: open doc.md as text, Open Preview to Side, then search click");
  await s.rpc({ op: "exec", command: "workbench.action.files.revert" }).catch(() => {});
  await s.rpc({ op: "open", file: s.ws + "/other.md", col: 1, preview: false }); await sleep(1500);
  await s.palette("Markdown OKF-Schema Studio: Open Preview", undefined); await sleep(4000);
  await s.facts("T12 side preview open");
  await s.rpc({ op: "exec", command: "workbench.action.focusFirstEditorGroup" }); await sleep(500);
  await s.search("zebrafish");
  await clickRow("Line 30 of doc"); await sleep(4000);
  await s.facts("T12 side preview: after search click doc.md line 30 (jump must stay text)");
  await s.snap("t12-side-preview-jump");
  await s.close();
})().catch((e) => { console.error(e); process.exit(1); });
