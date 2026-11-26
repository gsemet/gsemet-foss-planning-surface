// The DOM of cards whose body starts with or holds `---`, and of the titled admonition left with `---`
// first, with one build (head or base).
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const tree = (e, depth = 0) => {
  const own = e.children.length ? "" : ` ${JSON.stringify(e.textContent.trim().slice(0, 40))}`;
  const cls = e.getAttribute("class"); const hidden = e.getAttribute("hidden") !== null && e.getAttribute("hidden") !== undefined ? " hidden" : "";
  return `${"  ".repeat(depth)}<${e.tagName.toLowerCase()}${cls ? ` .${cls.replace(/ /g, ".")}` : ""}${e.getAttribute("data-source-line") ? ` L${e.getAttribute("data-source-line")}` : ""}${hidden}>${own}\n${e.children.map((c) => tree(c, depth + 1)).join("")}`;
};
const SHAPES = [
  ["r6 item 27: card in note, Alpha --- Beta", "::::{note}\n:::{card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n"],
  ["card at top level, Alpha --- Beta", ":::{card}\nAlpha\n\n---\n\nBeta\n:::\n"],
  ["titled card in note, Alpha --- Beta", "::::{note}\n:::{card} T\nAlpha\n\n---\n\nBeta\n:::\n::::\n"],
  ["backtick card in note, Alpha --- Beta --- Gamma", "::::{note}\n```{card}\nAlpha\n\n---\n\nBeta\n\n---\n\nGamma\n```\n::::\n"],
  ["card in note, blank then --- first", "::::{note}\n:::{card}\n\n---\n\nAlpha\n\nBeta\n:::\n::::\n"],
  ["card in note, --- first with no blank", "::::{note}\n:::{card}\n---\nAlpha\n\nBeta\n:::\n::::\n"],
  ["card in alert, Alpha --- Beta", "> [!NOTE]\n> :::{card}\n> Alpha\n>\n> ---\n>\n> Beta\n> :::\n"],
  ["card in dropdown, Alpha --- Beta", "::::{dropdown} D\n:::{card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n"],
  ["grid card in note", "::::::{note}\n::::{grid}\n:::{grid-item-card}\nAlpha\n\n---\n\nBeta\n:::\n::::\n::::::\n"],
  ["titled admonition left with --- first", "::::{admonition} Title words\n\n\n---\n\nLast\n::::\n\nEnd\n"],
  ["note left with --- first", "::::{note}\n\n\n---\n\nLast\n::::\n\nEnd\n"],
];
(async () => {
  for (const [name, source] of SHAPES) {
    console.log(`=== ${name} ${JSON.stringify(source)}`);
    try { const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); console.log(page.document.children.map((c) => tree(c, 1)).join("").trimEnd()); }
    catch (error) { console.log(`  THROWS ${error.message}`); }
  }
})();
