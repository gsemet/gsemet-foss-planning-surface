// Claim B at this head: many spellings of a {div} (and other) callout. For each that renders a box,
// the chord that would put `---` or a heading first is sent; an accepted move must leave the box with
// its title and every word.
// Usage: node --import ./scripts/register-myst-patches.mjs <this> <buildRoot>
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");

const OPEN = ["{div}", "{ div }", " {div}", "{DIV}", "{Div}", "{div .x}", "{div .callout-tip}", "{.x .callout-tip}",
  '{div class="callout-tip"}', '{div class="x callout-tip"}', "{div class=callout-tip}", "{.callout-tip}", "{div}   ",
  "{container}", "{admonition} T", "{note}", "{tip}", "{dropdown} T", "{div #id}", "{#id .callout-tip}", "{container} callout-tip"];
const OPT = {
  none: [], colon: [":class: callout-tip"], colonTwo: [":class: x callout-tip"], colonQuoted: [':class: "callout-tip"'],
  colonUpper: [":CLASS: callout-tip"], colonList: [":class: [callout-tip]"], colonName: [":name: a", ":class: callout-tip"],
  colonAfter: [":class: callout-tip", ":name: a"], colonSpaced: [":class:    callout-tip   "], colonIndented: ["  :class: callout-tip"],
  yaml: ["---", "class: callout-tip", "---"], yamlList: ["---", "class: [x, callout-tip]", "---"],
  yamlBlock: ["---", "class:", "  - x", "  - callout-tip", "---"], yamlQuotedKey: ["---", '"class": callout-tip', "---"],
  yamlFlow: ["---", "{class: callout-tip}", "---"], yamlEscape: ["---", 'class: "callout\\x2dtip"', "---"],
  yamlAnchor: ["---", "name: &c callout-tip", "class: *c", "---"], yamlFolded: ["---", "class: >", "  callout-tip", "---"],
  yamlUpper: ["---", "Class: callout-tip", "---"], yamlMulti: ["---", 'class: "x', '  callout-tip"', "---"],
  yamlMerge: ["---", "<<: {class: callout-tip}", "---"], yamlClasses: ["---", "classes: callout-tip", "---"],
};
const SPOIL = { rule: ["---"], heading: ["## Headword"] };
const summary = (page) => {
  const box = page.document.querySelectorAll("aside, details").filter((e) => /admonition|callout/u.test(e.getAttribute("class") ?? ""));
  return {
    boxes: box.length,
    titles: page.document.querySelectorAll(".admonition-title, summary, .callout-title").map((e) => e.textContent.trim()).join("|"),
    words: ["Firstword", "Lastword", "Headword"].filter((w) => box.some((e) => e.textContent.includes(w))).join(","),
  };
};
(async () => {
  const counts = { spellings: 0, boxes: 0, sent: 0, moved: 0, refused: 0, broken: 0, throwsSource: 0 };
  for (const open of OPEN) for (const [on, opt] of Object.entries(OPT)) for (const [sn, sp] of Object.entries(SPOIL)) for (const gap of ["blank", "tight"]) {
    const lines = [`::::${open}`, ...opt, ...(gap === "blank" ? [""] : []), "Firstword.", "", ...sp, "", "Lastword.", "::::"];
    const source = `${lines.join("\n")}\n`;
    counts.spellings += 1;
    let page; try { page = await renderMappedPage(source, "/w/a.md", "file:///w/a.md"); } catch { counts.throwsSource += 1; continue; }
    const before = summary(page);
    if (!before.boxes || !before.words.includes("Firstword") || !before.words.includes("Lastword")) continue;
    counts.boxes += 1;
    const first = lines.indexOf("Firstword.") + 1;
    const other = lines.indexOf(sp[0], first) + 1;
    const run = fixture({ text: source });
    counts.sent += 1;
    await run.send("previewBlockMove", { line: first, endLine: first, neighbourLine: other, neighbourEndLine: other, direction: "down" });
    const [r] = run.of("previewBlockMoveResult");
    if (!r?.ok) { counts.refused += 1; continue; }
    counts.moved += 1;
    const written = run.document.getText();
    let after; try { after = summary(await renderMappedPage(written, "/w/a.md", "file:///w/a.md")); } catch (error) { after = { boxes: -1, titles: `THROWS ${error.message}`, words: "" }; }
    if (before.boxes !== after.boxes || before.titles !== after.titles || before.words !== after.words) {
      counts.broken += 1;
      console.log(`BROKEN ${open}|${on}|${sn}|${gap} ${JSON.stringify(before)} -> ${JSON.stringify(after)} :: ${JSON.stringify(source)}`);
    }
  }
  console.log(JSON.stringify(counts));
})();
