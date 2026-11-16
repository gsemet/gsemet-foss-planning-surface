# Verify CR-260

Head: d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d

Verdict: VERIFIED

## Claims

1. Diff lists only the three cards (judged at d43abe1).
   `git diff --stat origin/main` in the worktree:
   `concepts.md | 6 ++--`, `driver.md | 37 +++-`, `hosts/claude-code.md | 5 ++--`; 3 files, 43 insertions, 5 deletions.
   No CLI, hook, type, agent file or scenario file. `hosts/copilot.md` is unchanged (the specification allowed that).

2. "Opening reads" paragraph (d43abe1). `git grep -n "Opening reads" -- skills`:
   `driver.md:13:Opening reads: you judge what you read whole and what you read by section...` (bullets 14-47: whole, whole, whole or by part, by section, how to read a section, a Driver started again, a rule not read still binds).
   `concepts.md:340` and `hosts/claude-code.md` (see 3, 4) point to it.

3. Driver's read line in `concepts.md`, "Starting an agent" (d43abe1). `git grep -n "Opening reads" -- skills/chantier/references/concepts.md`:
   `concepts.md:340:(`claude-code` or `copilot`) that its "Opening reads" names;                  (a Driver's prompt)`.
   Lines 338-341 show the Driver's line and the worker's line (`Read <skill>/references/worker.md, section "<Role>", and <skill>/references/concepts.md; (a worker's prompt)`), unchanged in substance. Cosmetic: the trailing "(a Driver's prompt)" annotations are padded with spaces. Not a failure.

4. Changed line in `hosts/claude-code.md`, "Who reads it, when" (d43abe1). Diff hunk at line 132:
   "The Foreman reads this file with its card. A Driver reads the sections its card's "Opening reads" names ("Tools", "Auto mode", "Compacting", "The write guard"), when the step comes: "Auto mode" tells it what a refusal means and that it is reported, never worked around."
   The reported-never-worked-around text is kept.

5. Every heading the paragraph names exists, with that exact text (d43abe1).
   `git grep -n -E "^#+ ..."` output:
   - `claude-code.md`: `14:## Tools`, `50:## Heartbeat`, `323:### Auto mode`, `376:## Compacting`, `431:## The write guard`, `475:## Classes of session`, `699:### Allow rules to add`; `111:## Configuration`.
   - `concepts.md`: `6:## Words`, `308:## Starting an agent`, `411:## Escalation`, `437:## Rules`.
   - `driver.md`: `48:## Your means`, `387:## CR driver`, `505:## Stack driver`, `707:## QA driver`, `718:## Release driver`.
   - `pr-template.md` and `worker.md` are named as files; their headings are not named by the paragraph (worker.md `## Verifier` at line 95).
   Note: "Auto mode" is a `###` heading (under "Configuration"), so "up to the next heading of the same level" ends at "What the docs do not say" (line 361). That works.
   The `driver.md` link at the "ready to merge" line now reads `[ready to merge](concepts.md), "Words"`. The word's entry is the bullet "Ready to merge" at `concepts.md:12`, in "Words".

