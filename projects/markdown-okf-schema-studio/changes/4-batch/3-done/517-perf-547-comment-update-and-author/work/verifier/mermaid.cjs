// Verifier probe of CR-517: the diagram of the live PR body parses and renders with the
// repository's installed mermaid, in the installed headless Chromium (no download).
// Run from the worktree: node <this file> <pr body file>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const need = createRequire(path.join(process.cwd(), "package.json"));
const { chromium } = need("playwright-core");
const body = fs.readFileSync(process.argv[2], "utf8");
const blocks = [...body.matchAll(/```mermaid\r?\n([\s\S]*?)```/g)].map((match) => match[1]);
(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.setContent("<main></main>");
    await page.addScriptTag({ path: path.join(process.cwd(), "node_modules/mermaid/dist/mermaid.min.js") });
    for (const [index, source] of blocks.entries()) {
      const result = await page.evaluate(async (text) => {
        window.mermaid.initialize({ startOnLoad: false });
        const { svg } = await window.mermaid.render("probe", text);
        document.querySelector("main").innerHTML = svg;
        return { version: window.mermaid.version, nodes: document.querySelectorAll("g.node").length,
          edges: document.querySelectorAll("path.flowchart-link").length };
      }, source);
      console.log("diagram", index + 1, "of", blocks.length, "rendered", JSON.stringify(result));
    }
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error.message); process.exit(1); });
