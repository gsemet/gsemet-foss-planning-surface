// Usage: node shoot.cjs <siteRoot> <outDir> <tag>
const { createRequire } = require("module");
const req = createRequire(process.argv[2] + "/../../package.json");
const { chromium } = req("playwright-core");
const path = require("path");
const [site, out, tag] = process.argv.slice(2);
const url = (p) => "file:///" + path.join(site, p).replace(/\\/g, "/");
(async () => {
  const browser = await chromium.launch();
  const report = {};
  async function open(p, viewport) {
    const page = await browser.newPage({ viewport });
    await page.goto(url(p));
    return page;
  }
  async function cardShot(page, title, file) {
    const card = page.locator("details.scn", { hasText: title }).first();
    await card.evaluate((e) => { e.open = true; });
    await card.scrollIntoViewIfNeeded();
    await card.screenshot({ path: path.join(out, file) });
    return await card.evaluate((e) => ({
      tables: e.querySelectorAll("table").length,
      th: [...e.querySelectorAll("th")].map((t) => t.textContent),
      rows: e.querySelectorAll("tbody tr").length,
      gwt: e.querySelectorAll(".gwt").length,
      gwtText: [...e.querySelectorAll(".gwt")].map((g) => g.textContent.trim().length),
      notes: [...e.querySelectorAll(".scn-note")].map((n) => n.textContent),
    }));
  }
  const b130 = "requirements/block-editing/SwRS-MDOKFSTUDIO-BLOCK-130/index.html";
  let p = await open(b130, { width: 1100, height: 900 });
  const n = await p.locator("details.scn").count();
  report.b130cards = n;
  const first = p.locator("details.scn").first();
  const t1 = await first.locator("summary").textContent();
  report.first = { title: t1, ...(await cardShot(p, t1, `${tag}-block130-first-card.png`)) };
  report.chord = await cardShot(p, "The move chord in the text box moves the block and reopens its editor", `${tag}-block130-chord-card.png`);
  report.retry = await cardShot(p, "A refused keyboard move can be retried", `${tag}-block130-retry-card.png`);
  // all cards of the page
  report.allEmpty = await p.evaluate(() =>
    [...document.querySelectorAll("details.scn")].map((d) => d.querySelectorAll(".gwt").length && !d.querySelector("table") ? [...d.querySelectorAll(".gwt div")].every((x) => !x.textContent.replace(/^(Given|When|Then)/i, "").trim()) : false).filter(Boolean).length);
  await p.close();
  p = await open("requirements/gfm/SwRS-MDOKFSTUDIO-GFM-021/index.html", { width: 1100, height: 900 });
  const g = p.locator("details.scn");
  report.gfm021cards = await g.count();
  const gt = await g.first().locator("summary").textContent();
  report.gfm021 = { title: gt, ...(await cardShot(p, gt, `${tag}-gfm021-first-card.png`)) };
  await p.close();
  // phone width
  p = await open(b130, { width: 390, height: 800 });
  await p.evaluate(() => document.querySelectorAll("details.scn").forEach((d) => (d.open = true)));
  report.phone = await p.evaluate(() => ({
    docScrollW: document.documentElement.scrollWidth,
    clientW: document.documentElement.clientWidth,
    wrappers: [...document.querySelectorAll(".scn-table")].map((w) => [w.scrollWidth, w.clientWidth]).filter((x) => x[0] > x[1]).length,
    tables: document.querySelectorAll(".scn-table").length,
  }));
  const wide = p.locator(".scn-table").first();
  if (await wide.count()) await wide.scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(out, `${tag}-block130-phone.png`) });
  await p.close();
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
})();
