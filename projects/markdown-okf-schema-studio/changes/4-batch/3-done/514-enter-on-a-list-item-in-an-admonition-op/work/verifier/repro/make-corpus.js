// Crafted documents: every directive kind at top level, after a box, inside boxes, and nested.
const fs = require("node:fs");
const path = require("node:path");
const dir = process.argv[2];
fs.mkdirSync(dir, { recursive: true });
const T = "```";
const directives = [
  `${T}{mermaid}\ngraph TD\n  A --> B\n${T}`,
  `${T}{math}\nx = 1\n${T}`,
  `$$\ny = 2\n$$`,
  `\\begin{equation}\nz = 3\n\\end{equation}`,
  `${T}{code-block} python\n:caption: C\nprint(1)\n${T}`,
  `${T}{code} python\nprint(4)\n${T}`,
  `${T}{code-cell} python\nprint(5)\n${T}`,
  `${T}python\nprint(6)\n${T}`,
  `${T}{list-table} Caption\n:header-rows: 1\n* - a\n  - b\n* - 1\n  - 2\n${T}`,
  `${T}{csv-table} Caption\n:header: a, b\n1, 2\n${T}`,
  `${T}{table} Caption\n| a | b |\n| - | - |\n| 1 | 2 |\n${T}`,
  `${T}{table}\n| a | b |\n| - | - |\n| 1 | 2 |\n${T}`,
  `${T}{figure} x.png\nCaption text\n\nLegend text\n${T}`,
  `${T}{image} x.png\n${T}`,
  "![alone](x.png)",
  `::::{grid} 2\n:::{grid-item-card} Title\nHeader\n^^^\nBody\n+++\nFooter\n:::\n::::`,
  `:::{card} Card title\nCard body\n:::`,
  `::::{tab-set}\n:::{tab-item} One\nText one\n:::\n::::`,
  `${T}{topic} Topic title\nTopic body one.\n\nTopic body two.\n${T}`,
  `${T}{sidebar} Side title\nSide body.\n${T}`,
  `${T}{epigraph}\nEpigraph body.\n${T}`,
  `${T}{versionadded} 1.2\nVersion body.\n\n- item\n${T}`,
  `${T}{versionchanged} 1.2 Inline body.\n${T}`,
  `${T}{deprecated} 1.2\n\n\nLate body.\n${T}`,
  `:::{warning} One line body\n:::`,
  `${T}{note} One line body\n${T}`,
  `:::{seealso} One line\n:::`,
  `${T}{dropdown} Drop title\nDrop body.\n\n- d item\n${T}`,
  `:::{admonition} Custom *title*\n:class: dropdown\nBody.\n:::`,
  `${T}{div} callout-note\nCallout body.\n${T}`,
  "<details>\n<summary>Sum</summary>\n\nDetail body.\n\n</details>",
  "| a | b |\n| - | - |\n| 1 | 2 |",
  `${T}{eval-rst}\n.. note:: x\n${T}`,
  `${T}{glossary}\nTerm\n  Definition\n${T}`,
  `${T}{rubric} Rub\n${T}`,
  `${T}{parsed-literal}\nlit\n${T}`,
  `${T}{line-block}\nl1\nl2\n${T}`,
  "> quoted\n> text",
  "- item one\n- item two\n\n  - sub",
  "Term\n: Definition",
];
const shift = (text) => text;
let n = 0;
const write = (name, body) => { fs.writeFileSync(path.join(dir, `${String(n++).padStart(4, "0")}-${name}.md`), `${body}\n`); };
const outer = (body) => `:::::::::{note}\nBefore.\n\n${body}\n\nAfter.\n:::::::::`;
const alert = (body) => ["> [!NOTE]", "> Before.", ">", ...body.split("\n").map((l) => (l ? `> ${l}` : ">")), ">", "> After."].join("\n");
write("all-top", directives.map(shift).join("\n\nBetween.\n\n"));
for (const d of directives) {
  write("top", `Before.\n\n${d}\n\nAfter.`);
  write("after-box", `:::{note}\nIn.\n:::\n\n${d}\n\nAfter.`);
  write("note", outer(d));
  write("alert", alert(d));
  write("dropdown", `:::::::::{dropdown} T\nBefore.\n\n${d}\n\nAfter.\n:::::::::`);
  write("nested", `::::::::::{note}\n${outer(d)}\n\n- item\n\n  ${d.split("\n").join("\n  ")}\n::::::::::`);
  write("unclosed", `:::::::::{note}\nBefore.\n\n${d}`);
  write("unclosed-quote", `> :::::::::{note}\n> Before.\n>\n${d.split("\n").map((l) => (l ? `> ${l}` : ">")).join("\n")}`);
  write("quote-note", outer(d).split("\n").map((l) => (l ? `> ${l}` : ">")).join("\n"));
  write("context-adm", `${T}{note}\n:class: myst-context-admonition\n${d}\n${T}`);
}
console.log(n);
