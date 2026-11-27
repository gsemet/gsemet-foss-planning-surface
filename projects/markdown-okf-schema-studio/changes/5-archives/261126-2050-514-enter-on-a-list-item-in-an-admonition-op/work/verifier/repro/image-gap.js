// Known gap "image in a box": what a click on it opens, and what the move chord of each other
// block of the box does, through the real renderer, page helpers and PreviewManager.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const lines = (...l) => `${l.join("\n")}\n`;
const quote = (text) => lines("> [!NOTE]", ...text.replace(/\n$/u, "").split("\n").map((l) => (l ? `> ${l}` : ">")));
const images = {
  "image-only paragraph": "![alone](x.png)",
  "{image} directive": "```{image} x.png\n```",
  "{image} directive with options": "```{image} x.png\n:alt: a\n:width: 20px\n```",
};
const around = {
  paragraphs: (i) => ["Before.", "", i, "", "After."],
  "list before": (i) => ["- one", "- two", "", i, "", "After."],
  "list after": (i) => ["Before.", "", i, "", "- one", "- two"],
  "code around": (i) => ["```python", "a = 1", "```", "", i, "", "```python", "b = 2", "```"],
  "no blank lines": (i) => (i.startsWith("`") ? ["Before.", i, "After."] : ["# H", i, "", "After."]),
  "image first": (i) => [i, "", "After.", "", "Last."],
  "image last": (i) => ["First.", "", "Before.", "", i],
};
(async () => {
  for (const [kind, image] of Object.entries(images)) {
    for (const [name, make] of Object.entries(around)) {
      for (const box of ["note", "alert"]) {
        const body = make(image).join("\n");
        const source = box === "note" ? lines("::::{note}", body, "::::") : quote(body);
        const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
        const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
        const blocks = createMappedBlocks(page.document, context);
        const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
          tools: { blockSelection: {} }, blocks });
        const img = page.document.querySelectorAll("img")[0];
        const clicked = img?.closest("[data-sphinx-source-line]");
        const open = clicked ? blocks.editingElementFor(clicked, {}) : undefined;
        const range = open ? open.sourceRange ?? blocks.blockRange(open.element) : undefined;
        const out = [`${kind} | ${name} | ${box} | click on the image opens ${open ? `<${open.element.tagName.toLowerCase()}> ${range.line}-${range.endLine} of ${source.split("\n").length - 1}` : "nothing (no <img>)"}`];
        const boxElement = page.document.querySelectorAll(".admonition")[0];
        for (const child of blocks.mappedChildren(boxElement)) {
          for (const direction of ["up", "down"]) {
            const neighbour = moves.moveNeighbour(child, direction);
            if (!neighbour) continue;
            const a = blocks.blockRange(child), b = blocks.blockRange(neighbour);
            const run = fixture({ text: source });
            await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line,
              neighbourEndLine: b.endLine, direction });
            const [answer] = run.of("previewBlockMoveResult");
            const crossed = Math.min(a.line, b.line) < source.split("\n").findIndex((l) => /alone|\{image\}/u.test(l)) + 1
              && Math.max(a.line, b.line) > source.split("\n").findIndex((l) => /alone|\{image\}/u.test(l)) + 1;
            out.push(`    ${direction} ${a.line}-${a.endLine} <> ${b.line}-${b.endLine}${crossed ? " ACROSS-IMAGE" : ""}: ${answer?.ok ? "MOVED" : `refused (${answer?.reason})`}`);
          }
        }
        console.log(out.join("\n"));
      }
    }
  }
})();
