// Verifier evidence 6: a copy of a real planning page in an isolated, real VS Code window (own
// user-data and extensions folders), Studio custom editor, Auto width, driven over CDP only.
// Usage: node e6.js <worktree> <extensionRoot> <label> <shotDir> <port>
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { spawn } = require("node:child_process");

const [worktree, extensionRoot, label, shotDir, port] = process.argv.slice(2);
const { chromium } = require(path.join(worktree, "node_modules/playwright-core"));
const { writeTestProfileSettings, testProfileLaunchArgs } = require(path.join(worktree, "out/test/shared/testProfile"));
const code = path.join(process.env.LOCALAPPDATA, "Programs", "Microsoft VS Code", "Code.exe");
const source = path.resolve(__dirname, "../../../../../2-backlog/P3/comment-failure-messages-and-lost-drafts/01-intent.md");

const base = path.join(__dirname, `e6-${label}`);
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
async function until(what, probe, deadline = 90000) {
  const start = Date.now();
  let last;
  while (Date.now() - start < deadline) {
    try { const value = await probe(); if (value) return value; } catch (error) { last = error; }
    await wait(500);
  }
  throw new Error(`timed out waiting for ${what}: ${last ? last.message : ""}`);
}

async function main() {
  fs.rmSync(base, { recursive: true, force: true });
  const userData = path.join(base, "ud");
  const extensions = path.join(base, "ext");
  const notes = path.join(base, "notes");
  const helper = path.join(base, "helper");
  for (const dir of [userData, extensions, notes, helper]) fs.mkdirSync(dir, { recursive: true });
  writeTestProfileSettings(userData);
  const page01 = path.join(notes, "01-intent.md");
  fs.copyFileSync(source, page01);
  fs.writeFileSync(path.join(helper, "package.json"), JSON.stringify({ name: "open-helper", publisher: "verifier", version: "0.0.1",
    engines: { vscode: "^1.95.0" }, activationEvents: ["onStartupFinished"], main: "./extension.js" }));
  fs.writeFileSync(path.join(helper, "extension.js"), `const vscode = require("vscode");
exports.activate = async () => {
  await vscode.commands.executeCommand("workbench.action.closeSidebar");
  await vscode.commands.executeCommand("workbench.action.closeAuxiliaryBar");
  await vscode.commands.executeCommand("vscode.openWith", vscode.Uri.file(${JSON.stringify(page01)}), "markdown-okf-schema-studio.editor");
};
`);
  const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^(VSCODE_|ELECTRON_)/u.test(k)));
  const child = spawn(code, ["--no-sandbox", "--disable-updates", "--skip-welcome", "--skip-release-notes", "--disable-workspace-trust",
    `--user-data-dir=${userData}`, `--extensions-dir=${extensions}`, `--extensionDevelopmentPath=${extensionRoot}`,
    `--extensionDevelopmentPath=${helper}`, ...testProfileLaunchArgs(), `--remote-debugging-port=${port}`,
    "--remote-debugging-address=127.0.0.1", notes], { stdio: "ignore", env });
  console.log(`[${label}] spawned pid ${child.pid}, profile path length ${userData.length}`);
  let exited = false;
  child.on("exit", (status) => { exited = true; console.log(`[${label}] window exited ${status}`); });
  let browser;
  try {
    browser = await until("the debugging port", () => chromium.connectOverCDP(`http://127.0.0.1:${port}`));
    const workbench = await until("the workbench", () => browser.contexts()[0].pages().find((p) => p.url().includes("workbench")));
    await workbench.locator(".monaco-workbench").waitFor();
    await workbench.setViewportSize({ width: 960, height: 760 });
    const frame = await until("the preview frame", async () => {
      for (const candidate of workbench.frames()) {
        if (await candidate.locator("#sphinx-myst-preview-content pre").count() === 0) continue;
        if (await (await candidate.frameElement()).isVisible()) return candidate;
      }
      return undefined;
    });
    await frame.locator("[data-sphinx-preview-width-toggle]").first().waitFor({ state: "attached" });
    await wait(3000);
    const mode = () => frame.evaluate(() => document.documentElement.getAttribute("data-sphinx-preview-width"));
    console.log(`[${label}] first width mode ${await mode()}`);
    for (let i = 0; i < 3 && (await mode()) !== "auto"; i += 1) {
      await frame.evaluate(() => document.querySelector("[data-sphinx-preview-width-toggle]").click());
      await wait(800);
    }
    await frame.evaluate(async () => {
      await document.fonts.ready;
      window.dispatchEvent(new Event("resize"));
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    });
    await wait(1500);
    const state = await frame.evaluate(() => {
      const content = document.getElementById("sphinx-myst-preview-content");
      const style = getComputedStyle(content);
      const pre = content.querySelector("pre");
      return { mode: document.documentElement.getAttribute("data-sphinx-preview-width"), pane: window.innerWidth,
        column: content.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight),
        topLevel: pre.parentElement === content, box: pre.getBoundingClientRect().width, client: pre.clientWidth, scroll: pre.scrollWidth,
        wide: pre.hasAttribute("data-sphinx-preview-wide"), breakout: pre.style.getPropertyValue("--sphinx-preview-breakout") };
    });
    console.log(`[${label}] ${JSON.stringify(state)}`);
    await workbench.mouse.move(5, 750);
    const element = await frame.frameElement();
    const bounds = await element.boundingBox();
    await workbench.screenshot({ path: path.join(shotDir, `${label}-vscode-auto-planning-page.png`), clip: bounds });
    console.log(`[${label}] screenshot clip ${JSON.stringify(bounds)}`);
  } finally {
    if (browser) {
      try { const session = await browser.newBrowserCDPSession(); await session.send("Browser.close"); } catch (error) { console.log(`[${label}] Browser.close: ${error.message}`); }
      await browser.close().catch(() => undefined);
    }
    for (let i = 0; i < 20 && !exited; i += 1) await wait(500);
    if (!exited) { console.log(`[${label}] ending own window by pid ${child.pid}`); child.kill(); await wait(3000); }
  }
}

main().then(() => process.exit(0), (error) => { console.error(error); process.exit(1); });
