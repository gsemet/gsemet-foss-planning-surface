const t = (...l) => l.join("\n") + "\n";
const n = (...b) => t(":::{note}", ...b, ":::", "", "After.");
module.exports = [
  ["body text then block formula", n("The formula:", "$$", "y = 2", "$$")],
  ["body text then block formula then text", n("The formula:", "$$", "y = 2", "$$", "Done.")],
  ["body text then one line formula", n("The formula:", "$$ y = 2 $$")],
  ["body two paragraphs formula glued", n("Intro.", "", "The formula:", "$$", "y = 2", "$$", "", "End.")],
  ["alert text then block formula", t("> [!NOTE]", "> The formula:", "> $$", "> y = 2", "> $$")],
  ["body quote then formula", n("> quoted", "$$", "y = 2", "$$")],
  ["body list then formula", n("- item", "$$", "y = 2", "$$")],
  ["body code then formula", n("```py", "x", "```", "$$", "y = 2", "$$")],
  ["body heading then formula", n("## H", "$$", "y = 2", "$$")],
  ["body table then formula", n("| a |", "| - |", "| b |", "$$ y = 2 $$")],
  ["body formula alone", n("$$", "y = 2", "$$")],
  ["body field formula 2 lines", n(":a: b", "$$ y = 1", "z = 2 $$")],
  ["body +++ formula", n("+++", "x", "$$ y = 2 $$")],
  ["body closing tag then text", n("<div>", "word", "</div>", "after")],
  ["body unpaired details", n("<details>", "<summary>Table</summary>", "", "word", "", "</details>", "<table>", "<tr><td>cell</td></tr>", "</table>")],
  ["callout div", t(":::{div}", ":class: callout-tip", "", "Title text.", "", "- a", "- b", "", "Para.", ":::")],
  ["callout fence", t("::: {.callout-tip}", "## Title", "", "- a", "- b", "", "Para.", ":::")],
  ["callout colon braces", t(":::{div .callout-tip}", "- a", "", "Para.", ":::")],
];
