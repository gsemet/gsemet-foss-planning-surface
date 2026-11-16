# CR-131 evidence plan

All at the pushed head, each with the command and its output.

1. The cards name every forge call, on both forges: search `skills/chantier/references/` for
   `gh pr create --draft`, `glab mr create --draft`, `gh pr ready`, `glab mr update --ready`,
   `gh pr ready --undo`, `glab mr update --draft`.
2. Each bullet of the specification's "The cards" and "The report" maps to a line in a card: quote
   the line, by file and line number. The definition of ready is stated once and the other cards
   agree with it; no card still says a PR is opened as anything but a draft, and none says the
   stack driver opens one.
3. The cards do not contradict each other: read `driver.md`, `foreman.md`, `chief-of-staff.md`,
   `concepts.md`, `routing.md` on who turns a PR draft or ready. The Foreman stays out of it (it
   never edits a PR).
4. The CLI is unchanged: `git diff --stat origin/main...HEAD -- skills/chantier/scripts` is empty.
5. `evals/kit/forge.py` serves the new calls: run it on a throwaway state with `pr create --draft`,
   `pr view` (isDraft true), `pr ready` (false), `pr ready --undo` (true). `audit.py` allows
   `pr ready`.
6. Agent bodies: `just check` passes (identical bodies on both hosts), and `just scenario` passes.
