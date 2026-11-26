# Answers

Short name: `perf547`

1. perf547-Q1 (2026-11-26), "ticket 547 is reproduced in part (slow comment creation measured, slow
   selection not); where does the fix go?", choices "A. next batch (recommended)", "B. in batch-09",
   "C. later". The owner's free answer, verbatim: "Il y a des recommendations de fix dans le ticket tu
   les as pris en compte? Dès que possible tu fix dans le batch en cours et tu fais une analyse de
   perf en fenêtre réelle (relance 2 ou 3 fois pour avoir un peu de stabilité). Tu vas en profiter de
   ce fix pour rajouter la campagnes de PKI demander"

   So: the fix goes into batch-09 as soon as possible; a performance analysis in a real window is
   part of it, run two or three times for stability; the KPI campaign of `perf-kpi-real-window-tests`
   goes in with it ("PKI" read as KPI).

2. perf547-Q2 (2026-11-26), "may I download the reporter's gist (14 files, about 232 KB) to measure
   the selection on their document?" Answer, verbatim: "A. Oui (reco.)" (isolated folder, its files
   only read and displayed, measured without a window).

The ticket's recommendations, checked on 2026-11-26 against its text (no comment on the ticket): it
has no section proposing fixes; it names three root causes and a gist. Their points: unthrottled
`selectionchange` with the text walk, the whole-document fallback and `getBoundingClientRect`; the
button appended to the body; the two hover listeners during a drag; the `:has()` rules, three on the
content root; the tear-down and re-anchoring of every thread with `scroll.measure()` after a comment.
All were measured or read in the reproduction (see `intake/request.md`).

Destination: running batch batch-09.

Spec critic: yes (a layout rule the user sees changes; the change spans page styles, the comments code, tests and CI).
