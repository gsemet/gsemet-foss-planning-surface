import sys
B = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder"
sys.path.insert(0, B)
from fm import *
sid = full("StRS-PALETTE-001")
b = getbody(sid)
i = b.index("### Main paths")
b = b[:i] + "### Superseded\n\nThis use case is split into three: the formatting buttons (StRS-MDOKFSTUDIO-PALETTE-019), the GitHub Flavored Markdown constructs (StRS-MDOKFSTUDIO-PALETTE-020) and the MyST constructs (StRS-MDOKFSTUDIO-PALETTE-021). The link panel is covered by StRS-MDOKFSTUDIO-PALETTE-007 and the link requirements it names.\n"
setbody(sid, b)
