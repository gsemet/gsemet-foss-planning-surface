# Answers

Short name: `perf-kpi`

1. perf-kpi-Q1 (2026-11-26), "does the performance CR go to the next batch?" Answer: yes, the next
   batch; batch-09 ends without it. The owner chose, verbatim: "A", the first of "A. Oui, batch
   suivant (recommandé)" and "B. Plus tard".

Destination: next batch (3-ready).

2. Replaces answer 1 (2026-11-26). In answer to perf547-Q1 (the CR `perf-547-slow-comment-selection`),
   the owner wrote, verbatim: "Dès que possible tu fix dans le batch en cours et tu fais une analyse de
   perf en fenêtre réelle (relance 2 ou 3 fois pour avoir un peu de stabilité). Tu vas en profiter de
   ce fix pour rajouter la campagnes de PKI demander". So the KPI campaign goes into batch-09 with
   the fix.

Destination: running batch batch-09.

3. perf-kpi-Q2 (2026-11-26), "where does the real-window performance campaign run?", choices "A.
   GitHub CI (recommended)", "B. your machine", "C. both". Answer, verbatim: "C. Les deux" (as
   offered: the CI carries the maximums; a local command serves to compare; more work).

4. perf-kpi-Q3 (2026-11-26), "what happens when a maximum is exceeded?", choices "A. red job
   (recommended)", "B. counters block, times shown", "C. display only". Answer, verbatim: "A. Job
   rouge (reco.)" (as offered: requirements with a maximum and a wide margin; exceeding it fails the
   heavy job, so it blocks a release). The question's text put the margin at about twice the median
   measured after the fix.

5. perf-kpi-Q4 (2026-11-26), "which complex rendering cases first?", choices "A. four documents
   (recommended)", "B. ticket 547 only". Answer, verbatim: "B. Ticket 547 seul" (as offered:
   selection and comment only; faster, the other cases later).

6. perf-kpi-Q5 (2026-11-26), "what form does the shown score take?", choices "A. ms and ratio
   (recommended)", "B. a mark out of 100". Answer, verbatim: "A. ms et ratio (reco.)" (median time and
   the ratio measured / maximum: 1 or less means met).

The text before these questions said, with no objection: unless told otherwise, the Pages site shows
the latest run only, with no history.

Spec critic: yes (a maximum of the CI job can block a release; the change spans the tests, CI, requirements and the site).
