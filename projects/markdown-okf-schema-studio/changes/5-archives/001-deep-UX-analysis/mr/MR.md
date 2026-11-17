# Markdown OKF-Schema Studio: fix the editing problems found by the deep UX review

**Branch:** `dev/gsemet-deep-ux-analysis` → `master` · **Scope:** ``
and one line of `AGENTS.md` · **One squashed commit.**

## What changes for users

Before this MR, reading in the Studio preview worked well, but writing in it was risky. An edit
could silently lose text or rewrite parts of the file the user never touched. After this MR,
editing in the preview behaves like editing in a text editor. It changes only what the user
typed.

The changes users will notice most:

1. **No more lost or mangled text.**
   - Escape keeps what you typed.
   - Undo stays inside the editor.
   - Enter in a list adds a sibling item instead of re-parenting the items below it.
2. **Clean Git diffs.**
   - Editing one table cell changes one line; aligned and compact tables keep their layout.
   - Editing one frontmatter field changes that field only; folded text, flow lists and comments
     are kept byte for byte.
   - Typing produces a few undo steps, not one per character.
3. **Familiar keys.**
   - Enter saves one-line fields, and Cmd+Enter saves multi-line ones.
   - Tab indents in text and moves between table cells.
   - The caret lands where you click.
   - Each editor shows what it edits, its Done and Revert buttons, and its shortcuts.
4. **A preview that stays put.**
   - It keeps its document when another editor gets focus.
   - The edited block no longer jumps after a save.
   - Opening a file from Quick Open no longer covers it.
   - While you type, it updates its content in place instead of reloading the whole page.
5. **Easier to find and read.**
   - The preview opens from the editor title bar, the Explorer, or Cmd+K Shift+V.
   - Tabs read `Studio · file.md`.
   - Link problems read "File not found" instead of `[E10]`.
   - User messages no longer mention Sphinx.

Nothing was removed. Three behaviours were reviewed and deliberately kept as they are:

- links resolved from the Git root (`UX-22`);
- YAML-style value display (`UX-24`);
- `#` markers in the sticky heading band (`UX-34`).

## Why: the QA campaign

The extension had good unit and E2E coverage. We wanted to know how it holds up in daily use, so
we ran an exploratory QA campaign that used it the way a person does every day: reading, editing in
the source next to the preview, editing inside the preview, the Open With editor, OKF frontmatter,
and links.

**How.** An agent drove a real VS Code window with real mouse and keyboard input (Playwright on the
Electron window). It worked on the book chapters, the OKF requirement examples and synthetic
fixtures. Every finding has a bug sheet with:

- the use case and the steps on a named fixture;
- expected and observed behaviour;
- the code location;
- a screenshot;
- a "done when" criterion.

A second pass covered what the first one left out: line endings, diagrams and math, wikilinks,
complex frontmatter, reload, restricted mode, narrow layouts and typing latency.

**What it found.** Part 1 produced 37 findings, 34 approved for fixing: 9 high, 12 medium and 13
low.

- **Inline editing could lose or corrupt content without warning.** Escape reverted text that
  autosave had already written. Enter in a nested list re-parented unrelated items. In the Open
  With editor, Cmd+Z closed the editor mid-sentence.
- **Structured edits rewrote more than they should.** One cell edit reformatted the whole table.
  One frontmatter edit re-serialized the whole frontmatter. Both gave whole-block Git diffs.
- **Keyboard conventions differed per control.** Enter meant newline, save, or nothing depending
  on the field. Tab never indented or moved to the next cell.
- **The side preview lost its document** whenever a non-Markdown editor became active.
- **The tests did not type.** The E2E suite injected 51 synthetic messages and never used real
  typing, undo or Tab, which is why most of the above escaped it. The round-trip fixtures were
  already in the serializer's style, so reformatting went unnoticed. Screenshots were captured but
  nothing checked them.

Part 2 added 14 findings, `UX-35` to `UX-48` (for example, CRLF documents cannot be edited inline
past the first keystroke). They are **not** in this MR and are listed under follow-ups.

## What this MR brings

### Test tooling first

The campaign showed that the tests could not see these bugs, so the work started by making them
visible:

