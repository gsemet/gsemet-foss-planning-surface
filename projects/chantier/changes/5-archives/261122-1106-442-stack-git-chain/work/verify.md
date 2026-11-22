# Verify CR-442

Head: 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9

Judged at 311ccf4 (full SHA above) unless noted.

## Claims

1. Gate pass cited: `work/gates/20261122-032537.log` first line `gate CR-442 branch chantier/batch-30/cr-442-an-ordered-stack-is-checked-as-a-git-cha head 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9`, last line `result: pass at 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9`. PASS.
2. CI at the head: `gh pr checks 417` shows `just check` (macos, ubuntu, windows), `just eval-dry-run` and `just scenario (ubuntu-latest)` all `pass`. PASS.
3. Refusal paths of `ship` and `stack --out-of-draft` (first message, second message `branch moved since its last ship`, remote ref deleted, recorded-not-pushed, live start_on, series, release top-at-new-head and cut-from-main, seen-merged with and without journal line, not-checked cases, `git cannot read`; out-of-draft refusal naming `put CR-102, CR-103' PRs back to draft` / `put CR-102' PRs back to draft`, accepted chain, seen-merged, release, git cannot read), each on real git commits, record unchanged. Command: `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_stack_chain.py skills/chantier/scripts/cli/tests/test_stack_chain_cards.py -v` -> `28 passed in 96.10s`. PASS.
4. Card guard (`test_the_cards_carry_the_chain_check`, in the run above): PASSED.
5. Real refusal line in the PR body: scenario output at 311ccf4 holds `error: CR-103: branch not based on CR-102's head d8be1c4: rebase onto chantier/batch-01/cr-102-stack-middle, push, ship again; nothing recorded` (grep of scenario/results/20261122-032540-31664). PASS.
6. Review box: PR body has Review `pending`; the Driver's notes (`chantier log CR-442`) show `r2 inspector approved at be847cc6` then `committed as 311ccf4d`. Not a box claim yet; no failure.
7. PR description as posted (second pass, 311ccf4): `gh pr view 417 --json body` equals work/pr-body.md (only a trailing blank line differs); headRefOid 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9. Renders, no images, no username or home folder. Changes now matches `git diff --stat 9b22d874..HEAD` (13 files): `core/git.py`, `stack_chain.py` (new, holds `chain_below`), `commands/chain_check.py` (new), `stacks.py` (`stack_base` takes `landed`), `commands/delivery.py`, `declare/delivery.py`, `scenario/README.md`, `run_scenario.py` (scenario steps), tests incl. `test_hold_live_shared.py`, `driver.md`, `foreman.md`. Known gaps "None": no UNVERIFIED claim or missing evidence pair. PASS.

## Verdict

VERIFIED at 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9: claims 1-6 carried from the first pass at this same head (no move); claim 7 re-judged and passes.

## Description pass (third, posted body with Test plan boxes filled), head 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9

Command: `gh pr view 417 -R gsemet/chantier --json body,headRefOid` -> headRefOid 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9. Sections in template order, fold with blank lines after `</summary>` and before `</details>`, no image, no username or home folder.
- Changes vs `git diff --stat 9b22d874..HEAD` (13 files): every file named or covered (scenario README and run_scenario.py as "scenario steps", driver.md, foreman.md, chain_check.py, delivery.py, git.py, declare/delivery.py, stack_chain.py, stacks.py, tests). PASS.
- Test plan boxes checked, each names 311ccf4; Review box: `chantier log` shows `r2 inspector approved at be847cc6` then `r2 committed as 311ccf4d`, matching "committed as 311ccf4". Verified box: Driver verdict VERIFIED at 311ccf4 (log). CI line matches earlier `gh pr checks` claim 2. PASS.
- Known gaps "None": no UNVERIFIED claim, no missing evidence pair. Role names in body are product terms of a card change. PASS.
Earlier proofs carried from this same head (no move).

VERIFIED at 311ccf4d7860db8eb052f7e3a1e06eab0ff549b9.
