import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
R = "test/integration/realInput/"
drop_lines(R+"markers.ts", ["PALETTE-153","PALETTE-031","PALETTE-232","PALETTE-242","PALETTE-238","THEME-001","THEME-016","THEME-025",
  "StRS-MDOKFSTUDIO-PALETTE-001","StRS-MDOKFSTUDIO-PALETTE-005","StRS-MDOKFSTUDIO-PALETTE-007","StRS-MDOKFSTUDIO-PALETTE-015","StRS-MDOKFSTUDIO-THEME-002"])
mark_before(R+"editorWidgets.ts","export async function scenarioFigureEditor",["PALETTE-153"],kind="tests")
mark_before(R+"textEditing.ts","export async function scenarioSlashMenu",["StRS-MDOKFSTUDIO-PALETTE-015","PALETTE-232","PALETTE-238"],kind="tests")
mark_before(R+"textEditing.ts",'await expectValue("/h2 Enter to write the heading prefix"',["PALETTE-242"],kind="tests",above_doc=False)
mark_before(R+"textEditing.ts","export async function scenarioPalette",["StRS-MDOKFSTUDIO-PALETTE-005","PALETTE-031"],kind="tests")
mark_before(R+"previewWindow.ts","export async function scenarioToolbarState",["THEME-016"],kind="tests")
mark_before(R+"previewWindow.ts","await captureAfter(evidence, page, realInputId(`38-toolbar-",["StRS-MDOKFSTUDIO-THEME-002","THEME-001","THEME-025"],kind="tests",above_doc=False)
