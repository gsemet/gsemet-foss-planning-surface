import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
for s in ("StRS-LAYOUT-003","StRS-PALETTE-002","StRS-THEME-004","StRS-THEME-011"):
    addkey(full(s),"depends_on",["SwRS-MDOKFSTUDIO-LIFE-169","SwRS-MDOKFSTUDIO-LIFE-170"])
