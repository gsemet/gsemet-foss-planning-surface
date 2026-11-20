import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
P = "src/core/palette/paletteActions.ts"
drop_lines(P, ["PALETTE-263", "PALETTE-001", "PALETTE-275"])
mark_before(P, "aliases?: string[];", ["PALETTE-263"])
mark_before(P, "modes: EditActionMode[];", ["PALETTE-001"])
mark_before(P, "export interface EditActionSlash", ["PALETTE-275"])
replace_id(P, "PALETTE-268", "PALETTE-238")
replace_id(P, "PALETTE-052", "PALETTE-277")
mark_before(P, "numberedList: {", ["PALETTE-277"])
for i in ("PALETTE-273", "PALETTE-265", "PALETTE-274"):
    replace_id(P, i, "PALETTE-278")
