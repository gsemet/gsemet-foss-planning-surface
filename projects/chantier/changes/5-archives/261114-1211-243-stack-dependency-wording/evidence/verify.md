# Verify CR-243

Head: c4e3cae1ef9efea3110e8efa6e857b9841955e5a (PR 185, round 1 of 3)

Verdict: PASS. `just scenario` waived by the user for this batch; `just check` is CI's.

1. `git grep -n -E "last open dependency|every CR starts" -- skills/chantier/references` at c4e3cae: no output, exit 1 (no match). OK.
2. `git diff origin/main...HEAD -- skills/chantier/references/concepts.md`: the Parallel and Stack openings are the spec's text word for word (the Parallel line wrapping differs). Both say: a CR with a dependency starts only once it is `ready` (`take` refuses it until then), on the branch of its last dependency still open, else the default branch. This agrees with **Dependencies** (concepts.md ~181-187): `take` refuses until each `after` is `ready` or `merged`, and the start base is the last open dependency, else the default branch, in a stack too. OK.
3. `git grep -i "at once"` on foreman.md, driver.md and chief-of-staff.md: no hit says a dependent CR starts at once. The foreman.md hits (121, 146, 198, 277...) concern QA, restarts and rebase notes; the chief-of-staff.md:400 hit counts CRs "start at once" per slot (not a dependency claim). OK.
4. `git diff --name-only origin/main...HEAD`: only skills/chantier/references/concepts.md. `git status`: clean. OK.

Nit (not blocking): the Parallel paragraph has two over-long lines (not re-wrapped after the insertion); the rest of the file wraps near 100 columns.
