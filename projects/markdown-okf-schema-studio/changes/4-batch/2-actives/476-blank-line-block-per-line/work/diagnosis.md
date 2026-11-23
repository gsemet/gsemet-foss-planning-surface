# CR-476 diagnosis: CI job `visual` red at e1882e8

Reproduction (worktree batch-09-CR-476, same failures as CI, run ci-45220240477):

    npm run visual:render
    uv run --no-sync --group docs python test/visual/capture.py --group layout-width --group block-editing

Reproduced: the six `first-gap-empty-edit-dark-*` scenarios (v39, v40, v41, v54, v59, v62) and
`block-editing/v54-blank-lines-six-light-900`. (`block-editing/v04-paragraph-editor-open-dark-900` failed once
locally only, "caret is not at the clicked word": not in the CI log, flaky, unrelated.)

There are two separate causes. Neither is a layout regression; both are scenario/fixture expectations that the
CR's new rules made stale.

## 1. first-gap-empty-edit-dark-*: the fixture `20-empty-document.md` is now one blank line, and it shows a block

- `test/visual/fixtures/20-empty-document.md` is 1 byte: `\n` (od -c).
- The CR's `shownBlankLines` (src/core/mapping/blankRuns.ts, rule 2/3 of the spec: "a file of only blank lines:
  every line shows, a single one included") now lists run `1-1` for that text. The rendered page carries
  `data-okf-blank-runs="1-1"`, so edit mode draws one blank-line block (about 25 px) above the Start writing button.
  Before the CR a single blank line was never a run, so nothing was drawn.
- The check `check_first_element_gap` (test/visual/capture_comment_checks.py:789, mode "empty") measures the Start
  writing button against 40 px: 65.0 px now.
- Proof (probe `work/debugger/probe_empty_gap.py`, same rendered page, dark, 900 px, edit mode on):
  - marker `1-1` (fixture `\n`): button top 64.97 px, 1 blank-line block
  - marker `""` (what a 0-byte file gives): button top 40 px, 0 blank-line block
- Light `empty-start` / `empty-open` scenarios still pass only because they check ">= 20 px", not 40 px.
- The behaviour is the spec's intent (03-change-spec.md lines 109, 132-135, 383: "a file of only blank lines: every
  line shows"), so the product must not change. A truly empty document is a 0-byte file, which is what these
  scenarios mean ("Edit mode on with an empty file").

Fix: make the fixture a real empty file.

- `test/visual/fixtures/20-empty-document.md`: truncate to 0 bytes (remove the single `\n`; keep the file tracked).
  Used only by the `20-empty-document` scenarios (scenarioAssertions.ts:665, scenarioDefinitions1.ts:1261,1274,1287
  and the `empty-start` hint ones); all want a document with no body. Check that `visual:render` accepts an empty
  file (the probe above only simulates it by emptying the marker): if the renderer or the harness rejects a 0-byte
  fixture, fall back to the alternative below.
- Alternative (if a 0-byte fixture is not accepted): keep the `\n` fixture and make the "empty" gap check expect
  the block, that is in `test/visual/capture_comment_checks.py` (mode "empty", line ~789) measure the first
  `.sphinx-preview-blank-lines` (or the Start writing button less the blank blocks' height). Less good: it tests a
  different thing than the scenario's title.
- Also add a visual scenario or keep a unit test for "a document of one blank line shows one block above Start
  writing" (the unit test `an empty body with only blank lines shows its blank-line block before Start writing`
  in test/page/runtimeBlankLines.test.ts:378 already covers the page; the CR may add a fixture-based scenario if the
  spec's section on scenarios asks for it, it does not).

## 2. block-editing/v54-blank-lines-six-light-900: the new check compares with the wrong width

- Check added by the CR in `check_six_blank_lines` (test/visual/capture_blank_lines_block.py:120):
  `abs(box["width"] - state["content"]["width"]) > 4`, where `state["content"]` is `#sphinx-myst-preview-content`.
- That element is the whole pane (900 px) with 72 px padding each side; the text column is 756 px.
  Probe `work/debugger/probe_six.py`: content 900, paragraph 756, six blocks 756 each, padding 72/72. The six blocks
  are all at the right width and stacked; only the reference is wrong. The sibling check (line 83) already
  tolerates this: `abs(w - first_paragraph_width) > 4 and abs(w - content_width) > 4`.

Fix, in `test/visual/capture_blank_lines_block.py`, `check_six_blank_lines`: compare with the paragraph column like
line 83 does:

    first = state["paragraphs"][0]
    ...
    if abs(box["width"] - first["width"]) > 4 and abs(box["width"] - state["content"]["width"]) > 4:
        failures.append(Failure(name, f"blank-line block: one block is {box['width']:.0f} px wide, not the content column"))

(`state["paragraphs"]` holds the one `Text.` paragraph of `96-blank-lines-six.md`.) Update the docstring "as wide as
the content column" only if wanted; it stays true of the text column.

## After the fix

Re-run the command above: expect both groups green except possibly the unrelated flaky v04. Then `just ci-visual`.
No `src/` change, no visual baseline file involved (the harness has no stored baselines; only the checks failed).
