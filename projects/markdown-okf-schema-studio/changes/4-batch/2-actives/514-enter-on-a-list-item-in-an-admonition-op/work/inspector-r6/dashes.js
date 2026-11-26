// Mapped <p>/<h*> elements whose own words are not on the lines they open, for --- options blocks.
const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const t = (...l) => `${l.join("\n")}\n`;
const opts = [["---", "class: x", "---"], ["---", "class: x", "---", ""], ["--- ", "class: x", "---"], ["---", "class: x", "--- "], ["----", "class: x", "----"], ["---", "class: x", "----"], ["---", "---"], ["---", "class: x", "name: y", "---"]];
const later = [["---"], ["----"], ["-----"], ["--"], ["-"], ["- - -"], ["***"], ["--- "], ["  ---"], ["    ---"], ["> ---"], ["```", "---", "```"], ["Setext", "---"], ["Setext", "----"], []];
const heads = [[":::{note}", ":::"], ["```{note}", "```"], [":::{dropdown} T", ":::"], [":::{versionadded} 1", ":::"], [":::{div}\n:::", ""], [":::{admonition} T", ":::"]];
(async () => {
  const bad = new Map();
  for (const [head, tail] of heads.slice(0, 4).concat([heads[5]])) for (const opt of opts) for (const mid of later) for (const gap of [true, false]) {
    const body = ["Wone", "", ...(gap ? [] : []), ...mid, ...(gap ? [""] : []), "Wtwo", "", "Wthree"];
    const source = t(head, ...opt, ...body, tail);
    const lines = source.split("\n");
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const all = (e) => [e, ...e.children.flatMap(all)];
    for (const e of page.document.children.flatMap(all)) {
      const word = /^(Wone|Wtwo|Wthree)$/u.exec(e.textContent.trim())?.[1];
      if (!word || !/^(P|H\d)$/u.test(e.tagName)) continue;
      const hit = e.closest(MAPPINGS_SELECTOR);
      for (const exact of [false, true]) {
        const x = blocks.editingElementFor(hit, { exact });
        const r = x.sourceRange ?? blocks.blockRange(x.element);
        const text = lines.slice(r.line - 1, r.endLine).join("\n");
        if (!text.includes(word)) bad.set(`${JSON.stringify(source)} ${word} -> ${r.line}-${r.endLine} ${JSON.stringify(text)}`, 1);
      }
    }
  }
  console.log(`${bad.size} wrong`);
  console.log([...bad.keys()].slice(0, 40).join("\n"));
})();
