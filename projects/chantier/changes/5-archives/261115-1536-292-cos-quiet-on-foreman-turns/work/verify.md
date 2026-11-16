Head: f491f7d55085aa4bc78104999dfd7285b282eb3f

Claims, each judged at f491f7d:
1. Notice section exists: `grep -n "^#.*turn-end" hosts/claude-code.md` -> `112:## The Foreman's turn-end notice`; "finished a turn" at claude-code.md:117. chief-of-staff.md and routing.md link to hosts/claude-code.md and ../routing.md; targets exist (ls ok).
2. Scorecard: diff of evals/ adds only the J29 row; `grep -c "J27\|J28"` -> 0.
3. Diff touches four files: `git diff --stat origin/main...HEAD` -> SCORECARD.md, chief-of-staff.md, hosts/claude-code.md, routing.md (53 insertions, 0 deletions).
4. `just check` in the worktree: 200 passed, release-notes ok.
5. CI at head: `gh pr checks 237` -> check (macos, ubuntu, windows), eval-dry-run, scenario all pass.
6. PR description: posted body equals work/pr-body.md (diff: one trailing blank line); Summary/Deliverables/Changes match the diff; Known gaps lists the UNVERIFIED behaviour and the error exception; no STALE mark.
Behaviour (CoS quiet on a notice) is unprovable without a real Foreman batch: a Known gap, not a failure.

Description pass at f491f7d55085aa4bc78104999dfd7285b282eb3f:
7. Posted body (`gh pr view 237 --json body`) read against `git diff --stat origin/main...HEAD` (4 files, 53 insertions) and the template: Summary, Deliverables, Changes match the diff; Test plan SHAs are f491f7d; `gh pr checks 237` -> 5 checks pass; Known gaps carries both unproved claims; no STALE; renders (details fold closed properly).
8. Review box `approved at 4023df9`: `chantier log 292` -> "r1 approved at 842b800, committed as 4023df9 (rebased)"; box cites the committed-as SHA; carried to f491f7d by rebase ("already on f257647").

VERIFIED

---
Head: 190b208afe9d4a501ba0ee22ba0a47a81e87b57c

Re-judged at 190b208 after f491f7d -> 32df20b -> 190b208:
9. Diff: `git diff --stat origin/main...HEAD` -> 4 files (SCORECARD.md, chief-of-staff.md, hosts/claude-code.md, routing.md), 53 insertions. Notice section at claude-code.md:117; J29 row present; `git diff origin/main...HEAD -- evals | grep -c "^+.*J2[78]"` -> 0 (J27/J28 pre-exist on origin/main, count 2).
10. `just check` in worktree at 190b208: 223 passed, release-notes ok.
11. `gh pr checks 237`: 5 checks pass.
12. Posted body: Summary/Deliverables/Changes match the diff; Test plan SHAs are 190b208; Known gaps carries both unproved claims; no STALE.
13. FAIL: Review box says "approved at `190b208` (the move's pass...)". `chantier log 292` has no approved-pass note at 190b208 (grep "190b208\|62bd9ea" -> only a ship line and a CI note); the last approval note is "inspector approved at 32df20b6e9f..." for the conflict move. The box cites a SHA with no approval note. Fix: cite `32df20b` as the approval, "carried to 190b208 by a clean rebase", or log an approval note at 190b208.

NOT VERIFIED

---
Head: 190b208afe9d4a501ba0ee22ba0a47a81e87b57c

Description pass at 190b208 (code unchanged since the pass above):
14. Review box now reads "approved at 32df20b, carried from 32df20b to 190b208 by a clean rebase"; `chantier log 292` has "inspector approved at 32df20b6e9f..." (move f491f7d..32df20b), then the rebase to 190b208. Matches.
15. Posted body otherwise unchanged: Test plan SHAs 190b208, diff 4 files / 53 insertions, `gh pr checks 237` 5 pass, Known gaps carries both unproved claims, no STALE.

VERIFIED
