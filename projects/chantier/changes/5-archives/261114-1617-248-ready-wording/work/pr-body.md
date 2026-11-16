## Summary

One word, "ready", covered every change whose work is done, whether its pull request was a draft waiting on another change or an open one the user could merge. A draft read as "ready" invited a merge that lands in another branch. After this PR, a done change reads as one of three states, everywhere the user or an agent reads it: the CLI's output, the STATUS files, the web board and the Claude Code pane.

## Deliverables

| State | Icon | Meaning |
| --- | --- | --- |
| ready locally | 🟣 | work done and proven, no PR yet |
| PR in draft | 🟤 | PR open as a draft, waits for what is under it: do not merge |
| ready to merge | 🟢 | PR out of draft, everything under it ready to merge too |

- The CLI records the forge's draft state (`pr_draft`, set by `ship --draft` and `stack --out-of-draft` / `--draft`), so the word never runs ahead of the forge.
- 🔵 no longer marks any state; ✅ stays merged.
- Side by side at `2202425`, for one batch holding a change in each state: the web board's Home below, and `status` and `STATUS.md` show the same words and icons: ready to merge 🟢, PR in draft 🟤, ready locally 🟣, working 🟡. The pane is not shown: see Known gaps.

![The web board's Home in French: prête à merger, PR en draft, prête localement](https://github.com/user-attachments/assets/d0e808c4-fe30-47e0-892e-484cc29b2a16)

## Blast radius

Grade: 2. Printed lines that cards and the scenario match on change (`hand-back ready to merge` / `hand-back PR in draft`, `stack-ready-to-merge`). Revert restores the old words; old records read as "PR in draft" until a `ship` or `stack --out-of-draft` records otherwise.

## Autonomous decisions

- The derived word lives in a new `chantier/stacks.py` (with `chain` and `stack_base` moved down from `commands/facts.py`) so `status/` and `board/` can read it without importing `commands/`.

## Known gaps

- No screenshot of the pane from a real session.
- The documentation's PNG screenshots under `docs/` were not regenerated.
- The board's Kanban and batch views are not captured in the side-by-side (only Home).
- No scenario check reads `PR in draft` in the `to come:` line of `forge-stack`.

<details>
<summary>Details</summary>

## Changes

- `core/records.py`: `pr_draft` on a change's entry; `stacks.py`: `ready_word`.
- `commands/delivery.py`, `driver.py`, `facts.py`, `batch_status.py`, `forge_stack*.py`: the recorded draft and the printed words.
- `status/words.py`, `status/views.py`: icons, labels, `readiness` in `STATUS.json`.
- `board/`: the views show the label and the new colours.
- `hooks/register.tsx`, `types/index.d.ts`, `hooks/register.test.tsx`: the pane waits for the user only on "ready to merge".
- Cards, docs, SVGs and the scenario say the three words.

## Test plan

- [x] New or changed tests: the pane test expects the three labels; a new scenario stage `ready_words` (35/35 on both forges at `2202425`) covers the three states
- [x] Local gates at `2202425`: `just mod` 57 pass; the long gate is waived for this batch
- [x] Evidence at `2202425`: the web board's Home, `status` output and `STATUS.md` side by side (above)
- [x] Review: approved at `8686cb4` (rebase move), last edits at `2202425` carried from `8686cb4`
- [x] Verified at `2202425`
- [x] CI green at `2202425`: `gh pr checks 197`, 5 of 5 pass

## Internal references

CR-248 (ready-wording), batch-17. Evidence: `work/verifier/evidence/` in the CR folder.

</details>
