# CR 214, round 2, Inspector review: radio choice lists (whole change)

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-214` (uncommitted, on top of
04b71f01). I edited no repository file and committed, stashed or switched nothing. Scratch files are
under `/private/tmp/claude-502/cr214-driver/inspect-r2/`. This review covers round 1 and round 2
together.

## Verdict: APPROVE

No must-fix. The round 1 must-fix and nice-to-haves 1, 2, 3 and 6 are fixed. The host now refuses
forged groups without refusing real ones. The Done-when of `00-request.md` is met; the one gap is
"normal CI green", which only the PR run can show. Both gates pass. The nice-to-haves below are
optional. The first one, a heavy CI dispatch before the merge, is the one I recommend most.

## Evidence by check

### 1. Round 1 findings

| Round 1 item | State | Evidence |
| --- | --- | --- |
| Must-fix: the heading test could not fail | fixed | `test/core/render/radioGroups.test.ts:92`: 2+2 items around the heading, asserting `[["1:2: ", "2:2:x*"], ["4:2: *", "5:2: "]]`. The coder showed it fails under a mutation that merges the two lists. |
| NTH 1: group shape check on the host | fixed | `src/core/render/radioMarkers.ts` `isOneRadioGroup`, called by `radioSelectEdits`. A refusal gives `RADIO_GONE`. |
| NTH 2: GFM-027 criteria line | fixed | The line names `radioGroup`, 2 to 256 positions, and `checked` true. |
| NTH 3: ordered lists lost their numbers | fixed | The CSS is scoped to `ul > li.myst-radio-item`. The visual assertion checks `listStyleType: decimal`. The images show `1.`/`2.` followed by the radio. |
| NTH 6: fixed 1.5 s wait | fixed | It is replaced by a MutationObserver proof (see 2). |
| NTH 4 and 5: text click, focus after a write | deferred | Left as follow-ups, as the task said. |

**`isOneRadioGroup` is correct.** It requires:

- strictly ascending lines;
- each line a radio item with its `(` at the stated column;
- the same marker indentation and the same marker kind (the bullet character, or the ordered
  delimiter) on every option;
- between two options, none of these: a blank line (with quote markers ignored), a list item at the
  same or a smaller indentation, or a heading, thematic break or fence indented less than the item
  content.

It is called after the per-option checks, so a refusal never leaves a partial edit. The page sends
the positions in `querySelectorAll` document order, which is ascending, so real groups pass.

**Forged groups are refused.** I probed the built output
(`inspect-r2/probe/shape.mjs`). These are refused:

- two groups split by a blank line;
- a subset that skips a middle option;
- a group mixing nesting levels.

These are accepted:

- lazy continuation text;
- an item holding a fenced block with `- x` and `# y` inside;
- `9.`/`10.`;
- block quotes.

**It does not over-refuse.** One case looked like an over-refusal: a lazy line `2025. was a year`
between two options. The host refuses it, but I rendered it (`inspect-r2/probe/render.cjs`), and
markdown-it opens a new ordered list there, so the preview shows no group either. The host and the
renderer agree. A blank line inside a fenced block of an option is refused by the host, and the
renderer's `blankLineBetween` closes the run on the same raw blank line, so they agree there too.

**The deviation is sound.** Using the same marker indentation instead of the same `(` column is
right: `9. ( )` and `10. ( )` are one list with different `(` columns, and a test covers it. The
per-option column is still checked exactly, so the column check is not weakened.

**Tests are in place.**

- In `test/core/edits/radioSelect.test.ts`, the refusal test (6 shapes) is failing-first; the
  coder bypassed the check and saw it fail.
- The "accepted" test guards against over-refusal.
- In `test/session/radioChoice.test.ts`, "a forged choice that names the options of two groups"
  asserts no apply and `RADIO_GONE`.

### 2. The E2E no-write proof (`test/integration/radioChoice.test.ts`)

- **What it watches.** `watchToggles` is awaited, so the observer is attached before the click or
  key is sent. The page sets `aria-busy="true"` on every option synchronously, in the same handler
  that calls `postToggle` (`src/page/features/checkboxes.ts` `selectRadio`). The checkbox path does
  the same.
- **No race.** The busy flag is removed only in `settle`, which runs on a later
  `previewCheckboxResult` message. A MutationObserver callback is a microtask at the end of the
  click task, and `takeRecords()` collects any record not yet delivered. A sent toggle is therefore
  always seen with `aria-busy === "true"`. If a write replaced the frame, the `evaluate` would throw
  on the missing watch object, and the test would still fail.
- **The version checks stay.** The version and text equality checks are kept as a backstop. The
  no-op step now reads the version before the click; round 1 read it after.
- **Nothing is weakened.** There is no retry, no `force` and no raised timeout, and no existing
  assertion was weakened.
- **The arrows step has a sync point.** The `waitFor(focusedOption === …)` calls prove that the
  key handlers ran before `assertNoWrite`.
- **The click step has none.** It relies on Playwright's CDP input ack, which is normally enough
  (see nice-to-have 3).

### 3. Done-when of `00-request.md`

| Done-when | State |
| --- | --- |
| Parser and renderer, a unit test for every rule, including the 2-item minimum and mixed lists | met (round 1 table, plus the fixed heading case) |
| Real-input E2E: click, undo, selected no-op, Space and Enter, arrows | written and compiled in `just check`. **Not yet executed**: the heavy job is not dispatched (see nice-to-have 1). |
| Visual scenarios in Cream and Dark; before/after shots for the PR | `gfm/v10-radio-plan-cream-900` and `gfm/v11-radio-plan-dark-900` with 11 content assertions. The 4 shots are in `/private/tmp/claude-502/cr214-driver/shots/`. |
| New SwRS, proposed, and user docs | SwRS-MDOKFSTUDIO-GFM-039 is `proposed`. `docs/user/editing.md` has a new paragraph. |
| README section | "Decide in the page: choices in your plans" comes right after "Review with comment threads", with a Cream/Dark table like the cards section. The images come from `README_BY_ID` crops of the visual scenarios. |
| Demo fixture reused by the shot | `test/visual/fixtures/74-radio-plan.md` (2 groups, one of them ordered, plus a task list) is used by both scenarios. |
| Writing skill | `SKILL.md`: a "Choices" row in "What renders", a taste rule, and a pointer. The PLAN example is in `references/examples.md` and is rendered by `writingSkill.test.ts`, whose new FAMILIES entry needs a labelled `radiogroup` and a checked `radio`. `SKILL.md` is 154 lines (the limit is 160). The skill links nothing in the repository. Constitution §6 holds. |
| QA template | `qa-bug-template.md`: several approaches go in a radio group with the recommended option `(x)` and no "Uncheck" line; a single proposal keeps `Uncheck to disagree: [x]`; a reading agent checks for exactly one `(x)` and asks the owner when there is none or more than one. This matches the spec. It is mirrored briefly in that skill's `SKILL.md` and `charters.md`. No other copy and no sync check exist. |
| `just check` green, normal CI green | `just check` is green (see 10). Normal CI is still to come. |

### 4. README image risk

- **No pixel comparison in CI.** No CI job compares README images pixel by pixel.
  `generate-readme-images.py --check` runs only by hand. The `gallery` job (dispatch only,
  `heavy && gallery`) runs `ci-gallery` → `site:gallery` → `generate-readme-images.py`, which
  *writes* images into the job's checkout and uploads the site artifact. It never fails on a
  difference.
- **No risk from the Mac pixels.** Images made on macOS cannot break the normal or the heavy CI.
  Only `test/site/*` checks the README metadata: the counts, the unique names, and that a top crop
  reaches the right edge (1800 = 900 px × DPR 2). It passes.
- **Same as the other images.** The new images match the existing ones:
  - `.gitattributes` stores `*.png` in LFS (`git check-attr` shows `filter: lfs`, like
    `myst-cards-tabs-cream.png`), and git-lfs 3.8.1 is installed.
  - Both are 720×456, the same width as the other 720 px visual crops (`myst-cards-tabs-*`
    720×624).
  - The names follow the `<topic>-cream.png` / `<topic>-dark.png` pattern of `charts-*` and
    `myst-cards-tabs-*`.

### 5. The images, which I looked at myself

- **`radio-plan-cream.png`:**
  - round rings in place of the bullets;
  - the selected options have a terracotta ring and dot;
  - the unselected rings are clearly readable on cream;
  - the ordered group shows `1. ○` and `2. ◉`;
  - the radios line up with the task checkboxes;
  - the toolbar is collapsed in the top right.
- **`radio-plan-dark.png`:**
  - the same layout;
  - a blue selected ring and dot;
  - grey unselected rings that are readable;
  - the numbers are kept.
- **`before-cream.png` / `before-dark.png`:** the same fixture as plain text. Bullets and the
  literal `(x)` / `( )`, the ordered list shows `1. ( ) Ship…`, and the task checkboxes render. This
  is correct for 04b71f01.
- **`after-cream.png` / `after-dark.png`:** the same view as the README images, at the same 900 px
  crop as the before shots, so the pairs compare well.

### 6. Ring colour and CHANGELOG

- **Ring colour.** The unselected ring changed from `--studio-input-border` to
  `color-mix(in srgb, currentColor 55%, transparent)`. This is acceptable:
  - it follows the text colour on every theme (cream, dark, white, VS Code light and dark);
  - the images confirm that the round 1 token was too faint on cream;
  - the selected state keeps `--studio-focusBorder`, like the checkboxes;
  - the webview is Chromium, which supports `color-mix`.

  The only weak spot is high-contrast themes, where 55 % alpha lowers contrast (nice-to-have 4).
- **CHANGELOG.** Keep the entry. `## Unreleased` already holds per-feature entries in the same
  style (the grid card editor entry just below it), so this matches the convention.

### 7. Changed count assertions

These are counts only. The intent and the messages are unchanged apart from the appended reason.

- `test/site/e2eGroups.test.ts`: 408 → 410, and "plus 2 radio choice plan scenarios (CR 214)" is
  added to the message.
- `test/site/scenarioInvariants.test.ts`: 18 → 20 README sources.
- `test/site/captureRegistry.test.ts`: 24 → 26 README files ("20 visual + 6 real-window").

### 8. Requirements

- **No protected approved StRS was touched.** The only StRS in the diff is StRS-GFM-003, which is
  `proposed` and not on the protected list. Its change is generated: a `derived_by` entry and a
  Links line.
- **No approved requirement changed at all.** These are all the requirement files the change
  touches:
  - GFM-039 (new, `proposed`);
  - GFM-027 (`proposed`);
  - CORE-073 (`proposed`);
  - GFM-003 (`proposed`);
  - the gfm `index.md` (generated);
  - `log.md`.
- **CORE-073 may be edited.** Its `req_lifecycle` is `proposed` and its `status` is `stable`. The
  edit appends "radio choices in a plan" to the family list of a hand-written scenario, which is
  not a generated field, to match the test's new FAMILIES entry. A proposed SwRS follows its code,
  so this is allowed and required (constitution §1).
- **GFM-039 is complete.**
  - Its `implemented_in_files` and `tested_in_files` are generated.
  - It has rows for the refusal of a forged group and for an ordered list.
  - It names both visual scenarios as a method.
  - `okfreq` reports no warning on it.

### 9. Stray files

The worktree has no scratch or log files and nothing from the before tree. `git status --ignored`
shows only ignored generated files: `.pytest_cache`, `__pycache__` folders,
`test/visual/fixtures/gen-huge-document.md` and `out/`. These are not to be added. The scratch files
(`css.bak`, `radioGroups.bak`, `crop-radio.py`, `before-tree/`) are all under
`/private/tmp/claude-502/cr214-driver/`, outside the worktree.

**Paths to `git add`.** These are 43 paths, exactly the `git status --porcelain` list:

```text
.agents/guidelines/writing-skill-maintenance.guideline.md
.agents/skills/markdown-studio-exploratory-qa-claude/SKILL.md
.agents/skills/markdown-studio-exploratory-qa-claude/references/charters.md
.agents/skills/markdown-studio-exploratory-qa-claude/references/qa-bug-template.md
CHANGELOG.md
README.md
docs/user/editing.md
images/readme/radio-plan-cream.png
images/readme/radio-plan-dark.png
requirements/tiers/log.md
requirements/tiers/strs/gfm/StRS-MDOKFSTUDIO-GFM-003.md
requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-027.md
requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-039.md
requirements/tiers/swrs/gfm/index.md
requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-073.md
skills/writing-for-markdown-okf-schema-studio/SKILL.md
skills/writing-for-markdown-okf-schema-studio/references/examples.md
src/core/edits/sourceEdits.ts
src/core/preview/styles/contentLayoutStyles.ts
src/core/protocol/pageToHost.ts
src/core/protocol/pageToHostMessages.ts
src/core/render/checkboxMarkers.ts
src/core/render/mystInlineTransforms.ts
src/core/render/mystRenderer.ts
src/core/render/radioGroups.ts
src/core/render/radioMarkers.ts
src/page/features/checkboxes.ts
src/session/features/sourceEdits.ts
test/core/edits/radioSelect.test.ts
test/core/render/radioGroups.test.ts
test/core/render/writingSkill.test.ts
test/integration/radioChoice.test.ts
test/integration/trusted-suite.ts
test/page/runtimeHarness.ts
test/page/runtimeRadioGroups.test.ts
test/session/radioChoice.test.ts
test/site/captureRegistry.test.ts
test/site/e2eGroups.test.ts
test/site/scenarioInvariants.test.ts
test/visual/fixtures/74-radio-plan.md
test/visual/radioPlanScenarios.ts
test/visual/scenarioDefinitions1.ts
test/visual/scenarioIds.ts
```

### 10. Gates (run by me, in the foreground, nothing left running)

- **`just check`:** exit 0.
  - 3320 of 3320 unit tests pass.
  - 71 of 71 security tests pass.
  - 139 pytest tests pass, with 12 warnings. These are pre-existing pytest temp-dir cleanup
    `PermissionError` warnings from `test_expand_targz_rejects_relo…`, not failures.
  - Boundaries pass (313 modules), the limits pass (901 files) and the settings pass (19).
  - The requirements stage reports "1072 requirements, 0 errors, 21 warnings": 0 indexes, 0
    projections and 0 coverage files would change.
  - The log is `/private/tmp/claude-502/cr214-driver/inspect-r2/check.log`.
- **`uv run --group docs --group requirements okfreq validate --check-links --project-root .`:**
  "1072 requirements, 0 errors, 21 warnings". All the warnings are pre-existing, for example the
  `PALETTE-264` `url` cross-links. None concerns GFM-039, GFM-027, GFM-003 or CORE-073.
- **Worktree after the gates:** the same 43 paths as before.

## Must-fix

None.

## Nice-to-have

1. **Dispatch heavy CI on the PR before the merge**:
   `gh workflow run ci.yml --ref <branch> -f heavy=true`.
   - Why: `test/integration/radioChoice.test.ts` and its new no-write proof have never run. They
     only compile.
   - The change touches the webview and the host edit path, and CI rule 13 asks for the real VS Code
     jobs before such a change is merged.
   - The spec only needs normal CI, so this is the maintainer's call. It is the only executed
     evidence the E2E Done-when line can get.
2. **Wording and wrapping:**
   - `.agents/skills/markdown-studio-exploratory-qa-claude/references/qa-bug-template.md:95` leaves a
     short line ("…; the fix CR") after the insert. Rewrap the paragraph.
   - `.agents/guidelines/writing-skill-maintenance.guideline.md:45` is 109 characters, over the
     100-character wrap.
3. **`test/integration/radioChoice.test.ts`, the "click the selected option" step:** add a positive
   sync point before `assertNoWrite`, for example `waitFor` until `focusedOption(frame) === 5`,
   since the span with a tabindex takes the focus on mousedown. This proves the click reached the
   page, as the arrows step already does. Without it, the proof relies on the CDP input ack only.
4. **`src/core/preview/styles/contentLayoutStyles.ts`, `.myst-radio` border:** in high-contrast
   themes, a full-strength ring would read better, for example under `@media (forced-colors:
   active)` or with a `--studio-contrastBorder` fallback. This is cosmetic.
5. **Stress plan:** CI rule 12 asks for new real-window scenarios in `test/shared/stressPlan.ts`.
   That list holds only the real-input suite's scenario names, and the trusted-suite steps
   (`checkbox-toggle`, `table-empty-column`) are not in it. `radio-choice` follows that precedent,
   so this is not a defect. It is worth a backlog note if the stress job is ever extended to the
   trusted-suite steps.
6. **Still-open follow-ups from round 1, for the backlog:**
   - a click on the option text selects the option;
   - the focus goes back to the same control after a content patch, for radios and checkboxes.
