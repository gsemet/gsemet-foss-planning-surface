import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
R = "README.md"
t = open(R, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in t else "\n"
t = t.replace("\r\n", "\n")

# intro
a = t.index("- Chantier adds one more level")
b = t.index("## How Chantier works")
t = t[:a] + """- **Change Requests beside your tracker.** A Change Request (CR) is one more level over your
  tracker's issues: small requests are accepted and prioritised here, without entering the
  tracker ([more](#change-requests-lifecycle)).
- **One person to talk to.** You talk to the Chief of Staff, in your own session. It keeps the
  backlog and asks the questions a change needs. Nothing starts without your go, and you merge
  the pull requests. Optional: a Griller session grills beside it.
- **Direct or Foreman.** The Chief of Staff steers a batch itself (direct mode), or a nested
  Foreman session steers it (Foreman mode). In Foreman mode a CR can join a running batch; in
  direct mode, only once the batch is paused.
- **Zero configuration.** Your `AGENTS.md` is the only configuration. Everything chantier writes
  is Markdown and JSON in `.agents/changes/`, in your project.

""" + t[b:]

a = t.index("In direct mode, the Chief of Staff steers the batch itself:")
b = t.index("The same, in detail:")
t = t[:a] + """**Direct mode** (`/chantier:chief-of-staff direct`): the Chief of Staff steers the batch itself;
it works in a remote session; to grill while a batch runs, open a Griller session.

![How chantier works, in direct mode](docs/how-chantier-works-simple-direct.svg)

**Foreman mode** (`/chantier:chief-of-staff`): a nested Foreman session steers each batch, at the
desktop; your Chief of Staff stays free for a natural, dynamic conversation while it runs.

![How chantier works, in Foreman mode](docs/how-chantier-works-simple-foreman.svg)

The difference that matters most: once a batch runs in direct mode, a new CR, specified or not,
joins it only when all the other CRs are handled and the batch is paused; in Foreman mode a CR
can join while the batch runs.

""" + t[b:]
open(R, "w", encoding="utf-8", newline="").write(t.replace("\n", nl))

rep("docs/use-cases.md",
    "what differs is how dynamic the batch is while it runs: with a Foreman a \nCR may join a running\nbatch, in direct mode it joins only once every other CR is handled and the batch is paused.",
    "what differs is how dynamic the batch is while it runs: with a Foreman a\nCR may join a running batch; in direct mode a new CR, specified or not, joins only once every\nother CR is handled and the batch is paused.") if False else None
print("ok")
