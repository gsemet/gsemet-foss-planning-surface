import sys
B = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder"
sys.path.insert(0, B)
from fm import *
for k, n in (("A", "019"), ("B", "020"), ("C", "021")):
    setbody(full("StRS-PALETTE-" + n), open(f"{B}/bodies/s{k}.md", encoding="utf-8").read())
addkey(full("StRS-PALETTE-019"), "depends_on", ["SwRS-MDOKFSTUDIO-PALETTE-001"])
addkey(full("StRS-PALETTE-020"), "depends_on", ["SwRS-MDOKFSTUDIO-PALETTE-039"])
addkey(full("StRS-PALETTE-021"), "depends_on", ["SwRS-MDOKFSTUDIO-PALETTE-039"])
