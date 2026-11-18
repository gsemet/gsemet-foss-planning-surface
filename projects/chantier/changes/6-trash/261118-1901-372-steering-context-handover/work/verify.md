# Verify CR-372 (second verification)

Head: 3a9afc2c1cac56e56a5fadccc77d7e43c92352c7

No worktree, PR or commit (handover-Q3). All claims judged at 3a9afc2. Claims 1-5 of the first pass (record figures, experiments 02-10 rerun, no transcript text, chantier repo untouched, seven parts) are carried from the first pass at the same head 3a9afc2: only the study text and experiments/11 changed in round 2, and no 02-10 script or CSV was touched.

## Failed claims of the first pass, judged again

A. Part 7 and Part 4 ranges vs the CSV: PASS. Command: python min/max of `saving_usd` by kind over `09-replay-by-kind.csv` -> foreman -449.78 0.0, direct -46.45 0.0. The study (lines 238-241, 392-393) now says -449.78 to 0.00 (Foreman) and -46.45 to 0.00 (direct), names the cell of each bound, and says the Part 4 table is a selection whose largest loss is -236.26. Spot checks of table cells against the CSV (foreman wakes 60 -44.11/-32.12/-23.14/-9.60; wakes 100 no-leftover -13.71/-11.12/-10.37/0.00; direct ctx 250k -16.81/-9.58; no-driver 250k 30 min -50.42 and -9.14; no-driver wakes 100 -11.05) all match.
B. Driver 130,000 comparison in Part 4: PASS. A "The Driver's own threshold" paragraph, table and reading follow the Part 4 bullets. Table figures equal `11-replay-130k.csv` and `11-replay-130k-no-driver.csv` (foreman -3247.32/-365.37/-85.77/-15.60, 848/109/28/5; direct -283.64/-39.05/-13.55/-1.90; no-driver -1914.87/-240.30/-63.03/-11.66 and -235.97/-33.80/-12.24/-1.90). Part 7 quotes -15.60 to -3,247.32 and -1.90 to -283.64: matches.
C. Part 1 record compactions: PASS. New column "Compactions (record)": 11,6,2,2,3,2,6,1,1,1 for batch-17,18,19,21,22,23,24,25,26,27. Command: grep "compactions since" in batch-NN.md -> 11,6,2,2,3,2,6,1,1,1. Match; the transcript column is kept with both sources named.
D. Chief outside-budget as a second row: PASS. A "Chief, outside the budget" row follows each Foreman batch (17, 18, 23, 24, 25, 26, 27): $59.25, 49.39, 8.45, 30.21, 2.74, 5.20, 6.95 and calls. Command: grep "steering the batch (outside the budget)" in the records -> same values (1054, 760, 192, 486, 55, 94, 134 calls).

## New checks

E. Script 11 reruns to its quoted figures: PASS. Command: copy of experiments/ to a scratch folder, `python 11-driver-threshold-replay.py` and with `--no-driver-cost`, then `diff -q` of 11-replay-130k.csv, 11-replay-130k-no-driver.csv, 09-replay-by-kind.csv, 09-replay-by-kind-no-driver.csv against the CR's files -> all identical. Scratch removed. The command is at the script's top.
F. No transcript text in experiments/: PASS. The new files are 11-replay-130k*.csv (kind, delay, counts, dollars) and a script that loads 09; no message text.
G. Chantier repo untouched: carried from the first pass (same head; nothing in the repo changed).

VERIFIED
