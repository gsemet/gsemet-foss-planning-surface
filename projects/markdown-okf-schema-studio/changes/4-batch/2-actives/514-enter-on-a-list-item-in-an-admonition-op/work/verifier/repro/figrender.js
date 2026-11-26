// The documents left by erasing the block that Enter opens, as the head renders them.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const { renderMyst } = require(path.join(process.argv[2], "out/src/core/render/mystRenderer.js"));
const cases = {
  "gap-note after": "::::{note}\n\n  | a | b |\n  | - | - |\n  | 1 | 2 |\n  ```\n::::\n\nAfter.\n",
  "gap-alert after": "> [!NOTE]\n>\n>   | a | b |\n>   | - | - |\n>   | 1 | 2 |\n>   ```\n\nAfter.\n",
  "gap-fig before": "::::{note}\n- item\n\n  ```{figure} x.png\n  Caption text\n  ```\n\n- next item\n::::\n",
  "gap-fig after": "::::{note}\n- item\n\n  ```{figure} x.png\n\n- next item\n::::\n",
};
(async () => {
  for (const [name, source] of Object.entries(cases)) {
    const { html } = await renderMyst(source);
    console.log(`=== ${name} ${JSON.stringify(source)}`);
    console.log(html.replace(/ data-[a-z-]+="[^"]*"/gu, "").replace(/\n+/gu, " "));
  }
})();
