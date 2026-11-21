// run from the worktree root: node <this file>
const path = require("path"), fs = require("fs"), os = require("os");
const { pathToFileURL } = require("url");
const R = process.cwd();
const { chromium } = require(path.join(R, "node_modules/playwright-core"));
const { pinSiteFonts } = require(path.join(R, "out/test/page/pinnedFont"));
const { viewerPages, writeViewerPages } = require(path.join(R, "out/test/site/requirementsViewer/write"));
const { REQUIREMENTS_REPORT_PATH } = require(path.join(R, "out/test/site/requirementsViewer/model"));
(async () => {
  const siteRoot = fs.mkdtempSync(path.join(os.tmpdir(), "probe-"));
  const rep = path.join(siteRoot, "r.json");
  fs.copyFileSync(REQUIREMENTS_REPORT_PATH(R), rep);
  const model = writeViewerPages(siteRoot, rep, R);
  const spec = viewerPages(model, R).find(s => s.dir.endsWith("StRS-MDOKFSTUDIO-CORE-001") && s.body.includes('<svg class="metro"'));
  const b = await chromium.launch();
  for (const w of [1280, 800]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(pathToFileURL(path.join(siteRoot, spec.dir, "index.html")).href);
    await pinSiteFonts(p);
    const out = await p.evaluate(() => {
      const svg = document.querySelector("svg.metro"); const f = svg.getBoundingClientRect();
      const rows = [];
      for (const t of svg.querySelectorAll("tspan")) {
        const r = t.getBoundingClientRect(); const x = t.getAttribute("x");
        if (r.width && /long word/.test(t.textContent)) rows.push({ text: t.textContent, len: t.textContent.length, w: r.width, perChar: r.width / t.textContent.length, left: r.left - f.left, right: r.right - f.left, frameW: f.width, natural: svg.getAttribute("width"), font: getComputedStyle(t).font });
      }
      return rows;
    });
    console.log(w, JSON.stringify(out, null, 1));
  }
  await b.close(); fs.rmSync(siteRoot, { recursive: true, force: true });
})();
