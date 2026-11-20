import sys; sys.path.insert(0, "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from r2lib import *
drop_lines("test/build/integrationEditModeRestore.test.ts", ["PALETTE-264"])
drop_lines("test/security/package-contract.test.ts", ["PALETTE-001"])
drop_lines("test/core/state/editLock.test.ts", ["THEME-016"])
p = "test/page/modules/paletteReq.requirements.test.ts"
t = rd(p); assert "outside the three modes" in t
wr(p, t.replace("outside the three modes", "outside the four modes"))
