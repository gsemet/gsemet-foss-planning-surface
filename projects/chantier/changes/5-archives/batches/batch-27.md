# batch-27

Opened 2026-11-18T14:33:05Z, closed 2026-11-18T17:47:48Z, parallel, steered by Foreman, budget $60, final cost $26.40. [batch-27.json](batch-27.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-359](../261118-1452-359-partial-stack-ask-windows-gate/) | Change Specification: the partial-stack ask says whether the local gate ran at its top | merged | https://github.com/gsemet/chantier/pull/324 | 1 | $1.37 |
| [CR-360](../261118-1459-360-gitignore-work-gates-anchor/) | Change Specification: the planning folder ignores every CR's work/gates/ | merged | https://github.com/gsemet/chantier/pull/325 | 1 | $1.42 |
| [CR-361](../261118-1518-361-summary-lint-hint-path/) | The summary lint hint gives a path summary set can read | merged | https://github.com/gsemet/chantier/pull/327 | 1 | $1.34 |
| [CR-362](../261118-1518-362-spec-title-front-matter/) | A front matter is never a CR's title, and the board's panel hides it | merged | https://github.com/gsemet/chantier/pull/326 | 1 | $1.40 |
| [CR-363](../261118-1518-363-cli-unavailable-stops-session/) | Change Specification: a session whose chantier CLI cannot run stops at once | merged | https://github.com/gsemet/chantier/pull/328 | 1 | $1.73 |
| [CR-364](../261118-1529-364-archive-in-pr-from-settings/) | Archive in the PR: off unless the project asks for it | merged | https://github.com/gsemet/chantier/pull/330 | 1 | $2.24 |
| [CR-365](../261118-1518-365-one-cr-batch-top-gate/) | Change Specification: the batch's top runs the local gate in a batch with no stack | merged | https://github.com/gsemet/chantier/pull/329 | 1 | $1.58 |
| [CR-366](../261118-1610-366-release-v0-13-0/) | Version PR for chantier v0.13.0 | merged | https://github.com/gsemet/chantier/pull/331 | 0 | - |
| [CR-367](../261118-1731-367-bug-handoff-and-the-record-show-pr-none/) | Change Specification: a release CR's merged PR stays in its record | merged | https://github.com/gsemet/chantier/pull/332 | 1 | $1.36 |
| [CR-368](../261118-1745-368-ask-the-release-s-post-merge-word-with-t/) | Ask the release's post-merge word with the merge go | merged | https://github.com/gsemet/chantier/pull/333 | 1 | $1.19 |

## Cost

- Total: $26.40 of a $60 budget
- Foreman $12.67 (48%), Drivers $6.48 (25%), workers $7.25 (27%)
- Most: CR-364 $2.24, CR-363 $1.73, CR-365 $1.58
- Foreman: 52 wakes, context 172,831 tokens on average, 266,305 at its peak
- Driver chantier:cr-driver with its workers: $11.09 (608 calls)
- Chief of Staff, steering the batch (outside the budget): $6.95 since the batch opened (134 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $21.98 since the batch opened (513 calls, 12 spec-writers, 7 spec critics)
- Chief of Staff, whole session: $1110.35, context 262,149 tokens; not counted: 1 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro


## 2026-11-18, CR-359 to CR-365 (batch-27)

- nothing worth changing (critic: 4 points dropped)

## 2026-11-18, CR-366 (batch-27, release v0.13.0)

- [chantier] Steps 4 and 5 (tag, publication) needed a second Driver start after the merge, because the user's word for them was collected apart from the merge go (also seen in v0.12.0, CR-352): ask for that word together with the merge go, so one Driver runs the procedure to its end. (critic: keep)
- [chantier] `handoff CR-366` printed `PR: none; head -` although PR 331 was opened, green and merged; `STATUS.json` has `pr: null` (also seen in CR-352, v0.12.0): have `handoff` and the record keep the release's PR. (critic: keep)

## 2026-11-18, CR-367 and CR-368 (batch-27)

- nothing worth changing (critic: 3 points dropped)

Release retro: ../261118-1610-366-release-v0-13-0/work/retro.md
