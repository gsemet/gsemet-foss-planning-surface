// Renders small sources with one build; prints the text of the body or the renderer's error.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const { renderMappedPage } = require(path.join(root, "out", "test/session/mappedHtmlDom.js"));
(async () => {
  for (const [name, source] of [
    ["div in a note, dashes first", "::::{note}\n:::{div}\n---\nDiv text.\n\nMore.\n:::\n::::\n"],
    ["div at top level, dashes first", ":::{div}\n---\nDiv text.\n\nMore.\n:::\n\nAfter.\n"],
    ["div in a note, rule after text (as written by an erase)", "::::{note}\n:::{div}\n\n---\n\nMore.\n:::\n::::\n"],
    ["card in a note, dashes first", "::::{note}\n:::{card}\n---\nCard text.\n\nMore.\n:::\n::::\n"],
  ]) {
    console.log(`=== ${name} ${JSON.stringify(source)}`);
    try {
      const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
      console.log(`rendered ${JSON.stringify((page.document.querySelectorAll("aside, div")[0]?.textContent ?? "").replace(/\s+/g, " ").trim())} hr=${page.document.querySelectorAll("hr").length}`);
    } catch (error) {
      console.log(`THROWS ${error.constructor.name}: ${error.message}`);
    }
  }
})();
