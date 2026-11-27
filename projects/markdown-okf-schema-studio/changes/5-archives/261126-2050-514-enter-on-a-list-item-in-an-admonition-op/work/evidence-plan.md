# Evidence plan (written by the Driver; no investigator)

Kind of change: preview editing behaviour (which element Enter and a click open inside an
admonition or alert, the move chord and the edge keys of its block editors, the placeholder of an
emptied alert block), requirements, tests, user guide, one re-filmed feature clip.

| Claim | Before (base) | After (PR head) | Technique |
| --- | --- | --- | --- |
| Click on a body paragraph or item opens that block; title or frame opens the whole | whole admonition opens | pointed block opens | new unit, page and visual tests; before/after screenshots from the visual harness (dark), admonition and alert |
| Enter on an element reached with the arrows opens it alone | whole admonition opens | that element opens | page tests, visual keyboard scenario |
| Move chord in a body block editor moves it among the admonition's blocks; refused move shows its reason | nothing or whole admonition | inner move | page tests, core planner tests |
| Down/Up at the edge of a list in an admonition keeps the caret | next top-level block opens | editor stays | page test |
| An erased alert paragraph or item leaves `>` | empty line, alert cut | alert whole | core and session tests |
| The new tests fail on the base | | | run the new test files against the base's `src/` (detached worktree of the base), failing assertion names quoted |
| Keyboard navigation clip | stops at the first item, Enter opens the whole admonition | down to "the VSIX", opens alone | `check.json`, contact sheet, GIF in the PR body |
| Gates | | | `just check`, `just clip-kit-test`, `just requirements-lint`, `just preflight` (static on Windows), CI at the head |

Host and default matrix: none (no host or setting dependency, specification "Evidence").

Cannot be shown: motion and rhythm of the clip as watched (the maintainer's to judge); a macOS take.
