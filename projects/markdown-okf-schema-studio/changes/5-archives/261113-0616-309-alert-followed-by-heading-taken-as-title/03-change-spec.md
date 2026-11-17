# Change Specification: a GitHub alert keeps its title when it starts with a heading or a bold line

Code read at `origin/main` (`cb968299`). The local `main` is behind: cut the worktree from
`origin/main` and read the rules there. Rules: [constitution](../../../../constitution.md),
`AGENTS.md`, `requirements/guidelines/project.guidelines.md` ("During a change").

## Goal

A GitHub alert renders as GitHub renders it. Today `> [!NOTE]`, `> # h`, `> b` shows an admonition
titled "h" with no heading in the body; GitHub shows the title "Note", then a real `<h1>h</h1>`,
then `b`. The same happens with a lone bold first line (`> **Bold first**`). After the change:

- An alert's title is the default title of its kind ("Note", "Tip", ...), or the text after the
  marker when there is one (`> [!WARNING] Read this` keeps the title "Read this", as today).
- A heading on the first body line of an alert stays a heading in the body.
- A lone bold paragraph on the first body line stays a bold paragraph in the body.
- MyST admonitions (`:::{note}`, `` ```{note} ``) and Quarto callouts (`::: {.callout-tip}`) keep
  the title shortcut: a leading heading or lone bold line is still their title.

## Decisions carried (02-answers.md, advisor section 6)

1. USER-IMPACT, owner: match GitHub for `> [!NOTE]`-style alerts (default title, or the marker's
   text, which stays); a heading on the first line stays a heading in the body.
2. USER-IMPACT, owner: same for a lone bold first line, through `takeAdmonitionTitle`.
3. USER-IMPACT, owner: MyST `:::{note}` admonitions and Quarto callouts keep the shortcut.
4. INTERNAL: legacy bold-marker alerts (`> **Note**`, `> **Important**`, `> **Warning**`) follow
   the same rule as `[!NOTE]` alerts.
5. INTERNAL: the renderer tells an alert from a directive by the `githubAlert` flag already set on
   the admonition by `mapAlertSourceLines`; the rewritten text does not change, so the line mapping
   of GFM-009 is untouched.
6. INTERNAL: the heading inside an alert is treated like any heading inside an admonition today:
   out of the TOC column and the sticky band. Asserted in the test.
7. INTERNAL: the heading's `data-line` is asserted (line 2 for the input above).
8. INTERNAL: GFM-009 gets a new scenario; the MyST requirement gets a boundary line saying alerts
   are excluded from the shortcut; the writing skill is checked (see "Writing skill").
9. INTERNAL: the proof against GitHub is a committed fixture of GitHub's HTML, never a network call
   in a test.

## What changes

### Renderer: `src/core/directives/admonition.ts`

`renderAdmonition` (lines 33-50) infers a title with `takeAdmonitionTitle` when the directive has no
argument and no `admonitionTitle` child. Add one condition: skip the inference when
`admonition.data?.githubAlert === true`. The node then keeps its children, and the "admonition"
pass of `src/core/render/mystNormalize.ts` (around line 344) adds the default title of the kind, as
it already does for an alert whose body starts with a paragraph.

Why this works without a new pass: in `src/core/render/mystRenderer.ts` the tree pass
"alert source lines" (`mapAlertSourceLines`, line 428) runs before "normalize nodes" (line 522),
which runs the directive plug-ins; `mapAlertSourceLines` in `src/core/render/mystGithubAlerts.ts`
sets `data.githubAlert = true` on the `admonition` child of every directive that opens on one of
`alertLines`, and `alertLines` holds both `[!TYPE]` and legacy bold-marker alerts. Alerts between
context tags are flagged too (`src/core/render/mystContextTags.ts:180`, run in the "context tags"
pass, also before normalization).

- Update the doc comment of `renderAdmonition` ("an admonition without arguments or title, except a
  rewritten GitHub alert, takes its title ...").
- Add `// @implements_req SwRS-MDOKFSTUDIO-GFM-009` next to the new condition (the function already
  carries MYST-006; keep it).
- `takeAdmonitionTitle` (`src/core/render/mystNode.ts:115`) is unchanged. The Quarto path in
  `mystNormalize.ts` (the "callout div" pass, around line 269) is unchanged.
- `src/core/render/mystGithubAlerts.ts` is unchanged (no change to the rewritten text or to
  `alertLines`).

### Tests

New file `test/core/render/alertTitle.test.ts` (or tests appended to
`test/core/render/mystFeatures.test.ts`; a new file is preferred to keep that file under the size
check). Use `renderPreviewDocument` and the HTML helpers as in the existing test "a leading bold
paragraph or heading supplies the MyST admonition title" (`mystFeatures.test.ts:513`). Each test
carries `// @tests_req SwRS-MDOKFSTUDIO-GFM-009`.

| Input | Expected |
| --- | --- |
| `> [!NOTE]\n> # h\n> b\n` | one `.admonition.note`; its `.admonition-title` text is "Note"; it contains an `h1` with text "h" whose `data-line` is 2, then a paragraph "b"; the admonition carries lines 1 to 3 |
| `> [!NOTE]\n> **Bold first**\n>\n> b\n` | title "Note"; the first body paragraph holds a `strong` "Bold first"; then a paragraph "b" |
| `> [!WARNING] Read this\n> ## h\n> b\n` | title "Read this"; an `h2` "h" in the body |
| `> **Note**\n> # h\n> b\n` (legacy bold marker) | title "Note"; an `h1` "h" in the body |
| `> [!TIP]\n> ### h\n` between context tags (as in the GFM-009 boundary rows) | title "Tip"; an `h3` "h" in the body |
| `[TOC]` then `# Top`, then `> [!NOTE]\n> ## Inside` | the TOC lists "Top" and not "Inside" |

