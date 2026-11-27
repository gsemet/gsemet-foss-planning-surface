const path = require("node:path");
const root = process.argv[2];
const { renderMyst } = require(path.join(root, "out/src/core/render/mystRenderer.js"));
(async () => { for (const s of [[":::{dropdown} Title", "", "", "---", "", "Beta", ":::"], [":::{dropdown} Title", "Alpha", "", "---", "", "Beta", ":::"]]) console.log(JSON.stringify((await renderMyst(`${s.join("\n")}\n`)).html)); })();
