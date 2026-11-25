// Probes and captures the real gallery, base and head, each built from the same CI reports artifact.
// Usage: node probe-real-site.mjs <head worktree> <base worktree> <evidence folder>
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const [head, base, evidence] = process.argv.slice(2).map((p) => path.resolve(p));
const { chromium } = createRequire(path.join(head, "package.json"))("playwright-core");
fs.mkdirSync(evidence, { recursive: true });

const types = { ".html": "text/html; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml", ".json": "application/json" };
async function serve(root, port) {
  const server = http.createServer((req, res) => {
    const file = path.join(root, path.normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)));
    if (!file.startsWith(root) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return void res.writeHead(404).end();
    res.writeHead(200, { "content-type": types[path.extname(file)] ?? "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise((r) => server.listen(port, "127.0.0.1", r));
  return server;
}
const servers = [await serve(path.join(head, "out", "site"), 8765), await serve(path.join(base, "out", "site"), 8764)];
const headUrl = "http://127.0.0.1:8765/gallery.html";
const baseUrl = "http://127.0.0.1:8764/gallery.html";

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1280, height: 860 } });
const errors = [];
context.on("page", (p) => p.on("pageerror", (e) => errors.push(`${p.url()}: ${e.message}`)));
const log = (label, value) => console.log(label, typeof value === "string" ? value : JSON.stringify(value));
const pause = (p) => p.waitForTimeout(400);
const state = (p) => p.evaluate(() => {
  const v = document.querySelector(".capture-viewer");
  const n = document.querySelector("[data-capture-missing]");
  const a = document.activeElement;
  return {
    url: location.href.replace(/^.*\/(gallery\.html)/, "$1"),
    open: v.open,
    heading: v.open ? v.querySelector("h2").textContent : null,
    position: v.open ? v.querySelector("[data-capture-position]").textContent : null,
    title: document.title,
    notice: n && n.getClientRects().length ? n.textContent : null,
    focus: a?.matches?.(".capture-open") ? a.getAttribute("data-capture-id") : a?.tagName,
  };
});
/** A strip that shows location.href, added by this script because a headless page has no address bar. */
async function shot(p, name) {
  await p.evaluate(() => {
    const bar = document.createElement("div");
    bar.id = "verifier-address";
    bar.textContent = "address (location.href, strip added by the capture script): " + location.href;
    bar.style.cssText = "position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#ffe27a;color:#111;font:16px monospace;padding:8px 12px;border-top:2px solid #111;overflow-wrap:anywhere";
    const v = document.querySelector(".capture-viewer");
    (v?.open ? v : document.body).append(bar);
  });
  await p.evaluate(() => Promise.all([...document.querySelectorAll(".capture-viewer[open] img")].map((i) => i.decode().catch(() => {}))));
  await pause(p);
  await p.screenshot({ path: path.join(evidence, name) });
  await p.evaluate(() => document.getElementById("verifier-address").remove());
  log("captured", name);
}

const page = await context.newPage();
await page.goto(headUrl);
const ids = await page.locator("a.capture-open").evaluateAll((l) => l.map((a) => a.dataset.captureId));
const registry = "block-editing/r01-paragraph-blur-commit";
const step = ids.find((i) => /^block-editing\/v.*light.*--/.test(i)) ?? ids.find((i) => /\/v.*--/.test(i));
const visual = ids.find((i) => /^block-editing\/v.*light-\d+$/.test(i)) ?? ids.find((i) => /\/v.*-\d+$/.test(i));
log("cards:", String(ids.length));
log("chosen ids:", { visual, step, registry, registryPresent: ids.includes(registry) });

