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

Critic, 2026-11-26: 6 findings; 3 applied as fixes (the lower CR's scenario, report and sample names;
the "how we test" page and header order with CR-507; the place directly above CR-517
`perf-547-comment-update-and-author`, so that the maximums are measured after the whole fix, as
answer 4's "after the fix" says: still to be written in the specification), 3 asked (the lower CR's
manual job, what `just preflight` runs, the site page as its own CR).

Notes on the specification's open questions (Chief of Staff):
- Open question 1: settled by the lower CR's final specification, CR-516
  `perf-547-slow-comment-selection`.
- Open question 3: left as the specification says; answer 4 asks for a red heavy job that blocks a
  release, and nothing more.
- Open question 4: answered in chat on 2026-11-26 (no "ISO 28149" found; likely ISO/IEC/IEEE
  29148:2018, with ISO/IEC 25010:2023 and ISO/IEC 25023:2016 for time behaviour). No mention was
  asked for; the specification claims no conformance.

7. perf-kpi-Q6 (2026-11-26), "CR-516 adds a manual CI job and a local command for its measure; the KPI
   campaign adds its own `perf` job and commands; what becomes of CR-516's?", choices "A. replace them
   (recommended)", "B. keep both". Answer, verbatim: "A. Les remplacer (reco.)" (one entry only; a
   one-off measure then needs a full heavy run).

8. perf-kpi-Q7 (2026-11-26), "on Linux or macOS, what does `just preflight` do when a time passes a
   maximum calibrated for the CI machine?", choices "A. compare (recommended)", "B. fail locally too".
   Answer, verbatim: "A. Comparer (reco.)" (locally it shows the differences without failing; the
   maximums block in CI only).

9. perf-kpi-Q8 (2026-11-26), "is the scores page on GitHub Pages a CR of its own, above the KPI job,
   in batch-09?", choices "A. two CRs (recommended)", "B. one CR". Answer, verbatim: "A. Deux CR
   (reco.)" (job, maximums and requirement first, mergeable without waiting for the page).

10. perf-kpi-Q9 (2026-11-26), "the local comparison command would run on Linux/macOS only, as the
    real-window tests do not run on Windows, your machine; what do you want?", choices "A. Windows
    later (recommended)", "B. Windows in batch-09", "C. Linux/macOS is enough". Answer, verbatim:
    "B. Windows dès batch-09" (as offered: clearly larger work, not specified yet; delays the end of
    the batch).

Chief of Staff's reading of answer 10: the local comparison command (`just perf-kpi`) also runs on
Windows, in this CR. The question was about that command only; the other real-window stages stay on
Linux and macOS. Found on main 5f0746d, to be confirmed by the specification: the real-window tests
inject mouse and keyboard through Playwright over the window's debugging port
(`test/integration/run-tests.ts`), not through the system's pointer; what skips Windows today is in the
`justfile` (`preflight`, the `ci-*` targets) and `CONTRIBUTING.md`, "Windows".

Answer 9 splits this CR: the site page is `perf-kpi-pages`, stacked above this one. This CR ends at the
report files (`kpi.json`, `kpi.md`), the job, the maximums and their requirement.

Spec critic: second pass after the next specification (answer 10 changes behaviour).

Critic, second pass, 2026-11-26: 3 findings; 2 applied as fixes (the perf launches overwrite the
integration stage's report: settled by keeping that report intact, no decision of the owner's at
stake; the unproved Windows claims marked as unproved), 1 asked (the Windows support as a CR of its
own).

11. perf-kpi-Q10 (2026-11-26), "the Windows support of the comparison command has to be tried on your
    own machine (a VS Code window, session unlocked); is it a CR of its own, above the KPI job, still
    in batch-09?", choices "A. separate CR (recommended)", "B. one CR". Answer, verbatim: "B. Une
    seule CR" (as offered: one cycle less, but the KPI job and the page above it wait for the Windows
    try).

12. The owner's instruction for the night (2026-11-27, Chief of Staff session), verbatim: "ok je te
    laisse finaliser la nuit. mode stack. plus de question, je suis off. tu peux faire jusqu a 6 retry
    part tache. fini par une pipeline long uniquement sur le dernier commit."

    Applied by the Chief of Staff: round limit 6; no question to the owner; one heavy CI run only, at
    the last commit of the final stack. So the specification's "first heavy CI run of this branch"
    is replaced: `maximumMs` comes from the medians of three targeted `perf_547` dispatches on the CI
    runner, on a head that holds CR-516 and CR-517, made before this CR removes that job (same
    scenario, same samples), same rule (about twice the median, rounded up to the next 10 ms), run ids
    written where the specification asks. The two job timeouts come from those runs' duration times
    three launches, with room. The final heavy run is the "second run": `perf` green, both ratios at
    most 1; if it is red or the job is near its timeout, fix at cause and run again at the new last
    commit.

13. livraison-Q1 (2026-11-27, Chief of Staff session), "deliver the performance fix (CR-516, CR-517)
    now, without waiting for CR-518 and CR-519?", answer, verbatim: "A. Livrer maintenant (reco.)".
    CR-516 and CR-517 get their own heavy CI and are merged first; item 12 stays for this CR: no heavy
    run at its head, the next heavy run is the one at CR-519's head.

14. fin-batch-Q1 (2026-11-27, Chief of Staff session), "how do I finish batch-09: stop at the fix,
    keep CR-518 and CR-519 with lighter rounds, or change nothing?", answered later in the same
    session, verbatim: "Mais fini tout les 3 autres." Read by the Chief of Staff: CR-517, this CR and
    CR-519 stay in batch-09 and are finished. No lighter rule was chosen: the rigor is unchanged.

15. local-Q1 (2026-11-27, Chief of Staff session), "lighten the local tests for CR-518 and CR-519?",
    choices "A. yes (recommended)" (no visual tests on the owner's PC, left to CI; `just check` once
    per round, not re-run by the reviewer; targeted tests during the work), "B. no". Answer,
    verbatim: "Oui découpe la CI maintenant juste après celle que tu fini il faut pouvoir aller vite."

    Applied by the Chief of Staff: A for this CR (replaces the last sentence of item 14). The CR
    `split-heavy-ci-jobs` comes after CR-517 and before this one, which then adapts its job to the
    split workflow.

16. The owner's instruction (2026-11-27, Chief of Staff session), verbatim: "Fait ce qu'il faut pour
    merger ce qui reste rapidement et on clos le batch vite. On fera les teste visuels lourd dans un
    second batch". Which CRs leave batch-09 is being confirmed (close-Q1).

17. The owner's instruction (2026-11-27, Chief of Staff session), verbatim: "Il faut rebase. Après en
    P1 tu mets une CR sur un plan d'optimisation des check locau et CI. Parallisarion, test lourd que
    après merge ou optionnellelenr sur les PR". `split-heavy-ci-jobs` left batch-09 for the backlog P1
    (replaces its place in item 15). This CR stays held until close-Q1 is answered.

18. close-Q1 (2026-11-27, Chief of Staff session), "do I take CR-518 and CR-519 out of batch-09?",
    choices "A. yes, to the next batch (recommended)", "B. no, finish them in batch-09". Answer,
    verbatim: "Les 2 dernière je ferais plus tard sur les tests de perf en pages, met en P1". Applied:
    this CR leaves batch-09 for the backlog P1.

Destination: backlog P1 (item 18; replaces the running batch).
