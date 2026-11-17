# T03 — Machine checks for screenshots

| Field | Value |
| --- | --- |
| Fixes | [QA-03](../../08-test-campaign-gaps/QA-03-screenshots-are-not-asserted.md) |
| Depends on | T02 |
| Gate | `unit trusted visual` |
| Risk | Low (test tooling; checks are report-only unless a scenario opts in) |
| Commit message | `test(vscode): add geometry checks to screenshot campaigns` |

## Goal

Screenshots today are checked only by a human reading the note. Add cheap DOM geometry checks that
run at every capture, in both campaigns, and print PASS or FAIL in the note:

- the static visual campaign (`test/visual/capture.py`);
- the real-input E2E campaign (T02 harness).

A scenario can make specific checks **required**: a required failing check fails the test. In this
task no existing scenario is made required. Later UI tasks (T15, T18, T19, T23, T26, T35) opt their
scenarios in. The agent-based visual review (QA-03 point 2) is run by T40 using `visual-review.md`
in the plan folder; it is not code.

## Allowed files

- `test/shared/geometry-checks.js` (new, plain JavaScript)
- `test/integration/realInput/harness.ts` (extend `Evidence.capture`)
- `test/visual/capture.py` (call the checks, extend the note, write a summary)
- `test/visual/scenarios.ts` (only the optional `machineChecks?: string[]` field on the scenario type)
- `test/visual/renderFixtures.ts` (only if needed so `machineChecks` reaches the manifest)
- `test/webview/geometryChecks.test.ts` (new)

## `test/shared/geometry-checks.js`

Plain browser JavaScript, no module syntax. It declares exactly one function:

```js
function studioGeometryChecks(options) {
  // options: { overlays?: string[], ignoreWithin?: string[] }
  // returns { checks: [{ id, applicable, pass, detail }] }
}
```

Checks, with these ids:

| id | Applicable when | Pass when |
| --- | --- | --- |
| `overlay-covers-text` | At least one visible element matches an overlay selector. Default overlays: `.sphinx-preview-table-menu`, `.sphinx-preview-frontmatter-menu`, `.sphinx-preview-link-tooltip`, `[role="tooltip"]`. | No client rect of a **text range** inside `#sphinx-myst-preview-content` (text nodes under `td, th, p, li, h1–h6, pre, dd, dt`) intersects an overlay rect by more than 4 px². Ignore text inside the overlay itself and inside `ignoreWithin` selectors. Default `ignoreWithin`: `[data-sphinx-preview-block-editor]`, `[data-okf-frontmatter-editor]`, `[data-sphinx-preview-table-cell-selected]`, `[data-okf-editing]`. `detail` lists up to 5 covered text excerpts (30 chars each). |
| `overlay-clipped` | Same as above. | Every visible overlay rect lies within `[0, innerWidth] × [0, innerHeight]`, with 1 px tolerance. |
| `identifier-split` | The content has a `td`/`th` whose trimmed text matches `^\S{1,24}$`. | For each such cell, a range over its text has client rects on a single line (all rects share the same `top`, ±1 px). `detail` lists up to 5 split identifiers. |
| `status-two-lines` | `[data-sphinx-preview-status]` contains a visible `strong` and a visible `[data-sphinx-preview-status-message]`. | `message.top >= strong.bottom - 1`. |

Do not include the floating preview toolbar in the default overlays. Its overlap with content is
UX-44, which is out of scope.

## Unit tests (`test/webview/geometryChecks.test.ts`)

The file runs in Node, without a browser. Test what can be tested without layout:

- the file evaluates with `vm.runInNewContext` and defines `studioGeometryChecks`;
- with a minimal fake `document` whose `querySelectorAll` returns `[]` for everything, every check
  returns `applicable: false, pass: true`.

## Real-input harness

Extend `Evidence.capture(page, frame, name, note, options?)` with
`options.checks?: { required?: string[]; overlays?: string[]; ignoreWithin?: string[] }`:

- Read the JS file with `fs` from the extension root (`test/shared/geometry-checks.js`). Evaluate it
  in the frame with
  `frame.evaluate("(function(options){" + source + "\nreturn studioGeometryChecks(options);})(" + JSON.stringify(opts) + ")")`.
- Append a `## Machine checks` section to the note: one line per check,
  `PASS`/`FAIL`/`n/a`, `id`, detail.
- If a check listed in `required` fails, throw an `Error` naming the check and its detail **after**
  writing the note and the screenshot.

## Visual campaign (`capture.py`)

- Load `EXTENSION_ROOT / "test" / "shared" / "geometry-checks.js"` once at module level
  (`GEOMETRY_SOURCE`).
- In `check_final_frame`, after the existing `page.evaluate`, run:

  ```python
  page.evaluate("(options) => {" + GEOMETRY_SOURCE + "\nreturn studioGeometryChecks(options);}", {})
  ```

  Store the result's `checks` in `result["machineChecks"]`.
- For each check whose `id` is in `scenario.get("machineChecks", [])` and that is applicable and
  failing, append `Failure(scenario["page"], f"machine check {id}: {detail}")`. No scenario sets the
  field in this task, so nothing new fails.
- In `sidecar_text`, add a `Machine checks` section listing every check:
  `PASS`/`FAIL`/`n/a`, id, detail.
- After the campaign, write `test/visual/screenshots/MACHINE-CHECKS.md`: a table of scenario id ×
  failing applicable checks, with "required" or "report-only" for each. Link it from `INDEX.md` with
  one line under the run status.
- In `scenarios.ts`, add `machineChecks?: string[]` to the scenario type. Check that the manifest
  written by `renderFixtures.ts` carries the field to Python. If scenarios are serialized whole, no
  change is needed.

## Steps

1. Write the JS file and the unit test.
2. Wire it into the harness. Re-run the `trusted` gate: the T02 notes must now contain machine-check
   sections.
3. Wire it into `capture.py` and run the `visual` gate.
4. In the report, list the report-only failures that appear in `MACHINE-CHECKS.md`. They are the
   known baseline for the UI tasks. Do not fix them here.

## Expected changes to existing tests

- No existing scenario becomes required.
- **Added after the T00 review (follow-up).** One stale visual check, in `test/visual/capture.py`:
  the `visibleHeaders` value (in the page script, around line 425) reads each visible `thead th`
  with `cell.textContent`, which now includes the description toggle glyphs (`Value◀▶`). The
  intended labels are unchanged (`Name`, `Value`). Change only that `.map(...)` so it ignores
  buttons:

  ```js
  .map((cell) => {
    const copy = cell.cloneNode(true);
    copy.querySelectorAll('button').forEach((button) => button.remove());
    return copy.textContent?.trim() || '';
  }),
  ```

  Do not change the comparison with `["Name", "Value"]`. Expected effect on the visual gate: the
  baseline line `narrow schema headers are ['Name', 'Value◀▶'], expected Name/Value` is reported
  as "now passing"; no new failure line appears.

## Must not change

- Product code under `src/`.
- Existing visual assertions and scenario contents, apart from the new optional field.

## Done when

- The `unit`, `trusted` and `visual` gates pass.
- Every visual note and every real-input note has a "Machine checks" section.
- `MACHINE-CHECKS.md` exists and is linked from the visual `INDEX.md`.
