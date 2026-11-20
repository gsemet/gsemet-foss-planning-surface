// Exploration probe: Studio in VS Code diff views. Usage: node diffprobe.js <mode: default|assoc> <outDir>
const { chromium } = require("C:/Users/gaeta/Projets/studio-grill-diff-view/node_modules/playwright-core");
const { spawn, execSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const mode = process.argv[2] ?? "default";
const outDir = process.argv[3];
const scratch = __dirname;
const root = path.join(scratch, `run4-${mode}`);
const ws = path.join(root, "ws");
const userData = path.join(root, "user");
const extDir = path.join(root, "ext");
const code = "C:/Users/gaeta/AppData/Local/Programs/Microsoft VS Code/Code.exe";
const extensionRoot = "C:/Users/gaeta/Projets/studio-grill-diff-view";
const port = mode === "default" ? 9347 : 9348;
const log = [];
const note = (s) => { console.log(s); log.push(s); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function setup() {
  fs.rmSync(root, { recursive: true, force: true });
  fs.mkdirSync(ws, { recursive: true });
  fs.mkdirSync(path.join(userData, "User"), { recursive: true });
  const tail = Array.from({ length: 40 }, (_, i) => `\nParagraph ${i + 1} of the long tail, used to test scrolling.\n`).join("");
  const body = (word) => `# Diff probe\n\nThis paragraph mentions Alpha once.\n\n## Section two\n\n- first item\n- second item with Alpha\n\n:::{note}\nA MyST note that says ${word}.\n:::\n\n| Col A | Col B |\n| --- | --- |\n| 1 | 2 |\n` + tail + `\n## Last section\n\nThe very end of the document, ${word}.\n`;
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
    "window.dialogStyle": "custom",
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
    const file = path.join(outDir, `p4-${mode}-${String(shot).padStart(2, "0")}-${name}.png`);
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
  const previewScroll = async () => { const fr = await studioFrame(); return fr ? fr.evaluate(() => Math.round(document.scrollingElement.scrollTop)) : "no frame"; };

  // Q3: a Studio editor open, Replace All from the search view.
  note("CASE studio-open-replace-all");
  await quickOpen("doc.md");
  if (mode === "default") await palette("View: Reopen Editor With...", "Markdown OKF-Schema Studio");
  await settle(5000);
  await page.keyboard.press("Control+Shift+H");
  await sleep(1200);
  await page.keyboard.press("Control+A");
  await page.keyboard.type("Alpha", { delay: 20 });
  await page.locator(".search-view .replace-input textarea, .search-view .replace-input input").first().click();
  await page.keyboard.press("Control+A");
  await page.keyboard.type("Omega", { delay: 20 });
  await sleep(2500);
  const all = page.locator(".search-view .replace-all-button, .search-view [aria-label^='Replace All']").first();
  note(`  replace all buttons: ${await all.count()}`);
  if (await all.count()) await all.click(); else await page.keyboard.press("Control+Alt+Enter");
  await sleep(2000);
  const dlg = page.locator(".monaco-dialog-box");
  note(`  dialog: ${await dlg.count() ? await dlg.innerText() : "none"}`);
  await snap("replace-all-dialog");
  const ok = page.locator(".monaco-dialog-box .dialog-buttons a, .monaco-dialog-box .dialog-buttons .monaco-button").first();
  if (await ok.count()) await ok.click();
  await settle(5000);
  await facts("after replace all");
  await snap("studio-after-replace-all");
  const fr = await studioFrame();
  if (fr) note(`  studio shows Omega: ${await fr.locator("#sphinx-myst-preview-content", { hasText: "Omega" }).count()}, Alpha: ${await fr.locator("#sphinx-myst-preview-content", { hasText: "Alpha" }).count()}`);
  note(`  file on disk has Omega: ${fs.readFileSync(path.join(ws, "doc.md"), "utf8").includes("Omega")}`);
  const dirty = await page.evaluate(() => [...document.querySelectorAll(".tabs-container .tab")].map((t) => t.classList.contains("dirty")));
  note(`  tabs dirty: ${JSON.stringify(dirty)}`);

  fs.writeFileSync(path.join(outDir, `p4-${mode}-log.txt`), log.join("\n") + "\n");
  await browser.close().catch(() => {});
  child.kill();
}

main().catch((e) => { console.error(e); fs.writeFileSync(path.join(outDir, `p4-${mode}-log.txt`), log.join("\n") + "\nERROR " + e.stack + "\n"); process.exit(1); });
