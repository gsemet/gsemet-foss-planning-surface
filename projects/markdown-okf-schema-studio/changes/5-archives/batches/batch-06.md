# batch-06

Opened 2026-11-17T18:29:08Z, closed 2026-11-20T18:26:47Z, stack, steered by Foreman, no budget, final cost $368.29. [batch-06.json](batch-06.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-340](../261117-2011-340-req-marker-gate/) | gate requirement markers | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/410 | 1 | $2.61 |
| [CR-347](../261120-0644-347-req-garden-core-diagrams-trust/) | garden the requirements of rendering-core, diagrams and trust-security | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/418 | 6 | $34.59 |
| [CR-424](../261120-1146-424-external-pr-404-list-item-edit/) | Take ownership of external PR 404: list item edit scope, list items in the TOC (opt-in) | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/431 | 2 | $26.46 |
| [CR-426](../261120-1048-426-flaky-buildqueue-test/) | Flaky test: test/node-services/buildQueue.test.ts ('still renders a build whose buffer already moved on, and cleans up on dispose', compiled line 116, false !== true) failed once in a just check run during CR-349 and passed before and after. Not touched by CR-349. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/432 | 1 | $4.20 |
| [CR-341](../261117-2011-341-req-main-paths-depends-on/) | a Main path may cite an SwRS the StRS depends on | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/409 | 1 | $1.72 |
| [CR-348](../261120-0647-348-req-garden-myst-code-gfm/) | garden the requirements of myst, code-blocks, gfm | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/419 | 2 | $30.63 |
| [CR-425](../261120-1146-425-real-window-test-flakes/) | Real-window integration test flakes. paste-url is a race in the test (diagnosis: CR-350 work/diagnosis.md); proposed test-only fix: drop the obsolete stored-mode wait at test/integration pasteUrl.test.ts:155 and the same wait in dropFiles.test.ts and findInPreview.test.ts. checkbox-toggle also flaked on main 24c9eef (CI run 44651927198). | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/435 | 1 | $11.43 |
| [CR-342](../261117-2121-342-req-use-case-diagrams/) | a use-case diagram on each StRS, on GitHub and on the requirements site | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/412 | 2 | $4.71 |
| [CR-349](../261120-0835-349-capturenow-tooltip-wait-diagnostic/) | Name the stuck tooltip when the capture helper's tooltip wait times out | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/426 | 1 | $6.97 |
| [CR-428](../261120-1305-428-ci-linux-table-breakout-widths/) | Run the tableBreakout width tests on Linux in CI. The static jobs skip them (no Chromium), so CR-351's pinned-font widths and the 12 owner verdicts are verified on Windows only; its spec asks Linux widths within 1 px of Windows. Run them in the visual job (Chromium present), or under xvfb, and record the Linux widths. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/436 | 2 | $7.99 |
| [CR-346](../261118-1059-346-req-garden-toolbar-lifecycle/) | garden the requirements of toolbar-navigation and lifecycle-sync | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/414 | 4 | $20.96 |
| [CR-350](../261120-0859-350-ci-gallery-on-dispatch/) | Build the gallery and site on a heavy CI dispatch | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/428 | 1 | $11.76 |
| [CR-430](../261120-1305-430-myst-numref-captionless-figure/) | Bug: SwRS MYST-019's {numref} scenario contradicts the code: a numref to a figure with no caption keeps an inert placeholder instead of what the SwRS says; no test covers it. Decide which is right, fix the other, add a test. Found by batch-06 CR-348 (PR 419). | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/437 | 2 | $7.69 |
| [CR-343](../261118-1234-343-req-garden-block-table/) | garden the requirements of block-editing and table-editing | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/417 | 7 | $30.76 |
| [CR-351](../261120-0916-351-font-independent-layout-tests/) | layout tests that do not depend on the page font | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/429 | 2 | $11.27 |
| [CR-431](../261120-1305-431-req-code-mismatches-cr347/) | Code/requirement mismatches found by batch-06 CR-347 (PR 418, listed as Known issue lines in its body): SwRS CORE-010, CORE-025, DIAG-005, DIAG-009, TRUST-042 say something the code does not do. For each, decide whether the code or the SwRS is right and fix the other. Details in PR 418 body and CR-347's work folder. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/439 | 2 | $9.72 |
| [CR-344](../261118-1425-344-req-garden-review-frontmatter/) | garden the requirements of review-annotations, frontmatter-editing, frontmatter-schema | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/416 | 6 | $32.43 |
| [CR-432](../261120-1535-432-list-item-reorder-handles/) | List items get reorder handles on the left, like table rows, to reorder the items of a list in edit mode. Owner's words (2026-11-20): 'il faut mettre des ancre de reordonnement de la liste sur la gauche comme les ligne d une table. tu feras ca dans une autre CR'. Follows CR-424 (PR 404, item-level list editing). | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/443 | 2 | $24.29 |
| [CR-345](../261119-2323-345-req-garden-palette-theme-layout/) | garden the requirements of palette-slash, theme-zoom and layout-width | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/415 | 7 | $26.46 |
| [CR-427](../261120-1020-427-breakout-font-load-hang/) | tableBreakout tests: a pinned font that fails to load hangs the test run, because openPage never closes Chromium, instead of failing it. Close the browser on that error path (found in CR-351, PR 429). | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/433 | 1 | $7.93 |
| [CR-429](../261120-1019-429-mermaid-reserved-ids-check/) | The use-case diagram check added by CR-342 (test/site/requirementsViewer/useCaseDiagram.ts, the site build and the guideline "Use case diagram of a StRS") lets through a Mermaid diagram whose participant id is a reserved word: in batch-06, six PALETTE StRS sequence diagrams used `Box` as an id and failed to parse; renaming it to `Field` fixed them (CR-345). Make the failure early and clear: `just requirements-lint` or `just check` should parse every StRS diagram (or at least reject Mermaid's reserved ids) and name the StRS and the word, and the guideline should list the words to avoid. Found by the batch-06 Foreman, 2026-11-17. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/434 | 1 | $7.42 |
| [CR-433](../261120-1421-433-release-notes-style/) | release notes, short and demo-first | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/442 | 1 | $3.61 |
| [CR-434](../261120-1714-434-release-1-10-0/) | Release 1.10.0 | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/444 | 0 | $3.96 |

## Cost

- Total: $368.29, no budget
- Foreman $25.71 (7%), Drivers $165.68 (45%), workers $176.90 (48%)
- Most: CR-347 $34.59, CR-344 $32.43, CR-343 $30.76
- Foreman: 238 wakes, context 181,895 tokens on average, 267,191 at its peak
- Driver chantier:cr-driver with its workers: $322.13 (8334 calls)
- Driver chantier:stack-driver with its workers: $16.37 (387 calls)
- Driver chantier:release-driver with its workers: $3.96 (79 calls)
- Chief of Staff, steering the batch (outside the budget): $30.90 since the batch opened (634 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $16.47 since the batch opened (407 calls, 11 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $115.42, context 182,556 tokens; not counted: 8 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

## 2026-11-20: CR-340..CR-351, CR-424..CR-434 (batch-06)

- [chantier] A second stack Driver was started on a CR whose record the first had already left, 25 minutes before the first one's hand-back arrived: a subagent Driver cannot SendMessage a Desktop `local_` Foreman session (its hand-back reaches the Foreman only as its final report), and `hosts/claude-code.md` lists "SendMessage to main" as proved: correct that row for a Desktop Foreman, and name in the stack-driver prompt's `Steering:` line what a subagent sends.
- [chantier] The worktree base `take` printed for a CR in a stack was wrong several times (CR-424, CR-427, CR-429: the Foreman told each Driver to create its worktree on origin/main), and the stale "PR in draft … after CR-425" label went into ask A-30: derive the printed base and the waits-on label from the forge state of the PRs, not from the recorded order.
- [project] "Filename too long" blocked a base checkout or worktree five times (CR-348, CR-350, CR-427, CR-431, CR-432), so fail-before claims went into PR bodies as UNVERIFIED: set `core.longpaths` (or a shorter worktree root) in the project's `AGENTS.md` and guidelines so a Verifier can check out the base.
- [project] The paste-url real-window flake went red twice (CR-350 dispatch 44647675614, CR-424 heavy run) and has no open item; `realinput-t45`, `previewManager.test.ts:162` and the checkbox-toggle timeout are already filed: file paste-url (and the drop-files case) and add both to the default stress scenarios.

(critic: kept 4, dropped 6)
