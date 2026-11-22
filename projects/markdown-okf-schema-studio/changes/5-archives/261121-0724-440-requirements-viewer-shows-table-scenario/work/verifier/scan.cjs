const { createRequire } = require("module");
const fs = require("fs"), path = require("path");
const site = process.argv[2];
const { chromium } = createRequire(site + "/../../package.json")("playwright-core");
(async () => {
  const dirs = [];
  const walk = (d) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name === "index.html" && /SwRS-/.test(p)) dirs.push(p); } };
  walk(path.join(site, "requirements"));
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 390, height: 800 } });
  let sideways = 0, scrolling = [], withTable = 0;
  for (const f of dirs) {
    await page.goto("file:///" + f.split(String.fromCharCode(92)).join("/"));
    const r = await page.evaluate(() => { document.querySelectorAll("details.scn").forEach((d) => (d.open = true));
      return { doc: document.documentElement.scrollWidth > document.documentElement.clientWidth, t: document.querySelectorAll(".scn-table").length,
        w: [...document.querySelectorAll(".scn-table")].filter((w) => w.scrollWidth > w.clientWidth && getComputedStyle(w).overflowX === "auto").length }; });
    if (r.t) withTable++; if (r.doc) sideways++; if (r.w) scrolling.push([path.basename(path.dirname(f)), r.w]);
  }
  console.log(JSON.stringify({ pages: dirs.length, withTable, pagesScrollingSideways: sideways, pagesWithInnerScrollTable: scrolling.length, sample: scrolling.slice(0, 3) }));
  await b.close();
})();
