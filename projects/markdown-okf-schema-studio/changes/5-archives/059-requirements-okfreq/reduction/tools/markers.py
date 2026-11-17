import json, csv, collections
tr=json.load(open("trace.json")); impl=tr["implemented"]; tested=tr["tested"]; val=tr.get("validation_tests",{})
rows=list(csv.DictReader(open("mapping.csv")))
R={r["id"]:r for r in json.load(open("reqs.json"))}
tile_of={r["old_id"]:(r["new_tile_key"],r["action"]) for r in rows}
before_i=sum(len(impl.get(i,[])) for i in tile_of if i.startswith("SwRS")); before_t=sum(len(tested.get(i,[])) for i in tile_of if i.startswith("SwRS"))
ti=collections.defaultdict(set); tt=collections.defaultdict(set); per=collections.defaultdict(lambda:[0,0,0,0])
for i,(k,a) in tile_of.items():
    if not i.startswith("SwRS") or a=="drop-implementation-detail": continue
    for f in impl.get(i,[]): ti[k].add(f)
    for f in tested.get(i,[]): tt[k].add(f)
after_i=sum(len(v) for v in ti.values()); after_t=sum(len(v) for v in tt.values())
for i,(k,a) in tile_of.items():
    if not i.startswith("SwRS"): continue
    s=R[i]["scope"]; per[s][0]+=len(impl.get(i,[])); per[s][1]+=len(tested.get(i,[]))
scope_of_tile={}
for r in csv.DictReader(open("tiles.csv")): scope_of_tile[r["tile_key"]]=r["scope"]
for k in ti: per[scope_of_tile[k]][2]+=len(ti[k])
for k in tt: per[scope_of_tile[k]][3]+=len(tt[k])
print("impl file-links", before_i, "->", after_i, " test file-links", before_t, "->", after_t)
for s,v in sorted(per.items()): print(f"{s:22} impl {v[0]:4}->{v[2]:4}  test {v[1]:4}->{v[3]:4}")
# tiles with most test files (marker fan-out)
fan=sorted(((len(tt[k]),k) for k in tt), reverse=True)[:12]; print(fan)
# dropped detail: tests that would lose their marker
drop=[i for i,(k,a) in tile_of.items() if a=="drop-implementation-detail"]
print("drop ids", [(i.replace("SwRS-MDOKFSTUDIO-",""), tested.get(i)) for i in drop])
json.dump(dict(before_impl=before_i, after_impl=after_i, before_test=before_t, after_test=after_t,
  per_scope={s:dict(impl_before=v[0],test_before=v[1],impl_after=v[2],test_after=v[3]) for s,v in per.items()}), open("markers.json","w"), indent=1)
