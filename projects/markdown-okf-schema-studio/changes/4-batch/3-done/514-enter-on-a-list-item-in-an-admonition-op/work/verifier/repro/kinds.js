// Which kinds of block between two paragraphs of a box move with the chord, and past which
// the paragraphs move: real renderer, page helpers and PreviewManager.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const L = (...l) => `${l.join("\n")}\n`;
const KINDS = {
  "GFM table": ["| a | b |", "| - | - |", "| 1 | 2 |"],
  "fenced code": ["```python", "a = 1", "```"],
  "tilde code": ["~~~", "a = 1", "~~~"],
  "indented code": ["    a = 1"],
  "quote": ["> Quoted."],
  "heading": ["## Head"],
  "thematic break": ["---"],
  "ordered list": ["1. one", "2. two"],
  "task list": ["- [ ] one", "- [x] two"],
  "definition list": ["Term", ": Definition"],
  "$$ math": ["$$", "x = 1", "$$"],
  "{math}": ["```{math}", "x = 1", "```"],
  "{mermaid}": ["```{mermaid}", "graph TD", "  A --> B", "```"],
  "mermaid fence": ["```mermaid", "graph TD", "  A --> B", "```"],
  "{code-block}": ["```{code-block} python", "print(1)", "```"],
  "{list-table}": ["```{list-table}", "* - a", "  - b", "```"],
  "{csv-table}": ["```{csv-table}", "a,b", "1,2", "```"],
  "{figure}": ["```{figure} x.png", "Caption text", "```"],
  "nested colon admonition": [":::{tip}", "Tip.", ":::"],
  "nested backtick admonition": ["```{tip}", "Tip.", "```"],
  "nested dropdown": [":::{dropdown} Title", "Drop.", ":::"],
  "{card}": [":::{card} Card", "Body.", ":::"],
  "{div}": [":::{div}", "Div.", ":::"],
  "{rubric}": ["```{rubric} Rubric", "```"],
};
const BOXES = {
  note: (body) => L("::::::{note}", ...body, "::::::"),
  alert: (body) => L("> [!NOTE]", ...body.map((l) => (l ? `> ${l}` : ">"))),
  dropdown: (body) => L("::::::{dropdown} Box", ...body, "::::::"),
};
(async () => {
  for (const [kind, lines] of Object.entries(KINDS)) {
    for (const [boxName, box] of Object.entries(BOXES)) {
      const source = box(["Before.", "", ...lines, "", "After."]);
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
      const blocks = createMappedBlocks(page.document, context);
      const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
        tools: { blockSelection: {} }, blocks });
      const boxElement = page.document.querySelectorAll(".admonition")[0];
      const children = blocks.mappedChildren(boxElement);
      const name = (e) => { const r = blocks.blockRange(e); return `${e.tagName.toLowerCase()} ${r.line}-${r.endLine}`; };
      const out = [];
      for (const child of children) {
        const text = child.textContent.trim();
        const role = text === "Before." ? "Before" : text === "After." ? "After" : "K";
        for (const direction of role === "Before" ? ["down"] : role === "After" ? ["up"] : ["up", "down"]) {
          const neighbour = moves.moveNeighbour(child, direction);
          if (!neighbour) { out.push(`${role} ${direction}: none`); continue; }
          const a = blocks.blockRange(child), b = blocks.blockRange(neighbour);
          const run = fixture({ text: source });
          await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line,
            neighbourEndLine: b.endLine, direction });
          const [answer] = run.of("previewBlockMoveResult");
          out.push(`${role} ${direction}: ${answer?.ok ? "moved" : `refused (${answer?.reason})`}`);
        }
      }
      console.log(`${kind} | ${boxName} | children [${children.map(name).join(", ")}] | ${out.join("; ")}`);
    }
  }
})();
