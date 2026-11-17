from st import *
A="StRS-MDOKFSTUDIO-TOOLBAR-013"
t=rd(A)
old="""   - SwRS-MDOKFSTUDIO-TOOLBAR-120: the choice is accepted by the host only when anchorToEditor is a boolean
   - Option SwRS-MDOKFSTUDIO-TOOLBAR-120 (refusal): a value that is not a boolean is not accepted
3. The choice is kept for the panel
"""
new="""   - SwRS-MDOKFSTUDIO-TOOLBAR-120: the choice is kept for the panel
   - Option SwRS-MDOKFSTUDIO-TOOLBAR-120 (refusal): a value that is not a boolean is not accepted by the host
3. The panel keeps the choice
"""
assert old in t; wr(A,t.replace(old,new))
for s in ("LIFE-169","LIFE-170"):
    print(drop("SwRS-MDOKFSTUDIO-"+s,"derives_from",[A]))
print(get_list("SwRS-MDOKFSTUDIO-TOOLBAR-120","depends_on"), get_list("SwRS-MDOKFSTUDIO-TOOLBAR-120","derives_from"))
