import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
rep("docs/use-cases.md",
    "what differs is how dynamic the batch is while it runs: with a Foreman a CR may join a running\nbatch, in direct mode it joins only once every other CR is handled and the batch is paused.",
    "what differs is how dynamic the batch is while it runs: with a Foreman a CR may join a running\nbatch; in direct mode a new CR, specified or not, joins only once every other CR is handled and\nthe batch is paused.")
rep("docs/tutorial-claude-code.md",
    "This installs three skills (the router `chantier`, `chief-of-staff` and `griller`) and twelve agents (`chantier:cr-driver`,\n",
    "This installs three skills (the router `chantier`, `chief-of-staff` and `griller`) and twelve\nagents (`chantier:cr-driver`,\n")
print("ok")
