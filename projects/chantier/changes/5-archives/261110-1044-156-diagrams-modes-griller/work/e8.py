import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
rep("skills/chief-of-staff/SKILL.md",
    "Chief of Staff for a change-request team on Claude Desktop or a Copilot SDK host.",
    "Chief of Staff for a change-request team (Foreman mode on Claude Desktop or a Copilot SDK host,\n  direct mode anywhere).")
rep("docs/tutorial-claude-code.md",
    "This installs one skill (the Chief of Staff) and twelve agents",
    "This installs three skills (the router `chantier`, `chief-of-staff` and `griller`) and twelve agents")
rep("docs/use-cases.md",
    "what differs is how dynamic the batch is while it runs.",
    "what differs is how dynamic the batch is while it runs: with a Foreman a CR may join a running\nbatch, in direct mode it joins only once every other CR is handled and the batch is paused.")
print("ok")
