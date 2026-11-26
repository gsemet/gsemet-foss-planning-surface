// The chord down on the first paragraph of a note, whose next block then takes the first place:
// the document written and the HTML rendered from it.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const { renderMyst } = o("src/core/render/mystRenderer.js");
const L = (...l) => `${l.join("\n")}\n`;
const KINDS = {
  "thematic break": ["---"],
  "heading": ["## Head"],
  "field list": [":Author: Someone"],
};
const BOXES = {
  "colon note": (body) => L(":::{note}", ...body, ":::"),
  "backtick note": (body) => L("```{note}", ...body, "```"),
  "alert": (body) => L("> [!NOTE]", ...body.map((l) => (l ? `> ${l}` : ">"))),
};
const visible = (html) => html.replace(/ data-[a-z-]+="[^"]*"/gu, "").replace(/\n+/gu, " ");
(async () => {
  for (const [kind, lines] of Object.entries(KINDS)) {
    for (const [boxName, box] of Object.entries(BOXES)) {
      const source = box(["Before.", "", ...lines, "", "After."]);
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      const context = { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" };
      const blocks = createMappedBlocks(page.document, context);
      const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
        tools: { blockSelection: {} }, blocks });
      const adm = page.document.querySelectorAll(".admonition")[0];
      const [first] = blocks.mappedChildren(adm);
      const neighbour = moves.moveNeighbour ? moves.moveNeighbour(first, "down") : undefined;
      console.log(`=== ${kind} | ${boxName}\nsource   ${JSON.stringify(source)}\nbefore   ${visible((await renderMyst(source)).html)}`);
      if (!neighbour) { console.log("chord down on \"Before.\": no neighbour"); continue; }
      const a = blocks.blockRange(first), b = blocks.blockRange(neighbour);
      const run = fixture({ text: source });
      await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line,
        neighbourEndLine: b.endLine, direction: "down" });
      const [answer] = run.of("previewBlockMoveResult");
      if (!answer?.ok) { console.log(`chord down on "Before.": refused (${answer?.reason})`); continue; }
      console.log(`chord down on "Before.": moved\nwritten  ${JSON.stringify(run.document.getText())}\nafter    ${visible((await renderMyst(run.document.getText())).html)}`);
    }
  }
})();
