# Change specification: a grid inside a GitHub alert stays inside it

Type: fix. Triage: automatable, P2. Sources: `intake/request.md`, `01-intent.md`, `02-answers.md`.
Rules: `.agents/constitution.md`, `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`
and `requirements/guidelines/project.guidelines.md` ("During a change").

## 1. Goal

A `::::{grid}` written inside a GitHub alert (`> [!NOTE]` or the bold form `> **Note**`) renders
as one note that holds the whole grid, with every card, and the text after the alert renders
after the note, as it does on GitHub.

## 2. Reproduction (done on `main` at 6b803967, 2026-11-13)

Source (both heads give the same result):

```markdown
> [!NOTE]
> ::::{grid} 2
> :::{card} A
> Alpha
> :::
> :::{card} B
> Beta
> :::
> ::::

After.
```

`expandGithubAlertsWithLines` rewrites it to a three-colon `:::{note}` around the four-colon
grid. `renderMyst` then gives:

- an `aside.admonition.note` (lines 1 to 5) that holds a grid with card A only;
- card B as a separate block outside the note (lines 6 to 8);
- the grid's closing `::::`, the note's `:::` and the paragraph `After.` swallowed into a
  `<pre><code>` block (lines 9 to 11).

So the bug is worse than the intent says: the text after the alert is lost into a code block
too. With the rewritten fence lengthened by hand to `:::::{note}`, the same text renders
correctly: one note (lines 1 to 11) holding the grid with both cards, then `<p>After.</p>`.

## 3. Change

In `src/core/render/mystGithubAlerts.ts`, `expandGithubAlertsWithLines`, outside a colon
container (the `:::` branch):

- Scan the alert's body lines (`index + 1` to `end`, unquoted with `stripQuote`) for colon fence
  runs (the `COLON_OPEN` and `COLON_CLOSE` shapes) and take the longest length.
- The admonition's fence is one colon longer than that longest run, and at least three colons.
  With no colon fence in the body it stays `:::`: the common case does not change, byte for byte.
- The opening and closing lines use the same fence. The backtick branch (alert inside a colon
  container) does not change.
- `sourceLines` and `alertLines` keep their current shape: the number of output lines does not
  change, only the length of two of them.

## 4. Tests (written first, failing on `main`)

In `test/core/render/alertInsideColonContainer.test.ts` (or a sibling file in
`test/core/render/`), marked `@tests_req SwRS-MDOKFSTUDIO-GFM-009`:

1. The source of section 2 with `> [!NOTE]`, and again with `> **Note**`: the HTML has exactly
   one `aside` (the note); both card titles A and B and both bodies are inside it; `After.` is a
   `p` outside it; no `pre` is rendered.
2. In the same render, the `data-line` / `data-end-line` of the blocks map to the document: note
   1 to 9, grid 2 to 9, card A 3 to 5, card B 6 to 8, paragraphs `Alpha` 4 and `Beta` 7,
   `After.` 11. This is the "click on a card maps to its line" check at render level.
3. A plain alert with no colon fence in its body still expands to a `:::{note}` (a check on
   `expandGithubAlertsWithLines(...).text`).

The existing alert tests stay green unchanged.

## 5. Requirement

SwRS-MDOKFSTUDIO-GFM-009, scenario "Alerts inside a colon container" (or a new boundary scenario
next to it): add the row "an alert whose body holds a colon container (a `::::{grid}` of
`:::{card}`) | the admonition's colon fence is longer than every colon fence of its body; the
whole container stays inside the admonition and the text after the alert stays outside", and add
the case to the verification criteria and method. Then `just requirements-update` and a dated
entry in `requirements/tiers/log.md`.

## 6. Writing skill

No rendered syntax is added or removed, so `skills/writing-for-markdown-okf-schema-studio/` needs
no change, unless it states that grids cannot go inside alerts; the implementer checks with a
grep and removes such a line if found.

## 7. Out of scope

- A colon container inside an alert that is itself inside a colon container (the backtick
  branch). Not reported, not probed.
- The block editor and palette (`blockQuoteRange.ts`, PALETTE-115): they work on the source
  alert, which this change does not touch.

## 8. Done when

The tests of section 4 pass, the SwRS is updated, and `just preflight` passes.
