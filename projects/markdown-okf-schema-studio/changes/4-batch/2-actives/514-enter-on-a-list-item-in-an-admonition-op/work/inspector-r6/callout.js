// For many spellings of a div: does it render a callout, and is a heading / a --- moved first refused?
const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const { renderMyst } = o("src/core/render/mystRenderer.js");
const { firstBlockRefusal } = o("src/core/mapping/boxFirstBlock.js");
const open = [":::{div}", ":::{div} ", "::: {div}", ":::{ div }", ":::{DIV}", ":::{div .callout-note}", ":::{div .a.callout-note}", ":::{.a.callout-note}",
  ":::{div #x.callout-note}", ":::{div #x .callout-note}", ":::{div class=callout-note}", ":::{div class = \"callout-note\"}", ":::{div class=\"a callout-note\"}", ":::{.callout-note}",
  ":::{div} x", "```{div}", "~~~{div}", ":::{div} .callout-note"];
const opts = [[], [":class: callout-note"], [":class: a callout-note"], ["  :class: callout-note"], [" :class: callout-note"], ["", ":class: callout-note"],
  [":name: z", ":class: callout-note"], ["---", "class: callout-note", "---"], ["---", "class: [a, callout-note]", "---"], ["---", "class:", "  - callout-note", "---"],
  [" ---", "class: callout-note", "---"], ["----", "class: callout-note", "----"], ["---", "Class: callout-note", "---"], ["---", "\"class\": \"callout\x2dnote\"", "---"],
  [":Class: callout-note"], [":class:callout-note"], ["---", "class: callout-note", "--- "], ["---", "class: callout-note", "----"]];
(async () => {
  const wraps = [["", ""], ["> ", "> "], ["- ", "  "], ["::::{note}\n", ""]];
  const gaps = new Map();
  let count = 0, boxes = 0;
  for (const op of open) for (const opt of opts) for (const [first, rest] of wraps) {
    const nested = first.startsWith("::::");
    const fence = op.trim().replace(/\{.*$/u, "").trim();
    const raw = [op, ...opt, "", "Alpha", "", "## Head", fence];
    const lines = nested ? ["::::{note}", ...raw, "::::"] : raw.map((l, i) => (i ? rest : first) + l);
    const source = `${lines.join("\n")}\n`;
    count++;
    let html;
    try { html = (await renderMyst(source)).html; } catch (e) { gaps.set(`THROW ${op} ${JSON.stringify(opt)}`, 1); continue; }
    const callout = /<aside[^>]*class="admonition simple/u.test(html) && !nested || (nested && /<aside[^>]*class="admonition simple/u.test(html));
    if (!callout) continue;
    boxes++;
    const at = lines.findIndex((l) => l.endsWith("Alpha")) + 1;
    const head = lines.findIndex((l) => l.endsWith("## Head")) + 1;
    if (!firstBlockRefusal(lines, at, { line: head, endLine: head })) gaps.set(`NOT REFUSED ${JSON.stringify(first)} ${op} ${JSON.stringify(opt)}`, 1);
  }
  console.log(`${count} spellings, ${boxes} render a callout, ${gaps.size} gaps`);
  for (const k of gaps.keys()) console.log(k);
})();
