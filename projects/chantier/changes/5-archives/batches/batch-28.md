# batch-28

Opened 2026-11-18T18:09:15Z, closed 2026-11-19T22:19:10Z, stack, steered by Foreman, budget $150, final cost $122.40. [batch-28.json](batch-28.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-369](../261119-0930-369-open-an-empty-batch-paused-waiting-for-i/) | Open an empty batch, paused, waiting for its first CR | merged | https://github.com/gsemet/chantier/pull/335 | 2 | $5.33 |
| [CR-371](../261118-1927-371-ruff-check-scripts/) | Change Specification: `just check` runs ruff's lint rules on `scripts/` | merged | https://github.com/gsemet/chantier/pull/334 | 1 | $1.07 |
| [CR-370](../261119-0930-370-a-specified-cr-joins-the-waiting-batch-o/) | Factory mode: a CR made ready joins the open batch on its own | merged | https://github.com/gsemet/chantier/pull/342 | 2 | $4.74 |
| [CR-374](../261118-1928-374-explain-refusals-why-and-what-to-do/) | Change Specification: explain a refusal before the user hits it, why, and what to do now | merged | https://github.com/gsemet/chantier/pull/336 | 1 | $1.81 |
| [CR-373](../261119-0930-373-audit-j1-qa-driver/) | Change Specification: the eval audit's J1 accepts the QA driver's first line | merged | https://github.com/gsemet/chantier/pull/338 | 1 | $2.28 |
| [CR-375](../261119-0930-375-the-watcher-starts-on-its-own-with-a-run/) | The watcher starts on its own with a running batch | merged | https://github.com/gsemet/chantier/pull/341 | 1 | $4.12 |
| [CR-372](../../6-trash/261118-1901-372-steering-context-handover/) | Change Specification: a costed study of handing a long batch's steering to a fresh session | dropped | - | 2 | $3.72 |
| [CR-376](../261119-0930-376-surface-agentless-launch/) | Change Specification: a board started by hand serves a planning surface with no agent | merged | https://github.com/gsemet/chantier/pull/339 | 3 | $2.98 |
| [CR-377](../261119-0930-377-release-user-publishes/) | A release is finished after the user publishes it by hand | merged | https://github.com/gsemet/chantier/pull/340 | 1 | $1.41 |
| [CR-378](../261119-0930-378-planning-folder-validate/) | Change Specification: chantier validate checks a whole planning folder | merged | https://github.com/gsemet/chantier/pull/345 | 1 | $3.66 |
| [CR-379](../261119-0930-379-optimise-the-startup-core-in-size-and-ef/) | Change Specification: optimise the startup core in size and efficiency | merged | https://github.com/gsemet/chantier/pull/344 | 1 | $3.68 |
| [CR-380](../261119-0930-380-pane-spend-verdict-draft/) | Change Specification: the CR board pane shows the spend's age, the carried verdict and the draft wording | merged | https://github.com/gsemet/chantier/pull/343 | 1 | $3.29 |
| [CR-383](../261119-0930-383-spec-writers-and-slots-set-from-the-boar/) | Change spec: spec-writers and slots set from the board's configuration | merged | https://github.com/gsemet/chantier/pull/348 | 4 | $8.77 |
| [CR-384](../261119-0930-384-session-events-board-griller/) | Change Specification: the watcher wakes the Chief of Staff on what the user does in the board | merged | https://github.com/gsemet/chantier/pull/351 | 3 | $7.14 |
| [CR-387](../261119-0930-387-the-chief-of-staff-grants-a-4th-and-5th/) | Change Specification: the Chief of Staff grants a 4th and 5th round when the batch caused the red | merged | https://github.com/gsemet/chantier/pull/349 | 1 | $1.34 |
| [CR-385](../261119-0930-385-addressed-events-one-typed-journal-that/) | Change Specification: addressed events, one typed journal that says whom to wake | merged | https://github.com/gsemet/chantier/pull/353 | 1 | $4.53 |
| [CR-386](../261119-0930-386-surface-server-one-elected-process-for-t/) | Change Specification: the surface server | merged | https://github.com/gsemet/chantier/pull/354 | 2 | $5.89 |
| [CR-381](../../6-trash/261119-1116-381-docs-sphinx-rtd/) | Change Specification: the documentation as a Sphinx site on Read the Docs | dropped | https://github.com/gsemet/chantier/pull/346 | 2 | $4.38 |
| [CR-382](../../6-trash/261119-1116-382-docs-style-guide-and-anti-slop-review-of/) | Change Specification: a docs style guide and an anti-slop review of every page | dropped | https://github.com/gsemet/chantier/pull/347 | 1 | $4.38 |
| [CR-388](../261119-2217-388-release-v0-14-0/) | Version PR for chantier v0.14.0 | merged | https://github.com/gsemet/chantier/pull/356 | 0 | $1.19 |

## Cost

- Total: $122.40 of a $150 budget
- Foreman $44.14 (36%), Drivers $33.50 (27%), workers $44.76 (37%)
- Most: CR-383 $8.77, CR-384 $7.14, CR-386 $5.89
- Foreman: 157 wakes, context 183,754 tokens on average, 266,695 at its peak
- Driver chantier:cr-driver with its workers: $73.89 (3385 calls)
- Driver chantier:stack-driver with its workers: $3.18 (181 calls)
- Driver chantier:release-driver with its workers: $1.19 (63 calls)
- Chief of Staff, steering the batch (outside the budget): $19.77 since the batch opened (264 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $64.67 since the batch opened (1414 calls, 26 spec-writers, 10 spec critics)
- Chief of Staff, whole session: $1205.62, context 179,340 tokens; not counted: 6 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

No retro was written.

Release retro: ../261119-2217-388-release-v0-14-0/work/retro.md
