// Remaining Changes and Deliverables claims: callout title, version admonition body, unclosed
// admonition, text on an opening line, directives of a body, nested boxes, a box inside a list.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
const L = (...l) => `${l.join("\n")}\n`;
const tidy = (t) => t.replace(/\s+/gu, " ").trim();
const all = (e) => [e, ...e.children.flatMap(all)];

const SHAPES = [
  ["div callout (:class:)", L("::::{div}", ":class: callout-tip", "", "Alphaword", "", "Betaword", "::::"), ["=Tip", "Alphaword", "Betaword"]],
  ["div callout with title heading", L("::::{div}", ":class: callout-tip", "", "## Titleword", "", "Alphaword", "::::"), ["Titleword", "Alphaword"]],
  ["div callout in note", L("::::::{note}", "::::{div}", ":class: callout-tip", "", "Alphaword", "::::", "::::::"), ["=Tip", "=Note", "Alphaword"]],
  ["version, body after blank", L(":::{versionadded} 1.0", "", "", "Bodyword", ":::"), ["Bodyword", "1.0"]],
  ["version, body after options", L(":::{versionchanged} 2.0", ":class: x", "", "Bodyword", "", "Lastword", ":::"), ["Bodyword", "Lastword", "2.0"]],
  ["version, argument text and body", L(":::{deprecated} 3.0 Argword", "Bodyword", ":::"), ["Bodyword", "Argword"]],
  ["unclosed note, inner fence", L("::::{note}", "Alphaword", "", ":::{tip}", "Tipword", ":::"), ["Alphaword", "Tipword", "=Tip", "=Note"]],
  ["unclosed note, inner code", L(":::{note}", "Alphaword", "", "```python", "codeword", "```"), ["Alphaword", "codeword"]],
  ["unclosed backtick note, inner shorter code", L("````{note}", "Alphaword", "", "```python", "codeword", "```"), ["codeword"]],
  ["one-line warning", L(":::{warning} Onelineword", ":::"), ["Onelineword", "=Warning"]],
  ["warning with first line and body", L(":::{warning} Onelineword", "", "Bodyword", ":::"), ["Onelineword", "Bodyword"]],
  ["card title in note", L("::::{note}", ":::{card} Cardtitle", "Cardbody", ":::", "::::"), ["Cardtitle", "Cardbody"]],
  ["diagram", L("::::{note}", "Alphaword", "", ":::{mermaid}", "graph TD", "  A --> B", ":::", "::::"), ["graph TD"]],
  ["math directive", L("::::{note}", "Alphaword", "", ":::{math}", "y = 2", ":::", "::::"), ["y = 2"]],
  ["code-block", L("::::{note}", "Alphaword", "", ":::{code-block} python", ":caption: Capword", "", "codeword", ":::", "::::"), ["codeword", "Capword"]],
  ["fence code", L("> [!NOTE]", "> Alphaword", ">", "> ```py", "> codeword", "> ```"), ["codeword"]],
  ["nested boxes", L("::::::{note}", "Outerword", "", "::::{tip}", "Innerword", "", "Secondword", "::::", "::::::"), ["=Note", "=Tip", "Outerword", "Innerword", "Secondword"]],
  ["box in a list", L("- Itemword", "", "  ::::{note}", "  Alphaword", "", "  - Subword", "  ::::", "- Next"), ["Itemword", "=Note", "Alphaword", "Subword"]],
  ["alert in a list", L("- Itemword", "", "  > [!NOTE]", "  > Alphaword", "  >", "  > - Subword", "- Next"), ["Itemword", "=Note", "Alphaword", "Subword"]],
];

(async () => {
  for (const [name, source, words] of SHAPES) {
    console.log(`\n=== ${name} ${JSON.stringify(source)}`);
    let page; try { page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); } catch (error) { console.log(`  THROWS ${error.message}`); continue; }
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const lines = source.split("\n");
    console.log(`  mapped ${page.document.querySelectorAll(MAPPINGS_SELECTOR).map((e) => { const r = blocks.blockRange(e); return `<${e.tagName.toLowerCase()} ${r.line}-${r.endLine}>`; }).join("")}`);
    for (const word of words) {
      const found = all(page.document).filter((e) => e.tagName && (word.startsWith("=") ? tidy(e.textContent ?? "") === word.slice(1) : tidy(e.textContent ?? "").includes(word)));
      const leaf = found[found.length - 1];
      if (!leaf) { console.log(`  [${word}] no element shows it`); continue; }
      const hit = leaf.closest(MAPPINGS_SELECTOR);
      if (!hit) { console.log(`  [${word}] <${leaf.tagName}> under no mapped element`); continue; }
      for (const [how, exact] of [["click", false], ["enter", true]]) {
        const x = blocks.editingElementFor(hit, { exact });
        const r = x.sourceRange ?? blocks.blockRange(x.element);
        console.log(`  [${word}] ${how} on <${leaf.tagName.toLowerCase()}> -> <${x.element.tagName.toLowerCase()} ${r.line}-${r.endLine}> ${JSON.stringify(lines.slice(r.line - 1, r.endLine).join("\n"))}`);
      }
    }
  }
})();
