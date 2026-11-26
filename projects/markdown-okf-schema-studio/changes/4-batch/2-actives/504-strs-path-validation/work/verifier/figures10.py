"""StRS coverage figures from okfreq reports of main, the base and the head. usage: figures10.py <folder>"""
import collections
import json
import sys

folder = sys.argv[1]
for name in ("main", "base", "head"):
    rep = json.load(open(f"{folder}/rep-{name}.json", encoding="utf-8"))
    every = {r["id"]: r for r in rep["requirements"]}
    strs = [r for r in rep["requirements"]
            if r["id"].startswith("StRS") and (r.get("frontmatter") or {}).get("req_lifecycle") not in ("deprecated", "superseded")]
    cov = [s for s in strs if s["stakeholder_test_coverage"]["status"] == "covered"]
    full = [s for s in strs if s["stakeholder_test_coverage"].get("linked_swrs")
            and all(x["status"] == "covered" for x in s["stakeholder_test_coverage"]["linked_swrs"])]
    direct = [s for s in strs if (s["stakeholder_test_coverage"].get("validation_tests") or {}).get("count")]
    both = [s["id"] for s in direct if s in full]
    print(name, "live", len(strs), "covered", len(cov), "all linked SwRS covered", len(full),
          "direct tests_req", len(direct), "both", both)
    linked = {x["id"]: x["status"] for s in strs for x in s["stakeholder_test_coverage"].get("linked_swrs") or []}
    exempt = collections.Counter(v for k, v in linked.items()
                                 if (every.get(k, {}).get("frontmatter") or {}).get("annotation_exemption"))
    print("  exempt linked SwRS by status", dict(exempt))
