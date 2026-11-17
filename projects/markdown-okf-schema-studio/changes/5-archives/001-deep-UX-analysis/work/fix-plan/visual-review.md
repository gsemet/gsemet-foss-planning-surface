# Agent visual review protocol (QA-03 step 2)

This protocol is used by T40. Reviewers in other tasks may use it too, for the screenshots of their
task. A human only looks at failures.

## Input per screenshot

- The PNG file.
- Its note (`.txt` in the visual campaign, `.md` in real-input campaigns). The note contains:
  - the expected content;
  - the "stakeholder visual checks";
  - the "Machine checks" section (T03).

## Reviewer instructions (copy into the subagent prompt)

You review UI screenshots of a VS Code Markdown preview extension. For each PNG in your batch:

1. Open the image with the Read tool, then read its note.
2. Turn the note's expected content and visual checks into yes/no assertions. Always add these
   generic assertions:
   - **G1** no floating control (toolbar, menu, tooltip) covers text that belongs to another
     element;
   - **G2** no control or tooltip is clipped by the edge of the view;
   - **G3** short identifiers in tables are not split across lines;
   - **G4** text is readable against its background in the captured theme;
   - **G5** the element named by the scenario is visible;
   - **G6** status pages show the title and the message on separate lines.
3. Judge each assertion from the image. If the machine checks in the note disagree with what you
   see, say so explicitly.
4. Output one JSON object per screenshot:

   ```json
   { "image": "<path>", "scenario": "<id>", "assertions": [
     { "id": "G1", "text": "…", "pass": true, "why": "one line" } ],
     "overall": "pass" }
   ```

   `overall` is `"pass"` or `"fail"`. It is `"fail"` if any assertion fails.

Write the array to `PLAN/visual-review/batch-<N>.json`. Do not modify any other file.

## Merge

The orchestrator concatenates the batches into `review.json` and writes `SUMMARY.md`: counts, then
each failing image with its failing assertions and the image path. Failures that point to a
regression of an approved fix block T40. Others go to `followups.md`.
