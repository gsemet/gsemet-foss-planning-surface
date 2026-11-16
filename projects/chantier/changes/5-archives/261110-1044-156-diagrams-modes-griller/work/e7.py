import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])

R = "README.md"
rep(R, """Modern coding agents like Claude Code or Copilot provide "nested session" features.
Chantier uses them to give you a single "ticket office" to talk to,
while one "Foreman" coordinates the work underneath, or, in direct mode, the Chief of Staff itself.
""", """- Chantier adds one more level over your tracker's issues (Jira, GitHub, GitLab...): the
  [Change Request](#change-requests-lifecycle), for the small requests that never reach the tracker.
- You talk to one person, the Chief of Staff, in your own session; a Griller, another session of
  yours, can grill and specify the backlog beside it.
- A batch is steered by a Foreman in a nested session, or, in direct mode, by the Chief of Staff
  itself.
- There is nothing to configure: your `AGENTS.md` is the only configuration, and chantier writes
  only in `.agents/changes/`.
""")

rep(R, """![How chantier works, in short](docs/how-chantier-works-simple.svg)

The same, in detail:
""", """In direct mode, the Chief of Staff steers the batch itself:

![How chantier works in direct mode, in short](docs/how-chantier-works-simple-direct.svg)

With a Foreman, a nested session steers the batch:

![How chantier works with a Foreman, in short](docs/how-chantier-works-simple-foreman.svg)

The difference: with a Foreman, a Change Request may join while the batch runs; in direct mode it
joins only once every other one is handled and the batch is paused.

The same, in detail:
""")

rep(R, """A "Change Request" is an idea, a bug, a report, an issue, that you want to study.

Chantier translated this into a markdown file in a folder that will be carried in various folder during planning, study, implementation, QA, deployment and finally archive.
""", """A "Change Request" is one more level over the issues of your tracker (Jira, GitHub, GitLab...).
It lets you accept and prioritise small requests that do not belong in the tracker: an idea, a bug,
a report. The tracker keeps the strategic vision, the external requests and the long-term planning.

Chantier turns each request into a folder in `.agents/changes/`, carried through planning, study, implementation, QA, deployment and finally archive.
""")
print("ok")
