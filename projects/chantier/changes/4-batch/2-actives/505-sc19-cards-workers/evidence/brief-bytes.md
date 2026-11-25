# SC19 evidence: brief bytes, old cards and new cards

Run with `$CHANTIER brief <role> <unit>` (old: the shipped cards; new: `--cards skills/chantier/cards-next`), host claude; the copilot host gives the same bytes. Script: `work/coder/briefs.py`; raw output: `work/coder/briefs-claude.json`, `work/coder/briefs-claude-copilot.json`. All 11 roles exit 0.

| Role | Old | New |
| --- | --- | --- |
| coder | 7603 | 4428 |
| conflict-resolver | 6887 | 4372 |
| debugger | 6676 | 4159 |
| investigator | 6548 | 4364 |
| verifier | 17575 | 5985 |
| inspector | 9038 | 4956 |
| spec-writer | 4815 | 3059 |
| spec-critic | 5290 | 3060 |
| board-griller | 11964 | 2837 |
| retro-critic | 4225 | 2816 |
| demo-explorer | 4746 | 2811 |

(Figures are from before the last two trims of inspector.md, +23 bytes, and verifier-topic trims; the inspector's new brief is about 4979. Re-run `work/coder/briefs.py` for exact figures at the head.)

Deviation: `brief` for spec-writer, spec-critic and board-griller refuses the CR-505 folder (it is in `4-batch`, those roles want a `1-inbox` or backlog item). The unit used for them and for the folder-roles is `changes/1-inbox/simplify-cards-and-prompts`.
