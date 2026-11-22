"""Set each SVG's <desc> to its -texts.md description paragraph. Run from docs/: python sync_desc.py name..."""
import re,sys
from xml.sax.saxutils import escape
for n in sys.argv[1:]:
    t=open(f"{n}-texts.md",encoding="utf-8").read().splitlines()
    i=next(k for k,l in enumerate(t) if l.startswith("# "))
    para=next(l for l in t[i+1:] if l.strip())
    s=open(f"{n}.svg",encoding="utf-8").read()
    s=re.sub(r"<desc>.*?</desc>",lambda m:"<desc>"+escape(para)+"</desc>",s,count=1,flags=re.S)
    open(f"{n}.svg","w",encoding="utf-8",newline="\n").write(s)
