## Summary

When a batch merges a PR, the main checkout stays at an older commit. In this repository that matters: the plugin runs in place, so a merged fix to the CLI keeps running unfixed until someone pulls (a merged model price went on leaving that model's calls unpriced). In any project the main checkout falls behind the default branch as the batch merges.

After each merge it records, the steering session now brings the main checkout to the default branch's new head, by a fast-forward only and only when that is safe: on the default branch, no change to any tracked file, nothing diverged, no untracked or ignored file in the way. Otherwise it does nothing and says why in one line. It is on by default; a rule in the project's `AGENTS.md` turns it off. It is a convenience, never a gate.

## Deliverables

The procedure the steering session follows (it stops at the first step that says no, and records one line):

| Step | Check | A "no" says |
| --- | --- | --- |
| 1 | the project's rules forbid it | `the project's rules forbid it: <rule>` |
| 2 | `git symbolic-ref --quiet --short HEAD` is the default branch | `on <branch>, not <default>` or `detached HEAD` |
| 3 | `git status --porcelain --untracked-files=no` is empty | `tracked changes: <paths>` |
| 4 | `git fetch <remote> <default>` | `fetch failed: <text>` |
| 5 | `git merge --ff-only --no-overwrite-ignore <remote>/<default>` | `diverged`, `untracked file in the way: <path>`, or the host's exact refusal |

The outcome is one note on the merged CR (`main checkout: fast-forwarded to <sha7>`, `already at <sha7>` or `not fast-forwarded: <why>`), and the next report carries it in Notes. The CLI changes nothing and runs no new git command. `--no-overwrite-ignore` is what keeps an ignored file safe: by default `git merge` overwrites one silently.

The scenario shows a fast-forward done and a refusal (tracked change, untracked file, ignored file in the way) followed by a catch-up at the next merge. The eval kit gains a rail, J26, that checks the main checkout follows the default branch after a recorded merge, and J22 now accepts only this exact merge form.

## Blast radius

Grade: **1**. The change is card text, docs, the scenario and the eval kit; no CLI behaviour changes. A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The scripted and staged steering sessions read the new head with `git rev-parse --short=7 HEAD` (read-only), which the specification's command list did not name; the scenario check and J26 allow it.
- The scenario harness skips `main checkout:` notes when looking for the release's back-note, so the new note does not hide it.

<details>
<summary>Details</summary>

## Changes

- Cards: the batch-steering card holds the procedure (a new bullet "The main checkout after a merge"); the planning card points to it for a session that steers alone and reports the latest note; `status-layout.md` adds the line to Notes; `concepts.md` amends the CLI paragraph and the git rule.
- Docs: `AGENTS.md`, `CONTRIBUTING.md`, `docs/planning-modes.md`, `docs/use-cases.md` state the new behaviour and the off switch.
- Scenario: a scripted steering session runs steps 2 to 5; a helper lands the user's merge on the bare origin without the fake forge.
- Eval kit: `audit.py` (J22 exception, new J26), `dry_run.py` (clean case and a planted plain `git merge` case), `SCORECARD.md`, and the eval READMEs and runbooks corrected.

## Human decisions

- On by default in every project, under strict conditions; a rule in the project's `AGENTS.md` turns it off.
- Tried after each recorded merge, not once at the pause.
- A skip costs the batch nothing: one line, no ask, no gate, no workaround.
- Untracked files are never moved, read or deleted, ignored ones included.
- The promise "writes only in the planning folder" gains the clause "and fast-forwards a clean main checkout after a merge it records".

## Impacts

No visual change. Maintainers see the main checkout follow the default branch after each merge; a batch that fixes the CLI runs the fix at once. Cards load at the next session or with `/reload-plugins`.

## Test plan

- [ ] New or changed tests: scenario section 8 (done and refused cases, both forges), dry-run J26 and plain-merge cases
- [x] Local gates at `deae40a`: `just check`; `just scenario` (594/594 on both forges at `b14f86f`) and `just eval-dry-run` (7 of 7 cases; the planted plain `git merge` fails with `FAIL [J22]`) carried from `b14f86f`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [ ] Evidence: none, no visual change (card text, docs, scenario, eval kit)
- [x] Review: approved at `deae40a` (after a move review of the restack)
- [x] Verified at `deae40a`
- [x] CI green at `deae40a`

## Internal references

- CR-210 main-checkout-fast-forward
- Specification: `.agents/changes/4-batch/2-actives/210-main-checkout-fast-forward/03-change-spec.md`

</details>
