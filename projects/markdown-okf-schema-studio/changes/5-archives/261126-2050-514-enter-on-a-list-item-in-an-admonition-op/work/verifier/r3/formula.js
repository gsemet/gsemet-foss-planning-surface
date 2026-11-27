// Claim A at this head: for every formula shape, what Enter and a click open on every mapped element
// that shows the formula, and on the formula's own innermost element; whether the opened lines hold
// the whole formula; what Enter opens on every other mapped element of the box.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <file.md>...
const fs = require("node:fs");
const path = require("node:path");
const [root, ...files] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");

(async () => {
  for (const file of files) {
    const source = fs.readFileSync(file, "utf8");
    const lines = source.split("\n");
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    console.log(`=== ${path.basename(file)} ${JSON.stringify(source)}`);
    const all = (e) => [e, ...e.children.flatMap(all)];
    const need = lines.map((l, i) => [l, i + 1]).filter(([l]) => /y = 2|\$\$/u.test(l)).map(([, n]) => n);
    const open = (e, exact) => {
      const x = blocks.editingElementFor(e, { exact });
      const r = x.sourceRange ?? blocks.blockRange(x.element);
      return { tag: x.element.tagName.toLowerCase(), a: r.line, b: r.endLine };
    };
    const formulaNodes = all(page.document).filter((e) => e.textContent && e.textContent.includes("y = 2"));
    const leaf = formulaNodes[formulaNodes.length - 1];
    if (!leaf) { console.log("  no element shows the formula text"); continue; }
    const hit = leaf.closest(MAPPINGS_SELECTOR);
    const c = open(hit, false);
    console.log(`  click on the formula -> <${c.tag}> ${c.a}-${c.b} formula lines ${need} held=${need.every((n) => n >= c.a && n <= c.b)}`);
    for (const e of page.document.querySelectorAll(MAPPINGS_SELECTOR)) {
      const r = open(e, true);
      const shows = e.textContent.includes("y = 2");
      const text = lines.slice(r.a - 1, r.b).join("\n");
      console.log(`  enter <${e.tagName.toLowerCase()} ${e.getAttribute("class") ?? ""}> -> ${r.a}-${r.b}${shows ? ` shows-formula held=${need.every((n) => n >= r.a && n <= r.b)}` : ""} ${JSON.stringify(text)}`);
    }
  }
})();
