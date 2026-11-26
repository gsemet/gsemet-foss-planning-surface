// Property probe of the real renderer, page helpers and session at one build:
// inside a box, no click, Enter, chord or erase may cut a fence; a move keeps every block.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot> <corpusDir> [--verbose]
const fs = require("node:fs");
const path = require("node:path");
const [root, dir] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");

const SOURCE = "/w/a.md", DOC = "file:///w/a.md";
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
const cuts = (range, list) => list.filter((f) => cut(range, f));

async function load(source) {
  const page = await renderMappedPage(source, SOURCE, DOC);
  const context = { activeSourceFile: SOURCE, documentId: DOC };
  const blocks = createMappedBlocks(page.document, context);
  const moves = installBlockMoves({ document: page.document, window: {}, context, host: {}, state: {},
    tools: { blockSelection: {} }, blocks });
  return { page, blocks, moves };
}
const isBox = (e) => e.matches("aside.admonition,details.admonition,[data-okf-github-alert]")
  || /\bcallout-/u.test(e.getAttribute("class") ?? "") || e.tagName === "DETAILS";
const inBox = (e) => { for (let p = e.parentElement; p; p = p.parentElement) if (isBox(p)) return true; return false; };
const all = (e) => [e, ...e.children.flatMap(all)];
const norm = (t) => t.replace(/\s+/gu, " ").trim();
const words = (html) => (norm(html).match(/\S+/gu) ?? []).sort().join(" ");
const pageText = (p) => words(all(p.document).filter((e) => e.children.length === 0).map((e) => e.textContent).join(" "));
const shape = (p) => all(p.document).filter((e) => isBox(e) || /figure|PRE|TABLE|UL/u.test(e.tagName))
  .map((e) => e.tagName + ":" + (e.getAttribute("class") ?? "")).sort().join(",");

(async () => {
  const counts = { docs: 0, opens: 0, openCuts: 0, moves: 0, refused: 0, moveBreaks: 0, erases: 0, eraseBreaks: 0 };
  for (const name of fs.readdirSync(dir).sort()) {
    if (!/-(note|alert|dropdown|nested|unclosed|unclosed-quote|quote-note)\.md$/u.test(name)) continue;
    const source = fs.readFileSync(path.join(dir, name), "utf8");
    const list = fences(source);
    const page = await load(source);
    counts.docs += 1;
    const mapped = page.page.document.querySelectorAll(MAPPINGS_SELECTOR).filter(inBox);
    const seen = new Set();
    for (const element of mapped) {
      for (const [gesture, target, exact] of [["click", element, false], ["enter", element, true],
        ...all(element).filter((e) => e.children.length === 0).map((e) => ["leaf", e, false])]) {
        const hit = target.closest(MAPPINGS_SELECTOR);
        const editing = page.blocks.editingElementFor(hit, { exact });
        let range = editing.sourceRange;
        if (!range) range = page.blocks.blockRange(editing.element);
        const pair = [range.line, range.endLine];
        counts.opens += 1;
        const bad = cuts(pair, list);
        if (bad.length && !seen.has(String(pair))) {
          seen.add(String(pair)); counts.openCuts += 1;
          console.log(`OPEN-CUT ${name} ${gesture} <${editing.element.tagName} ${editing.element.getAttribute("class") ?? ""}> ${pair} cuts ${bad.map((f) => `${f.s}-${f.e}${f.closed ? "" : "(open)"}`)}`);
        }
      }
      for (const direction of ["up", "down"]) {
        const neighbour = page.moves.moveNeighbour(element, direction);
        if (!neighbour) continue;
        const a = page.blocks.blockRange(element), b = page.blocks.blockRange(neighbour);
        const run = fixture({ text: source });
        await run.send("previewBlockMove", { line: a.line, endLine: a.endLine, neighbourLine: b.line,
          neighbourEndLine: b.endLine, direction });
        const [answer] = run.of("previewBlockMoveResult");
        counts.moves += 1;
        if (!answer?.ok) { counts.refused += 1; console.log(`REFUSED ${name} ${direction} ${a.line}-${a.endLine} <> ${b.line}-${b.endLine}: ${answer?.reason}`); continue; }
        const after = await load(run.document.getText());
        if (pageText(after.page) !== pageText(page.page) || shape(after.page) !== shape(page.page)) {
          counts.moveBreaks += 1;
          console.log(`MOVE-BREAK ${name} ${direction} ${a.line}-${a.endLine} <${element.tagName}> <> ${b.line}-${b.endLine} <${neighbour.tagName}> text=${pageText(after.page) === pageText(page.page)} shape=${shape(after.page) === shape(page.page)}`);
        }
      }
    }
  }
  console.log(JSON.stringify(counts));
})();
