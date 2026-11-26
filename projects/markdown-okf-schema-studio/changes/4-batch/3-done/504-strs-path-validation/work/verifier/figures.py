"""StRS coverage figures of an okfreq report (live StRS only)."""
import collections
import json
import sys

report = json.load(open(sys.argv[1], encoding="utf-8"))
reqs = {r["id"]: r for r in report["requirements"]}
RETIRED = ("deprecated", "superseded")


def fm(r):
    return r.get("frontmatter") or {}


def live(r):
    return str(fm(r).get("req_lifecycle") or r.get("req_lifecycle") or r.get("lifecycle")) not in RETIRED


strs = [r for r in reqs.values() if r["id"].startswith("StRS") and live(r)]
print("keys:", sorted(strs[0].keys()))
status = lambda v: v.get("status") if isinstance(v, dict) else v
covered = [r["id"] for r in strs if status(r.get("stakeholder_test_coverage")) == "covered"]
print("live StRS", len(strs), "covered", len(covered))
for key in ("stakeholder_test_coverage",):
    print("sample", json.dumps(strs[0].get(key))[:400])
    print("statuses", dict(collections.Counter(status(r.get(key)) for r in strs)))
children = collections.defaultdict(list)
for r in reqs.values():
    if r["id"].startswith("SwRS") and live(r):
        for parent in fm(r).get("derives_from") or []:
            children[parent].append(r)
for key in ("test_coverage", "coverage"):
    if any(key in r for r in reqs.values() if r["id"].startswith("SwRS")):
        full = [s["id"] for s in strs if children[s["id"]] and all(status(c.get(key)) == "covered" for c in children[s["id"]])]
        print(f"live StRS with every live derived SwRS {key}=covered:", len(full))
direct = [(r["id"], r.get("tested_in_files") or fm(r).get("tested_in_files")) for r in strs]
for s in strs:
    if s["id"].endswith("TRUST-012"):
        d = {k: v for k, v in s.items() if k not in ("text", "body", "frontmatter")}
        print("TRUST-012", json.dumps(d)[:1500])
