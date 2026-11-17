// Records the panels of the 40-second storyboard from a real VS Code window with a CDP screencast.
// Writes frames, frames.json and events.json (mouse track, clicks, panel marks, zoom rects).
import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { writeFile } from "node:fs/promises";
const require = createRequire(process.env.TRIAL_NODE_ROOT + "/package.json");
const { chromium } = require("playwright-core");
const S = process.env.TRIAL_SCRATCH, PORT = 9344, DOC = "checkout-outage.md";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const env = { ...process.env };
for (const k of Object.keys(env)) if (/^(VSCODE_|ELECTRON_|__CFBundle)/.test(k)) delete env[k];
const child = spawn("/Applications/Visual Studio Code.app/Contents/MacOS/Code", [
  "--force-device-scale-factor=2", "--disable-updates", "--skip-welcome", "--skip-release-notes", "--disable-workspace-trust", "--new-window",
  `--remote-debugging-port=${PORT}`, "--remote-debugging-address=127.0.0.1",
  `--user-data-dir=${S}/vscode-user`, `--extensions-dir=${S}/vscode-ext`,
  `${S}/demo-workspace`, `${S}/demo-workspace/${DOC}`,
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

mkdirSync(`${S}/shots`, { recursive: true });
const snap = async (name) => {
  const c = await ctx.newCDPSession(page);
  const r = await c.send("Page.captureScreenshot", { format: "png" });
  await writeFile(`${S}/shots/${name}.png`, Buffer.from(r.data, "base64"));
  await c.detach();
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
const panel = (id) => { console.log("panel", id); ev("panel", { id }); };
const close = () => ev("close");
const mark = (id, rect) => ev("mark", { id, rect });
const zoom = (id, rect) => ev("zoom", { id, rect });
let mx = 900, my = 420;
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
const box = async (loc) => { const b = await loc.boundingBox(); if (!b) throw new Error("no box " + loc); return b; };
const clickLoc = async (loc, dur = 0.7) => { const b = await box(loc); await moveTo(b.x + b.width / 2, b.y + b.height / 2, dur); await click(); return b; };
const union = (a, b, pad = 24) => {
  const x = Math.min(a.x, b.x) - pad, y = Math.min(a.y, b.y) - pad;
  return { x, y, w: Math.max(a.x + a.width, b.x + b.width) + pad - x, h: Math.max(a.y + a.height, b.y + b.height) + pad - y };
};
// The rectangle of a text inside an element, in the coordinates of its own document.
const textIn = (loc, text) => loc.evaluate((el, wanted) => {
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  for (let t = w.nextNode(); t; t = w.nextNode()) {
    const i = t.data.replaceAll("\u00a0", " ").indexOf(wanted);
    if (i >= 0) { const g = document.createRange(); g.setStart(t, i); g.setEnd(t, i + wanted.length); const b = g.getBoundingClientRect(); return { x: b.x, y: b.y, width: b.width, height: b.height }; }
  }
  throw new Error("no text " + wanted);
}, text);
const grow = (r, by = 5) => ({ x: r.x - by, y: r.y - by, w: r.width + 2 * by, h: r.height + 2 * by });
const shift = (r, o) => ({ ...r, x: r.x + o.x, y: r.y + o.y });
// Wheels the pane under the cursor by dy, with an eased speed, in dur seconds.
async function wheel(dy, dur) {
  const steps = Math.max(2, Math.round(dur * 40)), t0 = now();
  let done = 0;
  for (let i = 1; i <= steps; i++) {
    const target = dy * (0.5 - 0.5 * Math.cos(Math.PI * i / steps));
    const d = Math.round(target - done);
    if (d) { await page.mouse.wheel(0, d); done += d; }
    const wait = t0 + (i / steps) * dur - now();
    if (wait > 0) await sleep(wait * 1000);
  }
}
// Brings loc to the given height of the window.
const scrollTo = async (loc, top, dur) => { const b = await box(loc); await wheel(b.y - top, dur); };

// Maximises or restores the preview group; the tab click gives the group the focus the key needs.
async function pageFills(full, f) {
  for (let i = 0; i < 5; i++) {
    const w = (await (await f.frameElement()).boundingBox()).width;
    if ((w > W * 0.8) === full) return;
    await page.locator(".tab", { hasText: "Studio" }).first().click();
    await sleep(300);
    await page.keyboard.press("Control+Alt+m");
    await sleep(1200);
  }
  throw new Error("the preview group did not change size");
}

await page.locator(".part.sidebar").isVisible().then(async (v) => { if (v) { await page.keyboard.press("Meta+b"); await sleep(600); } });

rmSync(`${S}/take`, { recursive: true, force: true });
mkdirSync(`${S}/take`, { recursive: true });
const cdp = await ctx.newCDPSession(page);
const size = await page.evaluate(() => [innerWidth, innerHeight, devicePixelRatio]);
const [W, H] = size;
console.log("size", size);
const frames = [], pending = [];
let n = 0;
cdp.on("Page.screencastFrame", (e) => {
  const i = ++n;
  frames.push({ n: i, t: e.metadata.timestamp });
  pending.push(writeFile(`${S}/take/f_${String(i).padStart(6, "0")}.jpg`, Buffer.from(e.data, "base64")));
  cdp.send("Page.screencastFrameAck", { sessionId: e.sessionId }).catch(() => {});
});
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 90, maxWidth: Math.round(W * size[2]), maxHeight: Math.round(H * size[2]), everyNthFrame: 1 });
ev("start");
try {
  // Panel 2: the raw Markdown in the built-in text editor, alone in the window.
  await page.locator(".editor-instance .monaco-editor").first().click({ position: { x: 300, y: 200 } });
  await moveTo(W * 0.6, H * 0.5, 0.3);
  panel(2);
  await sleep(600);
  for (let i = 0; i < 16; i++) { await page.keyboard.press("Control+PageDown"); await sleep(190); }
  await sleep(300);
  close();
  await page.keyboard.press("Meta+ArrowUp");
  await sleep(600);

  // Panel 3: the switch to the extension, beside the same text.
  panel(3);
  await sleep(200);
  await clickLoc(page.locator('.editor-actions a[aria-label*="Preview"]').first(), 0.9);
  let f = await frameOf();
  await f.locator(".myst-radio").first().waitFor({ timeout: 15000 });
  await moveTo(W * 0.74, H * 0.55, 0.6);
  await sleep(2300);
  await snap("03-switch");
  close();

  // The page takes the whole window for the reading panels.
  await pageFills(true, f);
  await moveTo(W * 0.9, H * 0.5, 0.2);
  await wheel(-6000, 0.3);
  await sleep(500);
  const more = f.locator('[data-sphinx-preview-toolbar] button[title="Show view controls"]');
  const widthButton = f.locator("[data-sphinx-preview-width-toggle]");
  await snap("04-full");

  // Panel 4: the top of the page.
  panel(4);
  await sleep(500);
  await wheel(90, 2.4);
  await sleep(300);

  // Panel 5: slow scroll to the wide table, cramped in the column, then Auto lets it out.
  panel(5);
  await scrollTo(f.locator("h2", { hasText: "Impact by service" }), 110, 1.7);
  await sleep(300);
  await snap("05-margin");
  await clickLoc(more, 0.6);
  await sleep(350);
  await clickLoc(widthButton, 0.4);
  await sleep(350);
  const less = f.locator('[data-sphinx-preview-toolbar] button[title="Hide view controls"]');
  if (await less.count()) await clickLoc(less, 0.35);
  await f.evaluate(() => document.activeElement?.blur());
  await moveTo(W * 0.5, H * 0.8, 0.5);
  await sleep(1500);
  await snap("05-auto");

  // Panel 6: the sequence diagram.
  panel(6);
  await scrollTo(f.locator("h2", { hasText: "Timeline" }), 120, 1.6);
  await sleep(500);
  await wheel(230, 1.3);
  await sleep(500);
  await snap("06-sequence");

  // Panel 7: the chart.
  panel(7);
  await scrollTo(f.locator("h2", { hasText: "Error rate" }), 150, 1.3);
  zoom(7, union(await box(f.locator("h2", { hasText: "Error rate" })), await box(f.locator(".myst-vega-figure, .vega-embed").first()), 30));
  await sleep(1700);
  await snap("07-chart");

  // Panel 8: the code block.
  panel(8);
  await scrollTo(f.locator("h2", { hasText: "Root cause" }), 150, 1.1);
  zoom(8, union(await box(f.locator("p", { hasText: "retried at once" }).first()), await box(f.locator("pre").first()), 30));
  await sleep(1400);
  await snap("08-code");
  close();

  // Back beside the source for comment, edit and answer.
  await pageFills(false, f);
  const para = f.locator("p", { hasText: "retried at once" }).first();
  await moveTo(W * 0.75, H * 0.6, 0.2);
  await scrollTo(para, 200, 0.4);
  await sleep(900);
  await snap("09-beside");

  const feBox = await (await f.frameElement()).boundingBox();
  const fe0 = () => feBox;

  // Panel 9: select a phrase, open a thread, type.
  panel(9);
  { const b = await box(para); zoom(9, { x: feBox.x + 4, y: b.y - 70, w: W - feBox.x - 4, h: 330 }); }
  const r0 = await textIn(para, "retried at once"), r = { x: r0.x, y: r0.y, w: r0.width, h: r0.height };
  const fe = await (await f.frameElement()).boundingBox();
  await moveTo(fe.x + r.x, fe.y + r.y + r.h / 2, 0.6);
  await page.mouse.down();
  await moveTo(fe.x + r.x + r.w, fe.y + r.y + r.h / 2, 0.5);
  await page.mouse.up();
  await sleep(300);
  await snap("09-selected");
  const create = f.locator("[data-okf-comment-create]");
  await create.waitFor({ state: "visible", timeout: 5000 });
  await clickLoc(create, 0.4);
  await sleep(300);
  await page.keyboard.type("Did the mobile app retry too?", { delay: 28 });
  await sleep(350);
  await snap("09-typed");
  await page.keyboard.press("Meta+Enter");
  await sleep(700);
  await clickLoc(f.locator("mark[data-okf-comment-thread]").first(), 0.4);
  await sleep(1500);
  await snap("09-comment");
  close();
  await page.keyboard.press("Escape");
  await sleep(400);

  // Panel 10: edit one word in the page; the source follows.
  const toggle = f.locator("[data-sphinx-preview-edit-toggle]");
  await toggle.click();
  await sleep(900);
  const budget = f.locator("p", { hasText: "retry budget stays" }).first();
  await moveTo(W * 0.75, H * 0.6, 0.2);
  await scrollTo(budget, 330, 0.4);
  await sleep(1000);
  panel(10);
  const bb = await box(budget);
  await moveTo(bb.x + bb.width * 0.5, bb.y + bb.height * 0.5, 0.6);
  await click();
  await sleep(600);
  await snap("10-open");
  const area = f.locator("textarea:visible").first();
  const w5 = await area.evaluate((el) => {
    const c = getComputedStyle(el), g = document.createElement("canvas").getContext("2d");
    g.font = c.font;
    const before = el.value.slice(0, el.value.indexOf("five"));
    const b = el.getBoundingClientRect();
    return { x: b.x + parseFloat(c.paddingLeft) + g.measureText(before).width + g.measureText("five").width / 2, y: b.y + parseFloat(c.paddingTop) + parseFloat(c.lineHeight) / 2 };
  });
  console.log("word", w5);
  await moveTo(fe.x + w5.x, fe.y + w5.y, 0.5);
  ev("click", { x: mx, y: my });
  await page.mouse.dblclick(mx, my);
  await sleep(350);
  await page.keyboard.type("three", { delay: 90 });
  await sleep(450);
  await snap("10-typed");
  await clickLoc(f.getByRole("button", { name: "Done" }), 0.6);
  await sleep(700);
  mark(10, grow(shift(await textIn(budget, "three attempts"), fe)));
  mark(10, grow(await textIn(page.locator(".view-line", { hasText: "retry budget" }).first(), "three")));
  await sleep(1000);
  await snap("10-done");
  close();
  await toggle.click();
  await sleep(1000);

  // Panel 11: the answer moves the x in the file.
  const radio = f.locator(".myst-radio").nth(1);
  const item = f.locator(".myst-radio-item").nth(1);
  await moveTo(W * 0.75, H * 0.6, 0.2);
  await scrollTo(item, 420, 0.4);
  await sleep(1000);
  const line = page.locator(".view-line", { hasText: "Circuit breaker" });
  console.log("source line", await line.count());
  panel(11);
  await sleep(300);
  await clickLoc(radio, 0.9);
  await sleep(400);
  mark(11, grow(await box(radio).then((b) => ({ x: b.x - 2, y: b.y - 2, width: b.width + 4, height: b.height + 4 }))));
  mark(11, grow(await textIn(page.locator(".view-line", { hasText: "Circuit breaker" }).first(), "(x)")));
  await moveTo(mx + 260, my + 110, 0.5);
  await sleep(1800);
  await snap("11-answer");
  ev("end");
} catch (e) {
  console.error("FAILED", e);
  await snap("failure").catch(() => {});
  ev("end");
  process.exitCode = 1;
} finally {
  await cdp.send("Page.stopScreencast").catch(() => {});
  await Promise.all(pending);
  writeFileSync(`${S}/take/frames.json`, JSON.stringify({ size, frames }));
  writeFileSync(`${S}/take/events.json`, JSON.stringify(events));
  await browser.close().catch(() => {});
  try { process.kill(child.pid); } catch { /* already gone */ }
}
console.log("frames", frames.length, "secs", frames.at(-1).t - frames[0].t);
