// Records panels 2, 3 and 6 of the storyboard from a real VS Code window with a CDP screencast.
// Writes frames, frames.json and events.json (mouse track, clicks, panel marks, zoom rects).
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { writeFile } from "node:fs/promises";
const require = createRequire(process.env.TRIAL_NODE_ROOT + "/package.json");
const { chromium } = require("playwright-core");
const S = process.env.TRIAL_SCRATCH, PORT = 9344;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const env = { ...process.env };
for (const k of Object.keys(env)) if (/^(VSCODE_|ELECTRON_|__CFBundle)/.test(k)) delete env[k];
const child = spawn("/Applications/Visual Studio Code.app/Contents/MacOS/Code", [
  "--force-device-scale-factor=2", "--disable-updates", "--skip-welcome", "--skip-release-notes", "--disable-workspace-trust", "--new-window",
  `--remote-debugging-port=${PORT}`, "--remote-debugging-address=127.0.0.1",
  `--user-data-dir=${S}/vscode-user`, `--extensions-dir=${S}/vscode-ext`,
  `${S}/demo-workspace`, `${S}/demo-workspace/rollout-plan.md`,
], { stdio: "ignore", env, detached: true });
child.unref();

let browser, page, ctx;
for (let i = 0; i < 40 && !page; i++) {
  try {
    browser = await chromium.connectOverCDP(`http://127.0.0.1:${PORT}`);
    ctx = browser.contexts()[0];
    page = ctx.pages().find((p) => p.url().includes("workbench"));
  } catch { /* the window is still starting */ }
  if (!page) await sleep(1000);
}
if (!page) throw new Error("no workbench page");
await page.waitForSelector(".monaco-workbench .part.editor", { timeout: 60000 });
await sleep(6000);

const snap = async (name) => {
  const cdp = await ctx.newCDPSession(page);
  const r = await cdp.send("Page.captureScreenshot", { format: "png" });
  await writeFile(`${S}/${name}.png`, Buffer.from(r.data, "base64"));
  await cdp.detach();
};
const frameOf = async () => {
  for (let i = 0; i < 60; i++) {
    for (const f of page.frames()) {
      try { if (await f.locator("#sphinx-myst-preview-content").count()) return f; } catch { /* detached */ }
    }
    await sleep(250);
  }
  throw new Error("no preview frame");
};

const events = [];
const now = () => Date.now() / 1000;
const ev = (type, data = {}) => events.push({ t: now(), type, ...data });
let mx = 500, my = 300;
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
async function moveTo(x, y, dur = 0.7) {
  const x0 = mx, y0 = my, steps = Math.round(dur * 60), t0 = now();
  for (let i = 1; i <= steps; i++) {
    const k = ease(i / steps);
    mx = x0 + (x - x0) * k; my = y0 + (y - y0) * k;
    await page.mouse.move(mx, my);
    ev("m", { x: mx, y: my });
    const wait = t0 + (i / steps) * dur - now();
    if (wait > 0) await sleep(wait * 1000);
  }
}
async function click() {
  ev("click", { x: mx, y: my });
  await page.mouse.down(); await sleep(60); await page.mouse.up();
}
const box = async (loc) => { const b = await loc.boundingBox(); if (!b) throw new Error("no box"); return b; };

// The sidebar stays closed; the raw source fills the window.
await page.locator(".part.sidebar").isVisible().then(async (v) => { if (v) { await page.keyboard.press("Meta+b"); await sleep(600); } });
await snap("00-before");

mkdirSync(`${S}/take`, { recursive: true });
rmSync(`${S}/take`, { recursive: true, force: true });
mkdirSync(`${S}/take`, { recursive: true });
const cdp = await ctx.newCDPSession(page);
const size = await page.evaluate(() => [innerWidth, innerHeight, devicePixelRatio]);
const frames = [], pending = [];
let n = 0;
cdp.on("Page.screencastFrame", (e) => {
  const i = ++n;
  frames.push({ n: i, t: e.metadata.timestamp });
  pending.push(writeFile(`${S}/take/f_${String(i).padStart(6, "0")}.jpg`, Buffer.from(e.data, "base64")));
  cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId }).catch(() => {});
});
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: Math.round(size[0] * size[2]), maxHeight: Math.round(size[1] * size[2]), everyNthFrame: 1 });
ev("start");
try {
  ev("panel", { id: 2 });
  await moveTo(size[0] * 0.4, size[1] * 0.45, 0.8);
  await sleep(900);
  const btn = page.locator('.editor-actions a[aria-label*="Preview"]').first();
  const bb = await box(btn);
  await moveTo(bb.x + bb.width / 2, bb.y + bb.height / 2, 0.7);
  ev("panel", { id: 3 });
  await click();
  const f = await frameOf();
  await f.locator(".myst-radio").first().waitFor({ timeout: 15000 });
  await sleep(4200);
  await snap("03-page");

  // Panel 6: bring the question into view on both sides, then click the second option.
  const radio = f.locator(".myst-radio").nth(1);
  await radio.scrollIntoViewIfNeeded();
  const src = await box(page.locator(".editor-instance .monaco-editor").first());
  await page.mouse.move(src.x + 200, src.y + 300);
  await page.mouse.wheel(0, 2000);
  await sleep(900);
  await snap("05-scrolled");
  ev("panel", { id: 6 });
  const rb = await box(radio);
  const ib = await box(f.locator(".myst-radio-item").nth(1));
  const sb = await box(page.locator(".view-line", { hasText: "Behind a flag" }));
  const top = Math.min(sb.y, ib.y) - 50, bottom = Math.max(sb.y + 2 * sb.height, ib.y + ib.height) + 50;
  ev("zoom", { rect: { x: sb.x - 20, y: top, w: ib.x + ib.width * 0.75 - sb.x + 40, h: bottom - top } });
  await moveTo(rb.x + rb.width / 2, rb.y + rb.height / 2, 0.9);
  await sleep(350);
  await click();
  await sleep(250);
  await moveTo(mx + 330, my + 70, 0.5);
  await sleep(1800);
  await snap("06-clicked");
  ev("end");
} finally {
  await cdp.send("Page.stopScreencast").catch(() => {});
  await Promise.all(pending);
  writeFileSync(`${S}/take/frames.json`, JSON.stringify({ size, frames }));
  writeFileSync(`${S}/take/events.json`, JSON.stringify(events));
  await browser.close().catch(() => {});
  try { process.kill(child.pid); } catch { /* already gone */ }
}
console.log("frames", frames.length, "size", size, "secs", frames.at(-1).t - frames[0].t);
