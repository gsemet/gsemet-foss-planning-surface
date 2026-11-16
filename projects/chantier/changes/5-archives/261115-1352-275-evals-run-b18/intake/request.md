# Run the real-foreman and real-direct evals on the new chantier

Filed 2026-11-15 by the Chief of Staff, on the user's word: "rajoute une CR qui pilotera les evals après tout (donc en dépendance de toutes les autres tâches ouvertes du batch). Il me faudra les exécutions sur le nouveau Chantier."

The ask: once every other CR of batch-18 is merged (it waits for all of them, CR-268 to CR-274), run the two quick campaigns of evals/README.md on the sandbox with the chantier that main then holds: `real-foreman` (evals/real-foreman/RUNBOOK.md) and `real-direct` (evals/real-direct/RUNBOOK.md). Deliverable: the two reports in `evals/results/<campaign>-<date>.md` and the campaigns' "Last run" rows of evals/README.md, on one PR (evals/README.md, step 6: nothing else committed), with each campaign's findings and the audit, judge and cost numbers.

Constraints from the repository (to respect, and to settle in the spec):
- AGENTS.md: during an eval the main checkout does not change, neither its files nor its branch; the eval workspace is outside the repository and gets the plugin from the user's install. So the runs start only once the stack is merged and no other work runs on the main checkout.
- evals/README.md, "Before you start" and "The host's limits": on Claude Desktop, starting a Foreman's session needs a line typed in the desktop app (refused under Remote Control); 10 messages per session; Auto-fix off for the operator's session; `gh` logged in for a sandbox campaign.
- Who operates: a campaign needs an operator session playing the Chief of Staff and the user in the eval workspace. Say which parts a Driver of this batch can do itself (staging with evals/kit/setup.py, audit, cost, reading transcripts, writing the reports, the PR) and which are the user's step at the desktop (starting the operator's or the Foreman's session), with the exact prompt or command to paste.
- Generality: the runs here are on Claude Code with GitHub; the Copilot and GitLab trials stay the user's, later; name them as not covered.
