"""Per-report counts: covered StRS, StRS with every linked SwRS covered, StRS with a direct validation test."""
import json
import sys

for path in sys.argv[1:]:
    report = json.load(open(path, encoding="utf-8"))
    strs = [r for r in report["requirements"]
            if r["id"].startswith("StRS") and (r.get("frontmatter") or {}).get("req_lifecycle") not in ("deprecated", "superseded")]
    cov = [s for s in strs if s["stakeholder_test_coverage"]["status"] == "covered"]
    full = [s for s in strs if s["stakeholder_test_coverage"].get("linked_swrs")
            and all(x["status"] == "covered" for x in s["stakeholder_test_coverage"]["linked_swrs"])]
    direct = [s["id"] for s in strs if (s["stakeholder_test_coverage"].get("validation_tests") or {}).get("count")]
    name = "base" if "scratch\\vb" in path or "scratch/vb" in path else "head"
    print(name, "live", len(strs), "covered", len(cov), "all linked SwRS covered", len(full),
          "with direct tests_req", len(direct), direct if len(direct) < 6 else "")
