const { createRequire } = require("module");
const fs = require("fs"), path = require("path");
const site = process.argv[2];
const { chromium } = createRequire(site + "/../../package.json")("playwright-core");
(async () => {
  const dirs = [];
  const walk = (d) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p); else if (e.name === "index.html" && /SwRS-/.test(p)) dirs.push(p); } };
  walk(path.join(site, "requirements"));
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 390, height: 800 } });
  const out = [];
  for (const f of dirs) {
    await page.goto("file:///" + f.split(String.fromCharCode(92)).join("/"));
    const r = await page.evaluate(() => { const open = process_open(); return open; function process_open() {
      const before = document.documentElement.scrollWidth > document.documentElement.clientWidth;
      document.querySelectorAll("details.scn").forEach((d) => (d.open = true));
      const after = document.documentElement.scrollWidth > document.documentElement.clientWidth;
      const cw = document.documentElement.clientWidth;
      const wide = [...document.querySelectorAll("body *")].filter((e) => e.getBoundingClientRect().right > cw + 1).slice(0, 3).map((e) => e.tagName + "." + e.className + ":" + Math.round(e.getBoundingClientRect().right) + " in " + (e.closest(".scn-table") ? "scn-table" : e.closest(".gwt") ? "gwt" : "other"));
      return { before, after, wide }; } });
    if (r.after) out.push([path.basename(path.dirname(f)), r.before, r.wide]);
  }
  console.log(JSON.stringify(out));
  await b.close();
})();