- **A real-input E2E harness.** It drives the VS Code window with real mouse and keyboard and has
  one scenario per fix. Each scenario failed before its fix and passes after it.
- **Formatting-preservation corpora** for tables and frontmatter, written in the styles people
  actually use (compact and aligned tables, folded scalars, flow sequences, comments).
- **Geometry checks** on the screenshot campaigns: overlaps, clipping and wrapped identifiers are
  now asserted, not only captured.

The unit tests went from 315 to 655. The real-input suite went from nothing to 40 scenarios.

### Before and after

The before shots come from the QA campaign. The after shots come from replaying the same bug
sheets on this branch with real input.

**Inline editor: what is edited and how to finish** (`UX-07`, `UX-08`, `UX-09`). Before: clicking a
paragraph in edit mode gave no outline, no buttons and no hint, and edit mode reflowed every
paragraph with the source line breaks. After: the edited block is outlined, the source shows in a
monospace editor with its line range and shortcuts, Done and Revert are explicit, and the
surrounding paragraphs keep their flow.

| Before | After |
| --- | --- |
| ![Before: inline editing](/uploads/5a26d18a046aad56f1fa63255aea9f6b/01-inline-editor-before.jpg) | ![After: inline editing](/uploads/9e473d348cbe3843efe3e7554cf1948d/01-inline-editor-after.jpg) |

**Table toolbar** (`UX-14`, `UX-15`). Before: the toolbar floated over the previous row and used
icon-only buttons, and short identifiers such as `nw-02` wrapped. After: the toolbar sits above
the table with labelled buttons and says which cell is edited; short cells stay on one line.

| Before | After |
| --- | --- |
| ![Before: table toolbar](/uploads/60f2675962ce96e231557fa65973e283/02-table-toolbar-before.jpg) | ![After: table toolbar](/uploads/b793ce688295925f2fc4b76b3a97b861/02-table-toolbar-after.jpg) |

**Link problems in plain words** (`UX-23`). Before: a broken link in the frontmatter showed a bare
`[E10]`. After: it reads "File not found", and the tooltip explains which target did not resolve.

| Before | After |
| --- | --- |
| ![Before: link diagnostics](/uploads/89bd44022308c39292db4aeb8bd2431f/03-link-diagnostics-before.jpg) | ![After: link diagnostics](/uploads/b632dbdffca1857f0fffc7f248d3b1bc/03-link-diagnostics-after.jpg) |

**Entry point and tab title** (`UX-30`, `UX-32`). Before: the preview could only be opened from the
Command Palette, and the tab read `Markdown OKF-Schema Studio: file.md`. After: a title-bar
button, an Explorer entry and Cmd+K Shift+V open it, and the tab reads `Studio · file.md`.

| Before | After |
| --- | --- |
| ![Before: entry point](/uploads/ad0a5cce757d860aba7debb3bc19ee1f/04-entry-point-before.jpg) | ![After: entry point](/uploads/b88109fb39af504baba540748279c0a8/04-entry-point-after.jpg) |

**Frontmatter lists and new fields** (`UX-17`, `UX-19`, `UX-20`). Before: pressing Enter in the title
saved `title: |` as a block scalar, and the row menu covered the next row's value. After: Enter
saves a one-line field, list items suggest Markdown targets and say when a file does not exist,
and the row actions stay inside the edited row. The after shot was taken in a narrow window,
which clips the list input.

| Before | After |
| --- | --- |
| ![Before: frontmatter list](/uploads/328e64c0634d04bec5d6a33d4a33261a/05-frontmatter-list-before.jpg) | ![After: frontmatter list](/uploads/3f0937402a715ab242fe39e903ca5ca1/05-frontmatter-list-after.jpg) |

**Diffs, before and after** (`UX-12`, `UX-16`), on the same edits as the bug sheets.

Editing one table cell, before:

```diff
-|-------|--------|------|--------|--------------|...|----------|
+| ------- | -------- | ------ | -------- | -------------- |...| ---------- |
-| nw-02 | North | 9 | 2 | no | ...
+| nw-02 | North Pole | 9 | 2 | no | ...
```

After, only the edited line changes:

