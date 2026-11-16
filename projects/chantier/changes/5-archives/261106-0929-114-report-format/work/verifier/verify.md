# Verifier, CR-114, at 4959358 (open gaps only)

Worktree CLI and card, scratch repos outside the batch. Evidence: evidence/verifier-heartbeat.md, evidence/verifier-two-tables.md. Earlier proof: evidence/verifier-status-word.md.

## (1) Card and SKILL.md against the first "Done when"
chief-of-staff.md "Reports" (lines 129-141) holds:
- Progress: header (number and name, mode, slots in use, CRs done, spend, budget); table CR, subject (few words), state, PR as a link, cost; cost table; always-there **For you:** (or "nothing"). All spec elements present.
- Completion: header (merged of total, spend, budget); table CR, subject, result, PR, rounds, cost; cost table one line per Driver type from `cost --by driver`; what the batch did not prove; **For you:** closing with what `close` lists. All present.
- Icons: waiting, working, to review, blocked, merged, each with its word; "belong to the report, STATUS.md keeps its own".
- Forge word: "MR" on a GitLab remote in column and text, "PR" elsewhere, known from the remote as for P9.
- Refresh: line 125-128 "run `$CHANTIER status --refresh` with no epoch: records the current spend and STATUS.md and leaves the Foreman's heartbeat alone"; "Never read the Foreman's transcript" kept (line 128).
- SKILL.md "status?" row (line 58): `$CHANTIER status --refresh` (no epoch), then `status`, links and STATUS.md; points to "While it runs". Agrees. Minor: Completion's PR column is not said to be a link (spec does not say so either).

## (2) Heartbeat left alone
Scratch repo p2 (GitLab remote), `open --parallel`, fake Foreman transcript. `status --refresh --epoch 1` set heartbeat 2026-11-06T09:26:24Z. After a spend increase (transcript +1M input), `status --refresh` with no epoch: exit 0, spent_usd 3.0 -> 5.0, heartbeat still 2026-11-06T09:26:24Z. A stale `--epoch 0` still exits 3.

## (3) Each table takes its own word
status._rows_markdown (the function that writes every table, batch STATUS.md and the top-level per-batch tables) called per table: one GitLab MR link plus one other link gives header `MR`; links all GitHub gives `PR`; no link gives `PR/MR`; all GitLab gives `MR`. Each table's word depends only on its own rows. Note: in a mixed table the non-GitLab cell is also labelled `MR` (the table's word), as the spec's "a table takes the word of its own links" says. Not shown through the CLI: only one batch can be open at once, so two live batch tables with different links cannot coexist; the function call stands in.

VERIFIED
