import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
rep("docs/use-cases.md",
    "**direct mode**. The lifecycle is the same; what differs is how dynamic the batch is while it runs: with a Foreman a CR may join a running\nbatch; in direct mode a new CR, specified or not, joins only once every other CR is handled and\nthe batch is paused.",
    "**direct mode**. The lifecycle is the same; what differs is how dynamic the batch is while it\nruns: with a Foreman a CR may join a running batch; in direct mode a new CR, specified or not,\njoins only once every other CR is handled and the batch is paused.")
rep("docs/tutorial-claude-code.md",
    "twelve\nagents (`chantier:cr-driver`,\n`chantier:coder`, ",
    "twelve\nagents (`chantier:cr-driver`, `chantier:coder`, ")
print("ok")
