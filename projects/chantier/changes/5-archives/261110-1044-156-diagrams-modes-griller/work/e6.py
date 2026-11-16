import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])

# ---- session-start.md section 4
f = "skills/chantier/references/session-start.md"
start = "- **Change Request (CR):** one change to make, e.g. one issue."
end = "- **Drivers and workers:**"
with open(f, encoding="utf-8", newline="") as fh:
    t = fh.read()
nl = "\r\n" if "\r\n" in t else "\n"
i = t.index(start)
j = t.index(end)
new = """- **Change Request (CR):** one more level over the project's tracker issues (Jira, GitHub,
  GitLab…). It lets small requests outside the tracker be accepted and prioritised; the tracker
  keeps the strategic vision, external requests and long-term planning. A CR gets:
  - a folder in `.agents/changes/` (the request, its analysis, the user's answers, the
    self-contained Change Specification written before any code);
  - a branch and a worktree its Driver creates.

  It ends as one pull request.
- **One person to talk to, the Chief of Staff (me):** the only session that opens and runs
  batches. It keeps the backlog and asks the questions a CR needs. Nothing starts without the
  user's go. The user reviews and merges each PR; only a release's PR or fix is merged for them,
  on their word. (A Griller says "the Chief of Staff" of another session instead.)
  - A **Griller** is another session of yours that grills and specifies the backlog beside it,
    optional, never running batches.
- **Direct or Foreman:** a batch (`batch-<n>`) is steered either:
  - by a **Foreman**, a separate session that reports back to me, where a CR may join while the
    batch runs;
  - or by me in **direct mode**, where a CR joins only once every other CR is handled and the
    batch is paused, and I hold no grill while it runs (use a Griller).
- **Zero configuration:** the project's `AGENTS.md` is the only configuration (I learn how it
  builds, tests and merges from it). Everything chantier writes is Markdown and JSON in
  `.agents/changes/`.
""".replace("\n", nl)
t = t[:i] + new + t[j:]
with open(f, "w", encoding="utf-8", newline="") as fh:
    fh.write(t)

# ---- release-template.md
rep("skills/chantier/references/release-template.md", "merged PRs' Impacts sections", "merged PRs' Deliverables sections")

# ---- chief-of-staff skill description
print("ok")
