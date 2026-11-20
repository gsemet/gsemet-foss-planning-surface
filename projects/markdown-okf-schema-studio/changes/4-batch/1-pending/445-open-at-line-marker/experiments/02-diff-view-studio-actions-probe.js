// Exploration probe: Studio in VS Code diff views. Usage: node diffprobe.js <mode: default|assoc> <outDir>
const { chromium } = require("C:/Users/gaeta/Projets/studio-grill-diff-view/node_modules/playwright-core");
const { spawn, execSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const mode = process.argv[2] ?? "default";
const outDir = process.argv[3];
const scratch = __dirname;
const root = path.join(scratch, `run2-${mode}`);
const ws = path.join(root, "ws");
const userData = path.join(root, "user");
const extDir = path.join(root, "ext");
const code = "C:/Users/gaeta/AppData/Local/Programs/Microsoft VS Code/Code.exe";
const extensionRoot = "C:/Users/gaeta/Projets/studio-grill-diff-view";
const port = mode === "default" ? 9343 : 9344;
const log = [];
const note = (s) => { console.log(s); log.push(s); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function setup() {
  fs.rmSync(root, { recursive: true, force: true });
  fs.mkdirSync(ws, { recursive: true });
  fs.mkdirSync(path.join(userData, "User"), { recursive: true });
  const body = (word) => `# Diff probe\n\nThis paragraph mentions Alpha once.\n\n## Section two\n\n- first item\n- second item with Alpha\n\n:::{note}\nA MyST note that says ${word}.\n:::\n\n| Col A | Col B |\n| --- | --- |\n| 1 | 2 |\n`;
  fs.writeFileSync(path.join(ws, "doc.md"), body("hello"));
  fs.writeFileSync(path.join(ws, "other.md"), "# Other file\n\nAnother document.\n");
  execSync("git init -q && git add . && git -c user.name=p -c user.email=p@example.invalid commit -qm init", { cwd: ws });
  fs.writeFileSync(path.join(ws, "doc.md"), body("hello, changed in the working tree").replace("## Section two", "## Section two (edited)"));
  const settings = {
    "workbench.startupEditor": "none",
    "security.workspace.trust.enabled": false,
    "telemetry.telemetryLevel": "off",
    "update.mode": "none",
    "extensions.autoUpdate": false,
    "workbench.tips.enabled": false,
    "git.enabled": true,
    "window.restoreWindows": "none",
    "chat.disableAIFeatures": true,
    "workbench.secondarySideBar.defaultVisibility": "hidden",
  };
  if (mode === "assoc") settings["workbench.editorAssociations"] = { "*.md": "markdown-okf-schema-studio.editor" };
  fs.writeFileSync(path.join(userData, "User", "settings.json"), JSON.stringify(settings, null, 2));
}

async function main() {
  setup();
  fs.mkdirSync(outDir, { recursive: true });
  const child = spawn(code, [
    `--user-data-dir=${userData}`, `--extensions-dir=${extDir}`, `--extensionDevelopmentPath=${extensionRoot}`,
    `--remote-debugging-port=${port}`, "--remote-debugging-address=127.0.0.1", "--disable-workspace-trust",
    "--skip-welcome", "--skip-release-notes", "--new-window", ws,
  ], { stdio: "ignore", detached: false });
  let browser;
  for (let i = 0; i < 60 && !browser; i++) {
    try { browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`); } catch { await sleep(1000); }
  }
  let page;
  for (let i = 0; i < 60 && !page; i++) {
    page = browser.contexts()[0]?.pages().find((p) => p.url().includes("workbench"));
    if (!page) await sleep(500);
  }
  await page.setViewportSize({ width: 1400, height: 860 }).catch(() => {});
  await page.waitForSelector(".monaco-workbench", { timeout: 60000 });
  await sleep(6000);
  let shot = 0;
  const snap = async (name) => {
    shot++;
    const file = path.join(outDir, `p2-${mode}-${String(shot).padStart(2, "0")}-${name}.png`);
    await page.screenshot({ path: file });
    note(`  screenshot ${path.basename(file)}`);
  };
  const facts = async (label) => {
    const f = await page.evaluate(() => {
      const tabs = [...document.querySelectorAll(".tabs-container .tab")].map((t) => (t.getAttribute("aria-label") || t.textContent || "").trim() + (t.classList.contains("active") ? " [active]" : ""));
      const visibleWebviews = [...document.querySelectorAll("iframe.webview, .webview")].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 20 && r.height > 20; }).length;
      return {
        tabs,
        diffEditors: document.querySelectorAll(".monaco-diff-editor").length,
        textEditors: [...document.querySelectorAll(".editor-instance .monaco-editor")].filter((e) => e.getBoundingClientRect().width > 20).length,
        visibleWebviews,
        sideBySideDivider: document.querySelectorAll(".side-by-side-editor, .editor-instance.side-by-side").length,
        notifications: [...document.querySelectorAll(".notification-list-item-message")].map((n) => n.textContent.trim()),
      };
    });
    note(`${label}: ${JSON.stringify(f)}`);
  };
  const chooseRow = async (wanted) => {
    const labels = await page.evaluate(() => [...document.querySelectorAll(".quick-input-list .monaco-list-row")].map((r) => r.getAttribute("aria-label") ?? ""));
    const idx = labels.findIndex((l) => l.split(",")[0].trim().toLowerCase().startsWith(wanted.toLowerCase()));
    note(`  rows for "${wanted}": ${JSON.stringify(labels.slice(0, 6))} -> index ${idx}`);
    if (idx < 0) { await page.keyboard.press("Escape"); return false; }
    const row = page.locator(".quick-input-list .monaco-list-row").nth(idx);
    await row.click();
    await sleep(1500);
    return true;
  };
  const palette = async (text, pick) => {
    await page.keyboard.press("Escape");
    await page.keyboard.press("F1");
    await page.waitForSelector(".quick-input-widget input", { state: "visible" });
    await page.keyboard.type(text, { delay: 10 });
    await sleep(1000);
    if (!(await chooseRow(text))) return;
    if (pick) {
      await sleep(500);
      await page.keyboard.type(pick, { delay: 10 });
      await sleep(900);
      await chooseRow(pick);
    }
  };
  const quickOpen = async (file) => {
    await page.keyboard.press("Escape");
    await page.keyboard.press("Control+P");
    await sleep(500);
    await page.keyboard.type(file, { delay: 10 });
    await sleep(900);
    await page.keyboard.press("Enter");
    await sleep(2500);
  };
  const closeAll = async () => { await palette("View: Close All Editors"); await sleep(800); };
  const settle = (ms = 3500) => sleep(ms);

  const studioFrame = async () => {
    for (const fr of page.frames()) {
      try { if (await fr.locator("#sphinx-myst-preview-content").count()) { const el = await fr.frameElement(); if (await el.isVisible()) return fr; } } catch {}
    }
    return undefined;
  };
  const titleActions = async () => page.evaluate(() => [...document.querySelectorAll(".editor-group-container.active .editor-actions .action-label")].map((a) => a.getAttribute("aria-label") || a.title).filter(Boolean));

  // P1: a Studio editor is active: which title actions exist, and does the Git "Open Changes" one open a diff?
  note("CASE studio-editor-title-open-changes");
  await quickOpen("doc.md");
  if (mode === "default") await palette("View: Reopen Editor With...", "Markdown OKF-Schema Studio");
  await settle(5000);
  note(`  title actions: ${JSON.stringify(await titleActions())}`);
  const openChanges = page.locator(".editor-group-container.active .editor-actions .action-label[aria-label^='Open Changes']").first();
  if (await openChanges.count()) { await openChanges.click(); await settle(4000); } else note("  no Open Changes title action");
  await facts("after title Open Changes");
  await snap("studio-title-open-changes");
  await closeAll();

  // P2: Source Control view: click the changed file.
  note("CASE scm-click");
  await palette("View: Show Source Control");
  await sleep(2500);
  const scmRow = page.locator(".scm-view .monaco-list-row", { hasText: "doc.md" }).first();
  note(`  scm rows with doc.md: ${await page.locator(".scm-view .monaco-list-row", { hasText: "doc.md" }).count()}`);
  if (await scmRow.count()) { await scmRow.click(); await settle(4000); }
  await facts("after SCM click");
  await snap("scm-click");
  await closeAll();

  // P3: Studio editor made dirty by an edit inside Studio, then Compare with Saved, then Git: Open Changes.
  note("CASE studio-dirty-compare-saved");
  await quickOpen("doc.md");
  if (mode === "default") await palette("View: Reopen Editor With...", "Markdown OKF-Schema Studio");
  await settle(5000);
  let fr = await studioFrame();
  note(`  studio frame: ${fr ? "yes" : "no"}`);
  if (fr) {
    const para = fr.locator("#sphinx-myst-preview-content p", { hasText: "This paragraph mentions" }).first();
    await para.dblclick().catch((e) => note("  dblclick failed " + e.message));
    await sleep(1500);
    await page.keyboard.press("End");
    await page.keyboard.type(" Typed in Studio.", { delay: 20 });
    await sleep(800);
    await page.keyboard.press("Control+Enter");
    await sleep(2000);
  }
  await facts("studio after edit");
  await snap("studio-dirty");
  await palette("File: Compare Active File with Saved");
  await settle(4000);
  await facts("studio dirty -> compare with saved");
  await snap("studio-dirty-compare-saved");
  await palette("File: Revert File");
  await closeAll();

  // P4: no side preview; a git diff is active; run Open Preview to Side.
  note("CASE open-preview-from-git-diff");
  await quickOpen("doc.md");
  if (mode === "assoc") await palette("View: Reopen Editor With...", "Text Editor");
  await palette("Git: Open Changes");
  await settle(3500);
  await palette("Markdown OKF-Schema Studio: Open Preview to Side");
  await settle(5000);
  await facts("open preview from git diff");
  await snap("open-preview-from-git-diff");
  // Scroll the diff to the end: does the side preview follow?
  const diffModified = page.locator(".monaco-diff-editor .editor.modified .view-lines").first();
  if (await diffModified.count()) {
    await diffModified.click();
    await page.keyboard.press("Control+End");
    await settle(2500);
  }
  await facts("git diff scrolled to end");
  await snap("git-diff-scrolled-end");
  await closeAll();

  // P5: no side preview; the replace preview diff is active; run Open Preview to Side.
  note("CASE open-preview-from-replace-preview");
  await page.keyboard.press("Escape");
  await page.keyboard.press("Control+Shift+H");
  await sleep(1200);
  await page.keyboard.type("Alpha", { delay: 20 });
  const replaceBox = page.locator(".search-view .replace-input textarea, .search-view .replace-input input").first();
  await replaceBox.click();
  await page.keyboard.press("Control+A");
  await page.keyboard.type("Omega", { delay: 20 });
  await sleep(2500);
  const match = page.locator(".search-view .monaco-list-row .search-match, .search-view .monaco-list-row .match").first();
  if (await match.count()) await match.click();
  await settle(4000);
  const modified = page.locator(".monaco-diff-editor .editor.modified .view-lines").first();
  if (await modified.count()) await modified.click();
  await palette("Markdown OKF-Schema Studio: Open Preview to Side");
  await settle(5000);
  await facts("open preview from replace preview");
  await snap("open-preview-from-replace-preview");
  await closeAll();

  // P6: a Studio editor stays open beside the search; Replace All; does Studio show the new text?
  note("CASE studio-open-replace-all");
  await quickOpen("doc.md");
  if (mode === "default") await palette("View: Reopen Editor With...", "Markdown OKF-Schema Studio");
  await settle(5000);
  await page.keyboard.press("Control+Shift+H");
  await sleep(1200);
  await page.locator(".search-view .replace-input textarea, .search-view .replace-input input").first().click();
  await page.keyboard.press("Control+A");
  await page.keyboard.type("Omega", { delay: 20 });
  await sleep(1500);
  await page.keyboard.press("Control+Alt+Enter");
  await sleep(2500);
  await facts("after replace all");
  await snap("studio-after-replace-all");
  fr = await studioFrame();
  if (fr) note(`  studio text has Omega: ${await fr.locator("#sphinx-myst-preview-content", { hasText: "Omega" }).count()}`);
  await palette("File: Revert File");
  await closeAll();

  // P7: Timeline view: click the commit entry of doc.md.
  note("CASE timeline");
  await quickOpen("doc.md");
  if (mode === "assoc") await palette("View: Reopen Editor With...", "Text Editor");
  await palette("Explorer: Focus on Timeline View");
  await sleep(3000);
  const tl = page.locator(".timeline-tree-view .monaco-list-row, .pane-body.timeline .monaco-list-row").first();
  note(`  timeline rows: ${await page.locator(".timeline-tree-view .monaco-list-row, .pane-body.timeline .monaco-list-row").count()}`);
  if (await tl.count()) { await tl.click(); await settle(4000); }
  await facts("after timeline click");
  await snap("timeline");
  await closeAll();

  fs.writeFileSync(path.join(outDir, `p2-${mode}-log.txt`), log.join("\n") + "\n");
  await browser.close().catch(() => {});
  child.kill();
}

main().catch((e) => { console.error(e); fs.writeFileSync(path.join(outDir, `p2-${mode}-log.txt`), log.join("\n") + "\nERROR " + e.stack + "\n"); process.exit(1); });
