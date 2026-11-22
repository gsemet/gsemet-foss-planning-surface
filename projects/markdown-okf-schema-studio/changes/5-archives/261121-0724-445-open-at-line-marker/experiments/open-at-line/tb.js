// Run B: settings matrix and Studio placement. T12 (off/off, off/on), T13, T10, T3.
const { launch, sleep, STUDIO, fs, path } = require("./lib");
(async () => {
  const s = await launch("tb-matrix", { port: 9431 });
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
  const explorerOpen = async (file) => { await page.keyboard.press("Control+Shift+E"); await sleep(700); await page.locator(".explorer-viewlet .monaco-list-row", { hasText: file }).first().click(); await sleep(3500); };
  const closeAll = async () => { await s.rpc({ op: "exec", command: "workbench.action.closeAllEditors" }); await sleep(800); };
  fs.writeFileSync(path.join(s.ws, "links.md"), "# Links\n\nGo to [the other file heading](other.md#other-file) now.\n\nOr [plain link](other.md).\n");
  await s.rpc({ op: "exec", command: "markdown-okf-schema-studio.showFeatureIntroductionsAgain" }); await sleep(2500);

  // ---- T12: search off, files off
  s.note("T12 search off / files off");
  await set(false, false);
  await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(3500);
  await s.facts("T12 off/off search click doc.md line 30 (expect text, no Studio)");
  await closeAll();
  await explorerOpen("other.md");
  await s.facts("T12 off/off explorer open other.md (expect text)");
  await closeAll();

  // ---- T12: search off, files on
  s.note("T12 search off / files on");
  await set(false, true);
  await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(5000);
  await s.facts("T12 off/on search click doc.md line 30 (expect Studio at line 30)");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await closeAll();
  await explorerOpen("other.md");
  await s.facts("T12 off/on explorer open other.md (expect Studio, top)");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t12-off-on-explorer");
  await closeAll();

  // ---- T13: file shown in Studio in another group
  s.note("T13 files on, search on");
  await set(true, true);
  await s.search("zebrafish"); await clickRow("Line 30 of doc"); await sleep(5000);
  await s.facts("T13 setup: Studio tab of doc.md in group 1");
  await s.rpc({ op: "exec", command: "workbench.action.newGroupRight" }); await sleep(1000);
  await explorerOpen("doc.md");
  await s.facts("T13 plain opening from the Explorer with group 2 focused (expect new Studio tab in group 2, group 1 tab kept, no text tab)");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t13-plain-group2");
  // close the group 2 tab, keep group 2 focused
  await s.rpc({ op: "exec", command: "workbench.action.closeActiveEditor" }); await sleep(1000);
  await s.rpc({ op: "exec", command: "workbench.action.focusSecondEditorGroup" }); await sleep(500);
  await s.facts("T13 before jump (group 2 focused, empty)");
  await s.search("zebrafish"); await clickRow("Line 40 of doc"); await sleep(5000);
  await s.facts("T13 jump to line 40 with group 2 focused (expect group 1 Studio revealed at 40, no new Studio tab, no text tab)");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  await s.snap("t13-jump-group2");
  await closeAll();

  // ---- T10: Studio's own navigation, files on
  s.note("T10 files on: link from a Studio tab");
  await s.rpc({ op: "exec", command: "workbench.action.editorLayoutSingle" }); await sleep(500);
  await explorerOpen("links.md");
  await s.facts("T10 Studio tab of links.md");
  const marks = fs.readFileSync(s.logF, "utf8").split("\n").length;
  for (const fr of await s.studioFrames()) {
    try { const el = await fr.frameElement(); if (!(await el.isVisible())) continue; await fr.locator('a[href*="other.md#"]').first().click(); s.note("  clicked link in the Studio frame"); } catch (e) { s.note("  link click failed " + String(e).slice(0, 120)); }
  }
  await sleep(5000);
  await s.facts("T10 after following a link to other.md#other-file with files on");
  s.note("  marker: " + JSON.stringify(await s.marker()));
  const ev = fs.readFileSync(s.logF, "utf8").split("\n").slice(marks - 1).filter((l) => l.includes('"tabs"') && l.includes('"kind":"text"') && l.includes("other.md"));
  s.note("  text tab events for other.md after the link: " + ev.length);
  await s.snap("t10-link-files-on");
  const nav = await page.evaluate(() => [...document.querySelectorAll("[aria-label]")].map((e) => e.getAttribute("aria-label")).filter((l) => /back|next|forward/i.test(l)).slice(0, 8));
  s.note("  nav labels in workbench dom: " + JSON.stringify(nav));
  for (const fr of await s.studioFrames()) {
    try { const el = await fr.frameElement(); if (!(await el.isVisible())) continue; const labels = await fr.evaluate(() => [...document.querySelectorAll("button, [role=button]")].map((b) => (b.getAttribute("aria-label") || b.title || b.textContent || "").trim()).filter(Boolean).slice(0, 25)); s.note("  frame buttons: " + JSON.stringify(labels)); } catch {}
  }
  await closeAll();

  // ---- T10 files off: link opens a text editor that stays text
  s.note("T10 files off: link from a Studio tab");
  await set(true, false);
  await s.rpc({ op: "openWith", file: s.ws + "/links.md", viewType: STUDIO, col: 1 }); await sleep(4000);
  await s.facts("T10 files off: Studio tab of links.md");
  for (const fr of await s.studioFrames()) {
    try { const el = await fr.frameElement(); if (!(await el.isVisible())) continue; await fr.locator('a[href*="other.md#"]').first().click(); s.note("  clicked link in the Studio frame"); } catch (e) { s.note("  link click failed " + String(e).slice(0, 120)); }
  }
  await sleep(5000);
  await s.facts("T10 files off: after the link (expect a text editor for other.md that stays text)");
  await closeAll();

  // ---- T3: raw text on purpose, files on
  s.note("T3 files on: Open as Text");
  await set(true, true);
  await explorerOpen("doc.md");
  await s.facts("T3 Studio tab of doc.md");
  await s.palette("Markdown OKF-Schema Studio: Open as Text"); await sleep(4000);
  await s.facts("T3 after Open as Text (expect text editor stays text, Studio tab closed)");
  await closeAll();
  s.note("T3b dirty document: Open as Text");
  await explorerOpen("doc.md");
  s.note("  wedit: " + JSON.stringify(await s.rpc({ op: "wedit", file: s.ws + "/doc.md" }))); await sleep(1500);
  await s.facts("T3b Studio tab, document dirty");
  await s.palette("Markdown OKF-Schema Studio: Open as Text"); await sleep(4000);
  const t3b = await s.facts("T3b after Open as Text on a dirty document");
  s.note("  doc state: " + JSON.stringify(await s.rpc({ op: "doc", file: "doc.md" })).slice(0, 120) + " dialogs=" + t3b.d.dialogs);
  await s.snap("t3b-open-as-text-dirty");
  await s.rpc({ op: "exec", command: "workbench.action.files.revert" }); await sleep(800);
  await closeAll();
  s.note("T3c Reopen Editor With > Text Editor from a Studio tab");
  await explorerOpen("other.md");
  await s.facts("T3c Studio tab of other.md");
  await s.palette("View: Reopen Editor With...", "Text Editor"); await sleep(4500);
  await s.facts("T3c after Reopen Editor With > Text Editor (stays text if a signal exists, else replaced: known limit)");
  await closeAll();
  s.note("T3d Open With > Text Editor (vscode.openWith default)");
  await s.rpc({ op: "openWith", file: s.ws + "/other.md", viewType: "default", col: 1 }); await sleep(4500);
  await s.facts("T3d after vscode.openWith default on other.md (files on)");
  await s.close();
})().catch((e) => { console.error(String(e).slice(0, 600)); process.exit(1); });
