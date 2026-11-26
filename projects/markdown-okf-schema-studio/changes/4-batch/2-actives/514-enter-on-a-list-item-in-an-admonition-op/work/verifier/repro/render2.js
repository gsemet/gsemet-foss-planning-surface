// Rendered HTML of a note whose first body line is a thematic break, as one build renders it.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const { renderMyst } = require(path.join(root, "out/src/core/render/mystRenderer.js"));
const cases = [
  ":::{note}\n\n\n---\n\nAfter.\n:::\n",
  ":::{note}\n\n---\n\nBefore.\n\nAfter.\n:::\n",
];
(async () => {
  console.log(`build: ${path.basename(root)}`);
  for (const source of cases) {
    const { html } = await renderMyst(source);
    console.log(JSON.stringify(source), html.replace(/ data-[a-z-]+="[^"]*"/gu, "").replace(/\n+/gu, " "));
  }
})();
