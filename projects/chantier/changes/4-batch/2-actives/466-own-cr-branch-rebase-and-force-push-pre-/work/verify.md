Head: e17cd34ba18773aa1f73c0be0b74d33d093e7c9a

NOT VERIFIED (the PR description only; the change itself is proved).

Claims, each judged at e17cd34b:

1. `just check` (lint, 2288 tests, release-notes) passes in the worktree: output ends
   `2288 passed, 20 skipped in 115.18s` and `release-notes: ... ok`. The new `test_rebase_rules.py`
   (table of rebase commands matched by their rules, narrow forms unmatched, remote fill `upstream/`,
   preflight warn and deny, card-text check) and `test_driver_prompt.py` run inside it.
2. Code: `git diff origin/main...HEAD` shows the 13 rebase samples in `allow_samples.py`, the shared
   `project_remote` and ` origin/` fill in `permissions.py`, the `Rewrites:` line between `writes:` and
   `Steering:` in `driver_prompt.py`, no line for `none`; the scenario step and README updated.
3. Cards: grep shows `foreman.md` "A Driver's refused rebase", `chief-of-staff.md` "A refused rebase",
   `driver.md` "Means: a rebase the host refuses", `concepts.md` `Rewrites:` column and rule 8,
   `routing.md` lines, `hosts/claude-code.md` rule rows and the 2026-11-23 mark; no remaining "asked
   only when the host refuses you too" without the rebase.
4. Deviations from the spec, all disclosed in Known gaps: the `--exec` ban is not in `driver.md`
   (it is in conflict-resolver.md, concepts.md rule 8 and the Rewrites text); the preflight asserts
   live in `test_rebase_rules.py`. Accepted.

Failed claim: the PR description at e17cd34b.
- Its Test plan proofs (`just check` at 6ca37b7: 2173 passed; `eval-dry-run` at 6ca37b7) name 6ca37b7,
  not the head and not a carried SHA: `git range-diff` shows 6ca37b7 replaced by e17cd34b and
  `git patch-id --stable` differs (df80799b vs ae9d4c7c), so the rebase changed the patch; the proof is
  not carried.
- Known gaps says "Not rebased onto CR-465 (no commits there yet)": the branch is now on main
  (b4cb7066) with CR-465's commits in it, so the bullet is stale.
- `eval-dry-run` at the head is not proved by me (not run); the description's claim is at 6ca37b7.
