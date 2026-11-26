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

const CASES = [
  // [bullet, name, source, [[tag or null, text]]]
  ["B1", "formula right under text", N("Alpha\n$$ y = 2 $$"), [[null, "y = 2"]]],
  ["B1", "formula under a quote", N("> Alpha\n$$ y = 2 $$"), [[null, "y = 2"]]],
  ["B1", "formula after +++", N("+++\nx\n$$ y = 2 $$"), [[null, "y = 2"]]],
  ["B1", "formula under item text", N("- Item\n  $$\n  y = 2\n  $$\n- Next"), [[null, "y = 2"], [null, "Item"]]],
  ["B1", "formula in table cell", N("| a |\n| - |\n| $$ y = 2 $$ |"), [[null, "y = 2"]]],
  ["B1", "formula after other text", N("Alpha $$ y = 2 $$ beta"), [[null, "y = 2"]]],
  ["B1", "formula followed by text in item", N("- Item\n\n  $$ y = 2 $$ after\n- Next"), [[null, "y = 2"]]],
  ["B1", "formula followed by text, longer paragraph", N("Alpha\n\n***\n$$ y = 2 $$ after\nmore"), [[null, "y = 2"]]],
  ["B1", "inline HTML in multi-line definition", N("Term\n  : ***\n    <span>kept</span> words"), [["SPAN", "kept"]]],
  ["B1", "unpaired details", N("<details>\n<summary>Sumword</summary>\n\nword\n\n</details>\n<table>\n<tr><td>cellword</td></tr>\n</table>"), [["SUMMARY", "Sumword"], ["TD", "cellword"], ["P", "word"]]],
  ["B1", "table under a closing tag", N("<div>\n\nword\n\n</div>\n<table>\n<tr><td>cellword</td></tr>\n</table>"), [["TD", "cellword"]]],
  ["B1", "text under a closing tag", N("<div>\nword\n</div>\nafterword"), [[null, "afterword"]]],
  ["B1", "details in details", N("<details>\n<summary>Outer</summary>\n<details>\n<summary>Innerword</summary>\n\nword\n\n</details>\n</details>"), [["SUMMARY", "Innerword"]]],
  ["B1", "html element closes outside list", N("- Itemword\n\n  <div>\n\n  ![a](x.png)\n\n</div>\n\nTail"), [[null, "Itemword"]]],
  ["B2", "later paragraph of tight item after code", N("- Item\n  ```{math}\n  y = 1\n  ```\n  laterword\n- Next"), [["P", "laterword"]]],
  ["B2", "later paragraph of tight item after code fence", N("- Item\n  ```py\n  x\n  ```\n  laterword\n- Next"), [["P", "laterword"]]],
  ["B3", "options block with later --- line", ":::{note}\n---\nclass: x\n---\nAlphaword\n\nBetaword\n\n---\n:::\n", [["P", "Alphaword"], ["P", "Betaword"]]],
  ["B3", "dropdown options block with later ---", ":::{dropdown} T\n---\nopen: true\n---\nAlphaword\n\n---\n\nBetaword\n:::\n", [["P", "Alphaword"], ["P", "Betaword"]]],
  ["B4", "image paragraph", N("Alpha\n\n![a](x.png)\n\nBeta"), [["IMG", ""]]],
  ["B4", "image directive", "::::{note}\nAlpha\n\n:::{image} x.png\n:::\n\nBeta\n::::\n", [["IMG", ""]]],
  ["B5", "table caption", "::::{note}\nAlpha\n\n:::{table} Capword\n| a |\n| - |\n| cell |\n:::\n\nBeta\n::::\n", [[null, "Capword"]]],
  ["B5", "tab panel", ":::::{note}\n::::{tab-set}\n:::{tab-item} One\nPanelword\n\nSecondword\n:::\n::::\n:::::\n", [["P", "Panelword"], ["BUTTON", "One"]]],
  ["B6", "one opening tag alone", N("Alpha\n\n<b>One\n\nTwo</b>\n\nBeta"), [[null, "One"], [null, "Two"]]],
  ["B6", "closing tag paragraph", N("Alpha\n\nPara</details>\n\nBeta"), [[null, "Para"]]],
  ["B7", "note left open ending on quoted tip", ":::{note}\nAlphaword\n\n> :::{tip}\n> Tipword\n> :::\n", [["P", "=Tip"], ["P", "Alphaword"], ["P", "Tipword"], ["ASIDE", "Tipword"], ["BLOCKQUOTE", "Tipword"]]],
  ["O1", "tight item followed by HTML comment", N("- Itemword\n  <!-- hidden -->\n- Next"), [[null, "Itemword"]]],
  ["O1", "tight item followed by HTML", N("- Itemword\n  <div>x</div>\n- Next"), [[null, "Itemword"]]],
  ["O1", "tight item followed by link definition", N("- Itemword\n\n  [ref]: https://example.org\n- Next"), [[null, "Itemword"]]],
  ["O1", "tight item followed by footnote definition", N("- Itemword[^f]\n\n  [^f]: Footword\n- Next"), [[null, "Itemword"]]],
  ["O1", "tight item followed by target", N("- Itemword\n  (lab)=\n- Next"), [[null, "Itemword"]]],
  ["O1", "tight item followed by percent comment", N("- Itemword\n  % hidden\n- Next"), [[null, "Itemword"]]],
  ["O2", "item with code", N("- Itemword\n\n  ```py\n  x\n  ```\n\nBeta"), [[null, "Itemword"]]],
  ["O2", "item with second paragraph", N("- Itemword\n\n  Second\n\nBeta"), [[null, "Itemword"]]],
  ["O2", "tight item with directive", N("- Itemword\n  :::{tip}\n  x\n  :::\n- Next"), [[null, "Itemword"]]],
  ["O3", "formula line under a table", N("| a |\n| - |\n| b |\n$$ y = 2 $$"), [[null, "y = 2"]]],
  ["O3", "formula line under a piped table", N("a | b\n- | -\n1 | 2\n$$ y = 2 $$"), [[null, "y = 2"]]],
  ["O4", "raw svg in directive in list item", N("- Itemword\n\n  ::::{tip}\n  words\n\n  <svg viewBox=\"0 0 1 1\">\n  <title>pic</title>\n  </svg>\n  ::::\n- Next\n\nAfter."), [[null, "Itemword"]]],
  ["O6", "alert paragraph with a lazy line", "> [!NOTE]\n> Alphaword\nlazy\n>\n> Betaword\n", [["P", "Alphaword"]]],
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
