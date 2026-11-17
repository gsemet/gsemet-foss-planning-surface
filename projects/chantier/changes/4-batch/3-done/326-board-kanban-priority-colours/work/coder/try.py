import sys; sys.path.insert(0,sys.argv[0].rsplit('/',1)[0])
from colours import *
for c in sys.argv[1:]:
    t=mix(c,'#ffffff',.86)
    print(c,round(hue(c),1),gap(hue(c)),t,round(cr(c,t),2))
