import csv, json, re, collections
rows=[r for r in csv.DictReader(open("mapping.csv")) if r["old_id"].startswith("SwRS")]
R={r["id"]:r for r in json.load(open("reqs.json"))}
tiles={r["tile_key"]:r for r in csv.DictReader(open("tiles.csv"))}
def kind(r):
    a=r["action"]
    if a=="supersede":
        m=re.search(r"\((keep|fold-as-scenario|merge-into|replace-by-crosscutting)\)", r["reason"]); return m.group(1)
    return a
K=collections.Counter(); KS=collections.defaultdict(collections.Counter); EX=collections.defaultdict(list)
for r in rows:
    k=kind(r); K[k]+=1; KS[k][R[r["old_id"]]["scope"]]+=1
    if len(EX[k])<8: EX[k].append(r["old_id"].replace("SwRS-MDOKFSTUDIO-",""))
print(dict(K))
for k in K: print(k, dict(KS[k].most_common()))
# cross-cutting family sizes: all members of X tiles
X=collections.defaultdict(lambda: collections.Counter())
for r in rows:
    t=tiles.get(r["new_tile_key"])
    if t and t["crosscutting"]=="yes": X[r["new_tile_key"]][R[r["old_id"]]["scope"]]+=1
for k,v in sorted(X.items(), key=lambda kv:-sum(kv[1].values())): print(k, sum(v.values()), dict(v))
# scenario folds by kind
fk=collections.Counter()
for r in rows:
    if kind(r)=="fold-as-scenario":
        fk[r["reason"].split("scenario of")[0].split()[-1]]+=1
print("fold kinds", fk)
# implementation-flavoured wording in normative sentence
impl_words=re.compile(r"\b(preview[A-Z]\w+|data-[a-z-]+|--[a-z-]+|\w+\.ts\b|CSSOM|aria-\w+|[a-z]+[A-Z]\w+\(|\bpx\b)")
c=collections.Counter(); ex=[]
for r in rows:
    d=R[r["old_id"]]["description"]
    if impl_words.search(d): c[R[r["old_id"]]["scope"]]+=1; ex.append(r["old_id"].replace("SwRS-MDOKFSTUDIO-",""))
print("impl-wording", sum(c.values()), dict(c.most_common()), ex[:10])
json.dump(dict(kinds=dict(K), kinds_per_scope={k:dict(v) for k,v in KS.items()}, examples=EX,
  crosscut={k:dict(v) for k,v in X.items()}, fold_kinds=dict(fk), impl_wording=sum(c.values()), impl_wording_per_scope=dict(c)), open("patterns.json","w"), indent=1)
