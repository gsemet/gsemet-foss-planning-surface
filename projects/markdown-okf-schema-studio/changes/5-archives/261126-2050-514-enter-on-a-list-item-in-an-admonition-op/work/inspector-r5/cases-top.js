const t = (...l) => l.join("\n") + "\n";
const det = (...inner) => t("- Step", "  <details>", "  <summary>More</summary>", "", ...inner.map((l) => (l ? "  " + l : "")), "", "  </details>", "- next", "", "After.");
module.exports = [
  ["top heading above closing tag", det("## Head")],
  ["top paragraph above closing tag", det("words")],
  ["top quote above closing tag", det("> quoted")],
];
