"""Print the declared path section of StRS ids ("GROUP-NNN#S<n>") at a revision."""
import re
import subprocess
import sys

REPO, REV = sys.argv[1:3]
sys.stdout.reconfigure(encoding="utf-8")
files = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", REV, "requirements/tiers/strs"], capture_output=True, check=True).stdout.decode().split("\n")
for spec in sys.argv[3:]:
    rid, frag = spec.split("#")
    f = next(x for x in files if x.endswith(f"StRS-MDOKFSTUDIO-{rid}.md"))
    t = subprocess.run(["git", "-C", REPO, "show", f"{REV}:{f}"], capture_output=True, check=True).stdout.decode("utf-8").replace("\r\n", "\n")
    m = re.search(rf"^#### Path {frag}\b.*?(?=^#### Path |^### |^## |\n<!-- okf:links)", t, re.M | re.S)
    print(f"===== {spec}")
    print(m.group(0).strip() if m else "NOT FOUND")
