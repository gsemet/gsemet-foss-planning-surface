# 06 - Verification, round 1 (head 8e14593)

Checks run by the Verifier in the worktree:

- XML parse of docs/release-driver.svg: OK.
- font-size: values used 14, 16, 16.5, 28; none below 14 (regex search for 0-13 finds nothing).
- `<desc>` vs the texts file's prose paragraph: identical, byte for byte (2900 chars).
- Anonymisation: case-insensitive search of both files for project name, repository, #3xx, 1.6.0/1.6.1, run/commit ids, vsce, marketplace, years, the owner's quoted words, clock times, UTC: no real hit (only "stroke-width 1.6" and the word "changelog" matched loose patterns).
- README: new `## Releases` section after "Detailed lifecycle" and before "What is Chantier?", links docs/release-driver.svg, which exists on the branch. Diff touches only README.md and the two new docs files.
- Renders (headless Chrome, 1760x1350): 06-render-light-page.png (white page), 06-render-dark-page.png (dark page). Read both: six lanes readable, no overlap, four green diamonds (merge, "yes, now", notes review and publish, thread), "owner asked nothing" bracket, dashed fix path (red heavy job -> fix-n.md -> Foreman -> CR driver -> merge -> new attempt), CI bars fanning out, forge outputs, loop arrow archive -> intake, footnote, numbers block. Own background keeps both identical.

Minor, not blocking: the "reviews the notes" diamond's label sits below-left of it and is slightly ambiguous next to the "yes, now" diamond; the time-axis position of the dashed fix path is schematic.
