// Prints the body markup of a dropdown whose body starts with dashes, and the mapped lines of the
// blocks of a box that has a block of options and a rule, as the build renders them.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const { renderMappedPage } = require(path.join(root, "out", "test/session/mappedHtmlDom.js"));
const dump = (e, d) => {
  const line = e.getAttribute("data-sphinx-source-line");
  console.log(`${"  ".repeat(d)}<${e.tagName.toLowerCase()} ${e.getAttribute("class") ?? ""}>${line === null ? "" : ` [${line}-${e.getAttribute("data-sphinx-source-end-line") ?? line}]`}${e.children.length ? "" : ` ${JSON.stringify(e.textContent.trim().slice(0, 30))}`}`);
  for (const c of e.children) dump(c, d + 1);
};
(async () => {
  for (const [name, source] of [
    ["dropdown, dashes first after an erase", ":::{dropdown} T\n\n---\n\nAfter.\n:::\n\nEnd.\n"],
    ["options block + rule", ":::{note}\n---\nclass: x\n---\nBefore.\n\n---\n\nAfter.\n:::\n"],
    ["options block + rule, code before the rule", ":::{note}\n---\nclass: x\n---\n```py\nx\n```\n\n---\n\nAfter.\n:::\n"],
    ["options block + rule, nested tip before the rule", "::::{note}\n---\nclass: x\n---\n:::{tip}\nTip.\n:::\n\n---\n\nAfter.\n::::\n"],
  ]) {
    console.log(`=== ${name} ${JSON.stringify(source)}`);
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    for (const e of page.document.querySelectorAll("body")[0]?.children ?? page.document.children ?? []) dump(e, 0);
  }
})();
