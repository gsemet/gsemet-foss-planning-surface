Bug on the published requirements site, found by the owner (2026-11-20) on SwRS-MDOKFSTUDIO-BLOCK-130:
every scenario card shows empty GIVEN / WHEN / THEN columns.

Cause: 343 SwRS files write some scenarios as a table (`| Input | Outcome |`); the viewer
(`test/site/requirementsViewer/model.ts`, `parseScenarios`) reads only GIVEN / WHEN / THEN / AND
lines, so a table scenario renders as three empty columns.

Done when: a table scenario shows its rows (Input, Outcome) on the site; a list scenario still shows
GIVEN / WHEN / THEN as today; no scenario card is ever empty when its source has content. Unit tests
cover both forms; the viewer fixture has a table scenario.
