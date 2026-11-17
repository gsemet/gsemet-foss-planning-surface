# 213 — QA skill: annotated evidence, a reasoned verdict, one bug template

:::{important}
**Owner GO, via the Chief of Staff, 2026-10-31.** Stacked on #237 (the QA skill CR, commit
`c1399a18`), because both edit the same skill files. Only
`.agents/skills/markdown-studio-exploratory-qa-claude/` changes. One clean commit, one ready PR, never
merge.
:::

| Part | What | Kind |
| --- | --- | --- |
| 1 | `--annotate` in the driver, and "How to annotate" | code + docs |
| 2 | "Why this is wrong", Verdict and Requirements on every finding | docs |
| 3 | One QA bug template, `references/qa-bug-template.md` | docs |

## Part 1 — annotation as a driver feature

The owner wants an annotated **Expected** shot on every finding where no working case exists. The
technique of the evidence pass is in [reports/cr213-annotation-technique.md](../work/reports/cr213-annotation-technique.md).

> [!WARNING]
> In that pass the rectangles were placed **by eye**. The feature must compute them from a selector
> (box in window coordinates → clip origin → device pixel ratio) and be tested on a real shot.

- A driver feature: `q shot <name> --annotate '<selector|x,y,w,h>' --note '<text>'` (repeatable), or
  `q run annotate.mjs`, whichever fits the driver best. Outline plus a one-line note; an arrow is
  optional.
- No new install: use what the repository already has (Playwright's page rendering, or an SVG overlay
  drawn in the page before the CDP shot, are good candidates). Document the choice.
- A short **How to annotate** section with one example, in the bug template and in `charters.md`.
- Proof: one annotated shot taken in a real window (session `cr213`, one window, stopped at the end)
  on a synthetic fixture, attached to the report.

## Part 2 — why a finding is wrong, and its verdict against the requirements (owner, 2026-10-31)

:::{important}
**Purpose, stated at the top of `SKILL.md`:** a campaign exists to find **bad behaviours that no test
and no requirement covers yet**. A finding with no requirement (a **Gap**) is the main target, not a
weaker kind of bug. The requirements search only tells a real gap (nothing specified) apart from a
**Decision** (a requirement says otherwise). It must never discourage reporting.
:::

In campaign 210, D1 (BLOCK-053) and QA210-10 (REVIEW-152) showed that only the coordinator checked the
requirements, and only by chance. The skill never mentions SwRS or StRS today.

Change `SKILL.md`, `references/bug-sheet-template.md` and `references/charters.md`:

1. **Purpose** paragraph at the top of `SKILL.md`, as above.
2. **Requirements search.** Before writing a sheet, the charter agent searches `requirements/`
   (okfreq or grep on the area and keywords) and records the matching IDs.
3. **"Why this is wrong"**, a mandatory section right after Currently / Expected, 3 to 6 lines of the
   agent's reasoning:
   - what the user was trying to do, and what the behaviour costs them (lost work, wrong result,
     lost context, extra steps, confusion);
   - which expectation it breaks, and where that expectation comes from: an invariant, an in-product
     case that works, a named convention (VS Code, Obsidian, spreadsheet), or plain user logic;
   - why a reasonable author would not accept it.

   A reader who does not know the code must be able to agree or disagree from this section alone.
   "It looks wrong" is not enough.
4. **Fields** `Verdict: Bug | Gap | Decision` and `Requirements: <IDs or "none found">`:

   | Verdict | When |
   | --- | --- |
   | **Bug** | a requirement is violated, or an objective invariant breaks (buffer diff beyond the edited lines, data loss, error, element off-viewport, focus stuck), or the product contradicts itself (the same input works elsewhere) |
   | **Gap** | no requirement and no test covers this; the fix CR writes the SwRS and the test. The sheet names the missing test (the template's "Test to add") |
   | **Decision** | a requirement explicitly specifies the observed behaviour but it looks wrong: an owner question (like D1), never filed as a bug; listed in the index's "Decisions for the owner" section |

5. **Expected names its source:** a requirement ID, an invariant, an in-product working case, or a
   convention.
6. **Triage** (coordinator): read "Why this is wrong" first. A weak reason sends the sheet back to the
   charter agent, or downgrades it to Low as an intent question. A Bug with a cited requirement carries
   that ID into the backlog item; Decisions go to the owner.
7. **Severity scale**, one more line: "an intent question is Low unless data is lost".

## Part 3 — one QA bug template (owner, 2026-10-31)

`references/bug-sheet-template.md` becomes the single canonical template, renamed
`references/qa-bug-template.md` (update every link). The same text is the campaign sheet and the backlog
item's `01-intent.md`: triage copies it as is and appends the priority ("· P2") to the plain line under the title; no front matter. Draft:
`/private/tmp/claude-502/cr213-qa-bug-template.md` (already used to rewrite the 10 open QA 210 bugs).

The draft template, already used for the open QA 210 bugs, is in [reports/cr213-qa-bug-template.md](../work/reports/cr213-qa-bug-template.md). Keep its sections and the plain line under the title (no front matter).


## Done when

- [ ] `q shot … --annotate … --note …` (or `annotate.mjs`) draws an outline at the selector's real
      position, proven on a real shot.
- [ ] `SKILL.md` opens with the campaign's purpose; sheets carry Verdict, Requirements and "Why this is
      wrong"; the index has "Decisions for the owner".
- [ ] `references/qa-bug-template.md` replaces `bug-sheet-template.md`; every link is updated.
- [ ] Syntax gates, scenario JSON parse and the relative-link check pass.

## Part 3b — Owner decisions and balance (owner, 2026-10-31, corrected)

The separate "Owner decisions" checklist is dropped (owner correction).

- Each proposal section of `references/qa-bug-template.md` ends with its own line, ticked by default:
  `Uncheck to disagree: [x]`. The proposal sections are **Suggested direction** (the fix), **Test to
  add**, **Requirement to write or change**, and **Promote replay to E2E** when it is proposed.
- When no test is proposed, the section says "No test: <reason>", followed by the same ticked line.
  Unticking it means "add one anyway".
- The fix CR carries out only the sections that are still ticked.
- **Balance rule**, in the template AND in `SKILL.md`: propose a test only when the defect could come
  back silently and no existing test is close (data loss, buffer diff, regression of a fixed bug,
  invariant). Requirements follow the same rule.
- The owner's example:

  ```markdown
  ## Test to add

  Real-input E2E: edit mode on, click a link-card header and a link-only paragraph, assert a block
  editor is open and the active file is unchanged; Cmd/Ctrl-click still navigates.

  Uncheck to disagree: [x]
  ```

## Rounds

rounds: 4 (owner, 2026-10-31, doc-only). Round 4 fixes only the `--clip SELECTOR` padding sentence of
`references/qa-bug-template.md` (34 px only with `--annotate`, wrapped at 100 characters) and, if it is a
one-line change, the stale `drawAnnotations` comment in `scripts/qa.mjs`. No other code.
