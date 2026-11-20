import sys
sys.path.insert(0,r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder")
from fm import *
S=lambda s:"StRS-MDOKFSTUDIO-"+s
A,Bs,C=S("PALETTE-019"),S("PALETTE-020"),S("PALETTE-021")
def reparent(sw,remove,add=()):
    i=full(sw); p,t,fm=load(i)
    cur=list(fm.get("derives_from") or [])
    new=[x for x in cur if x not in remove]
    for a in add:
        if a not in new: new.append(a)
    assert new,sw
    setlist(i,"derives_from",new)
    print(sw,[x.split("MDOKFSTUDIO-")[1] for x in new])
P1=S("PALETTE-001")
m={"A":[A],"B":[Bs],"C":[C],"BC":[Bs,C]}
for n in "039 043 045 048 049 050 052 053 083 266 003 002".split(): reparent("PALETTE-"+n,[P1],m["A"])
for n in "115 123 124 125 126 267".split(): reparent("PALETTE-"+n,[P1],m["B"])
reparent("PALETTE-269",[P1],m["BC"])
for n in "127 132 133 135 136 138 270 271 272 265 273 274 130 137".split(): reparent("PALETTE-"+n,[P1],m["C"])
for n in "004 021 054 058 072 089 092 109 150 153 160 213 238 242 263 264".split(): reparent("PALETTE-"+n,[P1])
reparent("PALETTE-001",[P1])
reparent("PALETTE-275",[P1],[S("PALETTE-015")])
reparent("PALETTE-114",[P1],[S("REVIEW-015")])
reparent("TABLE-111",[P1])
reparent("PALETTE-115",[S("PALETTE-005")])
reparent("TRUST-001",[S("PALETTE-002")])
for n in ("TRUST-005","TRUST-065"): reparent(n,[S("PALETTE-007"),S("PALETTE-013")])
reparent("TRUST-006",[S("THEME-011")])
reparent("CORE-028",[S("THEME-002")])
reparent("TABLE-085",[S("PALETTE-015")])
for n in ("192","196","203"): reparent("PALETTE-"+n,[S("PALETTE-013")])
