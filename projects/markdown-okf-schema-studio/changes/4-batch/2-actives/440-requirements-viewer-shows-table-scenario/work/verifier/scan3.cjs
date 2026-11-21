const { createRequire } = require("module");
const site = process.argv[2];
const { chromium } = createRequire(site + "/../../package.json")("playwright-core");
(async () => {
  const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 390, height: 800 } });
  await page.goto("file:///" + site + "/requirements/" + process.argv[3]);
  console.log(JSON.stringify(await page.evaluate(() => { const cw = document.documentElement.clientWidth;
    const w = [...document.querySelectorAll("body *")].filter((e) => e.getBoundingClientRect().right > cw + 1).slice(0, 4).map((e) => e.tagName + "." + e.className + ":" + Math.round(e.getBoundingClientRect().right) + " " + (e.textContent || "").slice(0, 40));
    return { sw: document.documentElement.scrollWidth, w }; })));
  await b.close();
})();
