# Alert lazy continuation lines: rendered outside the alert, and the palette edits the earlier alert

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-GFM-037 (to change), SwRS-MDOKFSTUDIO-PALETTE-115 · Area Rendering, inline editing (alerts) · Side preview · QA210-04 · Replay `scenarios/c3-1-alert-lazy-continuation-outside.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![Alert: lazy line rendered outside the box](evidence/currently.jpg) | ![Same input: the plain blockquote keeps the lazy line inside](evidence/expected.jpg) |
| *Currently: the lazy line `lazy continuation line of the note.` renders below the Note box (replay `c3-1` on b9118506).* | *Expected: the lazy line sits inside the alert, as the plain blockquote below it (same input, same preview) already does.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author wraps an alert's text without a leading `>` on the second line. CommonMark treats that as
a lazy continuation and GitHub renders it inside the alert; the plain blockquote right below it in
the same preview does too. Here the alert box stops after the first line, the lazy line appears as
a normal paragraph below it and the alert's block editor leaves it out, so the preview misrepresents
the document and the line cannot be edited with its alert. The palette shows a second symptom of
the same root (found by CR 180): the line is seen as outside the alert, so inserting an Alert on it
and picking WARNING rewrites the head of the earlier alert. GFM-037 says "Alerts end at the first unquoted line" with exactly this case as a scenario, so the render symptom was a Decision. The owner agreed on 2026-10-31 to follow CommonMark, so it is a Bug against CommonMark once GFM-037 changes. The palette symptom is a plain bug either way: PALETTE-115 lets a type pick replace the type word of the alert at the caret only.

## Steps to reproduce

Render symptom (reproduced in a real window):

1. Fixture `synth/admon.md`:

   ```markdown
   > [!NOTE]
   > Line one of a note.
   lazy continuation line of the note.
   ```

2. Open the file, open the side preview, switch edit mode on. Look at the alert, then click
   "Line one of a note.": the editor covers "Lines 5-6" only.

Palette symptom (second symptom, from CR 180, seen in a unit run, not yet in a real window):

1. Document `> [!TIP]\n> first\nSecond`.
2. Insert an Alert from the palette on `Second`, then pick WARNING.
3. Result: `> [!WARNING]\n> first\n> [!NOTE]\n> Second`; the earlier alert's head changed.

## Impact

The preview misrepresents the document. The palette symptom changes an alert the author did not
touch. No data loss on the render symptom (a type or text edit leaves the lazy line, one-line diff).

## Where it comes from

`src/core/render/mystGithubAlerts.ts` (alert block range and body split) ignores lazy continuation
lines; the palette's `insertAlert` in `src/page/.../editPalette.ts` then sees `Second` as outside
the alert.

## Suggested direction

Follow CommonMark: the lazy line stays inside the alert, as in a plain blockquote. Take the alert's end line from the blockquote token map rather than the last `>` line, so the render, the block editor and the palette use the same range. Before changing anything, the fix CR checks GitHub's real rendering and cites the CommonMark / GFM spec example for lazy continuation. Done when: the lazy line renders inside the alert and is part of its block editor; the palette never changes the head of an earlier alert; replay `c3-1` passes.

Uncheck to disagree: [x]

## Requirement to write or change

Change GFM-037 to CommonMark lazy continuation (owner agreed 2026-10-31). If GFM-037 is approved, the fix CR sets `approved_by` / `approved_on` to the owner when it changes it. PALETTE-115 is fixed in the same CR.

Uncheck to disagree: [x]

## Test to add

Add a render test (`> [!NOTE]\n> a\nb` gives one alert whose body contains `b`) and a unit test on the palette input above (the earlier alert's head is never changed). Both earn a test: the first pins the changed requirement, the second guards an edit to an alert the author did not touch.

Uncheck to disagree: [x]

Sources: sheet [c3-1](../../../210-qa-campaign-2026-10-31/work/03-admonitions/c3-1-alert-lazy-continuation.md),
replay [c3-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c3-1-alert-lazy-continuation-outside.json),
[campaign index](../../../210-qa-campaign-2026-10-31/work/00-index.md).
