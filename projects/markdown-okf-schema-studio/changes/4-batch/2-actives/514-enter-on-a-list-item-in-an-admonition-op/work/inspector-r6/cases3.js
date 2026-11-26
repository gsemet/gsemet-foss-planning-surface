const B = String.fromCharCode(92);
const t = (...l) => `${l.join("\n")}\n`;
const N = (...b) => t(":::{note}", ...b, ":::");
module.exports = [
  ["amsmath", N(B+"begin{align}", "y &= 2", B+"end{align}")],
  ["amsmath item", N("- Item", "", "  "+B+"begin{align}", "  y &= 2", "  "+B+"end{align}", "- Next")],
  ["amsmath item tight", N("- Item", "  "+B+"begin{align}", "  y &= 2", "  "+B+"end{align}", "- Next")],
  ["amsmath alert", t("> [!NOTE]", "> "+B+"begin{equation}", "> y", "> "+B+"end{equation}", ">", "> x")],
  ["amsmath alert item", t("> [!NOTE]", "> - Item", ">", ">   "+B+"begin{equation}", ">   y", ">   "+B+"end{equation}", "> - Next")],
  ["amsmath blank", N(B+"begin{align}", "y", "", "z", B+"end{align}", "", "End")],
  ["dollar escapes", N("$$ "+B+"text{"+B+"$5} + "+B+"$ 3 $$", "", "End")],
  ["percent", N("$$", "y % comment", "$$")],
  ["lbrace", N("$$ "+B+"{ y "+B+"} _a * b * c $$")],
  ["matrix", N("$$", B+"begin{pmatrix} a & b "+B+B, "c & d "+B+"end{pmatrix}", "$$")],
  ["ams in dollar", N("$$", B+"begin{aligned}", "a", B+"end{aligned}", "$$")],
];
