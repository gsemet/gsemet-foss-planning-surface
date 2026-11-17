from lib import *
S="StRS-MDOKFSTUDIO-"; W="SwRS-MDOKFSTUDIO-LIFE-"
def D(sw,*st): print("drop",sw,st,drop(W+sw,"derives_from",[S+x for x in st]))
D("100","LIFE-021","LIFE-003","LIFE-005"); D("108","LIFE-021")
for n in ("026","032","049","156"): D(n,"LIFE-001")
D("026","LIFE-010"); D("069","LIFE-010","LIFE-021","LIFE-007"); D("071","LIFE-010","LIFE-014"); D("156","LIFE-010")
D("119","LIFE-003"); D("125","LIFE-003")
D("018","LIFE-007")
set_list(W+"002","derives_from",[S+"LIFE-007"])
set_list(W+"172","derives_from",[S+"BLOCK-001"])
for n in "100 108 026 032 049 156 069 071 119 125 018 002 172".split():
    print(n,[x.replace(S,"") for x in get_list(W+n,"derives_from")])
