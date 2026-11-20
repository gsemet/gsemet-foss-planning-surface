import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
i=full("THEME-001"); b=getbody(i)
s=b.index("### Scenario (refusal): A theme mode the page does not know"); e=b.index("### Related requirements")
b=b[:s]+b[e:]
b=b.replace("- SwRS-MDOKFSTUDIO-LIFE-170: a new page starts from the stored mode, then the saved state, then the default.","- SwRS-MDOKFSTUDIO-LIFE-170: a new page starts from the stored mode, then the saved state, then the default; it also owns the refusal of a theme mode the page does not know.")
lines=[l for l in b.split("\n") if not l.startswith("- Method: test/page/diagReq.themeZoom.requirements.test.ts, unit test `an unknown theme mode")]
b="\n".join(lines).replace(" An unknown mode never shows.","")
setbody(i,b)
