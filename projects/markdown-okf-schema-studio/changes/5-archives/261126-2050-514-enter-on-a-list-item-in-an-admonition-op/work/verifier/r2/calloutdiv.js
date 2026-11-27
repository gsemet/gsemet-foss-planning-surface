// The move chord on a block of a callout written as a {div} directive: the page's neighbour, the
// host's answer, the document written and what the callout shows afterwards.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");

const CASES = [
  ["{div} with :class:, ---", ":::{div}\n:class: callout-tip\n\nBefore.\n\n---\n\nAfter.\n:::\n"],
  ["{div} with :class:, heading", ":::{div}\n:class: callout-tip\n\nBefore.\n\n## Head\n\nAfter.\n:::\n"],
  ["{div} with class argument, ---", ":::{div} callout-note\nBefore.\n\n---\n\nAfter.\n:::\n"],
  ["{div} with class argument, heading", ":::{div} callout-note\nBefore.\n\n## Head\n\nAfter.\n:::\n"],
  ["fence div {.callout-tip}, --- (control)", "::: {.callout-tip}\nBefore.\n\n---\n\nAfter.\n:::\n"],
];
const show = async (source) => {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const box = page.document.querySelectorAll("aside")[0] ?? page.document.querySelectorAll("div")[0];
  return { page, text: box ? `<${box.tagName.toLowerCase()} ${box.getAttribute("class")}> ${JSON.stringify(box.textContent.replace(/\s+/g, " ").trim())} hr=${box.querySelectorAll("hr").length}` : "(none)" };
};
(async () => {
  for (const [name, source] of CASES) {
    const { page, text } = await show(source);
    console.log(`\n=== ${name}\nsource  ${JSON.stringify(source)}\nbefore  ${text}`);
    const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
    const blocks = createMappedBlocks(page.document, context);
    const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {}, tools: { blockSelection: {} }, blocks });
    const first = page.document.querySelectorAll("p").find((e) => e.textContent.trim() === "Before.");
    const neighbour = moves.moveNeighbour(first, "down");
    if (!neighbour) { console.log("chord down on Before.: the page sends nothing"); continue; }
    const a = blocks.blockRange(first), b = blocks.blockRange(neighbour);
    const run = fixture({ text: source });
    await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line, neighbourEndLine: b.endLine, direction: "down" });
    const [r] = run.of("previewBlockMoveResult");
    console.log(`chord down on Before. (${a.line}-${a.endLine} past ${b.line}-${b.endLine}): ok=${r.ok} reason=${r.reason}`);
    const written = run.document.getText();
    console.log(`written ${JSON.stringify(written)}`);
    try { console.log(`after   ${(await show(written)).text}`); } catch (error) { console.log(`after   THROWS ${error.message}`); }
  }
})();
