// Verifier probe 2: where does the longest line end inside the widened pre? Loads probe.js helpers.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const source = fs.readFileSync(path.join(__dirname, "probe.js"), "utf8");
const helpers = source.slice(0, source.indexOf("async function main()")).replace('"use strict";', "");
const body = `
async function run() {
  const browser = await chromium.launch({ ignoreDefaultArgs: ["--hide-scrollbars"] });
  try {
    for (const [name, md] of [["shot", shotDocument], ["overflow", overflow]]) {
      const page = await open(browser, await build(name, md, 688, "cream"), 560);
      if (name === "overflow") await pinTestFonts(page);
      await toAuto(page);
      const out = await page.evaluate(() => [...document.querySelectorAll("#sphinx-myst-preview-content pre")].map((pre) => {
        const style = getComputedStyle(pre);
        let right = 0;
        const walker = document.createTreeWalker(pre, NodeFilter.SHOW_TEXT);
        while (walker.nextNode()) {
          const range = document.createRange();
          range.selectNodeContents(walker.currentNode);
          for (const r of range.getClientRects()) right = Math.max(right, r.right);
        }
        const box = pre.getBoundingClientRect();
        const inner = box.right - parseFloat(style.borderRightWidth);
        return "text right " + right.toFixed(2) + ", pre inner right " + inner.toFixed(2) + ", free " + (inner - right).toFixed(2)
          + " px, padding-right " + style.paddingRight + ", client/scroll " + pre.clientWidth + "/" + pre.scrollWidth;
      }));
      console.log("[" + label + "] " + name + " auto", JSON.stringify(out, null, 1));
      await page.close();
    }
  } finally {
    await browser.close();
    fs.rmSync(work, { recursive: true, force: true });
  }
}
run().catch((error) => { console.error(error); process.exit(1); });
`;
new Function("require", "__dirname", "process", helpers + body)(require, __dirname, process);
