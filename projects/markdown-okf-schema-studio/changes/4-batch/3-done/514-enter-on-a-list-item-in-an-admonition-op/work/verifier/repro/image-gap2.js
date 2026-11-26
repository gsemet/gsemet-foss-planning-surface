// Second pass on the Known gap "image in a box": more spellings of the image, more neighbours,
// and a count of the moves whose two blocks sit on both sides of the image.
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
  "backtick {image}": "```{image} x.png\n```",
  "colon {image}": ":::{image} x.png\n:::",
  "linked image paragraph": "[![alone](x.png)](https://example.org)",
  "two images paragraph": "![alone](x.png) ![alone](y.png)",
};
const neighbours = {
  paragraph: "Text.",
  heading: "## Head",
  table: "| a | b |\n| - | - |\n| 1 | 2 |",
  list: "- one\n- two",
  quote: "> Quoted.",
  code: "```python\na = 1\n```",
  admonition: ":::{tip}\nTip.\n:::",
};
(async () => {
  const tally = {};
  let shapes = 0, crossing = 0, crossingMoved = 0, clicks = 0, clicksOnWholeBox = 0, noImg = 0;
  const reasons = {};
  for (const [kind, image] of Object.entries(images)) {
    for (const [beforeName, before] of Object.entries(neighbours)) {
      for (const [afterName, after] of Object.entries(neighbours)) {
        for (const separator of ["blank", "none"]) {
          for (const box of ["note", "alert"]) {
            const body = (separator === "blank" ? [before, "", image, "", after] : [before, image, after]).join("\n");
            const source = box === "note" ? lines("::::::{note}", body, "::::::") : quote(body);
            const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
            const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
            const blocks = createMappedBlocks(page.document, context);
            const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
              tools: { blockSelection: {} }, blocks });
            const img = page.document.querySelectorAll("img")[0];
            if (!img) { noImg += 1; continue; }
            shapes += 1;
            const open = blocks.editingElementFor(img.closest("[data-sphinx-source-line]"), {});
            clicks += 1;
            const boxElement = page.document.querySelectorAll(".admonition")[0];
            if (open.element === boxElement) clicksOnWholeBox += 1;
            const key = `${kind} | ${separator} | ${open.element === boxElement ? "whole box" : "own <" + open.element.tagName.toLowerCase() + ">"}`;
            tally[key] = (tally[key] ?? 0) + 1;
            const imageLine = source.split("\n").findIndex((l) => /x\.png/u.test(l)) + 1;
            for (const child of blocks.mappedChildren(boxElement)) {
              for (const direction of ["up", "down"]) {
                const neighbour = moves.moveNeighbour(child, direction);
                if (!neighbour) continue;
                const a = blocks.blockRange(child), b = blocks.blockRange(neighbour);
                const first = a.line < b.line ? a : b, second = a.line < b.line ? b : a;
                if (!(first.endLine < imageLine && second.line > imageLine)) continue;
                crossing += 1;
                const run = fixture({ text: source });
                await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line,
                  neighbourEndLine: b.endLine, direction });
                const [answer] = run.of("previewBlockMoveResult");
                if (answer?.ok) {
                  crossingMoved += 1;
                  if (crossingMoved <= 6) console.log(`MOVED ${kind} | ${beforeName} / ${afterName} | ${separator} | ${box} | ${a.line}-${a.endLine} ${direction} ${b.line}-${b.endLine}\n  ${JSON.stringify(source)}\n  ${JSON.stringify(run.document.getText())}`);
                } else {
                  reasons[answer?.reason] = (reasons[answer?.reason] ?? 0) + 1;
                }
              }
            }
          }
        }
      }
    }
  }
  console.log(JSON.stringify(tally, null, 1));
  console.log(JSON.stringify({ shapes, noImg, clicks, clicksOnWholeBox, crossing, crossingMoved, reasons }));
})();
