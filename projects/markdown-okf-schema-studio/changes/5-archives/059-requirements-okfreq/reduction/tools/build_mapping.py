"""Builds mapping.csv, tiles.csv and counts from tiles_swrs.txt / tiles_strs.txt; validates coverage."""
import json, csv, re, collections, sys
R = json.load(open("reqs.json"))
ACTIVE = {r["id"]: r for r in R if r["lifecycle"] != "deprecated"}
TOK2SCOPE = {}
for r in R: TOK2SCOPE[r["id"].split("-")[2]] = r["scope"]
MAIN = {"rendering-core","code-blocks","gfm","myst","diagrams","frontmatter-schema","frontmatter-editing","layout-width"}
ACT = {"k":"keep","s":"fold-as-scenario","m":"merge-into","x":"replace-by-crosscutting","d":"drop-implementation-detail"}
def full(tok, level):
    p = "SwRS" if level=="SwRS" else "StRS"
    tok = tok.replace("StRS-","")
    return f"{p}-MDOKFSTUDIO-{tok}"
REFUSAL = re.compile(r"refus|reject|ignor|never|not |no |drop|cannot|without|invalid|unknown|stale|out of date|malformed|disabled|blocked|fails?|error", re.I)
BOUND = re.compile(r"\b\d+\b|at most|limit|cap|over |more than|bound|edge|end|first|last|empty|narrow", re.I)
def kind(title):
    if REFUSAL.search(title): return "refusal"
    if BOUND.search(title): return "boundary"
    return "nominal"
rows, tiles, seen = [], [], collections.Counter()
def parse(path, level):
    for line in open(path):
        line=line.strip()
        if not line or line.startswith("#"): continue
        key, flags, title, members = [x.strip() for x in line.split("|")]
        flags = flags.split(); X="X" in flags; NEW="NEW" in flags
        toks = members.split()
        tscope = TOK2SCOPE[key.split(".")[0] if key.split(".")[0]!="CORE" else "CORE"] if False else None
        prefix = key.split(".")[0]
        tscope = TOK2SCOPE[prefix]
        survivor = None; mem=[]
        for i,t in enumerate(toks):
            tid, _, a = t.partition(":")
            oid = full(tid, level)
            if not a:
                if i==0 and not NEW: a="k"
                elif level=="StRS": a="m"
                elif X and TOK2SCOPE[tid.replace("StRS-","").split("-")[0]]!=tscope: a="x"
                elif X and NEW: a="x"
                else: a="s"
            if a=="k": survivor=oid
            mem.append((oid,a))
        live = any(a!="d" for _,a in mem)
        tiles.append(dict(key=key, level=level, scope=tscope, title=title, survivor=survivor or ("NEW" if live else "-"),
                          crosscut=X, members=len(mem), live=live))
        for oid,a in mem:
            seen[oid]+=1
            r = ACTIVE.get(oid)
            if r is None: print("UNKNOWN or deprecated:", oid); continue
            oscope = r["scope"]; action = ACT[a]
            t = r["title"]
            if a=="k": reason=f"survivor id of {key}; retitle to '{title}'" if t!=title else f"survivor id of {key}"
            elif a=="s": reason=f"{kind(t)} scenario of {key}: '{t}'"
            elif a=="m": reason=f"same behaviour specified twice; merged into {key}: '{t}'"
            elif a=="x": reason=f"instance of the cross-cutting rule {key}: '{t}'"
            elif a=="d": reason=f"not observable behaviour (internal mechanism): '{t}'"
            if level=="StRS" and a=="m": reason=f"use case folded into {key}: '{t}'"
            if oscope in MAIN and a!="k":
                if a=="d": reason = "okfreq archive; "+reason
                else:
                    reason = f"okfreq supersede by the survivor of {key} ({ACT[a]}); "+reason
                    action = "supersede"
            rows.append((oid, key, action, reason, oscope, level))
parse("tiles_swrs.txt","SwRS"); parse("tiles_strs.txt","StRS")
missing = [i for i in ACTIVE if seen[i]==0]; dup=[i for i,c in seen.items() if c>1]
print("missing", len(missing), missing[:40]); print("dup", dup)
with open("mapping.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["old_id","new_tile_key","action","reason"])
    for oid,key,action,reason,_,_ in sorted(rows, key=lambda r:(r[5]!="StRS", r[0])): w.writerow([oid,key,action,reason])
with open("tiles.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["tile_key","level","scope","crosscutting","survivor_id","old_requirements","proposed_title"])
    for t in tiles:
        if t["live"]: w.writerow([t["key"],t["level"],t["scope"],"yes" if t["crosscut"] else "",t["survivor"],t["members"],t["title"]])
# counts
before = collections.Counter((r["scope"],r["type"]) for r in ACTIVE.values())
after = collections.Counter((t["scope"],t["level"]) for t in tiles if t["live"])
acts = collections.defaultdict(collections.Counter)
for oid,key,action,reason,osc,lvl in rows: acts[(osc,lvl)][action]+=1
out = {}
for s in sorted({r["scope"] for r in ACTIVE.values()}):
    out[s] = dict(swrs_before=before[(s,"SwRS")], swrs_after=after[(s,"SwRS")], strs_before=before[(s,"StRS")], strs_after=after[(s,"StRS")],
                  swrs_actions=dict(acts[(s,"SwRS")]), strs_actions=dict(acts[(s,"StRS")]))
    print(f"{s:22} SwRS {before[(s,'SwRS')]:4} -> {after[(s,'SwRS')]:3}   StRS {before[(s,'StRS')]:3} -> {after[(s,'StRS')]:2}  {dict(acts[(s,'SwRS')])}")
print("TOTAL SwRS", sum(before[(s,'SwRS')] for s in out), "->", sum(after[(s,'SwRS')] for s in out),
      " StRS", sum(before[(s,'StRS')] for s in out), "->", sum(after[(s,'StRS')] for s in out))
tot=collections.Counter(a for (_,lvl),c in acts.items() if lvl=="SwRS" for a in c.elements())
print(dict(tot))
sizes = collections.Counter(t["members"] for t in tiles if t["live"] and t["level"]=="SwRS")
print("tile size histogram", sorted(sizes.items()))
print("big tiles", [(t["key"],t["members"]) for t in tiles if t["members"]>=11 and t["level"]=="SwRS"])
json.dump(dict(per_scope=out, totals=dict(tot)), open("counts.json","w"), indent=1)
