# SC19 evidence: brief bytes, old cards against cards-next (round 2, final files)

`brief <role> <unit> --batch batch-31` with and without `--cards skills/chantier/cards-next`, LF bytes of the brief file, run by `work/coder/briefs.py` (raw: `work/coder/briefs-final.log`). Claude and Copilot briefs were identical in the earlier run (`briefs-claude-copilot.json`); this run is Claude. Declared boot is study-fable-v2 section 2.2 ("Start, new", Claude), base boot and new boot being the study's own figures.

| Role | Old brief | New brief | Saved | study-fable-v2 declared start (new) |
| --- | --- | --- | --- | --- |
| coder | 7549 | 4357 | 3192 | 13,966 (boot 9,357) |
| conflict-resolver | 6833 | 4318 | 2515 | group "other workers": 11.2 to 12.5 KB start base, +826, boot 8.2 to 8.7 KB |
| debugger | 6622 | 4105 | 2517 | same group figure |
| investigator | 6494 | 4310 | 2184 | same group figure |
| verifier | 17521 | 5936 | 11585 | 23,963 (boot 9,382) |
| inspector | 8984 | 4939 | 4045 | 15,422 (boot 9,378) |
| spec-writer | 4815 | 3054 | 1761 | not found |
| spec-critic | 5290 | 3060 | 2230 | not found |
| board-griller | 11964 | 2965 | 8999 | 19,655 (boot 11,096) |
| retro-critic | 4225 | 2816 | 1409 | not found |
| demo-explorer | 4746 | 2820 | 1926 | same group figure |

Deviation: `brief` refuses a `4-batch` folder for spec-writer, spec-critic and board-griller, so those three used the inbox folder `changes/1-inbox/simplify-cards-and-prompts` as the unit; retro-critic and demo-explorer take no unit.