```diff
-| nw-02 | North | 9 | 2 | no | ...
+| nw-02 | North Pole | 9 | 2 | no | ...
```

An aligned table keeps its padding; the edited cell is re-padded to its column:

```diff
 |:---------|:-----------|:--------:|------:|
-| alpha    | left       |  middle  |     1 |
+| alpha    | leftX      |  middle  |     1 |
 | beta     | text       |   mid    |    22 |
```

Editing the frontmatter title, before:

```diff
-title: Write CSV output
-description: When export is requested, the service SHALL write the report as CSV
-  output.
+title: |
+  Write CSV output: with quotes "and" colons
+description: When export is requested, the service SHALL write the report as CSV output.
-- StRS-CORE-001
+  - StRS-CORE-001
```

After, only the title changes:

```diff
-title: Write CSV output
+title: 'Write CSV output: with quotes "and" colons'
```

**Typing no longer reloads the preview** (`UX-28`). Before, almost every keystroke in the source
reloaded the whole preview page. On a 70 KB book chapter, typing 32 characters caused 26 full
reloads, which reset the page and its scripts each time. Now the preview swaps only its content area
inside the loaded page. The same test causes **0 reloads**, the scroll position does not move, and
the properties table and links update in place. If a render takes more than 1.5 s, a small overlay
says the preview is pending, without moving the content. The setting
`markdownOkfSchemaStudio.preview.incrementalUpdates` (on by default) turns this off. Anything
unusual falls back to a full reload.

![After: the chapter preview right after typing 32 characters, with no reload](/uploads/acdcf8fe300224e382a39e9d11310e7c/07-typing-no-reload-after.jpg)
![The pending overlay after 1.5 s, without moving the content](/uploads/af5b3c27f49d6abda98f25e782f01d57/06-pending-overlay-after.png)

### Full list of fixes

| ID | Sev. | Fix |
| --- | --- | --- |
| `UX-01` | High | Escape keeps text that autosave already wrote |
| `UX-03` | High | Undo stays in the inline editor in the Open With editor |
| `UX-04` | High | Enter adds a sibling list item |
| `UX-12` | High | One table cell edit is a one-line diff |
| `UX-16` | High | Only the edited frontmatter field changes |
| `UX-17` | High | Enter saves one-line fields; Cmd+Enter saves multi-line fields |
| `UX-25` | High | The side preview keeps its document when another editor gets focus |
| `QA-01` | High | Round-trip fixtures in the styles people actually use |
| `QA-02` | High | Real-input E2E harness |
| `UX-02` | Med. | One undo step per edit session |
| `UX-05` | Med. | Tab and Shift+Tab indent |
| `UX-06` | Med. | The caret lands at the click position |
| `UX-07` | Med. | Outline, Done and Revert, shortcut hint |
| `UX-10` | Med. | Insert a block between blocks |
| `UX-13` | Med. | Tab moves between cells; Tab on the last cell adds a row |
| `UX-18` | Med. | One click toggles a boolean |
| `UX-19` | Med. | List items: Enter, Backspace, link suggestions, click to edit |
| `UX-23` | Med. | "File not found" instead of `[E10]`; the badge jumps to the first issue |
| `UX-28` | Med. | The preview updates in place while you type: 0 page reloads, against 0.8 per character before |
| `UX-30` | Med. | Title-bar button, Explorer entry, Cmd+K Shift+V |
| `QA-03` | Med. | Geometry checks on screenshots, plus an agent review of all captures |
| `UX-08` | Low | Monospace editor, tab size 4 |
| `UX-09` | Low | No reflow in edit mode |
| `UX-11` | Low | The edited block stays in place after a save |
| `UX-14` | Low | Table toolbar above the table, with labels |
| `UX-15` | Low | Short cells do not wrap; overflow cue on wide tables |
| `UX-20` | Low | Row actions inside the edited row; nothing clipped |
| `UX-21` | Low | Add or remove fields where the table shows them; required fields protected |
| `UX-26` | Low | Status title and message on two lines; no user-facing "Sphinx" |
| `UX-27` | Low | The preview's editor group is locked, and released when it closes |
| `UX-29` | Low | No jump when scroll ownership changes |
| `UX-31` | Low | The editor is named "MyST + OKF Studio" |
| `UX-32` | Low | Tabs read `Studio · file.md` |
| `UX-33` | Low | The anchor toggle is disabled without a text editor; edit mode is remembered |

