// Enter on the first element of a tag name, then commit an erased editor (as the page posts it); prints the document.
// Usage: ... <this> <buildRoot> <cases.js> <caseName> <selector>
const path = require("node:path");
const [root, cases, name, selector] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
(async () => {
  const source = require(cases).find((c) => c[0] === name)[1];
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
  const e = page.document.querySelectorAll(selector)[0];
  const x = blocks.editingElementFor(e, { exact: true });
  const r = x.sourceRange ?? blocks.blockRange(x.element);
  const run = fixture({ text: source });
  await run.send("previewEditOpen", { editId: "e1", line: r.line, endLine: r.endLine });
  const [answer] = run.of("previewEditSource");
  console.log(`${name}: Enter on ${selector} opens ${r.line}-${r.endLine} ${JSON.stringify(answer.originalText)}`);
  await run.send("previewEditSave", { editId: "e1", line: r.line, endLine: r.endLine, originalText: answer.originalText, editedText: "\n", final: true });
  console.log("after erase: " + JSON.stringify(run.document.getText()));
})();
