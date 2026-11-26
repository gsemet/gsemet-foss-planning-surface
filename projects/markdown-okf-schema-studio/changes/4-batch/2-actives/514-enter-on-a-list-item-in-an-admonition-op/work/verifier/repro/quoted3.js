// Variants of the "quoted colon admonition left open" known gap, with the unquoted twin of each.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const all = (e) => [e, ...e.children.flatMap(all)];
const CASES = {
  "plain open note, quoted tip last": [":::{note}", "Before.", "", "> :::{tip}", "> Tip body.", "> :::"],
};
(async () => {
  for (const [name, body] of Object.entries(CASES)) {
    for (const quoted of [false, true]) {
      const lines = quoted ? body.map((l) => (l ? `> ${l}` : ">")) : body;
      const source = `${lines.join("\n")}\n`;
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
      const mapped = all(page.document).filter((e) => e.getAttribute("data-sphinx-source-line") !== null);
      const show = mapped.map((e) => { const r = blocks.blockRange(e); return `${e.tagName.toLowerCase()}${e.getAttribute("class")?.includes("admonition") ? `.${e.getAttribute("class").split(" ")[1]}` : ""} ${r.line}-${r.endLine}`; });
      const boxes = all(page.document).filter((e) => (e.getAttribute("class") ?? "").split(" ").includes("admonition")).map((e) => `${e.getAttribute("class")}[${e.getAttribute("data-sphinx-source-line") ?? "unmapped"}]`);
      console.log(`${name} | ${quoted ? "quoted  " : "unquoted"} | boxes: ${boxes.join("; ")} | mapped: ${show.join(", ")}`);
    }
  }
})();
