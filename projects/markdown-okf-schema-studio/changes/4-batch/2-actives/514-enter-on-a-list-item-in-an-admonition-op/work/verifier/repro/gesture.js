// One gesture through the real renderer, page helpers and PreviewManager of one build.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <file.md> <leaf text> <click|enter> [erase|keep]
const fs = require("node:fs");
const path = require("node:path");
const [root, file, wanted, gesture, action] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const source = fs.readFileSync(file, "utf8");
(async () => {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
  const all = (e) => [e, ...e.children.flatMap(all)];
  // The innermost mapped element that reads exactly the wanted text.
  const found = all(page.document).filter((e) => e.getAttribute("data-sphinx-source-line") !== null && e.textContent.trim() === wanted).pop();
  const hit = gesture === "enter" ? found : all(found).pop().closest("[data-sphinx-source-line]");
  const editing = blocks.editingElementFor(hit, { exact: gesture === "enter" });
  const r = editing.sourceRange ?? blocks.blockRange(editing.element);
  console.log(`${gesture} on "${wanted}" opens <${editing.element.tagName.toLowerCase()}> lines ${r.line}-${r.endLine}`);
  const run = fixture({ text: source });
  await run.send("previewEditOpen", { editId: "e1", line: r.line, endLine: r.endLine });
  const [answer] = run.of("previewEditSource");
  console.log(`editor text: ${JSON.stringify(answer?.originalText)} ${answer?.error ?? ""}`);
  if (!action) return;
  // An emptied textarea posts the block's own trailing line ending (blockEditor.ts textBoxText).
  const ending = answer.originalText.endsWith(String.fromCharCode(10)) ? String.fromCharCode(10) : "";
  const editedText = action === "erase" ? ending : answer.originalText;
  await run.send("previewEditSave", { editId: "e1", line: r.line, endLine: r.endLine, originalText: answer.originalText, editedText, final: true });
  console.log(`--- document after commit of ${action === "erase" ? "an erased editor" : "the unchanged text"} (writes: ${run.applyCalls.length}) ---`);
  console.log(run.document.getText());
  const after = await renderMappedPage(run.document.getText(), "/w/a.md", "file:///w/a.md");
  console.log(`tables rendered after: ${after.document.querySelectorAll("table").length}, before: ${page.document.querySelectorAll("table").length}`);
})();
