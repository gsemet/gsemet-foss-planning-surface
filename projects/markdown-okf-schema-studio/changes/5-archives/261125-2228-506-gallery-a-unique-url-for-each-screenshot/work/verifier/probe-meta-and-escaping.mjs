// 1. What a Meta click carries and does on the head page. 2. The shipped buildGallery over file names
// holding <, >, & and ", given through a stubbed directory listing (Windows allows no such name).
// Usage: node probe-meta-and-escaping.mjs <head worktree>
import path from "node:path";
import { createRequire } from "node:module";

const head = path.resolve(process.argv[2]);
const require = createRequire(path.join(head, "package.json"));
const { chromium } = require("playwright-core");
const fs = require("node:fs");
const { buildGallery } = require(path.join(head, "out/test/site/galleryPage.js"));
const { pageDocument } = require(path.join(head, "out/test/site/buildSite.js"));

const root = path.join(head, "virtual-shots");
const names = ['a<img src=x onerror=alert(1)>&"q.png', "plain.png"];
const real = { existsSync: fs.existsSync, readdirSync: fs.readdirSync };
fs.existsSync = (p) => (String(p) === root ? true : String(p).startsWith(root) ? false : real.existsSync(p));
fs.readdirSync = (p, o) => (String(p) === root ? names.map((name) => ({ name, isDirectory: () => false, isFile: () => true })) : real.readdirSync(p, o));
const html = pageDocument("gallery", "gallery.html", buildGallery(root));
Object.assign(fs, real);
console.log("raw markup from the file name in the HTML:", html.includes("<img src=x onerror"));
console.log("opener:", /<a class="capture-open"[^>]*a%3C[^>]*>/.exec(html)?.[0]);

const browser = await chromium.launch();
const context = await browser.newContext();
await context.route("http://probe.test/**", (route) => route.fulfill(route.request().url().includes("gallery.html") ? { contentType: "text/html", body: html } : { status: 404, body: "" }));
const page = await context.newPage();
let alerts = 0;
page.on("dialog", (d) => { alerts += 1; void d.dismiss(); });
await page.goto("http://probe.test/gallery.html");
const first = page.locator("a.capture-open").first();
console.log("ids read from the DOM:", JSON.stringify(await page.locator("a.capture-open").evaluateAll((l) => l.map((a) => a.dataset.captureId))));
await first.click();
await page.waitForTimeout(300);
const url = page.url();
console.log("after click:", JSON.stringify({ url, title: await page.title(), injectedImages: await page.locator("img[onerror]").count() }));
const direct = await context.newPage();
direct.on("dialog", (d) => { alerts += 1; void d.dismiss(); });
await direct.goto(url);
await direct.waitForTimeout(300);
console.log("direct load:", JSON.stringify(await direct.evaluate(() => ({ open: document.querySelector(".capture-viewer").open, position: document.querySelector("[data-capture-position]").textContent, noticeHidden: document.querySelector("[data-capture-missing]").hidden }))), "alerts:", alerts);

for (const modifier of ["Meta", "Control", "Shift", "Alt"]) {
  const p = await context.newPage();
  await p.goto("http://probe.test/gallery.html");
  await p.evaluate(() => {
    window.seen = [];
    document.addEventListener("click", (e) => { window.seen.push({ ctrl: e.ctrlKey, meta: e.metaKey, shift: e.shiftKey, alt: e.altKey, interceptedByPage: e.defaultPrevented }); e.preventDefault(); });
  });
  await p.locator("a.capture-open").first().click({ modifiers: [modifier] });
  await p.waitForTimeout(200);
  console.log(`${modifier} click, trusted input:`, JSON.stringify(await p.evaluate(() => window.seen)), "viewer open:", await p.evaluate(() => document.querySelector(".capture-viewer").open));
  await p.evaluate(() => {
    window.seen = [];
  });
  const flag = { Meta: "metaKey", Control: "ctrlKey", Shift: "shiftKey", Alt: "altKey" }[modifier];
  await p.evaluate((key) => document.querySelector("a.capture-open").dispatchEvent(new MouseEvent("click", { button: 0, bubbles: true, cancelable: true, [key]: true })), flag);
  console.log(`${modifier} click, synthetic event with ${flag}:`, JSON.stringify(await p.evaluate(() => window.seen)), "viewer open:", await p.evaluate(() => document.querySelector(".capture-viewer").open));
  await p.close();
}
await browser.close();
