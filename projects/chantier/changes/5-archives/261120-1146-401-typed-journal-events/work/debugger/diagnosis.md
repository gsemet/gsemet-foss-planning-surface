# Diagnosis: surface-board (github) "external_surface ran to the end"

Reproduction: scenario unit surface-board (see scenario/README.md), or read
scenario/results/scenario-20261120-115104-33260.md lines 1182-1196:
`KeyError: 'kind'` at scenario/run_scenario.py line 8908, in surface_config_page.

Cause: the CR moved the forge journal to version 2 lines, keyed `type` ("config@1"), no `kind`
(board/config_api.py line ~120 writes `"type": "config@1"`). The CR updated the scenario readers
of the journal at lines 1521, 1639, 1882, 1999, 2021, 2162 but missed this one, which still reads
`e["kind"]` on a line of the board's config save. The preceding checks pass; this one raises, so
the unit stops (11 checks after it never run: 184/195).

Other `["kind"]` hits in run_scenario.py read events.jsonl (batch events), not the forge journal;
no other journal reader remains (lines 8926-9100 have none).

Fix: scenario/run_scenario.py lines 8906-8909: replace `e["kind"]` with `e["type"]` and the expected
tuple `(1, "board", "config", "hosts.claude.roles.coder.model")` with
`(1, "board", "config@1", "hosts.claude.roles.coder.model")`. Also update the check's text
("one `config` line") to "one `config@1` line" if wished.
Then re-run the surface-board unit: later checks of that unit were never reached and may reveal
a further miss (e.g. on journal lines after the limits save).
