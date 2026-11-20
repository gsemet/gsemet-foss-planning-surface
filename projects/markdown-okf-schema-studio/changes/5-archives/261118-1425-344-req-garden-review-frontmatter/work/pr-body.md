## Summary

The requirements of three feature areas (review annotations, frontmatter editing, frontmatter schema) had drifted: several software requirements described the same behaviour twice, some stakeholder requirements had no diagram or contradicted the code, and many requirements were traced by file-wide marker blocks instead of by the test that checks them. This PR gardens them so that a reviewer can understand each use case from its stakeholder requirement and each software requirement is one observable behaviour, traced to the code that does it and the tests that check it.

No product behaviour changes: no rendered output, message, setting or command is different. Source edits are marker comment moves and test reorganisation only.

## Deliverables

- **Use case diagrams** on the stakeholder requirements of the three areas (a new `### Use case diagram` section before Main paths), plus one new stakeholder requirement for side-by-side comment cards (`REVIEW-018`) that gave several orphaned software requirements a parent.
- **Merged software requirements**, retired with `okfreq supersede` (nothing deleted): for example `REVIEW-069` into `REVIEW-054`, `REVIEW-101` into `REVIEW-100`, `REVIEW-081` into `REVIEW-044`, `FMEDIT-054` into `FMEDIT-016`, `FMSCHEMA-060` into `FMSCHEMA-050`, and the stakeholder requirement `FMSCHEMA-002` into `FMSCHEMA-001`.
- **Markers follow the requirements**: every in-force software requirement of the three areas has an implementation marker and a focused test marker; the file-level marker blocks of `okfFrontmatter.test.ts` and `previewEditing.test.ts` are dissolved onto the tests that check each behaviour, and the marker baseline only shrinks.
- **New focused tests**: a frontmatter flush test, a comment rename test, a frontmatter-edit refusal test, and a real-window TODO toggle scenario plus two schema steps (a schema's field order and badge, and a schema that cannot be parsed).

```text
before: a marker block of 14 IDs over one test file   ->  after: each test names the 1-3 IDs it checks
before: REVIEW-081 and REVIEW-044 both describe Save   ->  after: REVIEW-044 only, 081 superseded
```

## Approved requirements changed

Four approved stakeholder requirements changed in authored text. The owner agreed to these corrections in advance; each one is its own commit, and the owner re-approved them on 2026-11-17 (`approved_at` 2026-11-17T22:55:00+01:00). **Owner review requested on each commit:**

| Requirement | Commit | Change |
| --- | --- | --- |
| `REVIEW-001` | d95f960e | use case diagram added; no longer a parent of a trust requirement |
| `REVIEW-003` | 755038fd | diagram; Main paths cite `SwRS-REVIEW-044` (the folded `081`) |
| `REVIEW-012` | af8a418a | text now says the TODO action comes from the edition palette or the slash menu (it has no shortcut, as the code and `REVIEW-160` state); Main paths reshaped; diagram |
| `REVIEW-015` | ecbda4fc | diagram; the undo step is cited rather than derived |

## Blast radius

Grade: **1**. Requirement files, comments and tests only. A plain `git revert` restores the previous state; superseded requirements stay in place with their status.

## Autonomous decisions

- Placements between sibling gardening changes, settled as the owner delegated: this change touches in shared files only the IDs of its own three areas.
- `REVIEW-133`/`REVIEW-167` (tab items) and `FMEDIT-028` get no new test: existing focused tests already check them, so only markers were added.
- To respect the 1500-line limit of test files, the patch tests of `okfFrontmatter.test.ts` and the helpers of `previewEditing.test.ts` moved verbatim to new files.
- `FMSCHEMA-017`, `FMSCHEMA-018` and `FMSCHEMA-076` were re-parented from the superseded `FMSCHEMA-002` to `FMSCHEMA-001`.

## Known gaps

- A YAML syntax error in a schema file is still not reported as "Schema could not be parsed" (a known issue, unchanged by this PR, that a unit test asserts): the end-to-end step `stepSchemaProblem` therefore breaks a JSON5 schema, the case the requirement describes.
- The Mermaid state diagrams of `FMEDIT-008`, `FMSCHEMA-006` and `REVIEW-008` could not be parsed under Node locally; their syntax was checked by eye.
- The `commentStyles` test only proves that the output bytes are unchanged, not the full behaviour of its requirements.
- Deviation from the specification's checks 3 and 4: marker blocks of more than 3 IDs that name requirements of these three areas remain on the marker baseline in the files the specification keeps unchanged: `commentAnchors.test.ts`, `commentWrite.test.ts`, `inlineThread.test.ts`, `reviewComments.test.ts` (review annotations), `scenarioDefinitions1.ts` (`FMSCHEMA-001`, `006`, `029`) and the export HTML visual files `capture_export_html.py` and `exportHtmlScenarios.ts` (`FMSCHEMA-091`). Every in-force SwRS of the three areas, `FMSCHEMA-073` included, has a focused implementation marker.

<details>
<summary>Details</summary>

## Changes

- `requirements/tiers/strs/...`: diagrams, parents and wording for the three areas; new `REVIEW-018`; `FMSCHEMA-002` superseded by `FMSCHEMA-001`.
- `requirements/tiers/swrs/...`: 15 `okfreq supersede` merges and the `REVIEW-081` fold, scenario fixes (`REVIEW-086`, `094`, `119`, `133`, `167`), generated links.
- `src/`: marker comment renames and splits only (for example the `toggleBoolean` branch of `frontmatterValueEditor.ts`, `commentThreads.ts`, and the link handler of `links.ts`, where `FMSCHEMA-073` now marks the blocked-link warning branch).
- `test/`: markers moved to the focused tests, the three new tests, the new real-window scenario and steps registered in `realInput/run.ts`, and `okfFrontmatterPatches.test.ts` and `previewEditingHelpers.ts` split out.
- `scripts/` baseline of the marker check lowered; `requirements/tiers/log.md` entry added.

## Human decisions

- Published requirements are never deleted: merges and splits use `okfreq supersede`.
- The approved stakeholder requirements are corrected in this change, one commit each, reviewed by the owner on this PR.
- A generated link or an added diagram on an approved requirement is editorial and needs no re-approval.
- Shared rules (for example `BLOCK-041`, `BLOCK-058`, `TRUST-001`) are cited through the stakeholder requirement's `depends_on`, Main paths included, instead of being derived from it.
- Open points of the specification follow its recommendation; placements between sibling gardening changes are listed under Autonomous decisions.

## Impacts

No visual change; no user-facing change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): frontmatter flush, comment rename, frontmatter-edit refusal; each shown failing once by flipping an assertion
- [x] Local gates at `13a8545`: `just preflight` passed (on Windows its static stage only; the visual, integration, report and gallery stages run in CI)
- [ ] Evidence: none, no visible change
- [x] Review: approved at `13a8545` (the last change, the split marker block of `links.ts`, reviewed before its commit; the earlier changes and the conflict resolution of the rebase onto `main` were reviewed before it, the tree unchanged since)
- [x] Verified at `13a8545`
- [x] CI green at `13a8545`: the pull request checks (static, static-windows, visual, report) and the heavy run on the branch (integration and stress included) pass

## Internal references

- CR-344 req-garden-review-frontmatter (batch-06)

</details>
