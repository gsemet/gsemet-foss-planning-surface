"""TF-IDF cosine similarity over SwRS titles + normative sentences.
Outputs: sim-pairs.tsv (pairs >= 0.45), sim-summary.json, and template-skeleton clusters."""
import json, re, math, collections, itertools
R = json.load(open("reqs.json"))
A = [r for r in R if r["lifecycle"]!="deprecated" and r["type"]=="SwRS"]
STOP = set("the a an of to in on and or is are be by for with its it as at from that this when shall extension page host sets set into than then which while whose one each every no not".split())
def toks(s):
    s = re.sub(r"SwRS-MDOKFSTUDIO-\w+-\d+", " ", s)
    return [w for w in re.findall(r"[a-z][a-z0-9]+", s.lower()) if w not in STOP and len(w)>2]
docs = {r["id"]: toks(r["title"]+" "+r["description"]) for r in A}
df = collections.Counter(w for d in docs.values() for w in set(d))
N = len(docs)
vec = {}
for i,d in docs.items():
    tf = collections.Counter(d); v = {w: (1+math.log(c))*math.log(N/df[w]) for w,c in tf.items()}
    n = math.sqrt(sum(x*x for x in v.values())) or 1; vec[i] = {w:x/n for w,x in v.items()}
# inverted index for speed
inv = collections.defaultdict(list)
for i,v in vec.items():
    for w,x in v.items(): inv[w].append((i,x))
scope = {r["id"]: r["scope"] for r in A}; title={r["id"]:r["title"] for r in A}
pairs = []
for i,v in vec.items():
    acc = collections.Counter()
    for w,x in v.items():
        if df[w] > 150: continue
        for j,y in inv[w]:
            if j>i: acc[j]+=x*y
    for j,s in acc.items():
        if s>=0.45: pairs.append((round(s,3),i,j))
pairs.sort(reverse=True)
with open("sim-pairs.tsv","w") as f:
    f.write("score\tid_a\tid_b\tsame_scope\ttitle_a\ttitle_b\n")
    for s,i,j in pairs: f.write(f"{s}\t{i}\t{j}\t{scope[i]==scope[j]}\t{title[i]}\t{title[j]}\n")
# connected components at 0.55
par = {i:i for i in vec}
def find(x):
    while par[x]!=x: par[x]=par[par[x]]; x=par[x]
    return x
for s,i,j in pairs:
    if s>=0.55: par[find(i)]=find(j)
comps = collections.defaultdict(list)
for i in vec: comps[find(i)].append(i)
big = sorted([c for c in comps.values() if len(c)>1], key=len, reverse=True)
bands = collections.Counter()
for s,i,j in pairs:
    b = "0.75+" if s>=0.75 else "0.65-0.75" if s>=0.65 else "0.55-0.65" if s>=0.55 else "0.45-0.55"
    bands[(b, "intra" if scope[i]==scope[j] else "cross")]+=1
inpair = {x for _,i,j in pairs if _>=0.55 for x in (i,j)}
# skeleton templates: replace the most specific nouns, keep structural verbs
SKEL = [("refuses-in-read-only", r"(refus|reject|not offered|no ).*read-only|read-only.*(refus|reject|no |not )"),
 ("refuses-stale-render", r"(older|stale|out of date|newer than the render|names the render|another render|earlier patch|older render|of a stale)"),
 ("refuses-while-edit-open", r"while (an?|the) (block |markdown |field )?(edit|editor)s? (is )?(open|busy)|during an open edit|while an edit is open|while a field editor is open"),
 ("message-shape-validation", r"(message|request)s? (must|needs?|carr(y|ies)|is validated)|accepts only|accepted only|malformed|needs? (an?|its|both|string|array)|registered type|bounded (size|key|identifier)|host validates"),
 ("answer-matching-by-id", r"(answered|matched) (by|with) (its|the|their)? ?(edit )?id|same edit id|another (or a closed )?editor|after the (editor|popover) closed|arrives after"),
 ("timeout-no-answer", r"no answer|after \d+ seconds|times? out|within \d+ seconds|never waits long|forgotten after"),
 ("size-count-limit", r"(over|more than|at most|larger than|caps?|capped) \d|\d+ (mib|kib|mb|characters|entries|files|results|drawings|threads|comments|places|documents)"),
 ("cannot-apply-reported", r"cannot apply|vs code (cannot apply|rejects)|is reported and keeps|editor cannot apply"),
 ("setting-default", r"setting|defaults? to|is (on|off) by default"),
 ("persist-workspace-choice", r"(stored|stores|remembers?|saved) (for the workspace|state|choice|in the webview)|workspace choice|saved state of the panel"),
 ("focus-escape-closes", r"escape|closes? (the|its|only)|gives? the focus back|keeps? the focus|returns? (the focus|to the text box)"),
 ("shortcut-key", r"\b(cmd|ctrl|alt|shift)\b|arrow|enter|tab\b"),
 ("one-undo-step", r"undo|one edit|one document edit|single replacement"),
 ("css-presentation", r"\bpx\b|percent|colou?r|centred|wraps?|square|rounded|style|font"),
]
skel = collections.defaultdict(lambda: collections.Counter()); skex = collections.defaultdict(list)
for r in A:
    t = (r["title"]+" | "+r["description"]).lower()
    for k,p in SKEL:
        if re.search(p,t):
            skel[k][r["scope"]]+=1
            skex[k].append(r["id"].replace("SwRS-MDOKFSTUDIO-",""))
json.dump(dict(n=N, pairs=len(pairs), bands={f"{a}/{b}":c for (a,b),c in sorted(bands.items())},
   swrs_in_pair_055=len(inpair),
   components_055=[len(c) for c in big][:40], n_components_055=len(big),
   members_in_components=sum(len(c) for c in big),
   top_components=[[ (x.replace("SwRS-MDOKFSTUDIO-",""), title[x]) for x in sorted(c)][:12] for c in big[:15]],
   skeleton={k:dict(total=sum(v.values()), per_scope=dict(v.most_common()), ids=skex[k]) for k,v in skel.items()}),
   open("sim-summary.json","w"), indent=1)
print(N, len(pairs), dict(bands), len(inpair), len(big), sum(len(c) for c in big))
for k,v in skel.items(): print(k, sum(v.values()), dict(v.most_common(6)))
