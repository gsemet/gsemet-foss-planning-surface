// Attacks the first-place refusal: in many box spellings, with lines that render nothing above
// the body, every move chord on every mapped block of the box. After each accepted move: the box
// keeps its title and every word it showed.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
const { createMappedBlocks } = o("src/page/features/mappedBlocks.js");
const { installBlockMoves } = o("src/page/features/blockMoves.js");
const { MAPPINGS_SELECTOR } = o("src/page/features/pageRuntime.js");

const T = "```";
const q = (lines, p = "> ") => lines.map((l) => (l ? p + l : p.trimEnd()));
const colon = (open) => (b) => [`::::${open}`, ...b, "::::"];
const BOXES = {
  calloutDiv: (b) => ["::::{div}", ":class: callout-tip", "", ...b, "::::"],
  calloutDivTight: (b) => ["::::{div}", ":class: callout-tip", ...b, "::::"],
  calloutContainer: (b) => ["::::{container} callout-note", ...b, "::::"],
  calloutNoteClass: (b) => ["::::{note}", ":class: callout-tip", "", ...b, "::::"],
  important: colon("{important}"), caution: colon("{caution}"), error: colon("{error}"), upper: colon("{Note}"),
  note: colon("{note}"), attention: colon("{attention}"), hint: colon("{hint}"), danger: colon("{danger}"),
  seealso: colon("{seealso}"), noteSpaceAfter: colon("{note}   "), admonitionBare: colon("{admonition}"),
  admonitionTitled: colon("{admonition} Ttl"), dropdown: colon("{dropdown}"), dropdownT: colon("{dropdown} Ttl"),
  version: colon("{versionchanged} 2.0"), deprecated: colon("{deprecated} 2.0"),
  options: (b) => [":::{note}", ":class: x", "", ...b, ":::"],
  calloutDot: colon("{.callout-note}"), calloutPandoc: colon(" {.callout-note}"),
  tilde: (b) => ["~~~~{tip}", ...b, "~~~~"], tick: (b) => [`${T}\`{warning}`, ...b, `${T}\``],
  indented: (b) => ["- x", "", ...[":::{note}", ...b, ":::"].map((l) => (l ? `  ${l}` : l))],
  ordered: (b) => ["1. x", "", ...[":::{note}", ...b, ":::"].map((l) => (l ? `   ${l}` : l))],
  threeSpaces: (b) => ["   :::{note}", ...b.map((l) => (l ? `   ${l}` : l)), "   :::"],
  nested: (b) => [":::::{note}", "::::{tip}", ...b, "::::", ":::::"],
  alert: (b) => ["> [!NOTE]", ...q(b)], alertNoSpace: (b) => [">[!TIP]", ...q(b)],
  alertInList: (b) => ["- x", "", "  > [!NOTE]", ...q(b, "  > ")],
  noteInAlert: (b) => ["> [!NOTE]", ...q([":::{tip}", ...b, ":::"])],
  noteInAlertNoBlank: (b) => ["> :::{tip}", ...q(b), "> :::"],
  quotedNote: (b) => q([":::{note}", ...b, ":::"]),
  unclosed: (b) => [":::{note}", ...b],
};
const PREFIX = {
  none: [], comment: ["<!-- c -->"], commentBlank: ["<!-- c -->", ""], linkdef: ["[l]: http://e.com", ""],
  percent: ["% c", ""], blank: ["", ""], target: ["(lbl)=", ""],
};
const SPOILERS = {
  hr3: ["---"], hr5: ["-----"], hrSpaced: ["--- "], hrDash: ["- - -"], hrUnder: ["___"], hrStar: ["***"],
  atx: ["## Headword"], atx1: ["# Headword"], atx6: ["###### Headword"], setext: ["Headword", "==="],
  setext2: ["Headword", "---"], atxAttr: ["## Headword {#h}"], atxIndented: ["  ## Headword"],
  targetHeading: ["(t)=", "## Headword"], commentHeading: ["<!-- k -->", "## Headword"],
  listHeading: ["- ## Headword"], quoteHeading: ["> ## Headword"], bold: ["**Boldword**"],
  htmlHeading: ["<h2>Headword</h2>"], yaml: ["---", "zzz"],
};

