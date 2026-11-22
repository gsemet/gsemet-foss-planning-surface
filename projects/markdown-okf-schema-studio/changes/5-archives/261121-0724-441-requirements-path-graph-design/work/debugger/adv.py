import math
from fontTools.ttLib import TTFont
f=TTFont("node_modules/katex/dist/fonts/KaTeX_Main-Italic.woff2")
upm=f['head'].unitsPerEm; cmap=f.getBestCmap(); hm=f['hmtx']
t="a long word, URL or Japanese, Chinese or Korean paragraph wraps in"
adv=[hm[cmap[ord(c)]][0]*13.5/upm for c in t]
print("exact",sum(adv),"rounded",sum(round(a) for a in adv),"ceil",sum(math.ceil(a) for a in adv),"chars",len(t),"CHAR est",len(t)*6.4)
