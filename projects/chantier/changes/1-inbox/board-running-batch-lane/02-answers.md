Short name: `running-lane`

# Answers
1. running-lane-Q1 (2026-11-21): **What a drop on "running batch" does.** A. The board writes only the mark (`work/running-batch`, through factory-redefine's mark function); the Chief of Staff, woken by the watcher, adds the CR when its specification is final. The board still never edits a batch.
2. running-lane-Q2 (2026-11-21): **A CR whose specification is already final.** A. It joins at the Chief of Staff's next wake (`order add`), with one line to the user ("CR-431 added to batch-30 from the board").
3. running-lane-Q3 (2026-11-21): **A drop with no open batch.** A. The "running batch" half stays visible, greyed, saying "no running batch"; a drop on it places the CR in `3-ready` and says so.
4. running-lane-Q4 (2026-11-21): **What the "running batch" half shows.** A. The marked CRs and those in `1-pending`, each with its state ("waiting for its spec", "waiting for a slot"); running CRs stay on the batch page.
5. running-lane-Q5 (2026-11-21, after the full restatement): **Grilled enough.** A. Yes: the spec-writer, then the critic; destination the next batch (`3-ready`), with factory-redefine, this CR on top of it.
Spec critic: yes, it changes what the user sees and does on the board and the server's published API.
6. running-lane-Q6 (2026-11-21, the spec's open question 1): **A `3-ready` CR dropped on "running batch".** A. A journal line only; the Chief of Staff runs `order add` at its next wake, and the card moves then.
7. running-lane-Q7 (2026-11-21, the spec's open question 2): **Where a marked CR is drawn.** A. Once, in the "running batch" half only; it leaves its inbox or priority row.
8. running-lane-Q8 (2026-11-21, the spec's open question 3): **A grilled CR whose spec-writer has not started.** A. Keep factory-redefine's refusal, with a clear message on the board ("the grill is not finished").
Spec critic run (2026-11-21), fixes that need no user, for the spec-writer's next run: (5) the top half's sub-line gets its own i18n key ("{batch} · {state}", both languages), and the spec says whether `triage.idle` and `triage.running` are removed; (6) docs/web-board.md:163 ("writes in the backlog only ... never in a batch") is edited to name the mark among the backlog's writes; (7) the scenario's no-open-batch step is required at a named point, or dropped with the in-process test named as the cover. Findings 1 to 4 go to the user.
