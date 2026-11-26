"""Read-only: print job and ci-integration / ci-visual step durations of the runs the PR body cites.

Usage: python -I verify_desc_jobs.py <run id> [<run id> ...]
"""
import json
import subprocess
import sys
from datetime import datetime

REPO = "gsemet/markdown-okf-schema-studio"


def gh(path):
    out = subprocess.run(["gh", "api", "repos/%s/%s" % (REPO, path)], check=True, capture_output=True).stdout
    return json.loads(out.decode("utf-8"))


def seconds(item):
    if not item.get("started_at") or not item.get("completed_at"):
        return None
    start = datetime.fromisoformat(item["started_at"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(item["completed_at"].replace("Z", "+00:00"))
    return int((end - start).total_seconds())


for run in sys.argv[1:]:
    info = gh("actions/runs/%s" % run)
    print("== %s %s %s %s attempt %s %s created %s" % (
        run, info["head_sha"][:7], info["head_branch"], info["event"], info["run_attempt"],
        info["conclusion"], info["created_at"]))
    for job in gh("actions/runs/%s/jobs?per_page=50" % run)["jobs"]:
        if job["conclusion"] == "skipped":
            print("   %-16s skipped" % job["name"])
            continue
        steps = ["[%s: %s %s s]" % (s["name"], s["conclusion"], seconds(s)) for s in job["steps"]
                 if "ci-integration" in s["name"] or "ci-visual" in s["name"]]
        print("   %-16s %s %s job %s s %s" % (job["name"], job["id"], job["conclusion"], seconds(job), " ".join(steps)))
        if job["name"] == "visual" and job["conclusion"] != "success":
            for note in gh("check-runs/%s/annotations" % job["id"]):
                print("      annotation: %s" % note["message"][:200])
