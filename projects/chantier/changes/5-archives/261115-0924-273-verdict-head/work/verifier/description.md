# Description pass, CR-273

Head: 6af61f5dfda0a8e20aea72146f6c364299dbc565

Failed claims:
1. Test plan says "`test_verdict_note.py`, 6 cases"; the file has 5 parametrized CASES (no file, no Head line, short sha, another commit, full/indented/backticks). Fix to 5.
2. Internal references renders a literal backtick-n: "- CR-273 verdict-head`n- Scratch-batch transcript..." - two bullets are on one line (a PowerShell escape leaked into the posted body). Fix the line break.

Other checks (layout order, details block, blank lines, no internal refs outside last section, refusal table vs delivery.py, Changes vs diff stat) pass.