## How it was verified

Every fix went through the same loop:

1. A task file with allowed files, protected features, and a "done when" criterion.
2. A Sonnet implementer writes the failing test first, then the fix.
3. An independent gate runs: unit, types, contracts, full integration, and the visual campaign
   compared with a baseline.
4. An Opus reviewer reads the diff against a checklist and the list of protected features.
5. Up to three rounds of fixes.

| Check | Where | Result |
| --- | --- | --- |
| Unit, types, contracts | final tree | PASS, 655 unit tests (315 before) |
| Full integration: scroll, untrusted, trusted plus 40 real-input scenarios, standalone, reload | final tree | PASS |
| Visual campaign compared with the baseline taken before any change | final tree | PASS, 0 new failures |
| `UX-28`: full page reloads while typing 32 characters fast in a 70 KB chapter | final tree | **0** in 4 runs (26 before the work); 16 with the new setting turned off |
| Replay of every approved bug sheet in a real VS Code window with real input (37 scenarios) | the final tree without the last patch-chaining commit, which was re-measured by the `UX-28` row | **0 regressions**; 4 expected changes (`UX-21`, `UX-27`, `UX-28`, `UX-30`), each from an approved decision |
| Agent review of 143 screenshots | before the last six tasks | 0 regressions |

Known test flakiness, unrelated to this MR:

- `checkboxToggle.test.ts` "one undo restores the original source" depends on focus;
- the block-editor textarea wait times out under heavy machine load.

Both pass on rerun.

## Known limits and follow-ups

Not in this MR, and tracked locally:

- **Block editor follow-ups (requested).** Esc should behave like Cancel, replacing the `UX-01`
  behaviour. Home and End should move the caret within the edited block; today, on macOS, they
  scroll the whole preview, and End shifts a table by about 440 px. Also requested: a smaller font,
  the status line on the button row, and table cells using the same editor.
- **Part-2 findings `UX-35` to `UX-48`.** The most severe is `UX-35`: in CRLF documents, inline edits
  stop being saved after the first keystroke.
- **Preview updates (T34).**
  - The PlantUML patch has no fallback timer.
  - Link-target hints can stay stale until the next full load.
  - The properties-table update can still fall back to a full load during a typing burst.
- **Group lock (T39).** With `workbench.editor.closeEmptyGroups: false`, closing the preview can
  unlock an empty group that the user locked on purpose.

## How this was built, and what it cost

This work was done with Claude Code.

- **Roles.**
  - An Opus orchestrator ran the QA campaign, wrote the plan and gated every task.
  - Implementers wrote the code: Haiku for the first 7 tasks, Sonnet for the rest.
  - An independent Opus reviewer checked each task.
- **Elapsed time.** 2026-10-08 to 2026-10-14, including nights and usage-limit pauses.
- **Cost.** About **$341** at API list prices, or $348 with three short side sessions about this
  work. That is about $10 per approved fix, the QA campaign included.
  - The orchestrator is 48 % of the cost, reviews 22 %, and Sonnet implementers 21 %.
  - Most of the money is context, not generated text: cache writes are 44 % and cache reads 42 %.
- **Haiku against Sonnet as implementer.**
  - Haiku's own spend was about 6 times lower per task: $0.33 against $1.89.
  - It passed review in round 1 on 1 task of 7, against 22 of 35 for Sonnet.
  - It drew 4 times more blocker or major findings. These were silent data-loss bugs in YAML and
    table patching, all caught in review.
  - Once its review rounds are counted at the same reviewer effort, a Haiku task cost about as much
    as a Sonnet task and took twice as long.
  - Sonnet implementer with an Opus reviewer at low effort was the best setup: a median of about
    $2.5 and 21 minutes per task.
- **Caveats.**
  - The reviewer effort was lowered at the same time as the switch to Sonnet.
  - Only 7 tasks ran with Haiku.
  - The amounts are API-equivalent; a subscription bills differently.




