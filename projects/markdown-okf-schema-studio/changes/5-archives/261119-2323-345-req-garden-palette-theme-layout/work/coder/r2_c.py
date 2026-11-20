import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
P = "src/page/features/blockSourceEditor.ts"
drop_lines(P, ["PALETTE-001", "PALETTE-021"])
mark_before(P, "const palette = createEditPalette(", ["PALETTE-001"])
mark_before(P, "editorChrome.placePaletteAboveFrame(edit, palette.element);", ["PALETTE-021"])
