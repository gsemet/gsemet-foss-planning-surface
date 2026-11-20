import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
replace_id("test/core/palette/paletteActions.test.ts","PALETTE-265","PALETTE-001")
replace_id("test/core/render/mystPaletteRendering.test.ts","PALETTE-265","PALETTE-278")
C="test/page/modules/chartActions.test.ts"
drop_lines(C,["PALETTE-265"],lines_at=[17]); replace_id(C,"PALETTE-265","PALETTE-278")
replace_id("test/page/modules/editActions.test.ts","PALETTE-265","PALETTE-001",lines_at=[196])
replace_id("test/page/modules/editPalette.test.ts","PALETTE-265","PALETTE-001")
replace_id("test/page/modules/editPalette.test.ts","PALETTE-126","PALETTE-276")
S="test/page/modules/slashMenu.test.ts"
drop_lines(S,["PALETTE-265"],lines_at=[344])
replace_id(S,"PALETTE-268","PALETTE-238")
drop_lines(S,["PALETTE-053"],lines_at=[749]); replace_id(S,"PALETTE-052","PALETTE-277")
replace_id("test/visual/slashAdmonitionScenarios.ts","PALETTE-268","PALETTE-238")
replace_id("test/page/runtimeEditPalette.test.ts","PALETTE-265","PALETTE-001")
replace_id("test/page/runtimeEditPalette.test.ts","PALETTE-267","PALETTE-277")
for f in ("test/page/modules/optionAction.test.ts","test/visual/optionListScenarios.ts"):
    replace_id(f,"PALETTE-267","PALETTE-277")
Y="test/page/modules/slashSyntaxCoverage.test.ts"
replace_id(Y,"PALETTE-273","PALETTE-278"); replace_id(Y,"PALETTE-274","PALETTE-278")
mark_before(Y,'test("CR 248: tabs inserts',["PALETTE-001"],kind="tests",above_doc=False)
mark_before(Y,'test("CR 248: plantuml inserts',["PALETTE-001"],kind="tests",above_doc=False)
