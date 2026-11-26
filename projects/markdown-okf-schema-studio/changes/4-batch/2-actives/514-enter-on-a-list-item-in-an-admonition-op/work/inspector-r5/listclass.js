// The host move of a heading to the first place of a callout whose class is a YAML list.
const path = require("node:path");
const [root] = process.argv.slice(2);
const o = (p) => require(path.join(root, "out", p));
const { renderMappedPage } = o("test/session/mappedHtmlDom.js");
const { fixture } = o("test/session/blockFixture.js");
(async () => {
  for (const cls of ["class: [callout-tip]", "class: callout-tip"]) {
    const source = [":::{div}", "---", cls, "---", "Before.", "", "## Headword", "", "Tail.", ":::", ""].join("\n");
    const run = fixture({ text: source });
    await run.send("previewBlockMove", { moveId: "m1", line: 7, endLine: 7, neighbourLine: 5, neighbourEndLine: 5, direction: "up" });
    console.log(cls, JSON.stringify(run.of("previewBlockMoveResult").map(({ ok, reason }) => [ok, reason])));
    const after = run.document.getText();
    const page = await renderMappedPage(after, "/w/a.md", "file:///w/a.md");
    console.log(JSON.stringify(after), "titles:", page.document.querySelectorAll(".admonition-title").map((e) => e.textContent.trim()).join("|"));
  }
})();
