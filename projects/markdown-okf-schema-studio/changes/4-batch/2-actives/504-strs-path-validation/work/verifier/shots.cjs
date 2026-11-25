// usage: node shots.cjs <scratch vt folder> <evidence folder>
// Screenshots of the requirements viewer built from the base and the head, plus text checks.
const path = require("node:path");
const fs = require("node:fs");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const [scratch, out] = process.argv.slice(2);
const pages = {
  home: "requirements/index.html",
  life023: "requirements/lifecycle-sync/StRS-MDOKFSTUDIO-LIFE-023/index.html",
  code004: "requirements/code-blocks/StRS-MDOKFSTUDIO-CODE-004/index.html",
  swrs: "requirements/rendering-core/SwRS-MDOKFSTUDIO-CORE-082/index.html",
};

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  for (const [side, folder] of [["before", "site-base"], ["after", "site-head"]]) {
    for (const [name, rel] of Object.entries(pages)) {
      const file = path.join(scratch, folder, rel);
      if (!fs.existsSync(file)) { console.log(side, name, "no page", rel); continue; }
      await page.goto(pathToFileURL(file).href);
      await page.evaluate(() => document.querySelectorAll("details").forEach((d) => { d.open = true; }));
      if (name === "home") {
        const figures = await page.evaluate(() => ({
          cards: [...document.querySelectorAll(".req-stat")].map((c) => c.innerText.replace(/\n/g, " | ")),
          head: [...document.querySelectorAll(".req-table thead")][0]?.innerText,
          rows: [...[...document.querySelectorAll(".req-table")][0].querySelectorAll("tbody tr, tfoot tr")].map((r) => r.innerText.replace(/\t/g, " ; ")),
        }));
        console.log(side, "home", JSON.stringify(figures, null, 1));
        const start = page.locator("h2", { hasText: "The figures" });
        const box = await start.boundingBox();
        await page.screenshot({ path: path.join(out, `${side}-home-figures.png`), fullPage: true, clip: { x: 0, y: box.y - 10, width: 1280, height: 1150 } });
      } else {
        const sel = name === "swrs" ? "details.scn" : ".path-row";
        const rows = await page.evaluate((s) => [...document.querySelectorAll(s)].map((r) => (r.querySelector("summary, .path-name")?.innerText ?? "") + " || " + [...r.querySelectorAll(".cols section, .scn-tests")].map((x) => x.innerText.replace(/\s+/g, " ").slice(0, 160)).join(" ## ")), sel);
        console.log(side, name, rows.length, JSON.stringify(rows, null, 1));
        const target = page.locator(sel).first();
        if (await target.count()) {
          const box = await target.boundingBox();
          await page.screenshot({ path: path.join(out, `${side}-${name}.png`), fullPage: true, clip: { x: 0, y: Math.max(0, box.y - 120), width: 1280, height: 900 } });
        } else {
          await page.screenshot({ path: path.join(out, `${side}-${name}.png`) });
        }
      }
    }
  }
  // The share of SwRS pages with at least one scenario marked missing, over the head site.
  const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]));
  const html = walk(path.join(scratch, "site-head", "requirements")).filter((f) => /SwRS-[^\\/]+[\\/]index\.html$/.test(f));
  let missing = 0;
  let first;
  for (const f of html) {
    const n = (fs.readFileSync(f, "utf8").match(/class="tag missing"/g) || []).length;
    missing += n;
    if (n && !first && /TOOLBAR|PALETTE/.test(f)) first = f;
  }
  console.log("head SwRS pages", html.length, "missing marks", missing);
  if (first) {
    await page.goto(pathToFileURL(first).href);
    await page.evaluate(() => document.querySelectorAll("details").forEach((d) => { d.open = true; }));
    const box = await page.locator("details.scn", { has: page.locator(".tag.missing") }).first().boundingBox();
    console.log("missing example", path.basename(path.dirname(first)));
    await page.screenshot({ path: path.join(out, "after-swrs-missing.png"), fullPage: true, clip: { x: 0, y: Math.max(0, box.y - 160), width: 1280, height: 700 } });
  }
  await browser.close();
})();
