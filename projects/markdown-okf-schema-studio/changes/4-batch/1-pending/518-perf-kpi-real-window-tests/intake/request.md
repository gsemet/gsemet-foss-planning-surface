# Real-window performance KPI scores with budgets, shown on Pages

Real-window performance tests that give KPI scores on complex rendering use cases, published on
GitHub Pages, with requirements setting the limits to meet. Filed on 2026-11-26 from the Chief of
Staff session of batch-09, on the owner's message.

The owner, verbatim: "Sur ce bug de performance je pense que ce sera l'occasion de faire des tests de
performance en fenêtre réelles pour sortir des scores de PKI sur des use cases de rendu complexes. A
afficher dans le GitHub pages. Et on peut se mettre des requirements de score max à atteindre. Ça se
fait en iso 28149?"

Reading of the message ("PKI" taken as KPI):

- performance tests in a real VS Code window, on complex rendering use cases;
- a KPI score per use case;
- the scores shown on the project's GitHub Pages site;
- requirements that set the maximum each score must meet;
- the question of the standard to follow ("iso 28149").

The performance bug meant: https://github.com/gsemet/markdown-okf-schema-studio/issues/547 (text
selection and comment creation very slow on a large document with many tables and SVGs). Its
reproduction was in progress at filing; the bug has no CR yet.

What the project has at 5f0746d:

- `test/probe/previewProbe.ts` (`npm run probe`, headless Chromium, stub host, large generated
  chapter of `test/probe/largeChapter.ts`): with `--check` it fails on a scroll frame 95th percentile
  over 4 ms, a page reload while typing, a diagram redrawn or another block rebuilt by typing, a lost
  inline editor. No justfile target or workflow names it.
- `test/integration/performanceProbe.ts` (real window,
  `STUDIO_REAL_INPUT_SCENARIO=probe`): typing, scroll frames (normal and four times slower CPU),
  inline editor survival; writes `out/reports/probe/window-probe.json`; sets no limit; not part of the
  integration job.
- Neither measures text selection or comment creation, the paths of the issue.
- The requirements bundle holds no performance requirement (no match for performance, latency,
  response time or non-functional); some functional SwRS carry timeouts.
- The Pages site is built by `.github/workflows/pages.yml` from the reports of a green heavy run
  (`just site-assemble`); it shows no performance figure.
- Earlier performance study: `2-backlog/P4/deep-analysis-review/experiments/` 04, 05 and 06.

Standards, from public pages and excerpts only (the texts are sold; none was read whole):

- No source found for an "ISO 28149" matching this subject; the likely meaning is ISO/IEC/IEEE
  29148:2018 (requirements engineering, StRS and SwRS), which has clauses for performance
  requirements and verification. https://cdn.standards.iteh.ai/samples/72089/62bb2ea1ef8b4f33a80d984f826267c1/ISO-IEC-IEEE-29148-2018.pdf
- ISO/IEC 25010:2023 names the quality characteristic "performance efficiency" (time behaviour,
  resource utilization, capacity).
  https://standards.iteh.ai/catalog/standards/iso/8c5bd63e-9e67-4b55-90e3-8cb2b10a2030/iso-iec-25010-2023
- ISO/IEC 25023:2016 gives measures for it, among them mean response time and response time adequacy
  (measured time against a target).
  https://cdn.standards.iteh.ai/samples/35747/34b91bc957f647ce8bbb2093907d7bc0/ISO-IEC-25023-2016.pdf

To settle at the grill, none decided:

- the use cases and their documents; the KPIs and the definition of a score;
- the limits, and whether missing one fails CI, a release, or only shows on the site;
- the machine that measures (hosted runners vary from run to run: repetitions, a calibration, counts
  instead of times);
- how the limits are written in the requirements bundle;
- history of the scores across releases or only the latest;
- whether the fix of the issue is a CR of its own, before or after the measures.
