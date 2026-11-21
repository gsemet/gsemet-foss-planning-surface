Short name: `running-lane`

# Answers
1. running-lane-Q1 (2026-11-21): **What a drop on "running batch" does.** A. The board writes only the mark (`work/running-batch`, through factory-redefine's mark function); the Chief of Staff, woken by the watcher, adds the CR when its specification is final. The board still never edits a batch.
2. running-lane-Q2 (2026-11-21): **A CR whose specification is already final.** A. It joins at the Chief of Staff's next wake (`order add`), with one line to the user ("CR-431 added to batch-30 from the board").
3. running-lane-Q3 (2026-11-21): **A drop with no open batch.** A. The "running batch" half stays visible, greyed, saying "no running batch"; a drop on it places the CR in `3-ready` and says so.
4. running-lane-Q4 (2026-11-21): **What the "running batch" half shows.** A. The marked CRs and those in `1-pending`, each with its state ("waiting for its spec", "waiting for a slot"); running CRs stay on the batch page.
5. running-lane-Q5 (2026-11-21, after the full restatement): **Grilled enough.** A. Yes: the spec-writer, then the critic; destination the next batch (`3-ready`), with factory-redefine, this CR on top of it.
Spec critic: yes, it changes what the user sees and does on the board and the server's published API.
