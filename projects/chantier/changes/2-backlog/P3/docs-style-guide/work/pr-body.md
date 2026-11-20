## Summary

The documentation site had no written style, and several pages read as AI filler: a subtitle that restates the title, sentences of 50 words and more, agent internals in pages for the user. This PR adds a short style guide, `docs/STYLE.md`, and brings every page of the site to it. It changes how pages say things, not what chantier does: no page or image is added, removed, renamed or moved.

## Deliverables

The guide has sixteen numbered rules (S1 to S16), each prose rule with a bad example quoted from a page before the review and a good one. It stays outside the site (`exclude_patterns` in `docs/conf.py`). Later changes are held to it by one new `AGENTS.md` rule: a changed docs page follows the guide, and the Inspector treats each broken rule as blocking.

| Before | After |
| --- | --- |
| no style guide; `CONTRIBUTING.md`: "short sentences, exact terms" | `docs/STYLE.md`, named by backticked path in `AGENTS.md` and `CONTRIBUTING.md` (no link, so `chantier rules` does not make every role read it) |
| 21 pages unreviewed | 21 pages reviewed against S1 to S16 (the review table is under Changes) |

The page changed most, "Your gates": before at `2251916` (left), after at `0bed437` (right, carried from `787400e`). The restated subtitle and the 50-word bullets became a one-line opening and short sections.

| Before | After |
| --- | --- |
| ![The Your gates page before: restated subtitle, long bullets](./verifier/evidence/gates-before.png) | ![The Your gates page after: one-line opening and short sections](./verifier/evidence/gates-after.png) |

## Blast radius

Grade: **1**. Documentation text, one build exclusion and one test; a `git revert` restores the previous pages.

## Autonomous decisions

- The new test lives in `tests/test_docs_site.py`, not `test_plugin_files.py` as the specification says: that file is at its 400-line cap, and the new test reads the same shipped files.
- `site_pages()` in the docs test helper skips `STYLE.md`, as it is not a site page.

## Known gaps

- `docs/explanation/planning-modes.md` says the archive in the PR defaults to no; `docs/reference/planning-folder.md` says yes. Not rewritten here (a false statement is not fixed by this change); to be filed as an inbox item.
- No Read the Docs preview: the forge lists no such check on this PR.

<details>
<summary>Details</summary>

## Changes

- `docs/STYLE.md` (new, 69 lines); `AGENTS.md` one rule; `CONTRIBUTING.md` two lines; `docs/conf.py` excludes `STYLE.md`.
- All 21 site pages reworded (openings, split sentences, tables, fewer bold marks, alt texts).
- `tests/test_docs_site.py`: one test checks the guide exists, both files name it in backticks, and the `rules` link walk does not reach it.

### Review table

| Page | Rules broken | What changed |
|---|---|---|
| index.md | S4, S13, S15, S12 | bullets tightened, bold labels removed, alt texts say what the picture shows, direct-mode paragraph merged |
| installation.md | S3, S5, S12 | opening says what the page gives, entries table, sections for extra needs and the check, a Next line |
| tutorials/index.md | S3 | opener says what the page gives |
| tutorials/claude-code.md | S6, S13, S12 | preflight shortened, bold and emoji removed, long paragraphs split, link to agents-and-models |
| how-to/index.md | S3 | opener says what the page gives |
| how-to/use-cases.md | S6, S12, S13, S5 | paragraphs split, bold removed, PR description sections as a table, cost bullets |
| how-to/use-cases-foreman.md | S3, S6, S12 | opening, long paragraphs split, bullets, close-check list |
| how-to/use-cases-direct.md | S3, S6, S13 | opening, bold pseudo-headings became sections, bullets for parallel, series, stack |
| how-to/gates.md | S3, S6, S12, S1 | opening no longer restates the subtitle, sections added, long sentences split, internals reduced |
| how-to/agents-and-models.md | S3, S6, S5, S12 | opening, layers list split, Timing table, headings for key groups |
| how-to/release-process.md | S3, S6, S12 | opening, long paragraphs split, sections split |
| explanation/index.md | S3 | opener says what the page gives |
| explanation/planning-modes.md | S3, S12, S6, S2 | opening, duplicated remote text replaced by a link, autosync bullets cleaned, setup steps as prose |
| explanation/batches-and-lifecycle.md | S3, S5, S15, S12 | opening, batch modes as a table, path-like alt texts replaced, lifecycle detail list, numbered release example |
| explanation/costs.md | S3, S12, S16, S4 | sections, cost commands as code blocks, closing summary removed |
| reference/index.md | S3 | opener says what the page gives |
| reference/what-you-say.md | S3 | opening sentence |
| reference/boards.md | S3, S6, S15, S12 | opening, list for how to read it, long paragraphs split, alt text, guard section split |
| reference/web-board.md | S3, S6, S13, S12 | opening, prose bold removed, signal bullet split into sub-bullets, costs paragraphs as lists and numbered ticket, long paragraphs split |
| reference/planning-folder.md | S3, S6, S12, S5 | opening, sections for moves, batches, publication, STATUS, summary, worktrees, pause, close; close lists as bullets |
| reference/hosts.md | S3, S12, S13 | opening, headings, a note admonition, bullets |

## Impacts

Docs readers see clearer pages; later docs changes are reviewed against the guide.

## Test plan

- [x] New or changed tests: `test_the_docs_style_guide_is_wired_in_and_stays_out_of_the_rules`
- [x] Local gates at `0bed437`: `just check` passes (docs built with `-W`)
- [x] Evidence: before at `2251916`, after at `0bed437` (carried from `787400e`)
- [x] Review: approved at `0bed437` (the rebase onto the new base inspected; round 1 approved at `22519166`)
- [x] Verified at `0bed437`
- [x] CI green at `0bed437`: 5 checks pass

## Internal references

CR-382 docs-style-guide-and-anti-slop-review. Review table: `work/verifier/evidence/review-table.md`.

</details>