6. `` `context: <where it stopped `` is still in `driver.md` (d43abe1).
   `git grep -n -F 'context: <where it stopped' -- skills/chantier/references/driver.md`: lines 341, 362, 699 (lines moved by the 35 added lines; the scenario's card check looks for the text).

7. Long gate passed at the head (d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d). Gate log `20261114-194714.log` first line: `gate CR-260 branch chantier/batch-18/cr-260-change-specification-a-driver-s-opening- head d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d`. Last line `result: pass at d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d` (github 895/895, gitlab 873/873). `handoff` checklist: `[x] long gate passed`; its notes quote CI green at d43abe1. Not rerun, as the brief says.

8. PR description as posted on the forge (d43abe1).
   `gh pr view 201 --json body,headRefOid`: `headRefOid` is d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d. After trimming and normalising line breaks the posted body is identical to `work/pr-body.md` (3426 characters each, equality `True`).
   Summary, Deliverables and Changes match the diff: three cards, the before/after read table, the "ready to merge" link change. The Known gaps names the after measure and the no-loss check, as the specification asks. No role name outside Internal references.
   Test plan placeholders `<sha7>` (Local gates, Review, Verified, CI green) are the Driver's to fill. They are not a failure here. The Review box is not yet judged: the Driver fills it from its note (`r1 inspector approved at ce00ec3`; the round was committed as d43abe1, so the Driver cites the SHA its note names).

## Before measure (batch-18 first Drivers that reached their first round)

Script: `work/verifier/opening-reads.py` (the specification's "Method": CR-236's prompt sum, last usage per message id, opening cost = prompt of the first call holding an `Agent` tool use or a `chantier round` command, minus the prompt of the first call). Run:
`python -I work/verifier/opening-reads.py ~/.claude/projects/C--Users-gaeta-Projets-chantier/446cff2e-8291-4f73-9ff0-f19c29743e6e/subagents`
(session 446cff2e is the newest folder holding batch-18 `chantier:cr-driver` agent meta files.)

| CR | agent | started (UTC) | opening | read before the call |
| --- | --- | --- | --- | --- |
| CR-256 | aae10202fc2a73baa | 2026-11-14 18:43 | 64.3k | driver.md, spec, claude-code.md whole; concepts.md by section |
| CR-253 | ad764600b1d84dad6 | 2026-11-14 18:43 | 87.5k | driver.md, spec, concepts.md, claude-code.md, all whole |
| CR-258 | a9b584e39b5b5021a | 2026-11-14 19:30 | 52.9k | driver.md, spec, concepts.md, all whole |
| CR-257 | a41fb231abed92f69 | 2026-11-14 18:43 | 41.9k | driver.md, spec whole; concepts.md limit 130 |
| CR-260 | a63c25e23141c9d49 | 2026-11-14 18:43 | 42.0k | driver.md, spec whole; concepts.md offset 308, limit 100 |

- All five first Drivers of batch-18 have reached a first round; no restart Driver in the folder; none pending.
- Group of five: mean 57.7k, median 52.9k.
- Without CR-260 (this CR's own Driver, who already read by section while writing the change): four Drivers, mean 61.6k, median 58.6k. This is the cleaner before figure. The Drivers that read the host reference whole cost 64.3k and 87.5k; those that read `concepts.md` by section or skipped the host reference cost 41.9k to 52.9k. That matches the specification's measure on batch-16 and batch-17 (mean 49.7k).
- The request's ~58k is next to it: the batch-18 before figure (57.7k, or 61.6k without CR-260) is close to it. Two thirds of 57.7k is 38.5k; of 61.6k, 41.1k.
- Method note: the Read tool with no limit counts as "whole" in the script; a read past its default line limit is not distinguished.
- The after measure and the "no loss" check come at batch-18's close, after the merge, per the specification. The Driver copies the before figures above into the PR's Deliverables (the description still says they come after the merge). The script goes with the CR's archive as `evidence/opening-reads.py`.

## Verdict

VERIFIED at d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d.

## Pass 2: posted description (d43abe1)

Head: d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d (`gh pr view 201 --json headRefOid`, unchanged).

Claims carried from above, judged on `gh pr view 201 --json body` against the diff (3 cards, 43 insertions, 5 deletions) and the template audit:

1. Sections 1-2 (order, fold): Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details block holding Changes, Human decisions, Impacts, Test plan, Internal references; blank lines after `</summary>` and before `</details>`; nothing after. No Issues References (no `issue:` line expected). OK.
2. Section 3 (internal references): the CR name and the specification path appear only in Internal references. "Driver" and "Foreman" are product terms of cards the diff changes. OK.
3. Section 4 (Deliverables): the table names the three cards and sections that exist in the diff; the before figures match my table above (64.3k, 87.5k, 52.9k, 41.9k, 42.0k; mean 57.7k, median 52.9k; 61.6k without CR-260; target 38.5k to 41k). OK.
4. Sections 5-8: Changes and Impacts match the diff; grade 1 with revert; Autonomous decisions match the two choices (paragraph with bullets, worker line wording); Human decisions match `02-answers.md` (DR-Q1; O1-O3 are specification defaults, not dropped in substance). OK.
5. Section 10 (Known gaps): after measure and no-loss check named, no UNVERIFIED mark in the body. OK.
6. Test plan SHAs all `d43abe1`: local gates (gate log result pass at d43abe1, 895/895 and 873/873), Verified, CI green (handoff notes). Minor note: the Review item says approved at `d43abe1`, while the recorded note says `r1 inspector approved at ce00ec3`; the body explains that the pass was recorded on the reviewed state committed as d43abe1 (ce00ec3 is on main, d43abe1 is the single branch commit). Not a failure; the Driver may prefer quoting the note's SHA.

Verdict (pass 2): VERIFIED at d43abe1a1d2c90d5c75525947c5cd56c3fd4b23d.
