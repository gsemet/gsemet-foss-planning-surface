// Derives items-md.js from items-content.js: the same boxes and item shapes, with plain Markdown
// blocks (no directive) in the list item.
const fs = require("node:fs");
const path = require("node:path");
let s = fs.readFileSync(path.join(__dirname, "items-content.js"), "utf8");
const a = s.indexOf("const D = {");
const b = s.indexOf("const ind = ");
const tick = String.fromCharCode(96).repeat(3);
const kinds = {
  table: ["| aaa | bbb |", "| --- | --- |", "| ccc | ddd |"],
  html: ["<div>", "htmlword here", "</div>"],
  quote: ["> quotedword", "> secondword"],
  indented: ["", "    indentedword = 1"],
  rule: ["***"],
  heading: ["## Headword"],
  image: ["![altword](x.png)"],
  imagePara: ["![altword](x.png) captionword"],
  mathLabel: ["$$", "yvalue = 2", "$$ (eqlabel)"],
  mathOne: ["$$ yvalue = 2 $$"],
  amsmath: ["\\begin{align}", "zvalue = 3", "\\end{align}"],
  target: ["(mytarget)=", "paraword"],
  percent: ["% hiddencomment", "paraword"],
  field: [":fieldname: fieldvalue"],
  deflist: ["Termword", ": Defword"],
  tasks: ["- [ ] taskword", "- [x] doneword"],
  fenceCode: [`${tick}python`, "codeword = 6", tick],
  nested: ["- innerword", "  contword"],
  para: ["paraword", "contword"],
};
s = `${s.slice(0, a)}const D = ${JSON.stringify(kinds)};\n${s.slice(b)}`;
fs.writeFileSync(path.join(__dirname, "items-md.js"), s);
