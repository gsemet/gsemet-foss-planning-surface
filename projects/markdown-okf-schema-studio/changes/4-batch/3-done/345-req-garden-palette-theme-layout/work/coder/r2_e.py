import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
P = "src/page/modules/editPalettePopovers.ts"
drop_lines(P, ["PALETTE-036"], lines_at=[397])
mark_before(P, 'swatch.addEventListener("mousedown", keepFocus);', ["PALETTE-036"])
drop_lines("src/page/features/blockEditor.ts", ["PALETTE-089"])
mark_before("src/page/modules/linkPanel.ts", 'insertButton.addEventListener("click"', ["PALETTE-089"])
replace_id("test/visual/capture_comment_checks.py", "LAYOUT-018", "LAYOUT-011")
