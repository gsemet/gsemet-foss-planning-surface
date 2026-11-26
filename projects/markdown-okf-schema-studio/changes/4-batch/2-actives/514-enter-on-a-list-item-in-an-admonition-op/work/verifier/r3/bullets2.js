// Every Known gaps bullet of the posted description, one case or more per claim: what a click and Enter
// open on the element named, and what is left after that editor is emptied and committed.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> [filter]
const path = require("node:path");
const [root, filter] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const all = (e) => [e, ...e.children.flatMap(all)];
const N = (body) => `:::{note}\n${body}\n:::\n\nEndword.\n`;
const tidy = (t) => t.replace(/\s+/gu, " ").trim();

const N6 = (body) => "::::::{note}\n" + body + "\n::::::\n\nEndword.\n";
const CASES = [
  ["O2", "tight item with directive, long outer fence", N6("- Itemword\n  :::{tip}\n  x\n  :::\n- Next"), [[null, "Itemword"]]],
  ["O2", "tight item with backtick directive, long outer fence", N6("- Itemword\n  ~~~{tip}\n  x\n  ~~~\n- Next"), [[null, "Itemword"]]],
  ["O4", "raw svg in colon directive in list item", N6("- Itemword\n\n  ::::{tip}\n  words\n\n  <svg viewBox=\"0 0 1 1\">\n  <title>pic</title>\n  </svg>\n  ::::\n- Next\n\nAfter."), [[null, "Itemword"]]],
  ["O4", "raw svg in backtick directive in list item", N6("- Itemword\n\n  ~~~{tip}\n  words\n\n  <svg viewBox=\"0 0 1 1\">\n  <title>pic</title>\n  </svg>\n  ~~~\n- Next\n\nAfter."), [[null, "Itemword"]]],
  ["B6", "closing tag paragraph with its opening tag earlier", N("<details>\n<summary>S</summary>\n\nPara</details>\n\nBeta"), [[null, "Para"]]],
  ["B6", "closing tag of an inline element split over two paragraphs", N("Alpha\n\n<b>One\n\nTwo</b>\n\nBeta"), [["P", "Two"]]],
  ["B6", "closing b alone", N("Alpha\n\nPara</b>\n\nBeta"), [[null, "Para"]]],
  ["B6", "closing span alone", N("Alpha\n\n<span>One\n\nPara</span>\n\nBeta"), [[null, "Para"], [null, "One"]]],
  ["B6", "closing div paragraph", N("<div>\n\nPara</div>\n\nBeta"), [[null, "Para"]]],
  ["B6", "r6 closing details first", N("Para</details>"), [[null, "Para"]]],
  ["O3", "formula under table, item", N("- | a |\n  | - |\n  | b |\n  $$ y = 2 $$"), [[null, "y = 2"]]],
];
(async () => {
  for (const [bullet, name, source, targets] of CASES) {
    if (filter && !bullet.startsWith(filter)) continue;
    console.log(`\n=== ${bullet} ${name} ${JSON.stringify(source)}`);
    let page; try { page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); } catch (error) { console.log(`  source THROWS ${error.message}`); continue; }
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const lines = source.split("\n");
    const mapped = page.document.querySelectorAll(MAPPINGS_SELECTOR);
    console.log(`  mapped ${mapped.map((e) => { const r = blocks.blockRange(e); return `<${e.tagName.toLowerCase()} ${r.line}-${r.endLine}>`; }).join("")}`);
    for (const [tag, text] of targets) {
      const found = all(page.document.querySelectorAll("main")[0] ?? page.document)
        .filter((e) => (!tag || e.tagName === tag) && (text.startsWith("=") ? tidy(e.textContent) === text.slice(1) : tidy(e.textContent).includes(text)));
      const leaf = found[found.length - 1];
      if (!leaf) { console.log(`  [${tag ?? ""} ${text}] no such element`); continue; }
      const hit = leaf.closest(MAPPINGS_SELECTOR);
      if (!hit) { console.log(`  [${tag ?? ""} ${text}] <${leaf.tagName}> under no mapped element`); continue; }
      const results = {};
      for (const [how, exact] of [["click", false], ["enter", true]]) {
        const x = blocks.editingElementFor(hit, { exact });
        const r = x.sourceRange ?? blocks.blockRange(x.element);
        results[how] = { tag: x.element.tagName.toLowerCase(), line: r.line, endLine: r.endLine };
        console.log(`  [${tag ?? ""} ${text}] ${how} on <${hit.tagName.toLowerCase()}> -> <${results[how].tag}> ${r.line}-${r.endLine} ${JSON.stringify(lines.slice(r.line - 1, r.endLine).join("\n"))}`);
      }
      const same = results.click.line === results.enter.line && results.click.endLine === results.enter.endLine;
      for (const how of same ? ["click"] : ["click", "enter"]) {
        const { line, endLine } = results[how];
        const run = fixture({ text: source });
        await run.send("previewEditOpen", { editId: "e1", line, endLine });
        const [answer] = run.of("previewEditSource");
        if (!answer || answer.originalText === undefined) { console.log(`    erase(${how}): no source ${JSON.stringify(answer)}`); continue; }
        await run.send("previewEditSave", { editId: "e1", line, endLine, originalText: answer.originalText, editedText: answer.originalText.endsWith("\n") ? "\n" : "", final: true });
        const written = run.document.getText();
        let after; try { const p = await renderMappedPage(written, "/w/a.md", "file:///w/a.md"); after = JSON.stringify(tidy(p.document.querySelectorAll("main")[0]?.textContent ?? p.document.textContent).slice(0, 100)); } catch (error) { after = `THROWS ${error.message}`; }
        console.log(`    erase(${same ? "both" : how}) writes ${JSON.stringify(written)}\n      page ${after}`);
      }
    }
  }
})();
