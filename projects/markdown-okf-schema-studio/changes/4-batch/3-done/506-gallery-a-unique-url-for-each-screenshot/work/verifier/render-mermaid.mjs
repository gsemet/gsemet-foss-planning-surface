// Renders the Mermaid block of the posted PR body in Chromium, with the repository's own mermaid.
// Usage: node render-mermaid.mjs <head worktree> <body file> <png out>
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const [head, bodyFile, out] = process.argv.slice(2);
const require = createRequire(path.join(path.resolve(head), "package.json"));
const { chromium } = require("playwright-core");

const body = fs.readFileSync(bodyFile, "utf8").replace(/\r/g, "");
const blocks = [...body.matchAll(/```mermaid\n([\s\S]*?)```/g)].map((m) => m[1]);
console.log("mermaid blocks:", blocks.length);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1000, height: 700 } });
await page.setContent('<div id="d" style="width:960px"></div>');
await page.addScriptTag({ path: path.join(path.resolve(head), "node_modules/mermaid/dist/mermaid.min.js") });
const texts = await page.evaluate(async (source) => {
  window.mermaid.initialize({ startOnLoad: false });
  const { svg } = await window.mermaid.render("seq", source);
  document.getElementById("d").innerHTML = svg;
  return [...document.querySelectorAll("#d text")].map((t) => t.textContent.trim()).filter(Boolean);
}, blocks[0]);
console.log("texts:", JSON.stringify([...new Set(texts)]));
await page.locator("#d").screenshot({ path: out });
await browser.close();
