import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
i=full("LIFE-169"); b=getbody(i)
a="### Related requirements"
assert b.count(a)==1
new='''### Scenario (refusal): A palette mode or a theme mode outside the four is dropped

- GIVEN a workspace whose stored palette mode is gfm and an open preview
- WHEN the page posts previewPaletteModeChanged with a mode of the table, or previewThemeModeChanged with a theme mode of the table
- THEN the message is rejected by the protocol validator of its type, nothing is stored, no result is posted to the page, and the next preview still starts in the stored mode

| Message | Field value | Outcome |
| --- | --- | --- |
| previewPaletteModeChanged | html | rejected |
| previewPaletteModeChanged | the empty text | rejected |
| previewPaletteModeChanged | a number or true (not a string) | rejected |
| previewPaletteModeChanged | missing | rejected |
| previewThemeModeChanged | sepia (or neon) | rejected |
| previewThemeModeChanged | missing previewThemeMode | rejected |

### Scenario (nominal): An accepted palette mode or theme mode

- GIVEN a palette whose select changes to another of the modes strict, gfm, myst or full, or the Theme button pressed (any of current, dark, white and cream)
- WHEN the page posts the message once, with the identity fields documentId, revision and requestId (the envelope is checked first, see SwRS-MDOKFSTUDIO-TRUST-052) and the field mode or previewThemeMode
- THEN the host accepts it through the gate of its type (see SwRS-MDOKFSTUDIO-TRUST-065), stores the mode for the workspace, and the next preview starts in it (see SwRS-MDOKFSTUDIO-LIFE-170)

'''
b=b.replace(a,new+a)
anchor="- Criteria: after each change"
assert b.count(anchor)==1
b=b.replace(anchor,"- Method: test/core/protocol/pageToHost.test.ts (previewPaletteModeChanged accepts only strict, gfm, myst or full: html, the empty text, true and a missing mode are rejected; the number case is deduced from the validator, not tested) and test/integration/paletteMode.test.ts (an invalid palette mode is not stored); test/integration/untrusted-suite.ts (the palette mode of a Restricted Mode preview)\n- Method: test/core/protocol/pageStateMessages.test.ts, unit test `the page-state validators accept exactly what the frozen validator accepted` (the theme modes cream and neon and an absent mode, on the live validator PAGE_TO_HOST_VALIDATORS.previewThemeModeChanged in src/core/protocol/pageToHost.ts; the guard in src/session/features/viewState.ts repeats the check and is not tested separately)\n"+anchor)
b=b.replace("the stale-message drop is untested).\n","the stale-message drop is untested).\n",1)
setbody(i,b)
# parents: remove the four StRS from LIFE-169 derives_from, add depends_on on those StRS
FOUR=["StRS-MDOKFSTUDIO-LAYOUT-003","StRS-MDOKFSTUDIO-PALETTE-002","StRS-MDOKFSTUDIO-THEME-004","StRS-MDOKFSTUDIO-THEME-011"]
for n in ("169","170"):
    p,t,fm=load(full("LIFE-"+n))
    d=[x for x in fm["derives_from"] if x not in FOUR]
    print(n,"derives",d)
    setlist(full("LIFE-"+n),"derives_from",d)
