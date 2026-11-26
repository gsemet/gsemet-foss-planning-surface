// The tag pairs read for HTML written inside reparsed or offset bodies: each pair must name the
// lines that hold <q> and </q>.
const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const box = o("src/core/render/mystBoxLines.js");
let got;
const original = box.htmlTagLines;
box.htmlTagLines = (ast) => (got = original(ast));
const { renderMyst } = o("src/core/render/mystRenderer.js");
const t = (...l) => `${l.join("\n")}\n`;
const html = ["<q>", "", "word", "", "</q>"];
const block = ["<q>", "word", "</q>"];
const pad = ["Pad", "", "Pad", "", "Pad", ""];
const wraps = {
  note: [":::{note}", ":::"], options: [":::{note}", ":::", [":class: x", ""]], optionsNoBlank: [":::{note}", ":::", [":class: x"]],
  yaml: [":::{note}", ":::", ["---", "class: x", "---"]], dropdown: [":::{dropdown} T", ":::"], version: [":::{versionadded} 1", ":::"],
  grid: ["::::{grid}", "::::", [":::{grid-item}"], [":::"]], card: [":::{card}", ":::"], tab: ["::::{tab-set}", "::::", [":::{tab-item} A"], [":::"]],
  div: [":::{div}", ":::"], quote: [":::{note}", ":::", [], [], "> "], alert: ["> [!NOTE]", "", [], [], "> "], list: [":::{note}", ":::", ["- Item", ""], [], "  "],
  tabletag: ["```{list-table}", "```", ["* - a"]], fig: ["```{figure} a.png", "```"], backtick: ["```{note}", "```"], unclosed: [":::{note}", ""],
  admon: [":::{admonition} T", ":::"], gridopt: ["::::{grid} 2", "::::", [":gutter: 1", "", ":::{grid-item-card} T", ":class-card: x"], [":::"]],
  frontmatter: ["---\na: b\n---\n:::{note}", ":::"], blankfirst: [":::{note}", ":::", ["", "", ""]], context: [":::{note}", ":::", [":::{div} x"], []],
};
(async () => {
  for (const [name, [first, last, pre = [], post = [], prefix = ""]] of Object.entries(wraps)) {
    for (const [kind, body] of [["split", html], ["block", block]]) {
      const lines = t(...pad, first, ...pre, ...body.map((l) => prefix + l), ...post, last).split("\n");
      const source = lines.join("\n");
      const real = source.split("\n");
      got = undefined;
      try { await renderMyst(source); } catch (e) { console.log(name, kind, "THROWS", e.message); continue; }
      const a = real.findIndex((l) => l.includes("<q>")) + 1;
      const b = real.findIndex((l) => l.includes("</q>")) + 1;
      const ok = got?.some((p) => p.start === a && p.end === b);
      console.log(name, kind, `want ${a}-${b}`, `got ${JSON.stringify(got)}`, ok ? "" : "MISMATCH");
    }
  }
})();
