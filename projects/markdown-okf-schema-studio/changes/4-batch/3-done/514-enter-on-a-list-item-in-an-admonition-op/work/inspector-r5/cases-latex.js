const t = (...l) => l.join("\n") + "\n";
const B = String.fromCharCode(92);
const item = (...b) => t(":::{note}", ...b, ":::", "", "After.");
const beg = `${B}begin{align}`, end = `${B}end{align}`, body = `a &= 1 ${B}${B}`, b2 = "b &= 2";
module.exports = [
  ["latex tight", item(`- Text`, `  ${beg}`, `  ${body}`, `  ${b2}`, `  ${end}`, "- next")],
  ["latex loose", item(`- Text`, "", `  ${beg}`, `  ${body}`, `  ${b2}`, `  ${end}`, "", "- next")],
  ["latex first in item", item(`- ${beg}`, `  ${body}`, `  ${b2}`, `  ${end}`, "- next")],
  ["latex after quote", item(`- Text`, "", "  > quoted", `  ${beg}`, `  ${b2}`, `  ${end}`)],
  ["latex alert", t("> [!NOTE]", "> - Text", `>   ${beg}`, `>   ${b2}`, `>   ${end}`, "> - next")],
  ["tag dollar", item("- Text", "  $$", `  y = 2 ${B}tag{1}`, "  $$", "- next")],
  ["label dollar", item("- Text", "", "  $$", `  y = 2 ${B}label{eq:a}`, "  $$", "", "- next")],
  ["field list formula", item("Intro.", "", "- Text", "", "  :a: b", "  $$ y = 1", "  z = 2 $$", "", "- next")],
  ["formula with comparison", item("- Text", "", "  $$", "  a > b", "  $$", "", "- next")],
  ["formula with comparison alert", t("> [!NOTE]", "> - Text", ">", ">   $$", ">   a", ">   > b", ">   $$", "> - next")],
  ["body latex after text", item("The formula:", beg, b2, end)],
  ["body latex after blank", item("The formula:", "", beg, b2, end, "", "End.")],
];
