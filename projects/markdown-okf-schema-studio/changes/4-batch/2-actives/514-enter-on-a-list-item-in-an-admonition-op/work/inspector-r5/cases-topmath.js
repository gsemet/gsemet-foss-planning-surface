const t = (...l) => l.join("\n") + "\n";
module.exports = [
  ["top text then block formula", t("The formula:", "$$", "y = 2", "$$", "", "After.")],
  ["top text then one line formula", t("The formula:", "$$ y = 2 $$", "", "After.")],
  ["top list item formula", t("- The formula:", "  $$", "  y = 2", "  $$", "- next")],
  ["dropdown text then formula", t(":::{note}", ":class: dropdown", "The formula:", "$$", "y = 2", "$$", ":::")],
  ["box blank then field formula", t(":::{note}", "", ":a: b", "$$ y = 1", "z = 2 $$", ":::")],
  ["box blank then text formula no blank", t(":::{note}", "", "Text", "$$", "y = 2", "$$", "", "Tail", ":::")],
  ["box formula after two lines", t(":::{note}", "", "Line one", "line two", "$$", "y = 2", "$$", ":::")],
];
