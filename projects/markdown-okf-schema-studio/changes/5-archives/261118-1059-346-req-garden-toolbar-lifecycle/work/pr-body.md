## Summary

Gardens the requirements of the toolbar-navigation and lifecycle-sync scopes so that a reviewer can understand each use case from its stakeholder requirement (StRS), and each software requirement (SwRS) is one observable behaviour traced by implementation and test markers. No product behaviour changes.

## Deliverables

- Overlapping SwRS are merged with `okfreq supersede` (nothing is deleted): for example the Back/Next history refusals into one requirement, the find and replace options into one, the depth setting into the sticky band requirement, and the scroll sync rows split by setting.
- Every StRS of the two scopes has one `### Use case diagram` (Mermaid), written by the rule of the project guidelines; a new StRS, "Closing a preview or a folder leaves nothing behind", is split out of the reload StRS, which is narrowed to reload and view choices.
- Requirement markers now sit on the function or CSS rule that does the behaviour, not on file headers, `install*` functions or whole CSS aggregates. The page chrome and layout CSS are split into named constants; the joined preview stylesheet is byte-identical before and after (checked with a scratch script, no test added).
- 21 new tests cover lifecycle scenarios that no test checked; each was seen to fail once on purpose (assertion inverted in the compiled output). StRS validation markers sit on real tests (settings contract, heading fold check, find in preview, export HTML, workspace disposal).
- 8 new unit tests and 3 new visual checks (4 behaviours) cover the toolbar scenarios that no test checked, each seen to fail once on purpose:
  - every toolbar button's tooltip equals its title (16 buttons), the keyboard-focus tooltip, and the 12/14 px offsets with the toolbar covering scrolled text;
  - the Back/Next render gate (another render refused, the current render followed);
  - the second-root relative link, the malformed-escape link;
  - the Anchor pairing's initial state and own document;
  - "Scroll to the end" stays at the end;
  - the browser find opens a folded section.

Before and after, for the two scopes:

| | Before | After |
| --- | --- | --- |
| In-force toolbar-navigation SwRS | 50 | 34 |
| In-force lifecycle-sync SwRS | 34 | 30 |
| In-force StRS | 16 | 17 (one new closing StRS) |
| Use case diagrams | 0 | one per StRS |

## Blast radius

Grade: 1 (1 = low: local, easy to revert; 2 = medium; 3 = high: wide or hard to revert).

Requirement text, markers, comments, tests and one byte-identical CSS constant split. Roll back by reverting the commits.

## Autonomous decisions

- The scenario "Handle strip at the top of the page" moved to `SwRS-MDOKFSTUDIO-TABLE-007` (table-editing scope, outside the two scopes); the sibling table-editing change should rebase on it.
- Where a scenario cannot be tested at a reasonable cost, its SwRS verification note says so in one line.
- A "Known issue" is written in `SwRS-MDOKFSTUDIO-LIFE-125` (a non-boolean `descriptionsCollapsed` is dropped from the session state); no code fix is made here.

## Known gaps

- The browser find of SwRS-MDOKFSTUDIO-TOOLBAR-006 is checked through a text-fragment navigation, which runs Chromium's own find over the folded section; the Ctrl+F bar itself cannot be driven by Playwright. The SwRS note says so.
- No test for the watched-editor came-back branch, for the single restored panel and for the settings at integration level; noted in their SwRS.
- No validation marker on StRS-MDOKFSTUDIO-TOOLBAR-001: no reload step asserts a collapsed toolbar.
- The marker-gate baseline still lists the page chrome and layout CSS files and the real-input companion lines, which hold IDs of other scopes.
- The 17 Mermaid diagrams were parsed in node (a scratch Mermaid checker): the 10 sequence diagrams parse; 7 diagrams (the LIFE-001 flowchart and the state diagrams LIFE-007, -014, -022, TOOLBAR-001, -002, -006) could not be parsed there ("DOMPurify.addHook is not a function", no DOM), so they are not proved to parse; none was rendered.

<details>
<summary>Details</summary>

## Changes

- `requirements/`: supersedes, text fixes, StRS reparenting, new StRS, diagrams, log entry, regenerated indexes.
- `src/`, `test/`: marker moves, CSS constant split, moved tests, new tests.

## Human decisions

- Published requirements are never deleted; merges use supersede.
- Draft requirements that are implemented go to `proposed` (the draft StRS TOOLBAR-002 and -003 and their draft SwRS).
- No StRS touched was approved, so no re-approval commit is needed (checked at the start).
- A Main path may cite a SwRS the StRS lists in `depends_on`.

## Impacts

No visual change.

## Test plan

- [x] New or changed tests: 29 new unit tests (host, session, protocol, page, worker, settings, toolbar) and 3 new visual checks (`test/visual/capture_toolbar_checks.py`), each inverted once on purpose and seen to fail.
- [x] Local gates at 09385ce: `just check`, `just unit`, `just requirements-lint`, the toolbar-navigation visual group, `just preflight`.
- [x] Evidence: none (no visual change); CSS byte-identical comparison by scratch script.
- [x] Verified at 09385ce.
- [x] CI green at 09385ce.
- [x] Changelog: No user-facing change.

## Internal references

- CR-346, batch-06; archive not in the PR.

</details>
