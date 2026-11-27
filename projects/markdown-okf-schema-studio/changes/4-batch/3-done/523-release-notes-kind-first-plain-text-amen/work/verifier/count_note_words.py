import re, subprocess, sys, html
sys.stdout.reconfigure(encoding="utf-8")
t = subprocess.run(["git","show","HEAD:docs/releases-notes/2026-11-24-v1.12.1/release-notes.md"],capture_output=True,check=True).stdout.decode("utf-8")
L = t.splitlines()
def words(s, drop_symbols=True):
    toks = s.split()
    if drop_symbols: toks=[x for x in toks if re.search(r"\w",x)]
    return len(toks)
def clean(s):
    s=re.sub(r"<[^>]+>","",s); s=s.replace("**",""); s=s.replace("`","")
    s=re.sub(r"^\s*(#+|-)\s+","",s); return s.strip()
sub = clean(L[3]); print("subtitle:",words(sub),"|",sub)
print("--- list lines (smaller changes and folded)")
for n,l in enumerate(L,1):
    if l.startswith("- "): print(n, words(clean(l)), "over20" if words(clean(l))>20 else "ok")
print("--- highlights (heading + text)")
for a,b in [(18,23),(24,27)]:
    parts=[clean(L[i-1]) for i in range(a,b+1) if L[i-1].strip()]
    s=" ".join(parts); print(a,b,words(s), "sentences in text:", len(re.findall(r"[.!?](?=\s|$)", " ".join(parts[1:]).replace("Open With... >","Open With >"))))
# visible part: above first <details>, links and tags not counted
cut = next(i for i,l in enumerate(L) if l.startswith("<details"))
vis = "\n".join(L[:cut])
nolink = re.sub(r"<a [^>]*>.*?</a>","",vis,flags=re.S)
def total(s): return sum(words(clean(l)) for l in s.splitlines() if l.strip() and l.strip()!="---")
print("visible, links removed:", total(nolink), "| links counted:", total(vis))
noheader = "\n".join(L[16:cut]); print("visible body from first highlight:", total(noheader))