console.log("== direct load of three real ids (head)");
for (const [name, id] of [["visual", visual], ["step", step], ["registry", registry]]) {
  const p = await context.newPage();
  await p.goto(`${headUrl}#${id}`);
  await pause(p);
  log(`direct ${name}:`, await state(p));
  const img = await p.evaluate(async () => { const i = document.querySelector(".capture-image img"); await i.decode(); return { src: decodeURIComponent(i.getAttribute("src") ?? i.src).replace(/^http:\/\/127\.0\.0\.1:\d+\//, ""), width: i.naturalWidth }; });
  log(`image ${name}:`, img);
  await shot(p, `after-viewer-${name}.png`);
  await p.reload();
  await pause(p);
  log(`reload ${name}:`, await state(p));
  await p.close();
}

console.log("== head: open from the grid, Next, Back, Forward, close");
const card = page.locator(`a.capture-open[data-capture-id="${registry}"]`);
await card.click(); await pause(page); log("click:", await state(page));
await page.locator("[data-capture-next]").click(); await pause(page); log("Next:", await state(page));
await shot(page, "after-viewer-next.png");
await page.keyboard.press("ArrowLeft"); await pause(page); log("ArrowLeft:", await state(page));
await page.goBack(); await pause(page); log("Back:", await state(page));
await page.goBack(); await pause(page); log("Back:", await state(page));
await page.goBack(); await pause(page); log("Back:", await state(page));
await page.goForward(); await pause(page); log("Forward:", await state(page));
let n = await page.evaluate(() => history.length);
await page.keyboard.press("Meta+ArrowRight"); await pause(page); log("Meta+ArrowRight:", { ...(await state(page)), pushed: (await page.evaluate(() => history.length)) - n });
const prevented = await page.evaluate(() => ["altKey", "metaKey"].flatMap((m) => ["ArrowLeft", "ArrowRight"].map((key) => { const e = new KeyboardEvent("keydown", { key, [m]: true, bubbles: true, cancelable: true }); document.body.dispatchEvent(e); return `${m}+${key} defaultPrevented=${e.defaultPrevented}`; })));
log("modified arrows:", prevented);
await page.keyboard.press("Escape"); await pause(page); log("Escape:", await state(page));
log("card in view after close:", await card.evaluate((a) => { const r = a.closest("figure").getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }));
await page.goBack(); await pause(page); log("Back after Escape:", await state(page));
for (let i = 0; i < 3; i += 1) { await page.locator("[data-capture-next]").click(); await pause(page); }
log("Next x3:", await state(page));
await page.locator(".capture-close").click(); await pause(page); log("close button:", await state(page));

console.log("== head: modified and middle clicks");
for (const [label, options] of [["Control", { modifiers: ["Control"] }], ["middle", { button: "middle" }], ["Meta", { modifiers: ["Meta"] }]]) {
  const before = await page.evaluate(() => history.length);
  const waiting = context.waitForEvent("page", { timeout: 4000 }).catch(() => null);
  await card.click(options);
  const tab = await waiting;
  if (tab) { await tab.waitForLoadState(); await pause(tab); log(`${label} click new tab:`, await state(tab)); await tab.close(); } else log(`${label} click:`, "no new tab in this headless Chromium");
  log(`${label} click this page:`, { ...(await state(page)), pushed: (await page.evaluate(() => history.length)) - before });
}
log("card href resolved:", (await card.evaluate((a) => a.href)).replace(/^.*\/(gallery\.html)/, "$1"));

console.log("== head: unknown, malformed and markup fragments");
for (const [name, fragment] of [["unknown", "#nope/r99-gone"], ["malformed", "#%E0%A4%A"], ["markup", "#%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E"]]) {
  const p = await context.newPage();
  let dialogs = 0; p.on("dialog", (d) => { dialogs += 1; void d.dismiss(); });
  await p.goto(headUrl + fragment); await pause(p);
  log(`${name}:`, await state(p));
  log(`${name} injected:`, { noticeChildElements: await p.locator("[data-capture-missing] *").count(), alerts: dialogs });
  const order = await p.evaluate(() => { const a = document.querySelector("[data-capture-missing]").getBoundingClientRect(); const g = document.querySelector(".gallery").getBoundingClientRect(); return { noticeBottom: Math.round(a.bottom), gridTop: Math.round(g.top), above: a.bottom <= g.top }; });
  log(`${name} notice above the grid:`, order);
  if (name === "unknown") {
    await shot(p, "after-unknown-id.png");
    await p.locator("a.capture-open").first().click(); await pause(p); log("unknown, then a card:", await state(p));
    await p.goBack(); await pause(p); log("then Back:", await state(p));
    await p.evaluate(() => { location.hash = ""; }); await pause(p); log("then empty fragment:", await state(p));
  }
  await p.close();
}

console.log("== base: the previous page");
const old = await context.newPage();
await old.goto(baseUrl);
const index = ids.indexOf(registry);
log("base start:", { url: old.url().replace(/^.*\//, "") });
await old.locator(".capture-open").nth(index).click(); await pause(old);
const baseState = () => old.evaluate(() => ({ url: location.href.replace(/^.*\//, ""), open: document.querySelector(".capture-viewer").open, heading: document.querySelector(".capture-viewer h2").textContent, position: document.querySelector("[data-capture-position]").textContent, title: document.title, historyLength: history.length }));
log("base click:", await baseState());
await old.locator("[data-capture-next]").click(); await pause(old);
log("base Next:", await baseState());
await shot(old, "before-viewer-next.png");
await old.goBack(); await pause(old);
log("base Back leaves the gallery:", { url: old.url() });
await old.goto("about:blank");
await old.goto(`${baseUrl}#nope/r99-gone`); await pause(old);
log("base unknown fragment:", await old.evaluate(() => ({ url: location.href.replace(/^.*\//, ""), open: document.querySelector(".capture-viewer").open, notice: document.querySelector("[data-capture-missing]") !== null })));
await shot(old, "before-unknown-id.png");
await old.close();

console.log("== grid, base against head");
for (const width of [1280, 390]) {
  const measured = [];
  for (const [label, url] of [["before", baseUrl], ["after", headUrl]]) {
    const p = await context.newPage();
    await p.setViewportSize({ width, height: 860 });
    await p.goto(url);
    await p.evaluate(async () => { const first = [...document.querySelectorAll(".gallery img")].slice(0, 12); for (const i of first) { i.loading = "eager"; await i.decode(); } });
    // The page text names no build time; the boxes of the first cards are compared, images loaded.
    const boxes = await p.evaluate(() => [...document.querySelectorAll(".gallery figure")].slice(0, 12).flatMap((f) => [f, f.querySelector(".capture-open"), f.querySelector("img")].map((e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return [r.x, r.y, r.width, r.height, s.display, s.backgroundColor, s.cursor, s.borderTopWidth, s.textDecorationLine].join(" "); })));
    const png = await p.screenshot({ path: path.join(evidence, `${label}-grid-${width}.png`) });
    await p.keyboard.press("Tab");
    for (let i = 0; i < 40; i += 1) { if (await p.evaluate(() => document.activeElement?.classList.contains("capture-open"))) break; await p.keyboard.press("Tab"); }
    const outline = await p.evaluate(() => { const s = getComputedStyle(document.activeElement); return [document.activeElement.classList.contains("capture-open"), s.outlineStyle, s.outlineWidth, s.outlineColor, s.outlineOffset].join(" "); });
    const focused = await p.screenshot();
    measured.push({ boxes, png, outline, focused });
    await p.close();
  }
  const [a, b] = measured;
  const differing = a.boxes.map((v, i) => (v === b.boxes[i] ? null : { before: v, after: b.boxes[i] })).filter(Boolean);
  log(`grid ${width}px: boxes compared`, String(a.boxes.length));
  log(`grid ${width}px: differing boxes/styles`, differing.slice(0, 6));
  log(`grid ${width}px: screenshot bytes identical`, String(a.png.equals(b.png)));
  log(`grid ${width}px: focus outline before / after`, [a.outline, b.outline]);
  log(`grid ${width}px: focused screenshot bytes identical`, String(a.focused.equals(b.focused)));
}

console.log("== head: the site opened from disk");
const disk = await context.newPage();
const fileUrl = pathToFileURL(path.join(head, "out", "site", "gallery.html")).href;
const diskState = async (label) => { await pause(disk); const s = await state(disk); log(label, { ...s, url: s.url }); };
await disk.goto(`${fileUrl}#${registry}`); await diskState("file direct:");
await disk.locator("[data-capture-next]").click(); await diskState("file Next:");
await disk.keyboard.press("Escape"); await diskState("file Escape:");
await disk.goBack(); await diskState("file Back:");

log("page errors:", errors);
await browser.close();
for (const s of servers) { s.closeAllConnections(); s.close(); }