const summary = (page) => {
  const box = page.document.querySelectorAll("aside, details, [data-okf-github-alert]")
    .filter((e) => /admonition|callout/u.test(e.getAttribute("class") ?? "") || e.getAttribute("data-okf-github-alert") !== null);
  return {
    titles: page.document.querySelectorAll(".admonition-title, summary, .callout-title")
      .map((e) => e.textContent.trim()).join("|"),
    boxes: box.length,
    words: ["Firstword", "Lastword", "Headword", "Boldword", "zzz"].filter((w) => box.some((e) => e.textContent.includes(w))).join(","),
    rules: page.document.querySelectorAll("hr").length,
  };
};

(async () => {
  const counts = { docs: 0, moved: 0, refused: 0, broken: 0 };
  const reasons = new Map();
  const broken = new Map();
  for (const [bn, box] of Object.entries(BOXES)) for (const [pn, pre] of Object.entries(PREFIX)) for (const [sn, sp] of Object.entries(SPOILERS)) {
    const source = `${box([...pre, "Firstword.", "", ...sp, "", "Lastword."]).join("\n")}\n`;
    let page; try { page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); } catch (error) { reasons.set(`${bn} | source throws ${sn}`, 1); continue; }
    const blocks = createMappedBlocks(page.document, { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" });
    const moves = installBlockMoves({ document: page.document, window: {}, context: { activeSourceFile: "/w/a.md", documentId: "file:///w/a.md" }, host: {}, state: {}, tools: { blockSelection: {} }, blocks });
    counts.docs += 1;
    const before = summary(page);
    const seen = new Set();
    for (const block of page.document.querySelectorAll(MAPPINGS_SELECTOR)) {
      for (const direction of ["up", "down"]) {
        let neighbour;
        try { neighbour = moves.moveNeighbour(block, direction); } catch { continue; }
        if (!neighbour) continue;
        const a = blocks.blockRange(block), b = blocks.blockRange(neighbour);
        const message = { line: a.line, endLine: a.endLine, neighbourLine: b.line, neighbourEndLine: b.endLine, direction };
        const key = JSON.stringify([Math.min(a.line, b.line), Math.max(a.line, b.line)]);
        if (seen.has(key)) continue;
        seen.add(key);
        const run = fixture({ text: source });
        await run.send("previewBlockMove", message);
        const [result] = run.of("previewBlockMoveResult");
        if (!result?.ok) { counts.refused += 1; { const k = `${bn} | ${/^A heading/.test(result.reason) ? "heading" : /^A ---/.test(result.reason) ? "rule" : "text-between"}`; reasons.set(k, (reasons.get(k) ?? 0) + 1); } continue; }
        counts.moved += 1;
        const written = run.document.getText();
        let after; try { after = summary(await renderMappedPage(written, "/w/a.md", "file:///w/a.md")); } catch (error) { after = { titles: `THROWS ${error.message}`, boxes: -1, words: "" }; }
        const what = ["titles", "boxes", "words"].filter((k) => before[k] !== after[k]);
        if (what.length) {
          counts.broken += 1;
          const k = `${bn}|${sn}|${what}`;
          if (!broken.has(k)) broken.set(k, `BROKEN ${bn}|${pn}|${sn} ${direction} ${key} ${what.map((w) => `${w}: ${before[w]} -> ${after[w]}`).join("; ")} :: ${JSON.stringify(source)} => ${JSON.stringify(written)}`);
        }
      }
    }
  }
  for (const line of broken.values()) console.log(line);
  for (const [r, n] of reasons) console.log(`REASON ${n} ${r}`);
  console.log(JSON.stringify(counts));
})();
