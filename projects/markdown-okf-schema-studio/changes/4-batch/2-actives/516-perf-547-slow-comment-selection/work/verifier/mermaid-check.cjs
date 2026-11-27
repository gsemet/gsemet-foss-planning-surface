// Verifier probe of CR-516: draws each mermaid block of the pull request body in Chromium with the
// mermaid library of the repository. Run from the worktree: node <this file> <pull request body.md>
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");

const worktree = process.cwd();
const { chromium } = createRequire(path.join(worktree, "package.json"))("playwright-core");
const body = fs.readFileSync(path.resolve(process.argv[2]), "utf8").replace(/\r\n/g, "\n");
const blocks = [...body.matchAll(/```mermaid\n([\s\S]*?)```/g)].map((match) => match[1]);

(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.setContent("<!DOCTYPE html><body></body>");
    await page.addScriptTag({ path: path.join(worktree, "node_modules", "mermaid", "dist", "mermaid.min.js") });
    console.log(`${blocks.length} mermaid block(s)`);
    for (const [index, source] of blocks.entries()) {
      const result = await page.evaluate(async ([text, id]) => {
        try {
          window.mermaid.initialize({ startOnLoad: false });
          const { svg } = await window.mermaid.render(id, text);
          const holder = document.createElement("div");
          holder.innerHTML = svg;
          return `drawn, ${holder.querySelectorAll("g.node").length} nodes, ${holder.querySelectorAll("path.flowchart-link").length} links`;
        } catch (error) {
          return `FAILED: ${error.message}`;
        }
      }, [source, `block${index}`]);
      console.log(`block ${index + 1}: ${result}`);
    }
  } finally {
    await browser.close();
  }
})();
