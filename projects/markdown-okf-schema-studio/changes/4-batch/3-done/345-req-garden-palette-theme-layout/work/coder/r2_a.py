import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
P = "src/page/modules/editPalette.ts"
t = rd(P); e = eol(t)
lines = t.split(e)
assert lines[22].strip().startswith("// @implements_req") and lines[38].strip().startswith("// @implements_req") and lines[39] == ""
del lines[22:40]
wr(P, e.join(lines))
mark_before(P, "const keepFocus", ["PALETTE-036"])
mark_before(P, "const MODE_LABELS", ["PALETTE-002"])
mark_before(P, 'modeSelect.addEventListener("keydown"', ["PALETTE-017"])
mark_before(P, 'modeSelect.addEventListener("change"', ["LIFE-169"])
mark_before(P, "function runAction(", ["PALETTE-039"])
mark_before(P, "function openPopover(", ["PALETTE-031"])
mark_before(P, "function visibleActions(", ["PALETTE-001"])
mark_before(P, "function syncTypePicker(): void {", ["PALETTE-269"])
mark_before(P, "function menuEntries(", ["PALETTE-238"])
mark_before(P, "function runMenuEntry(", ["PALETTE-242"])
