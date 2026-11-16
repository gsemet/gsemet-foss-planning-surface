Head: c4e3cae1ef9efea3110e8efa6e857b9841955e5a

Claims, all judged at c4e3cae1ef9efea3110e8efa6e857b9841955e5a (run in the CR-243 worktree).

1. The diff touches only concepts.md.
   Command: `git diff --stat origin/main...HEAD`
   Output: ` skills/chantier/references/concepts.md | 15 ++++++++++-----` / `1 file changed, 10 insertions(+), 5 deletions(-)`. PASS.

2. The old wording is gone from the cards.
   Command: `Get-ChildItem skills/chantier/references -Recurse -File | Select-String -Pattern 'last open dependency|every CR starts'`
   Output: no match line; `matches=0`. PASS.

3. The Parallel and Stack sentences match the specification text.
   Command: `git diff origin/main...HEAD`
   Output: Parallel now reads "every CR with no open dependency starts from the default branch at once ... a CR with a dependency starts only once that dependency is `ready` (`take` refuses it until then), on the branch of its last dependency still open, else on the default branch (see **Dependencies**), and its PR stays a draft on that branch until the dependency merges"; Stack reads "every CR with no open dependency starts at once, on the default branch; a CR with a dependency starts only once that dependency is `ready` (`take` refuses it until then), on the branch of its last dependency still open, else on the default branch (see **Dependencies**), and the stack driver puts the PRs each on the previous one". Same as the specification; the unchanged tails are intact. PASS.

4. They agree with the Dependencies paragraph.
   Command: `Select-String -Path skills/chantier/references/concepts.md -Pattern 'last dependency still open|take. refuses'`
   Output: lines 181 ("`take` refuses a queued CR until ...") and 185 ("The CR starts on the branch of its last dependency still open") say the same as lines 109 and 119. PASS.

5. foreman.md, driver.md and chief-of-staff.md carry no contradicting wording.
   Command: `Select-String -Path foreman.md,driver.md,chief-of-staff.md -Pattern 'at once|waits for'`
   Output: foreman.md:130 "A queued CR that `status` shows `waits for ...` is not yours to start"; the other "at once" hits are about restarts, notes and stops, not about starting a dependent CR. PASS.

6. Working tree is clean. Command: `git status --short`. Output: empty. PASS.

Not run: `just scenario` (waived by the user for this batch). CI: 5 of 5 green, per the prompt.

VERIFIED
