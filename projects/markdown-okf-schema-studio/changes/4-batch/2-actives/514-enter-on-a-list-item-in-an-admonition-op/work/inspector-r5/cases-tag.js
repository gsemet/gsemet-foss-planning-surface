const t = (...l) => l.join("\n") + "\n";
const det = (...inner) => t(":::{note}", "- Step", "  <details>", "  <summary>More</summary>", "", ...inner.map((l) => (l ? "  " + l : "")), "", "  </details>", "- next", ":::", "", "After.");
module.exports = [
  ["one item list above closing tag", det("- only")],
  ["two item list above closing tag", det("- one", "- two")],
  ["one line quote above closing tag", det("> quoted")],
  ["heading above closing tag", det("## Head")],
  ["rule above closing tag", det("***")],
  ["one line formula above closing tag", det("$$ y = 2 $$")],
  ["image above closing tag", det("![a](x.png)")],
  ["div around heading", t(":::{note}", "- Step", "  <div>", "", "  ## Head", "", "  </div>", "- next", ":::")],
  ["alert heading above closing tag", t("> [!NOTE]", "> - Step", ">   <details>", ">   <summary>More</summary>", ">", ">   ## Head", ">", ">   </details>", "> - next")],
];
