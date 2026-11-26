// Lists the mapped elements of a source (what the arrows can select) with their class and lines.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <file.md>
const fs = require("node:fs");
const path = require("node:path");
const [root, file] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
(async () => {
  const source = fs.readFileSync(file, "utf8");
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
  console.log(`=== ${path.basename(file)} ${JSON.stringify(source)}`);
  for (const e of page.document.querySelectorAll(MAPPINGS_SELECTOR)) {
    const r = blocks.blockRange(e);
    console.log(`  <${e.tagName.toLowerCase()} ${e.getAttribute("class") ?? ""}> ${r.line}-${r.endLine} ${JSON.stringify(e.textContent.replace(/\s+/g, " ").trim().slice(0, 30))}`);
  }
})();
