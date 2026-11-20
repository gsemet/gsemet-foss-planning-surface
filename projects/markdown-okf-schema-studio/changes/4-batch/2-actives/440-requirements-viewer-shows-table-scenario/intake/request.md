# Requirements viewer shows table scenarios, not empty columns

Owner, 2026-11-20, on https://gsemet.github.io/markdown-okf-schema-studio/requirements/block-editing/SwRS-MDOKFSTUDIO-BLOCK-130/ : "les scenario sont vide" (screenshot: each scenario card shows empty GIVEN / WHEN / THEN columns).

Cause seen by the Chief of Staff: SwRS-MDOKFSTUDIO-BLOCK-130 writes its scenarios as a table (`| Input | Outcome |`), not as GIVEN / WHEN / THEN lines. The viewer (`test/site/requirementsViewer/model.ts`, `parseScenarios`) reads only GIVEN / WHEN / THEN / AND lines, so a table scenario shows three empty columns. 343 SwRS files in `requirements/tiers/swrs` use such tables: every one of them has empty scenario cards on the site.

Wanted: the viewer shows a table scenario as its table (Input | Outcome rows), and a scenario with both forms shows both. A unit test with a table scenario; the fixture gets one.
