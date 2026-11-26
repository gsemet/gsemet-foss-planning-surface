// New fence probe of this round: list items that hold a directive, in every kind of box.
// For every click and Enter on every element of a box: the opened lines cut no fence; the Enter
// ranges of two blocks held by the same list item do not overlap.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");

const strip = (l) => l.replace(/^(?:\s*>)*\s*(?:(?:[-*+]|\d+[.)])\s+)?/u, "");
function fences(source) {
  const out = [], stack = [];
  const lines = source.replace(/\n$/u, "").split("\n");
  lines.forEach((raw, i) => {
    const l = strip(raw), n = i + 1;
    const top = stack[stack.length - 1];
    if (top?.kind === "$$") { if (l === "$$") { out.push({ s: top.s, e: n, closed: true }); stack.pop(); } return; }
    if (top?.kind === "tex") { if (l.startsWith("\\end{")) { out.push({ s: top.s, e: n, closed: true }); stack.pop(); } return; }
    const m = /^(:{3,}|`{3,}|~{3,})(.*)$/u.exec(l);
    if (m && top?.kind === "f" && m[1][0] === top.f[0] && m[1].length >= top.f.length && m[2].trim() === "") {
      out.push({ s: top.s, e: n, closed: true }); stack.pop(); return;
    }
    const literal = top?.kind === "f" && top.f[0] !== ":" && !top.directive;
    if (literal) return;
    if (m) { stack.push({ kind: "f", s: n, f: m[1], directive: m[2].startsWith("{") }); return; }
    if (l === "$$") stack.push({ kind: "$$", s: n });
    else if (l.startsWith("\\begin{")) stack.push({ kind: "tex", s: n });
  });
  for (const open of stack) out.push({ s: open.s, e: lines.length, closed: false });
  return out;
}
const cut = ([a, b], f) => !((a === f.s && b === f.e) || (f.s < a && (b < f.e || (!f.closed && b <= f.e)))
  || (a <= f.s && f.e <= b) || b < f.s || a > f.e);

const T = "```";
const D = {"table":["| aaa | bbb |","| --- | --- |","| ccc | ddd |"],"html":["<div>","htmlword here","</div>"],"quote":["> quotedword","> secondword"],"indented":["","    indentedword = 1"],"rule":["***"],"heading":["## Headword"],"image":["![altword](x.png)"],"imagePara":["![altword](x.png) captionword"],"mathLabel":["$$","yvalue = 2","$$ (eqlabel)"],"mathOne":["$$ yvalue = 2 $$"],"amsmath":["\\begin{align}","zvalue = 3","\\end{align}"],"target":["(mytarget)=","paraword"],"percent":["% hiddencomment","paraword"],"field":[":fieldname: fieldvalue"],"deflist":["Termword",": Defword"],"tasks":["- [ ] taskword","- [x] doneword"],"fenceCode":["```python","codeword = 6","```"],"nested":["- innerword","  contword"],"para":["paraword","contword"]};
const ind = (lines, n) => lines.map((l) => (l ? " ".repeat(n) + l : l));
const ITEMS = {
  loose: (d) => ["- Text", "", ...ind(d, 2)],
  tight: (d) => ["- Text", ...ind(d, 2)],
  tail: (d) => ["- Text", ...ind(d, 2), "  tail text", "- next"],
  looseTail: (d) => ["- Text", "", ...ind(d, 2), "", "  tail para", "", "- next"],
  first: (d) => [`- ${d[0]}`, ...ind(d.slice(1), 2), "  tail", "- next"],
  only: (d) => [`- ${d[0]}`, ...ind(d.slice(1), 2)],
  wrapped: (d) => ["- Text", "  wrapped", ...ind(d, 2), "- next"],
  ordered: (d) => ["1. Text", "", ...ind(d, 3), "", "   para two"],
  sub: (d) => ["- Text", "  - sub", ...ind(d, 4), "- next"],
  comment: (d) => ["- Text", "  <!-- c -->", ...ind(d, 2)],
  heading: (d) => ["- # Head", ...ind(d, 2)],
  quote: (d) => ["- Text", "", "  > quoted", ...ind(d, 2)],
  afterCode: (d) => ["- Text", "  ```py", "  x", "  ```", "  tail", ...ind(d, 2)],
  twice: (d) => ["- Text", ...ind(d, 2), ...ind(d, 2), "  end"],
  trailing: (d) => ["- Text", ...ind(d, 2), "", "", "- next"],
};
const O = "`````````";
const q = (lines, prefix = "> ") => lines.map((l) => (l ? prefix + l : prefix.trimEnd()));
const BOXES = {
  colon: (b) => [":::::::::{note}", ...b, ":::::::::"],
  backtick: (b) => [`${O}{note}`, ...b, O],
  tilde: (b) => ["~~~~~~~~~{note}", ...b, "~~~~~~~~~"],
  alert: (b) => ["> [!NOTE]", ...q(b)],
  listAlert: (b) => ["- outer", "", "  > [!TIP]", ...q(b, "  > ")],
  listNote: (b) => ["- outer", "", ...ind([":::::::::{note}", ...b, ":::::::::"], 2)],
  dropdown: (b) => [":::::::::{dropdown} T", ...b, ":::::::::"],
  version: (b) => [":::::::::{versionadded} 1.0", ...b, ":::::::::"],
  callout: (b) => [":::::::::{.callout-note}", ...b, ":::::::::"],
  calloutDiv: (b) => [":::::::::{div}", ":class: callout-tip", "", ...b, ":::::::::"],
  options: (b) => [":::::::::{note}", ":class: dropdown", "", ...b, ":::::::::"],
  titled: (b) => [":::::::::{admonition} Title", ...b, ":::::::::"],
  unclosed: (b) => [":::::::::{note}", ...b],
  quoted: (b) => q([":::::::::{note}", ...b, ":::::::::"]),
  nestedBox: (b) => ["::::::::::{note}", ":::::::::{tip}", ...b, ":::::::::", "::::::::::"],
};

(async () => {
  const counts = { docs: 0, opens: 0, cuts: 0, overlaps: 0, inBoxItems: 0 };
  const cutKinds = new Map();
  for (const [bn, box] of Object.entries(BOXES)) for (const [dn, d] of Object.entries(D)) for (const [in_, item] of Object.entries(ITEMS)) {
    const source = `${[...box(["Before.", "", ...item(d), "", "After."]), "", "End."].join("\n")}\n`;
    const list = fences(source);
    const page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md");
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    counts.docs += 1;
    const isBox = (e) => /(^| )admonition( |$)|callout-/u.test(e.getAttribute("class") ?? "") || e.getAttribute("data-okf-github-alert") !== null;
    const inBox = (e) => { for (let p = e.parentElement; p; p = p.parentElement) if (isBox(p)) return true; return false; };
    const all = (e) => [e, ...e.children.flatMap(all)];
    const range = (hit, exact) => { const x = blocks.editingElementFor(hit, { exact }); const r = x.sourceRange ?? blocks.blockRange(x.element); return { r: [r.line, r.endLine], el: x.element }; };
    const seen = new Set();
    const mapped = page.document.querySelectorAll(MAPPINGS_SELECTOR).filter(inBox);
    for (const element of mapped) {
      for (const [gesture, target, exact] of [["click", element, false], ["enter", element, true],
        ...all(element).filter((e) => e.children.length === 0).map((e) => ["leaf", e, false])]) {
        const hit = target.closest(MAPPINGS_SELECTOR);
        const { r, el } = range(hit, exact);
        counts.opens += 1;
        const bad = list.filter((f) => cut(r, f));
        if (bad.length && !seen.has(String(r))) {
          seen.add(String(r)); counts.cuts += 1;
          const key = `${bn}|${dn}|${in_}`;
          if (!cutKinds.has(key)) cutKinds.set(key, `CUT ${key} ${gesture} <${el.tagName}> ${r} cuts ${bad.map((f) => `${f.s}-${f.e}${f.closed ? "" : "(open)"}`)} :: ${JSON.stringify(source)}`);
        }
      }
      if (element.closest("li") && element.tagName !== "LI" && element.tagName !== "UL" && element.tagName !== "OL") {
        const got = range(element, true).r;
        const src = source.split(String.fromCharCode(10)).slice(got[0] - 1, got[1]).join(" ");
        const words = all(element).filter((e) => e.children.length === 0 && !/admonition-title/.test(e.getAttribute("class") ?? "")).flatMap((e) => e.textContent.match(/[A-Za-z]{3,}|[0-9]+/g) ?? []).filter((w) => !["Warning", "Tip", "Added", "version"].includes(w));
        const missing = words.filter((w) => !src.includes(w));
        counts.content = (counts.content ?? 0) + 1;
        if (missing.length) { counts.wrong = (counts.wrong ?? 0) + 1; console.log(`WRONG ${bn}|${dn}|${in_} <${element.tagName}> ${got} text ${JSON.stringify(element.textContent.trim().slice(0, 40))} missing ${missing.slice(0, 4)}`); }
      }
      if (element.tagName === "LI") {
        counts.inBoxItems += 1;
        const kids = blocks.mappedChildren(element).map((c) => ({ c, r: range(c, true).r }));
        for (let a = 0; a < kids.length; a += 1) for (let b = a + 1; b < kids.length; b += 1) {
          const [x, y] = [kids[a].r, kids[b].r];
          const disjoint = x[1] < y[0] || y[1] < x[0];
          if (!disjoint) {
            counts.overlaps += 1;
            console.log(`OVERLAP ${bn}|${dn}|${in_} <${kids[a].c.tagName}> ${x} <${kids[b].c.tagName}> ${y}`);
          }
        }
      }
    }
  }
  for (const line of cutKinds.values()) console.log(line);
  console.log(JSON.stringify(counts));
})();
