# Garden the Studio requirements: coherent StRS for a human reviewer, fully traced SwRS

Owner's request (2026-11-17), Chief of Staff session.

## Goal

A human reviewer understands Studio by reading its StRS, and each StRS can be trusted down to the code:

1. Complete: every main use case of Studio has its StRS, no duplicate, no gap.
2. Readable: each StRS reads on its own at the right length, with a diagram (sequence or actors) that renders on the GitHub Pages requirements viewer (`test/site/requirementsViewer/`, which today renders only `user_need` and the "Main paths" map, not the StRS body).
3. Well split: each SwRS is one observable behaviour, neither too fine nor redundant.
4. Honestly traced: every `@implements_req` marker sits next to the code that does the behaviour, every `@tests_req` test checks the SwRS scenarios, and every exception is written with its reason.

Method: the okfreq-gardening skill (`.agents/skills/okfreq-gardening/SKILL.md`): read-only audit first, owner decisions, then changes in small CRs.

## Baseline (okfreq 0.17.0, main dedbdb2a)

- 1124 requirement files; in force: 80 StRS (16 approved, 62 proposed, 2 draft) and 475 SwRS (465 proposed, 10 draft); 569 retired (51+457 superseded, 2+59 deprecated).
- SwRS markers: 467/468 coverage targets with code markers (missing: SwRS-MDOKFSTUDIO-DIAG-128), 468/468 with test markers.
- StRS validation tests (`linked-swrs-and-validation-test`): 26 covered, counted over 133 StRS including retired ones.
- 0 diagrams in StRS; 78/80 active StRS have a "Main paths" section.

## Owner decisions so far

- Delete all deprecated requirements. Open: does this mean `deprecated` only (61) or also `superseded` (508)? It conflicts with `requirements/guidelines/requirements.guidelines.md` (published requirements are retired with `okfreq archive`/`supersede`, never deleted; `okfreq retire` is for unpublished drafts and records `retired_ids`), so the project guideline needs an explicit exception, and the viewer's "retired" notes and the SwRS `supersedes` links go with them.
- Add the relevant missing StRS, each fully traced (linked SwRS with code and test markers, and a direct validation test).
- The assessment runs through sub-agents.
