// Trial library (CR-445): drives a real VS Code (Code.exe) from outside over CDP, like experiments 01..04.
const { chromium } = require("C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-445/node_modules/playwright-core");
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");
const RUNS = "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-445/out/trials";
const EXT = "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-445";
const PROBE = path.join(__dirname, "probe-ext");
const CODE = "C:/Users/gaeta/AppData/Local/Programs/Microsoft VS Code/Code.exe";
const EVID = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/445-open-at-line-marker/evidence";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const STUDIO = "markdown-okf-schema-studio.editor";

function fixture(root) {
  const ws = path.join(root, "ws");
  fs.mkdirSync(ws, { recursive: true });
  const lines = ["# Open at line probe", ""];
  for (let i = 3; i <= 80; i++) lines.push(i % 2 ? `Line ${i} of doc: filler text for the paragraph number ${i}.` : "");
  lines[29] = "Line 30 of doc: the needle zebrafish is here.";
  lines[39] = "Line 40 of doc: the second needle zebrafish is here.";
  fs.writeFileSync(path.join(ws, "doc.md"), lines.join("\n") + "\n");
  const other = ["# Other file", ""];
  for (let i = 3; i <= 60; i++) other.push(i % 2 ? `Line ${i} of other: filler.` : "");
  other[29] = "Line 30 of other: the needle zebrafish is here.";
  fs.writeFileSync(path.join(ws, "other.md"), other.join("\n") + "\n");
  fs.writeFileSync(path.join(ws, "plain.txt"), "plain\n");
  return ws;
}

