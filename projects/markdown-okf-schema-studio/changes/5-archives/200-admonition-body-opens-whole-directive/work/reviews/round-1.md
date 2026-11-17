# CR 200 — Inspector review, round 1/3

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-200` (uncommitted diff, 8
modified files + new fixture `test/visual/fixtures/72-myst-admonition-editing.md`).

## What was checked

| Check | Result |
| --- | --- |
| `npm run compile`, then `node --test` on `out/test/session/alertBlockEditOpen.test.js` and `out/test/site/e2eGroups.test.js` | 12/12 pass |
| The new tests fail without the fix (compiled output copied to the scratchpad, selector reverted to `[data-okf-github-alert]`) | Both admonition tests fail (`actual [4,4]`, expected `[1,5]` / `[3,8]`); the six alert tests still pass |
| `uv run --group requirements okfreq validate --check-links --project-root .` | 1068 requirements, 0 errors, 0 warnings |
| Locked StRS | Not touched (only two SwRS files change under `requirements/`) |
| BLOCK-047 | Only a `### Rationale` section added, nothing else in the file and no code change. The row it cites ("The browser window loses the focus with no related target", line 72) exists. Doc-only and separate from the other changes, as asked. |
| Weakened assertions | None. The pinned known-issue assertion `[4,4]` became `[1,5]` plus an `originalText` check. The new colon-fence test also asserts that a trailing paragraph still opens alone (`[10,10]`). The test DOM now accepts `.class` selectors, and the check is a strict class-list match. |
| Screenshots `/private/tmp/claude-502/cr200-driver/screenshots/` | Before: the note title stays rendered and the editor opens inside the note on the second paragraph only. After: the note is hidden, one editor holds the `{note}` fence-to-fence text with the footer "Lines 5–9", and the tip stays rendered. Both match the claim. |

### Edge cases probed against the built code

| Case | Lines opened | Verdict |
| --- | --- | --- |
| Title of a titled backtick note | 1–3 (whole) | ok, title still works |
| Paragraph after the admonition | 5–5 | ok |
| Nested `{tip}` inside a `{note}`, click in the inner | 4–6 (inner) | ok, the nearest one wins, as the SwRS row says |
| Nested, click on an outer paragraph after the inner | 1–9 (outer) | ok |
| Admonition inside a list item | 3–5 (the admonition, not the list) | ok |
| Another item of that list | 1–7 (the list) | ok |
| `{versionadded}` body | 1–3 (whole) | acceptable (it is a directive) |
| **Context tag panel** `<instructions>…</instructions>`, click on a body paragraph | **1–7 (whole tag block)** | **not requested, see finding 1** |

## Findings

1. **Scope creep: context-tag panels now open as a whole.** `editingElementFor` matches every
   `aside.admonition`. Context tags (SwRS-MDOKFSTUDIO-MYST-013, `src/core/render/mystContextTags.ts`)
   also render as `aside.admonition.myst-context-admonition`, with a source range from the opening
   tag to the closing tag. So a click on any paragraph inside `<instructions>` … `</instructions>`
   now opens the whole tag block. In prompt and agent files such a block often covers most of the
   document. Before this change it opened only the clicked paragraph. The owner decision covers
   MyST admonitions (`:::{note}` and the backtick fence form) only, not context tags.
   Fix: exclude them, for example
   `aside.admonition:not(.myst-context-admonition)`. The test DOM wrapper would then need `:not`
   support, or a post-filter in code such as `alert.classList.contains("myst-context-admonition")`.
   Add a unit test showing that a click in a context-tag body still opens the paragraph only. The
   other option is to get an explicit owner decision and document context tags in BLOCK-014 and
   MYST-013.
2. **The BLOCK-014 Criteria is broader than its scenario text.** The Criteria says "an aside or
   details element of class admonition", while the nominal scenario and the new row say "a MyST
   admonition (`{note}`…)". After finding 1, make the Criteria name the exclusion, for example "other
   than a context-tag panel". Otherwise the Criteria and the rows describe different scopes.

### Non-blocking notes

- `details.admonition` (dropdown): a body click opens the whole directive. This is consistent with
  Option A. The coder disclosed it, and no test covers it, which is acceptable.
- Commit hygiene for the driver: the request asks for the BLOCK-047 rationale in a **separate,
  doc-only commit**, so split it from the BLOCK-014 code and test commit.
- In the before screenshot the editor's text box looks empty (the toolbar shows, no source text).
  It still proves paragraph-only, because the editor sits inside the still-rendered note. If the
  driver re-captures it, waiting for the source to arrive would make it clearer.

## Verdict

CHANGES REQUESTED
1. Exclude context-tag panels (`aside.admonition.myst-context-admonition`) from the whole-directive
   rule, or get an explicit owner decision. Add a unit test showing that a click in a context-tag
   body still opens the paragraph only, and that the test fails if the exclusion is removed.
2. Align the BLOCK-014 Criteria wording with that scope.
