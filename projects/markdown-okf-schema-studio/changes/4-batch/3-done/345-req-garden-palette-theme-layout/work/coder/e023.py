import sys,re
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
def cut(b,start,end):
    i=b.index(start); j=b.index(end,i)
    return b[:i]+b[j:], b[i:j]
b=getbody(full("LAYOUT-023"))
b,sec1=cut(b,"### Scenario (nominal): Table measured uncapped and rounded up","### Scenario (nominal): Table with row handles in edit mode")
b,sec2=cut(b,"### Scenario (nominal): Table with row handles in edit mode","### Scenario (refusal): Elements kept in the column")
# refusal rows
rows_move=[]
lines=b.split("\n"); out=[]
for l in lines:
    if l.startswith("| A wide table with an open cell editor") or l.startswith("| A table that fits the column (SwRS-MDOKFSTUDIO-LAYOUT-044)") or l.startswith("| A table with an open cell editor and a real resize") or l.startswith("| A table whose column minimums fit the column"):
        rows_move.append(l)
    else: out.append(l)
b="\n".join(out)
assert len(rows_move)==4,rows_move
# several triggers -> verification note
b,sec3=cut(b,"### Scenario (boundary): Several triggers in one frame","### Known issues")
# known issues moved
ki=[l for l in b.split("\n") if l.startswith("- Known issue: A table first measured while its cell editor")]
assert len(ki)==1
b=b.replace(ki[0]+"\n","")
# verification notes: move table methods
vm=[]
lines=b.split("\n");out=[]
for l in lines:
    if l.startswith("- Method: test/page/tableBreakout.test.ts") or l.startswith("- Method: test/core/preview/previewStyles.test.ts (table with row handles)") or l.startswith("- Method: test/visual/capture_layout_checks.py (wide table and oversized block)") and False:
        vm.append(l)
    else: out.append(l)
b="\n".join(out)
b=b.replace("### Known issues","""### Several triggers in one frame (verification note)

Five resizes, image loads or content-size changes before the next animation frame run the layout work (wide tables, width mode, measure, anchor, sticky headings) once in that frame, and a trigger after the frame ran asks for a new frame. This is checked by test/page/runtimeScroll.test.ts (`P-08: layout triggers within one frame measure the page once`).

### Known issues""",1)
b=b.replace("(wide table and oversized block, column off the centre, table-of-contents column, uncapped table, elements kept in the column, resize)","(wide table and oversized block, column off the centre, table-of-contents column, elements kept in the column, resize)")
b=b.replace("- Criteria: Breakout equals","- Criteria: The table cases (uncapped and rounded up, row handles, cell editor) are specified in SwRS-MDOKFSTUDIO-LAYOUT-044. Breakout equals")
setbody(full("LAYOUT-023"),b)
# 044
c=getbody(full("LAYOUT-044"))
add=sec1.rstrip()+"\n\n"+sec2.rstrip()+"""

### Scenario (nominal): A cell editor keeps the breakout of its table

- GIVEN Auto mode and a wide table with an open cell editor (a textarea inside a table cell frame, the table stays rendered)
- WHEN the editor moves to another cell (Tab, arrows, click) or the page resizes
- THEN the table keeps the breakout it had when the editor opened, and is measured again with the editor in place after a real resize

| Input | Outcome |
"""+"\n".join(["| --- | --- |"]+[r for r in rows_move])+"""

"""
c=c.replace("### Verification notes",add+"### Verification notes",1)
c=c.replace("- Criteria: the verdicts above","\n".join(vm)+"""
- Method: test/page/runtimePageControls.test.ts (the table cases of the breakout): T10b a wide table gets its fractional max-content width rounded up, so no cell wraps; T10b a table with row handles keeps their room left of it when it breaks out; visual scenario v84 (table uncapped and rounded up)
- Known issue: """+ki[0].split("Known issue: ",1)[1]+"""
- Criteria: the verdicts above""",1)
setbody(full("LAYOUT-044"),c)
# 022: depends_on 032
addkey(full("LAYOUT-022"),"depends_on",["SwRS-MDOKFSTUDIO-LAYOUT-032"])
d=getbody(full("LAYOUT-022"))
d=d.replace("### Known issues","### Related requirements\n\n- SwRS-MDOKFSTUDIO-LAYOUT-032: a table wider than the column in Margin scrolls inside its own box.\n\n### Known issues",1)
setbody(full("LAYOUT-022"),d)
# 001 criteria
e=getbody(full("LAYOUT-001"))
e=e.replace("cells, .","cells.")
setbody(full("LAYOUT-001"),e)
