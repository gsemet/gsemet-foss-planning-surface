// Refusal paths of a move inside an alert (spec Evidence step 6), page neighbour then host.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const L = (...l) => `${l.join("\n")}\n`;
const CASES = {
  "alert, comment line between list and paragraph": L("> [!TIP]", "> - a", "> - b", ">", "> <!-- x -->", ">", "> Para."),
  "alert, link definition between list and paragraph": L("> [!TIP]", "> - a", "> - b", ">", "> [ref]: https://example.org", ">", "> Para."),
  "top level, comment line between list and paragraph": L("- a", "- b", "", "<!-- x -->", "", "Para."),
  "top level, link definition between list and paragraph": L("- a", "- b", "", "[ref]: https://example.org", "", "Para."),
  "alert, list item then paragraph with a percent comment": L("> [!TIP]", "> - a", "> - b", ">", "> % hidden", ">", "> Para."),
};
(async () => {
  for (const [title, source] of Object.entries(CASES)) {
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
    const blocks = createMappedBlocks(page.document, context);
    const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
      tools: { blockSelection: {} }, blocks });
    const list = page.document.querySelectorAll("ul")[0];
    let neighbour;
    if (moves.moveNeighbour && title.startsWith("alert")) neighbour = moves.moveNeighbour(list, "down");
    else { const top = blocks.topLevelMappedBlocks(); neighbour = top[top.indexOf(list) + 1]; }
    const a = blocks.blockRange(list), b = blocks.blockRange(neighbour);
    const run = fixture({ text: source });
    await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line, neighbourEndLine: b.endLine, direction: "down" });
    const [answer] = run.of("previewBlockMoveResult");
    console.log(`${title}: list ${a.line}-${a.endLine}, neighbour <${neighbour.tagName.toLowerCase()} class="${neighbour.getAttribute("class") ?? ""}"> ${b.line}-${b.endLine}: ${answer.ok ? "MOVED " + JSON.stringify(run.document.getText()) : "refused: " + answer.reason}`);
  }
  const { planBlockMove } = o("src/core/mapping/blockMove.js");
  const plan = (title, text, first, second) => console.log(`planner, ${title}: ${JSON.stringify(planBlockMove(text, first, second))}`);
  plan("one block in a quote, one outside", L("> A", "", "B"), { line: 1, endLine: 1 }, { line: 3, endLine: 3 });
  plan("two separate quotes", L("> A", "", "> B"), { line: 1, endLine: 1 }, { line: 3, endLine: 3 });
  plan("alert block and the paragraph after the alert", L("> [!NOTE]", "> A", "", "B"), { line: 2, endLine: 2 }, { line: 4, endLine: 4 });
})();
