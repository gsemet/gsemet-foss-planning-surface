// Pairs of blocks in a box (direct, in a list item, in a quote of an item). Every element with words:
// PART = the opened lines lack one of its words; FENCE / TAG = the opened lines hold one fence line
// or one tag line of a pair without the other; ERASE-TAG as TAG. Usage: node ... <this> <buildRoot>
const path = require("node:path");
const root = process.argv[2];
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");
let n = 0;
const w = () => `w${(n++).toString(36)}z`;
const K = {
  para: () => [w()], two: () => [w(), w()], lazy: () => [`> ${w()}`, w()], setext: () => [w(), "==="], setext2: () => [w(), w(), "---"],
  head: () => [`## ${w()}`], hr: () => ["***"], quote: () => [`> ${w()}`], bq2: () => [`> ${w()}`, ">", `> ${w()}`],
  indented: () => [`    ${w()}`, `    ${w()}`], tilde: () => ["~~~", w(), "~~~"], openfence: () => ["```", w()],
  comment: () => ["<!--", w(), "-->"], pre: () => ["<pre>", w(), "", w(), "</pre>"], script: () => ["<textarea>", "", w(), "</textarea>"],
  divblk: () => ["<div>", w(), "</div>"], divsplit: () => ["<div>", "", w(), "", "</div>"], spanml: () => [`<span>${w()}`, `${w()}</span>`],
  emml: () => [`a <em>${w()}`, "", `${w()}</em> b`], open: () => ["<div>", "", w()], close: () => [w(), "", "</div>"],
  deflist: () => [w(), `: ${w()}`], defdl: () => [w(), `: ${w()}`, "", `  ${w()}`], hard: () => [`${w()}\`, w()],
  task: () => [`- [ ] ${w()}`, `- [x] ${w()}`], sub: () => [`- ${w()}`, `  ${w()}`, "", `  ${w()}`], table: () => [`| ${w()} |`, "| - |", `| ${w()} |`],
  pct: () => [`% ${w()}`], target: () => ["(lab)="], brk: () => ["+++"], role: () => [`{sub}\`${w()}\` ${w()}`],
  direct: () => [":::{tip}", w(), ":::"], code: () => ["```{code-block} py", w(), "```"], eval: () => ["```{eval-rst}", w(), "```"],
  fn: () => [`${w()}[^q]`, "", `[^q]: ${w()}`], ref: () => [`[${w()}][l]`, "", "[l]: http://example.com"],
  attr: () => ["{.cls}", w()], line: () => [`| ${w()}`, `| ${w()}`], linkml: () => [`[${w()}`, `${w()}](http://e.com)`],
  comm: () => [`${w()} <!-- c`, `d --> ${w()}`], img: () => [`${w()} ![a](x.png)`, w()], codespan: () => [`${w()} \`a`, `b\` ${w()}`],
};
const pre = (lines, first, rest) => lines.map((l, i) => ((i ? rest : first) + l).trimEnd());
const SHAPES = {
  direct: (a, b, g) => [...a, ...g, ...b],
  item: (a, b, g) => [...pre([...a, ...g, ...b], "- ", "  "), "- tail"],
  itemx: (a, b, g) => [...pre(["lead", ...g, ...a, ...g, ...b], "- ", "  "), "- tail"],
  quote: (a, b, g) => pre([...a, ...g, ...b], "> ", "> "),
  qitem: (a, b, g) => [...pre(pre([...a, ...g, ...b], "> ", "> "), "- ", "  "), "- tail"],
  nest: (a, b, g) => [...pre(["out", ...pre([...a, ...g, ...b], "- ", "  ")], "- ", "  "), "- tail"],
};
const BOXES = { note: (b) => [":::::{note}", ...b, ":::::"], alert: (b) => pre(b, "> ", "> ").map((l, i) => l).reduce((a, l) => [...a, l], ["> [!NOTE]"]) };
(async () => {
  const bad = new Map();
  let docs = 0, opens = 0;
  const names = Object.keys(K);
  for (const A of names) for (const B of names) for (const [sn, shape] of Object.entries(SHAPES)) for (const [bn, box] of Object.entries(BOXES)) for (const gap of [[], [""]]) {
    n = 0;
    const lines = box(shape(K[A](), K[B](), gap));
    const source = `${lines.join("\n")}\n`;
    let page;
    try { page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); } catch (e) { bad.set(`THROW ${A} ${B} ${sn} ${bn}`, [source]); continue; }
    docs++;
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const pairs = [];
    const stack = [];
    lines.forEach((l, i) => { for (const m of l.matchAll(/<(\/?)(div|span|em|pre|textarea)>/gu)) { if (!m[1]) stack.push([m[2], i + 1]); else { const k = stack.map((s) => s[0]).lastIndexOf(m[2]); if (k >= 0) { const [, s] = stack.splice(k)[0]; if (s !== i + 1) pairs.push([s, i + 1]); } } } });
    const inCode = [A, B].some((k) => ["indented", "tilde", "openfence", "code", "eval"].includes(k));
    const all = (e) => [e, ...e.children.flatMap(all)];
    for (const e of page.document.children.flatMap(all)) {
      const hit = e.closest(MAPPINGS_SELECTOR);
      if (!hit || e.closest(".footnotes")) continue;
      const words = [...new Set(e.textContent.match(/w[0-9a-z]z/gu) ?? [])];
      for (const exact of [false, true]) {
        const x = blocks.editingElementFor(hit, { exact });
        const r = x.sourceRange ?? blocks.blockRange(x.element);
        if (!r) continue;
        opens++;
        const text = lines.slice(r.line - 1, r.endLine).join("\n");
        let kind;
        if (words.some((v) => !text.includes(v))) kind = "PART";
        else if (!inCode && pairs.some(([s, t]) => (r.line <= s && s <= r.endLine) !== (r.line <= t && t <= r.endLine))) kind = "TAG";
        else {
          const fences = text.split("\n").filter((l) => /^[ \t>\-]*(:{3,}|`{3,}|~{3,})/u.test(l)).length;
          if (fences % 2 && A !== "openfence" && B !== "openfence") kind = "FENCE";
        }
        if (kind) {
          const key = `${kind} ${A} ${B} ${sn} ${bn}`;
          if (!bad.has(key)) bad.set(key, [source, e.tagName, exact, `${r.line}-${r.endLine}`, words]);
        }
      }
    }
  }
  console.log(`${docs} documents, ${opens} opens, ${bad.size} rows`);
  for (const [k, v] of bad) console.log(`${k} ${JSON.stringify(v)}`);
})();
