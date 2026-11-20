// Build the viewer pages only, then screenshot the map of chosen StRS at two widths.
const path = require("node:path");
const fs = require("node:fs");
const root = path.resolve(__dirname, "../..");
const { writeViewerPages } = require(path.join(root, "out/test/site/requirementsViewer/write.js"));
const { chromium } = require(path.join(root, "node_modules/playwright-core"));
const tag = process.argv[2] || "baseline";
const site = path.join(root, "out/graphlab/site");
const shots = path.join(root, "out/graphlab/shots", tag);
fs.mkdirSync(shots, { recursive: true });
const model = writeViewerPages(site, path.join(root, "out/reports/requirements/requirements-report.json"), root);
const ids = ["BLOCK-003", "FMSCHEMA-014", "BLOCK-014", "MYST-006", "REVIEW-012", "MYST-009"];
(async () => {
  const browser = await chromium.launch();
  const report = [];
  for (const [w, label] of [[1280, "desktop"], [800, "narrow"]]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    for (const id of ids) {
      const req = model.active.find((r) => r.id.endsWith(id));
      const files = [];
      const walk = (d) => { for (const f of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, f.name); if (f.isDirectory()) walk(p); else if (p.includes(req.id) && f.name === "index.html") files.push(p); } };
      walk(path.join(site, "requirements"));
      await page.goto(require("node:url").pathToFileURL(files[0]).href);
      await page.addStyleTag({ content: ".top{position:static!important}" }); const map = await page.$(".map");
      const box = await map.boundingBox();
      // overlap check: text/pill boxes in the svg
      const overlaps = await page.evaluate(() => {
        const svg = document.querySelector("svg.metro"); if (!svg) return -1;
        const els = [...svg.querySelectorAll("text:not(.pt), rect.pill")].map((e) => e.getBoundingClientRect()).filter((r) => r.width > 0);
        let n = 0; for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) { const a = els[i], b = els[j]; if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) n++; }
        return n;
      });
      report.push(`${label} ${id}: map ${Math.round(box.width)}x${Math.round(box.height)} overlaps=${overlaps}`);
      await map.screenshot({ path: path.join(shots, `${id}-${label}.png`) });
    }
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(shots, "metrics.txt"), report.join("\n") + "\n");
  console.log(report.join("\n"));
})();
