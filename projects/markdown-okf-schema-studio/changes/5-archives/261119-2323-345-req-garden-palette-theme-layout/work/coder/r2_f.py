import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
B = "src/page/modules/blockEditActions.ts"
drop_lines(B, ["PALETTE-049","PALETTE-053","PALETTE-130","PALETTE-268","PALETTE-265"], lines_at=[36,60,394,395,567])
for i,l in (("PALETTE-052",[59]),("PALETTE-123",[306]),("PALETTE-267",[316])):
    replace_id(B, i, "PALETTE-277")
replace_id(B, "PALETTE-137", "PALETTE-127")
for i in ("PALETTE-265","PALETTE-273","PALETTE-274"):
    replace_id(B, i, "PALETTE-278")
I = "src/page/modules/inlineEditActions.ts"
drop_lines(I, ["PALETTE-045"])
for i in ("PALETTE-048","PALETTE-135","PALETTE-138","PALETTE-126"):
    replace_id(I, i, "PALETTE-276")
