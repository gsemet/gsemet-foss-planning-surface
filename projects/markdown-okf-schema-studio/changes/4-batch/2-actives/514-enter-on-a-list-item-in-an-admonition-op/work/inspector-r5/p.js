// For each case: every mapped element in the first box, what click and Enter open (lines and text).
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <cases.js> [filter]
const path = require("node:path");
const [root, cases, filter] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
(async () => {
  for (const [name, source] of require(cases)) {
    if (filter && !name.includes(filter)) continue;
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
      const lines = source.split(/\r\n|\n/);
      for (const e of page.document.querySelectorAll(MAPPINGS_SELECTOR)) {
        const out = [];
        for (const exact of [true]) {
          const x = blocks.editingElementFor(e, { exact });
          const r = x.sourceRange ?? blocks.blockRange(x.element);
          out.push(`${exact ? "enter" : "click"} ${r.line}-${r.endLine} ${JSON.stringify(lines.slice(r.line - 1, r.endLine).join("\n"))}`);
        }
        console.log(`  <${e.tagName.toLowerCase()} ${e.getAttribute("class") ?? ""}> ${JSON.stringify(e.textContent.replace(/\s+/g, " ").trim().slice(0, 30))} ${out.join(" | ")}`);
      }
      const math = page.document.querySelectorAll(".math-display").length;
      if (math) console.log(`  math-display rendered: ${math}`);
    } catch (error) { console.log(`  THROWS ${error.message}`); }
  }
})();
