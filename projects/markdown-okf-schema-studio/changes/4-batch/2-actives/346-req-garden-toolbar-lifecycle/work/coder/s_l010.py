from st import *
A="StRS-MDOKFSTUDIO-LIFE-010"
t=rd(A)
old="- The Anchor button of the toolbar overrides the first choice for one panel.\n"
assert old in t; wr(A,t.replace(old,""))
