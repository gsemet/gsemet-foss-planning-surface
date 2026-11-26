// Usage: node capture.mjs <worktree with node_modules> <out/site folder> <output folder> <before|after>
// Before/after captures of the built site, headless, over file://, so no address bar and no path shows.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const [worktree, siteFolder, outFolder, side] = process.argv.slice(2);
const require = createRequire(path.join(path.resolve(worktree), "package.json"));
const { chromium } = require("playwright-core");
const site = path.resolve(siteFolder);
const out = path.resolve(outFolder);
fs.mkdirSync(out, { recursive: true });
const url = (file) => pathToFileURL(path.join(site, file)).href;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const failed = [];
page.on("requestfailed", (request) => failed.push(path.basename(request.url())));

await page.goto(url("docs/how-we-ship.html"), { waitUntil: "load" });
await page.locator("header.top").screenshot({ path: path.join(out, `${side}-header.png`) });
console.log(`${side} header: ${(await page.locator("header.top nav.site a").allInnerTexts()).join(", ")}`);

if (fs.existsSync(path.join(site, "docs/how-we-test.html"))) {
  await page.locator("header.top nav.site a", { hasText: "How we test" }).click();
  await page.waitForLoadState("load");
  console.log(`clicked "How we test": ${path.basename(page.url())}, h1 "${await page.locator("main h1").innerText()}"`);
  const diagram = page.locator('main img[src="../images/how-we-test/test-levels.svg"]');
  await diagram.scrollIntoViewIfNeeded();
  const size = await diagram.evaluate((img) => ({ complete: img.complete, natural: [img.naturalWidth, img.naturalHeight], shown: [img.clientWidth, img.clientHeight] }));
  console.log(`diagram: ${JSON.stringify(size)}`);
  await page.evaluate(() => window.scrollTo(0, 0));
  const box = await diagram.boundingBox();
  await page.setViewportSize({ width: 1280, height: Math.ceil(box.y + box.height + 60) });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: path.join(out, `${side}-page-top.png`) });
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.locator("main table").screenshot({ path: path.join(out, `${side}-table.png`), style: "header.top{visibility:hidden}" });
  const table = await page.locator("main table").evaluate((t) => ({ client: t.clientWidth, scroll: t.scrollWidth }));
  console.log(`table width: ${JSON.stringify(table)}`);
  const clip = await page.evaluate(() => {
    const heads = [...document.querySelectorAll("main h2")];
    const start = heads.find((h) => h.textContent.trim() === "What is not enforced yet");
    const end = heads[heads.indexOf(start) + 1];
    const main = document.querySelector("main").getBoundingClientRect();
    const top = start.getBoundingClientRect().top + window.scrollY - 12;
    return { x: main.left, y: top, width: main.width, height: end.getBoundingClientRect().top + window.scrollY - top };
  });
  await page.screenshot({ path: path.join(out, `${side}-not-enforced.png`), clip, fullPage: true, style: "header.top{visibility:hidden}" });
  // the diagram at its own size, to read its text
  await page.setViewportSize({ width: 1240, height: size.natural[1] || 700 });
  await page.goto(url("images/how-we-test/test-levels.svg"), { waitUntil: "load" });
  await page.screenshot({ path: path.join(out, `${side}-diagram-native.png`) });
} else {
  console.log("docs/how-we-test.html: not in this site");
}
console.log(`failed requests: ${failed.length ? failed.join(", ") : "none"}`);
await browser.close();
