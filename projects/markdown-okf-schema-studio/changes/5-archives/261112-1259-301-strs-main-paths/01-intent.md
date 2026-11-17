# Every use case (StRS) states its main paths

Decided by the owner on 2026-11-12, as the first of two changes; the second is the requirements
viewer (`P2/requirements-viewer`), which draws these paths as a metro map. This change comes first.

A StRS describes a whole use case (A, then B, then C gives D). Testing every way through it end to
end is too combinatorial; its SwRS are the options at each state, each tested on its own. A
`### Main paths` section in each StRS names one or two paths through the use case, step by step,
each step backed by the SwRS that moves the user from one state to the next, with the SwRS of the
other outcomes at that state.

Expected:

- The format of `../requirements-viewer/main-paths/FORMAT.md`, documented in
  `requirements/guidelines/project.guidelines.md` (and the okfreq skill if it lists StRS sections).
- Main paths written for every active StRS where possible (80 today, 16 areas). An agent drafts
  them from each StRS and its SwRS; it keeps only steps backed by an existing SwRS of that StRS and
  never invents behaviour. Sample: `../requirements-viewer/main-paths/StRS-MDOKFSTUDIO-DIAG-001.md`.
- A StRS whose SwRS do not form a path gets no section and is listed in the report, with the
  reason (for example a gap: a state with no SwRS to leave it).
- A check (okfreq lint or a project script, to decide at the grill) that every SwRS id of a Main
  paths section exists, is active and derives from that StRS.
- `just requirements-update` and a dated entry in `requirements/tiers/log.md`.

Review: the diff touches about 80 StRS files; ship it one area per commit inside the one PR, or
split it by area if the grill prefers several PRs.
