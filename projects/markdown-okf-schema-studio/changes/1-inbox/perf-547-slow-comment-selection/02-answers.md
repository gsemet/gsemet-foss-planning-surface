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

Critic, 2026-11-26: 6 findings; 3 applied as fixes (the measure on the reporter's document, the rules
of the new CI job, what "faster" means on hosted runners), 3 asked below.

3. perf547-Q3, "does the fix go as one CR or two?", choices "A. two CRs (recommended): 1) measure,
   `:has()` rules, comment button; 2) changed threads only and the Git author name, stacked above, in
   batch-09", "B. one CR". Answer, verbatim: "A. Deux CR (reco.)". The second CR is
   `perf-547-comment-update-and-author`.

4. perf547-Q4, "what about the three other points of the ticket (the whole-document fallback, the
   hover listeners, the selection copied on each scroll)?", choices "A. fix only those the 'before'
   runs show to cost (recommended)", "B. fix them all", "C. leave them". Answer, verbatim: "B. Tous
   corriger" (as offered: all three are fixed, even with no measured cost).

5. perf547-Q5, "where is the wait for the Git author name measured?", choices "A. in CI
   (recommended): a test folder as a Git repository with a user name; the report says so", "B. local
   only", "C. drop the point". Answer, verbatim: "A. En CI (reco.)". It applies to the second CR.
