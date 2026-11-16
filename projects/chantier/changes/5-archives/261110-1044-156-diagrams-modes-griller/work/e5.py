import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
for f in ("docs/batch-lifecycle.svg", "docs/batch-lifecycle-texts.md"):
    rep(f, "grill in another session of yours", "grill in a Griller session", count=2)
print("ok")
