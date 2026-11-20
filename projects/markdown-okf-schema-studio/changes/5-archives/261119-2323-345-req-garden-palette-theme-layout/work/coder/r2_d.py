import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
S = "src/core/preview/styles/"
def companion(name, host, why, rows):
    body = f"// Companion of: {host}\n// {why}\n"
    for kind, i, pt in rows:
        body += f"// @{kind}_req {PFX}{i} — {pt}\n"
    body += "export {};\n"
    wr(S + name, body)

drop_lines(S+"pageChromeStyles.ts", ["PALETTE-002","LAYOUT-002","THEME-031","THEME-043"])
companion("pageChromeStyles.markers.ts", S+"pageChromeStyles.ts",
  "Requirement markers for rules inside the PAGE_CHROME_CSS template string, where a comment cannot sit.",
  [("implements","PALETTE-002","button[data-tooltip]::after"),
   ("implements","LAYOUT-002","--sphinx-preview-content-max-width"),
   ("implements","THEME-031","html[data-sphinx-preview-theme-mode=\"cream\"]"),
   ("implements","THEME-043","--sphinx-preview-zoom")])

drop_lines(S+"contentLayoutStyles.ts", ["LAYOUT-001","LAYOUT-022","PALETTE-021","THEME-001"])
companion("contentLayoutStyles.markers.ts", S+"contentLayoutStyles.ts",
  "Requirement markers for rules inside the CONTENT_LAYOUT_CSS template string, where a comment cannot sit.",
  [("implements","LAYOUT-001","overflow-wrap: anywhere"),
   ("implements","LAYOUT-022","html[data-sphinx-preview-width=\"full\"]"),
   ("implements","PALETTE-021","the sticky palette rides down")])

drop_lines(S+"contentBlockStyles.ts", ["LAYOUT-043"])
companion("contentBlockStyles.markers.ts", S+"contentBlockStyles.ts",
  "Requirement markers for rules inside the CONTENT_BLOCK_CSS template string, where a comment cannot sit.",
  [("implements","LAYOUT-001","overflow-wrap: anywhere")])

drop_lines(S+"tableStyles.ts", ["LAYOUT-032"])
companion("tableStyles.markers.ts", S+"tableStyles.ts",
  "Requirement markers for rules inside the TABLE_CSS template string, where a comment cannot sit.",
  [("implements","LAYOUT-032","table[data-sphinx-table-overflow=\"true\"]")])

drop_lines(S+"propertiesStyles.ts", ["CORE-050"])
companion("propertiesStyles.markers.ts", S+"propertiesStyles.ts",
  "Requirement markers for rules inside a CSS template string of this file, where a comment cannot sit.",
  [("implements","CORE-050","@media (prefers-reduced-motion: reduce)")])
