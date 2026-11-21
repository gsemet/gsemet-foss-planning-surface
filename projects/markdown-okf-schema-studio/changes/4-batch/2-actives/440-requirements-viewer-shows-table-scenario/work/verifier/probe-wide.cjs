const { createRequire } = require("module");
const site = process.argv[2];
const { chromium } = createRequire(site + "/../../package.json")("playwright-core");
(async () => {
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 390, height: 800 } });
  await page.goto("file:///" + site + "/requirements/block-editing/SwRS-MDOKFSTUDIO-BLOCK-130/index.html");
  const r = await page.evaluate(() => {
    let t0; const d = document.querySelector("details.scn"); d.open = true;
    const td = d.querySelector("td"); td.textContent = "x".repeat(10).split("").map(() => "wide_unbroken_cell_text").join("_") ;
    td.style.whiteSpace = "nowrap";
    const w = d.querySelector(".scn-table");
    const t = w.querySelector("table"); t0 = w.querySelector("table"); t0.scrollLeft = 300;  const tt = { tOverflowX: getComputedStyle(t).overflowX, tScrollW: t.scrollWidth, tClientW: t.clientWidth, tScrollLeft: t.scrollLeft }; return { tt, tl: getComputedStyle(t).tableLayout, disp: getComputedStyle(t).display, scrollLeft: w.scrollLeft, tableW: t.offsetWidth, tdW: td.offsetWidth, tdWS: getComputedStyle(td).whiteSpace, tdText: td.textContent.length, overflowX: getComputedStyle(w).overflowX, wrapperScrollW: w.scrollWidth, wrapperClientW: w.clientWidth, docScrollW: document.documentElement.scrollWidth, docClientW: document.documentElement.clientWidth };
  });
  console.log(JSON.stringify(r));
  await b.close();
})();
