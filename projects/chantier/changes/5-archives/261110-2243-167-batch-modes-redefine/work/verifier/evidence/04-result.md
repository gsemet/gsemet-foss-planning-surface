# CR-167 verification at f010012

Scratch repos under the session scratchpad (not batch-09). Transcripts: run1..run5.txt here.

- open --parallel: exit 2, unrecognized argument (run1).
- default open: mode parallel; `take stack` refused (batch is not a stack) (run1).
- series A,B,C: status shows B waits for A queued, C waits for B; take B refused while A queued/working;
  after A ship + handback ready, take B shows base chantier/batch-01/cr-101-...; after `order merged A`,
  B's base is origin/main (run1, run2, run3).
- open --mode series with a CR before its dependency: exit 2 "CR-101 depends on CR-102: it cannot come before it in the series"; right order accepted (run4).
- order mode --note stack on series: accepted, batch becomes stack, take C accepted (run3); on parallel or stack: exit 2 (run5); --note parallel and no note on series: exit 2 (run3).
- docs/batch-modes.svg rendered with headless Chrome: batch-modes.png; layout clean, three lanes, legend, no overlap seen.
- docs/batch-modes-texts.md: all 89 SVG text strings found in it.

Not checked: the real Driver flow (worktrees were made by hand), scenario/CI (given as passing).
