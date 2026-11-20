import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
i=full("PALETTE-001")
b=getbody(i)
def rep(a,c):
    global b
    assert a in b, a
    b=b.replace(a,c,1)
rep("a value outside the three modes","a value outside the four modes")
rep("(see SwRS-MDOKFSTUDIO-PALETTE-265)","(see SwRS-MDOKFSTUDIO-PALETTE-278)")
add='''### Scenario (refusal): A mode that does not list an insertion command offers none

- GIVEN the palette or the slash menu in a mode below the one that lists a command
- WHEN the palette is shown or the slash is typed
- THEN the command is not offered, as the table says; the constructs of the document are rendered all the same (the insertion itself is SwRS-MDOKFSTUDIO-PALETTE-278)

| Command | Listed in | Not offered in |
| --- | --- | --- |
| Vega-Lite chart and Vega chart (/chart, /vega) | full | strict, gfm, myst |
| PlantUML diagram (/plantuml, /uml) | full | strict, gfm, myst |
| Content tabs (/tab-set, /tabs) | myst and full | strict, gfm |

### Scenario (nominal): The mode setting and the stored choice

- GIVEN the select of the palette, the setting defaultPaletteMode or a stored choice
- WHEN the mode is chosen
- THEN the table says what follows

| Input | Outcome |
| --- | --- |
| the select of the palette | offers Strict Markdown, GitHub (GFM), MyST and Full |
| the setting defaultPaletteMode or a stored choice full | the page starts in the Full mode |
| a message previewPaletteModeChanged with mode full | accepted and stored for the workspace |

### Verification notes
'''
rep("### Verification notes\n",add)
setbody(i,b)
