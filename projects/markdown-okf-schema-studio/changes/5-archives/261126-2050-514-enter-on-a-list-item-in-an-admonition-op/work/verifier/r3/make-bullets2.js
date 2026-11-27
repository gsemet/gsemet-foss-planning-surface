// bullets.js with other cases: correct fence nesting, tag-paragraph variants and the bare shapes.
const fs = require("node:fs");
const path = require("node:path");
const src = fs.readFileSync(path.join(__dirname, "bullets.js"), "utf8");
const start = src.indexOf("const CASES = [");
const end = src.indexOf("(async () => {");
const cases = String.raw`const N6 = (body) => "::::::{note}\n" + body + "\n::::::\n\nEndword.\n";
const CASES = [
  ["O2", "tight item with directive, long outer fence", N6("- Itemword\n  :::{tip}\n  x\n  :::\n- Next"), [[null, "Itemword"]]],
  ["O2", "tight item with backtick directive, long outer fence", N6("- Itemword\n  ~~~{tip}\n  x\n  ~~~\n- Next"), [[null, "Itemword"]]],
  ["O4", "raw svg in colon directive in list item", N6("- Itemword\n\n  ::::{tip}\n  words\n\n  <svg viewBox=\"0 0 1 1\">\n  <title>pic</title>\n  </svg>\n  ::::\n- Next\n\nAfter."), [[null, "Itemword"]]],
  ["O4", "raw svg in backtick directive in list item", N6("- Itemword\n\n  ~~~{tip}\n  words\n\n  <svg viewBox=\"0 0 1 1\">\n  <title>pic</title>\n  </svg>\n  ~~~\n- Next\n\nAfter."), [[null, "Itemword"]]],
  ["B6", "closing tag paragraph with its opening tag earlier", N("<details>\n<summary>S</summary>\n\nPara</details>\n\nBeta"), [[null, "Para"]]],
  ["B6", "closing tag of an inline element split over two paragraphs", N("Alpha\n\n<b>One\n\nTwo</b>\n\nBeta"), [["P", "Two"]]],
  ["B6", "closing b alone", N("Alpha\n\nPara</b>\n\nBeta"), [[null, "Para"]]],
  ["B6", "closing span alone", N("Alpha\n\n<span>One\n\nPara</span>\n\nBeta"), [[null, "Para"], [null, "One"]]],
  ["B6", "closing div paragraph", N("<div>\n\nPara</div>\n\nBeta"), [[null, "Para"]]],
  ["B6", "r6 closing details first", N("Para</details>"), [[null, "Para"]]],
  ["O3", "formula under table, item", N("- | a |\n  | - |\n  | b |\n  $$ y = 2 $$"), [[null, "y = 2"]]],
];
`;
fs.writeFileSync(path.join(__dirname, "bullets2.js"), src.slice(0, start) + cases + src.slice(end));