The MyST and Quarto shortcut stays covered by the existing tests "a leading bold paragraph or
heading supplies the MyST admonition title" and "Quarto callout classes render as semantic MyST
admonitions" in `mystFeatures.test.ts`; they must pass unchanged. Add one assertion to the new file
that `:::{note}\n# h\nb\n:::` still has the title "h" and no `h1`, tagged
`// @tests_req SwRS-MDOKFSTUDIO-MYST-001`.

The sticky band: `BAND_EXCLUDED` in `src/page/features/stickyHeadings.ts:111` and the excluded
selector in `src/page/modules/tocColumn.ts:50` both exclude `.admonition`. The rendered alert has
the class `admonition`, so asserting that class on the alert's `aside` (first row above) is the
proof; no page test is added.

### Proof against GitHub

Commit GitHub's HTML for the first two inputs as fixtures in `test/core/render/alert-fixtures/`
(`heading-first-line.github.html`, `bold-first-line.github.html`), captured once with
`gh api markdown -f mode=gfm -f text="$(printf '> [!NOTE]\n> # h\n> b\n')"` (and the bold input).
Put a one-line HTML comment on top of each fixture with the command and the date. The test reads
the fixture and checks that GitHub and Studio agree on the order and text of the body: GitHub's
title text "Note", then the `h1` "h" (or the `strong` "Bold first"), then "b". If the API output has
no `markdown-alert` markup, capture the HTML GitHub shows for the same text in a rendered Markdown
file instead and say so in the comment. Tests make no network call.

### Requirements

- `requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-009.md` (proposed, not approved: no owner
  agreement needed). Add a scenario:

  ```markdown
  ### Scenario (boundary): The first body line never becomes the title

  | Input | Outcome |
  | --- | --- |
  | `> [!NOTE]`, `> # h`, `> b` | the title is Note; `h` is a heading in the body, on line 2, before the paragraph `b` |
  | `> [!NOTE]`, `> **Bold first**`, `>`, `> b` | the title is Note; `Bold first` is a bold paragraph in the body |
  | `> [!WARNING] Read this`, `> ## h` | the title is Read this; `h` is a heading in the body |
  | `> **Note**`, `> # h` | the title is Note; `h` is a heading in the body |
  ```

  Add the test file to `tested_in_files` and `src/core/directives/admonition.ts` to
  `implemented_in_files`. Add a verification-note line naming the new test file and the GitHub
  fixtures, and extend the criteria: "the title is the marker text, else the default, never the
  first body line".
- `requirements/tiers/swrs/myst/SwRS-MDOKFSTUDIO-MYST-001.md` (proposed, not approved), scenario
  "Untitled admonition takes its title from the first body line": add one line under the table:
  "A GitHub alert (`> [!NOTE]`, `> **Note**`) is not an untitled admonition here: its first body
  line stays in the body (SwRS-MDOKFSTUDIO-GFM-009)." The advisor and the answers name MYST-005;
  MYST-005 is superseded and deprecated (`superseded_by: MYST-001`), so the live rule is MYST-001
  and MYST-005 is not edited.
- `just requirements-update`, its generated files committed, then
  `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`.
- A dated entry in `requirements/tiers/log.md` under `## 2026-11-12` (or the day of the change):
  "### A GitHub alert keeps its title when it starts with a heading or a bold line", naming GFM-009
  (new boundary scenario) and MYST-001 (boundary line), both proposed, not approved.

### Writing skill

`skills/writing-for-markdown-okf-schema-studio/` describes alerts as `> [!NOTE]` (`SKILL.md:37`)
and shows one alert without a heading (`references/examples.md:33`); it never mentions the title
shortcut. Studio now matches the standard syntax, so the skill does not change (the guideline asks
for an entry only where Studio differs). `test/core/render/writingSkill.test.ts` must pass; if it
fails, fix the skill in this PR.

### Changelog

Append to the end of `## Unreleased` in `CHANGELOG.md`:

```markdown
- A GitHub alert that starts with a heading or a bold line keeps its title ("Note", or the text
  after `[!NOTE]`) and shows that heading or bold line in its body, as GitHub does. MyST
  admonitions and Quarto callouts still take their title from a leading heading or bold line.
```

### Commit and PR

- One commit `fix(render): keep the title of a GitHub alert that starts with a heading`, per the
  commit guideline and its allowed scopes.
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`; its Tests section lists GFM-009 and
  MYST-001 with their source and test files. This PR sits in the batch stack (after
  card-in-blockquote-line-offset, per the advisor's order).

## Out of scope

- Any change to MyST admonitions or Quarto callouts (decision 3).
- Any change to `expandGithubAlertsWithLines`, the line mapping or the click-to-edit range of
  alerts.
- Rendering alerts with GitHub's own markup (`markdown-alert` classes); Studio keeps its
  admonition markup.
- Visual baselines: no visual fixture has an alert whose first body line is a heading or a bold
  line (searched in `test/visual/fixtures/` and the test sources), so none should change. If
  `just ci-visual` shows a diff, it is investigated, not re-baselined blindly.

## Evidence

- `just check` (unit, contract, file size, unused exports) and `just requirements-lint`.
- The new tests above pass and fail on `origin/main` before the fix (run them once without the
  `renderAdmonition` change and note it in the PR).
- The existing MyST and Quarto title tests pass unchanged.
- `just preflight` passes (constitution, section 4).
- Scenario steps for the PR (simulated preview is enough, no real window needed): open a document
  with `> [!NOTE]`, `> # h`, `> b`; the preview shows a Note alert with a large heading "h" inside
  and the paragraph "b"; a document with `:::{note}`, `# h`, `b`, `:::` still shows a note titled
  "h".

## Open questions

None.
