const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const n = (...l) => `${[":::{note}", ...l, ":::"].join("\n")}\n`;
const CASES = [
  ["tags in two comments", n("<!-- <div> -->", "", "Alpha", "", "<!-- </div> -->", "", "Beta")],
  ["comment opens, text closes", n("<!-- <b> -->", "", "Alpha</b>", "", "Beta")],
  ["self closing", n("<span />", "", "Alpha", "", "Beta</span>")],
  ["br and img", n("Alpha<br>", "beta<img src=x.png>", "", "- one<br/>", "- two")],
  ["unclosed p", n("<p>Alpha", "", "Beta", "", "<p>Gamma</p>")],
  ["li omitted", n("<ul>", "<li>a", "<li>b", "</ul>", "", "Beta")],
  ["attr with gt", n('<span title="a>b">Alpha</span>', "", "Beta")],
  ["tag in attr", n('<span title="</div>">Alpha</span>', "", "<div>", "", "Beta", "", "</div>", "", "Gamma")],
  ["inline across paragraphs", n("<b>One", "", "Two</b>", "", "Three")],
  ["para ends with close", n("<details>", "<summary>S</summary>", "", "One", "", "Para</details>", "", "Three")],
  ["details normal", n("<details>", "<summary>S</summary>", "", "One", "", "- a", "- b", "", "</details>", "", "Three")],
  ["kbd", n("Press <kbd>Ctrl</kbd>", "then", "", "- <kbd>A</kbd>", "- b")],
  ["sup multi", n("x<sup>2", "</sup> y", "", "Beta")],
];
(async () => {
  for (const [name, source] of CASES) {
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
      const all = (e) => [e, ...e.children.flatMap(all)];
      const rows = [];
      for (const e of page.document.children.flatMap(all)) {
        const hit = e.closest(MAPPINGS_SELECTOR);
        const own = e.children.length ? "" : e.textContent.trim();
        if (!hit || !own) continue;
        const f = (exact) => { const x = blocks.editingElementFor(hit, { exact }); const r = x.sourceRange ?? blocks.blockRange(x.element); return `${r.line}-${r.endLine}`; };
        rows.push(`${own.slice(0, 12)}=${f(false)}/${f(true)}`);
      }
      console.log(`  ${rows.join("  ")}`);
    } catch (error) { console.log(`  THROWS ${error.message}`); }
  }
})();
