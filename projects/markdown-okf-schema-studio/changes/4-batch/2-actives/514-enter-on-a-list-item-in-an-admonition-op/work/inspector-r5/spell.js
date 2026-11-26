// Own spellings: for each box opening, put "---" or a heading first in the body and compare the render
// with what firstBlockRefusal answers.
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { firstBlockRefusal } = o("src/core/mapping/boxFirstBlock.js");
const w = (open, opts = [], close = ":::", prefix = "", first = prefix) => ({ open, opts, close, prefix, first });
const C = [
  w(":::{div}", [":class: callout-tip", ""]),
  w(":::{div}", ["---", "class: [callout-tip]", "---"]),
  w(":::{div}", ["---", "class:", "  - callout-tip", "---"]),
  w(":::{div}", ["---", "name: x", "class: callout-tip", "---", ""]),
  w(":::{div}", ["---", "'class': 'callout-tip'", "---", ""]),
  w(":::{div}", [":name: x", ":class: callout-tip", ""]),
  w(":::{div}", [":class: foo callout-tip", ""]),
  w(":::{div}", [" :class: callout-tip", ""]),
  w(":::{div}", ["  :class: callout-tip", ""]),
  w(":::{div}", [":class:callout-tip", ""]),
  w(":::{div}", ["", ":class: callout-tip", ""]),
  w(":::{container}", [":class: callout-tip", ""]),
  w(":::{div}  ", [":class: callout-tip", ""]),
  w("```{div}", [":class: callout-tip", ""], "```"),
  w("> :::{div}", ["> :class: callout-tip", ">"], "> :::", "> "),
  w(">:::{div}", [">:class: callout-tip", ">"], ">:::", ">"),
  w("- :::{div}", ["  :class: callout-tip", ""], "  :::", "  "),
  w("::::{div .callout-tip}", [], "::::"),
  w(':::{div id=x class="callout-tip"}'),
  w(":::{div class=callout-tip}"),
  w(":::{.callout-tip #id}"),
  w(':::{.callout-note title="x"}'),
  w("::: {.callout-note}"),
  w(":::{ note }"), w(":::{note .foo}"), w(":::{versionadded} 1"), w(":::{VersionAdded} 1"), w(":::{Note}"), w(":::{DIV}", [":class: callout-tip", ""]),
  w(":::{admonition}", [":class: tip", ""]), w(":::{dropdown}"), w("::: {note}"), w(":::{note}", [":class: callout-tip", ""]),
  w(":::{div} extra", [":class: callout-tip", ""]),
  w("::: div", [":class: callout-tip", ""]),
  w(":::{callout}"), w(":::{callout-note}"), w(":::{exercise}"), w(":::{note}", ["---", "class: x", "---"]),
];
const sum = async (source) => {
  const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
  const boxes = page.document.querySelectorAll("aside, details, [data-okf-github-alert]")
    .filter((e) => /admonition|callout/u.test(e.getAttribute("class") ?? ""));
  const text = page.document.querySelectorAll("p").map((e) => e.textContent.trim()).join("|");
  const titles = page.document.querySelectorAll(".admonition-title, summary, .callout-title").map((e) => e.textContent.trim()).join("|");
  return { boxes: boxes.length, titles, before: /Before\./.test(page.document.querySelectorAll("aside, details").map((e)=>e.textContent).join(" ")), all: text };
};
(async () => {
  for (const c of C) {
    for (const [kind, block] of [["rule", "---"], ["head", "## Headword"]]) {
      const p = c.prefix, blank = p.trimEnd();
      const make = (a, b) => [c.open, ...c.opts, p + a, blank, p + b, blank, p + "Tail.", c.close, ""].join("\n");
      const good = make("Before.", block);
      const bad = make(block, "Before.");
      try {
        const g = await sum(good);
        if (!g.boxes) { console.log(`nobox ${kind} ${JSON.stringify(c.open)} ${JSON.stringify(c.opts)}`); continue; }
        const texts = good.split("\n");
        const first = 2 + c.opts.length;
        const refusal = firstBlockRefusal(texts, first, { line: first + 2, endLine: first + 2 });
        let b, err;
        try { b = await sum(bad); } catch (e) { err = e.message; }
        const broken = err ? `THROWS ${err}` : (!b.before || b.titles !== g.titles) ? `BROKEN titles ${JSON.stringify(g.titles)}->${JSON.stringify(b.titles)} shows=${b.before}` : "ok";
        const verdict = broken !== "ok" && !refusal ? "MISSED" : broken === "ok" && refusal ? "OVER" : "agree";
        console.log(`${verdict} ${kind} ${JSON.stringify(c.open)} ${JSON.stringify(c.opts)} refused=${Boolean(refusal)} ${broken}`);
      } catch (e) { console.log(`ERR ${kind} ${JSON.stringify(c.open)} ${e.message}`); }
    }
  }
})();
