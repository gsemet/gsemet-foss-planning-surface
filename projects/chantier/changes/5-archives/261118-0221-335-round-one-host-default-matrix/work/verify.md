Head: 5b86c93f86b93e38b5ea08c8c325db11bbb725c0

All claims judged at 5b86c93f86b93e38b5ea08c8c325db11bbb725c0 (pushed head, PR 295).

1. Only cards changed. `git diff --name-only origin/main..HEAD` output:
   skills/chantier/references/concepts.md, driver.md, inspector.md, spec-writer.md, verifier.md.
   Nothing outside skills/chantier/references/.
2. concepts.md has the "Host and default matrix" bullet after "Change Specification" (diff of `git diff origin/main..HEAD`); spec-writer.md, driver.md, inspector.md, verifier.md each link `[concepts](concepts.md), "Words"` to it (same diff).
3. driver.md puts the probe after the `r<n> approved at ..., committed as <sha>` note and before "rebase", under "while the CR has never been pushed and has a matrix"; a NOT VERIFIED probe is the next round under the limit; the pushed-head verifier is given the last matrix-r<n>.md. Plan sentence (Driver writes a matrix when the spec names none) and checklist/Inspector-prompt sentences present. Seen in the diff.
4. verifier.md: ground rule carries "except a matrix probe, below, run at the committed head before the CR's first push"; the "Matrix probe" paragraph says "Run no `$CHANTIER verdict` and no gate", writes matrix-r<n>.md with a `Head:` line; delta assessment counts matrix-r<n>.md as a previous judgment.
5. concepts.md rule 5 carries "(except a matrix probe, run at the committed head before the CR's first push: [verifier](verifier.md))" after its first sentence.
6. inspector.md: a cell with no test or tested only on a hand-built shape is `blocking`, after the blocking paragraph.
7. `uv run --no-sync --project . chantier phase --help`: usage `phase cr {investigator,...,verifier,release} [detail ...]`; `verifier` is accepted with a free detail. No CLI change needed.
8. PR 295 description (`gh pr view 295`): headRefOid equals the head above; renders (sections, mermaid, fold); Summary, Deliverables and Changes match the diff; Known gaps lists the unproved probe. The `<sha7>` placeholders in the Test plan are stale by the Driver's own note and are filled after this pass; not failed on.
9. This CR has no matrix of its own; no probe, no before/after (cards only).

VERIFIED

## Description-only pass (PR 295 body as posted), judged at 5b86c93f86b93e38b5ea08c8c325db11bbb725c0

Command: `gh pr view 295 --json body,title,headRefOid` (headRefOid = 5b86c93f86b93e38b5ea08c8c325db11bbb725c0, equal to `git rev-parse HEAD`) and `git diff origin/main...HEAD -U0` (5 files, all under skills/chantier/references/).
- Renders: sections in template order, one Details fold with blank lines after `</summary>` and before `</details>`, nothing after it, mermaid flowchart valid, no image.
- Consistent with the diff: Summary, Deliverables (concepts term, spec-writer matrix, Inspector blocking rule, probe file `verifier/matrix-r<n>.md`, no verdict or gate, previous judgment at the pushed head) and Changes (five files, rule 5 exception, driver, inspector, verifier probe paragraph, pushed-head exception, delta rule) all match the diff; no delivered change unmentioned.
- Internal references: CR name only in the last section; role names are product terms of a change to those roles' cards.
- Review box: `$CHANTIER log 335` has "r1 approved at a65a8d3d..., committed as 5b86c93f", the SHA the box cites.
- Test plan proofs all name 5b86c93; Known gaps has the one unproved claim, no UNVERIFIED mark left; no STALE; no image.
Verdict for this pass: VERIFIED