async function launch(name, opts = {}) {
  const { settings = {}, wsSettings, port, ws, noExt = false, root: rootIn } = opts;
  const root = rootIn ?? path.join(RUNS, name);
  if (!rootIn) fs.rmSync(root, { recursive: true, force: true });
  const wsDir = ws ?? (fs.existsSync(path.join(root, "ws")) ? path.join(root, "ws") : fixture(root));
  const userData = path.join(root, "user");
  const extDir = path.join(root, "ext");
  fs.mkdirSync(path.join(userData, "User"), { recursive: true });
  const base = {
    "workbench.startupEditor": "none", "security.workspace.trust.enabled": false, "telemetry.telemetryLevel": "off",
    "update.mode": "none", "extensions.autoUpdate": false, "workbench.tips.enabled": false, "git.enabled": false,
    "chat.disableAIFeatures": true, "window.dialogStyle": "custom", "workbench.secondarySideBar.defaultVisibility": "hidden",
    "window.restoreWindows": "preserve", "workbench.editor.enablePreview": true,
  };
  const sp = path.join(userData, "User", "settings.json");
  if (!rootIn || !fs.existsSync(sp)) fs.writeFileSync(sp, JSON.stringify({ ...base, ...settings }, null, 2));
  if (wsSettings) { fs.mkdirSync(path.join(wsDir, ".vscode"), { recursive: true }); fs.writeFileSync(path.join(wsDir, ".vscode", "settings.json"), JSON.stringify(wsSettings, null, 2)); }
  const cmdF = path.join(root, "probe-cmd.json"), outF = path.join(root, "probe-out.json"), logF = path.join(root, "probe-events.log");
  fs.rmSync(logF, { force: true });
  const p = port ?? 9400 + Math.floor(Math.random() * 400);
  const args = [`--user-data-dir=${userData}`, `--extensions-dir=${extDir}`, `--extensionDevelopmentPath=${PROBE}`];
  if (!noExt) args.push(`--extensionDevelopmentPath=${EXT}`);
  args.push(`--remote-debugging-port=${p}`, "--remote-debugging-address=127.0.0.1", "--disable-workspace-trust", "--skip-welcome", "--skip-release-notes", "--new-window", wsDir);
  const child = spawn(CODE, args, { stdio: "ignore", env: { ...process.env, PROBE_LOG: logF, PROBE_CMD: cmdF, PROBE_OUT: outF } });
  let browser;
  for (let i = 0; i < 60 && !browser; i++) { try { browser = await chromium.connectOverCDP(`http://127.0.0.1:${p}`); } catch { await sleep(1000); } }
  let page;
  for (let i = 0; i < 60 && !page; i++) { page = browser.contexts()[0]?.pages().find((x) => x.url().includes("workbench")); if (!page) await sleep(500); }
  await page.setViewportSize({ width: 1400, height: 860 }).catch(() => {});
  await page.waitForSelector(".monaco-workbench", { timeout: 60000 });
  const s = { root, ws: wsDir, userData, child, browser, page, logF, cmdF, outF, port: p, notes: [], shot: 0, name };
  s.note = (x) => { console.log(x); s.notes.push(x); };
  let id = 0;
  s.rpc = async (c, timeout = 15000) => {
    id++; fs.rmSync(outF, { force: true }); fs.writeFileSync(cmdF, JSON.stringify({ ...c, id }));
    const end = Date.now() + timeout;
    while (Date.now() < end) { if (fs.existsSync(outF)) { try { const o = JSON.parse(fs.readFileSync(outF, "utf8")); if (o.id === id) return o.r; } catch {} } await sleep(50); }
    return "rpc-timeout";
  };
  s.waitProbe = async () => { for (let i = 0; i < 60; i++) { if (fs.existsSync(logF) && fs.readFileSync(logF, "utf8").includes("probe-active")) return; await sleep(500); } };
  await s.waitProbe();
  s.snap = async (label) => { s.shot++; const f = path.join(EVID, `${name}-${String(s.shot).padStart(2, "0")}-${label}.png`); await page.screenshot({ path: f }); s.note(`  screenshot ${path.basename(f)}`); };
  s.state = () => s.rpc({ op: "state" });
  s.dom = () => page.evaluate(() => {
    const tabs = [...document.querySelectorAll(".tabs-container .tab")].map((t) => ((t.getAttribute("aria-label") || t.textContent || "").trim()) + (t.classList.contains("active") ? " [active]" : ""));
    const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 20 && r.height > 20; };
    return { tabs, webviews: [...document.querySelectorAll("iframe.webview, .webview")].filter(vis).length, monaco: [...document.querySelectorAll(".editor-instance .monaco-editor")].filter(vis).length, diff: document.querySelectorAll(".monaco-diff-editor").length, dialogs: document.querySelectorAll(".monaco-dialog-box").length, toasts: [...document.querySelectorAll(".notification-toast .notification-list-item-message")].map((n) => n.textContent.trim()) };
  });
  s.studioFrames = async () => { const out = []; for (const fr of page.frames()) { try { if (await fr.locator("#sphinx-myst-preview-content").count()) out.push(fr); } catch {} } return out; };
  s.marker = async () => {
    for (const fr of await s.studioFrames()) {
      try {
        const el = await fr.frameElement(); if (!(await el.isVisible())) continue;
        return await fr.evaluate(() => { const m = document.querySelector("[data-sphinx-line-marker]"); return { marker: m ? (m.textContent || "").trim().slice(0, 60) : null, attrs: m ? [...m.attributes].map((a) => a.name + "=" + a.value).join(" ").slice(0, 160) : null, scrollTop: Math.round(document.scrollingElement.scrollTop) }; });
      } catch {}
    }
    return "no-visible-studio";
  };
  s.facts = async (label) => {
    const st = await s.state(); const d = await s.dom();
    s.note(`${label}: tabs=${JSON.stringify(st.tabs?.map((t) => `${t.g}:${t.kind}:${t.label}${t.active ? "*" : ""}${t.dirty ? "!" : ""}`))} visibleText=${JSON.stringify(st.visible?.map((e) => e.uri.split("/").pop() + "@" + e.sel))} dom={webviews:${d.webviews},monaco:${d.monaco},diff:${d.diff},dialogs:${d.dialogs},toasts:${JSON.stringify(d.toasts)}}`);
    return { st, d };
  };
  s.palette = async (text, pick) => {
    await page.keyboard.press("Escape"); await page.keyboard.press("F1");
    await page.waitForSelector(".quick-input-widget input", { state: "visible" });
    await page.keyboard.type(text, { delay: 10 }); await sleep(900);
    const choose = async (w) => {
      const labels = await page.evaluate(() => [...document.querySelectorAll(".quick-input-list .monaco-list-row")].map((r) => r.getAttribute("aria-label") ?? ""));
      const idx = labels.findIndex((l) => l.split(",")[0].trim().toLowerCase().startsWith(w.toLowerCase()));
      if (idx < 0) { s.note(`  palette: no row for ${w}: ${JSON.stringify(labels.slice(0, 5))}`); await page.keyboard.press("Escape"); return false; }
      await page.locator(".quick-input-list .monaco-list-row").nth(idx).click(); await sleep(1200); return true;
    };
    if (!(await choose(text))) return false;
    if (pick) { await sleep(500); await page.keyboard.type(pick, { delay: 10 }); await sleep(800); return choose(pick); }
    return true;
  };
  s.quickOpen = async (text) => { await page.keyboard.press("Escape"); await page.keyboard.press("Control+P"); await sleep(500); await page.keyboard.type(text, { delay: 10 }); await sleep(900); await page.keyboard.press("Enter"); await sleep(1500); };
  s.closeAll = async () => { await s.palette("View: Close All Editors"); await sleep(600); };
  s.search = async (term) => { await page.keyboard.press("Escape"); await page.keyboard.press("Control+Shift+F"); await sleep(900); await page.keyboard.press("Control+A"); await page.keyboard.type(term, { delay: 15 }); await page.keyboard.press("Enter"); await sleep(2500); };
  s.searchRows = async () => {
    const rows = page.locator(".search-view .monaco-list-row");
    const cnt = await rows.count(); const info = [];
    for (let i = 0; i < cnt; i++) info.push(((await rows.nth(i).getAttribute("aria-label")) || "").slice(0, 80));
    return info;
  };
  s.close = async () => {
    fs.writeFileSync(path.join(EVID, `${name}.log`), s.notes.join("\n") + "\n");
    try { fs.copyFileSync(logF, path.join(EVID, `${name}-events.log`)); } catch {}
    await browser.close().catch(() => {}); child.kill(); await sleep(1500);
  };
  return s;
}
module.exports = { launch, sleep, fixture, STUDIO, EVID, RUNS, fs, path };
