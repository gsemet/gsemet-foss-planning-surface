import difflib
import json
import subprocess
import sys

old_path, local_path, new_out = sys.argv[1], sys.argv[2], sys.argv[3]
raw = subprocess.run(
    ["gh", "pr", "view", "529", "--repo", "gsemet/markdown-okf-schema-studio",
     "--json", "headRefOid,state,isDraft,updatedAt,body"],
    check=True, capture_output=True,
).stdout.decode("utf-8")
posted = json.loads(raw)
with open(new_out, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(raw)
body = posted["body"].replace("\r\n", "\n")
with open(old_path, encoding="utf-8-sig") as handle:
    old = json.load(handle)["body"].replace("\r\n", "\n")
with open(local_path, encoding="utf-8-sig") as handle:
    local = handle.read().replace("\r\n", "\n")
print("head", posted["headRefOid"], posted["state"], "draft", posted["isDraft"], posted["updatedAt"])
print("posted == work/pr-body.md:", body.rstrip("\n") == local.rstrip("\n"))
print("diff previously judged body -> posted body:")
sys.stdout.reconfigure(encoding="utf-8")
for line in difflib.unified_diff(old.split("\n"), body.split("\n"), "judged-at-r3", "posted", n=0, lineterm=""):
    print(line)
