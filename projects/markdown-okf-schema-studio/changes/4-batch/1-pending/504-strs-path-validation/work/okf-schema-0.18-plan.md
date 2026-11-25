# Plan against okf-schema 0.18.0 (prepared 2026-11-25 for the grill)

Sources:

- the okf-schema CR merged as PR #63, archived at
  `projects/okf-schema/changes/5-archives/261125-1100-outside-63-strs-acceptance-scenarios`
  (`03-change-spec.md`, rules 1 to 9; `02-answers.md`, Q27 to Q63);
- the Studio's `origin/main` on 2026-11-25.

0.18.0 is not on PyPI yet: PyPI still serves 0.17.0. Read its released documentation before the
spec, especially `explanation/okfreq-acceptance-paths` and `reference/okfreq-frontmatter`
(`#okfreq-declared-scenarios`).

## What changed from this CR's Q13 to Q25

| Point | Studio CR (Q13 to Q25) | Shipped in okfreq 0.18.0 |
|---|---|---|
| Mode | not named | New `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`. The old modes count no new markers. |
| `scenarios:` | One field, `S<n>` ids, on StRS and SwRS | Same: `[{id: S<n>, title}]` in the base schema. `id` matches `S[1-9][0-9]*`, so `S0` is refused. |
| Markers | `@accepts_req StRS-X#S<n>`; the fragment is optional on `@tests_req` | `@tests_req StRS-X#S<n>` makes a path **tested**; `@accepts_req StRS-X#S<n>` makes it **accepted** (`markers.accepts`). |
| Fragment | Optional | **Required** once the target declares `scenarios:`, on both verbs and on SwRS too. A fragmentless marker on such a target is an **error** and does not count. With no `scenarios:`, a fragmentless marker counts for the whole requirement and a fragment is an error. |
| Counters | tested = simulated bench, accepted = real VS Code bench | `tested` and `accepted` are independent counts of markers, not of test results. okfreq has no notion of a bench: its docs talk about execution cost (`@accepts_req` is the costly test closest to the product and runs on the main branch). The bench is the Studio's own convention. |
| StRS `covered` | Validation test plus the SwRS | Linked-SwRS rule **and** (every path accepted, or an acceptance waiver). "Tested" is reported but does not change the status. |
| Waiver | none | `acceptance_exemption: true` with a non-blank `acceptance_exemption_reason`, for the whole StRS. It changes only `covered`, never the counts. |
| Warnings | none | `W003`: a live StRS with no `scenarios:` (it proposes the block from the `Path <n>:` headings). `W004`: a live StRS with no counting `@accepts_req`. Neither changes the exit code. |
| `@accepts_req` on a SwRS | | An error, through the SwRS schema (`accepted_in_files` with `maxItems: 0`). |
| Older bundle schema | | In the new mode, `okfreq validate` **fails** until `swrs.schema.yaml` refuses `accepted_in_files`. The bundle schemas must be updated by hand: `init` never replaces them. |
| Generated fields | | On a StRS: `tested_in_files` and `accepted_in_files`, when they are listed in `generated_fields`. |
| Report | | `format_version` 2. Per StRS: `paths {total, tested, accepted}`, `tested`, `accepted`, `tests`, `acceptance_tests`, and `acceptance_exemption`. `validation_tests` holds the `@accepts_req` files. Aggregate: `paths`. Per SwRS: `transitions`. The Markdown gains Tested and Accepted columns, a "Missing transitions" column, and the line `StRS paths: tested t/n, accepted a/n`. |
| Approved requirements | Scripted migration (metadata only) agreed by the owner (Q24) | Same rule: an edit that only adds `scenarios:` leaves `approved_by`/`approved_at` as they are and is logged in `tiers/log.md`. Renaming a body heading to `Path S<n>:` is a body change, so it needs the owner's approval. |

## Studio numbers (origin/main, 2026-11-25)

- StRS: 15 approved and 80 proposed are live (95). The other 58 are 56 superseded and 2 deprecated.
- Paths: 151 in all, 30 of them on approved StRS. 3 live StRS have no path, among them
  TRUST-012 and TRUST-014.
- One `#### Path 0:` heading, in `StRS-MDOKFSTUDIO-LIFE-023`. `S0` is invalid.
- 185 `@tests_req StRS-…` markers in 62 files: 46 files in `test/integration` (real VS Code),
  8 in `test/visual`, and the rest in core, page, build, security and site.
- SwRS: 1073, every one with `### Scenario` headings. 3962 `@tests_req SwRS-…` markers, none
  with a fragment.
- Schemas: `requirements/tiers/_schema/{base,strs,swrs}.schema.yaml`. None of them has the 0.18
  declarations yet.
- The "scores" and the "HTML report" are the requirements viewer in `test/site/requirementsViewer/`
  (`model.ts`, `home.ts`), built from `out/reports/requirements/requirements-report.json`:
  - The home cards show implemented, tested and fully traceable (SwRS), plus "StRS with a
    stakeholder validation test", which counts `stakeholder_test_coverage.status == covered`.
  - The per-area table shows StRS, SwRS, Implemented and Tested.
  - The okfreq Markdown report `requirements-report.md` changes by itself.

## Proposed work, in order

1. Bump `okf-schema>=0.18.0` in `pyproject.toml` and lock it.
2. Copy into `requirements/tiers/_schema/` the 0.18.0 declarations that `okfreq init` writes into
   a new bundle:
   - in base: `scenarios`, and the `LIFECYCLE_DESCRIPTION` text with the `scenarios:` exception;
   - in strs: `tested_in_files`, `accepted_in_files`, `acceptance_exemption` and its reason, and
     the new top-level description;
   - in swrs: `accepted_in_files` refused.
3. Update `config.yml`: `markers.accepts: '@accepts_req'`, and add `accepted_in_files` to
   `generated_fields`.
4. Run a script that writes `scenarios:` on the 92 live StRS that have paths: `Path n` becomes
   `S<n>`, with the title after the colon. It changes metadata only, and the 15 approved StRS go
   in one `tiers/log.md` entry that names the Q24 agreement.
5. Give TRUST-012, TRUST-014 and the third StRS with no path a path. This is a normative change,
   so the owner reviews it.
6. Sort all 185 markers. Each one ends in exactly one of these states:
   - `@tests_req StRS-X#S<n>`: it walks path n on the simulated bench;
   - `@accepts_req StRS-X#S<n>`: it walks path n in real VS Code;
   - removed: a snapshot or a duplicate of a SwRS test, where its `@tests_req SwRS` marker stays.

   No fragmentless marker may remain, because it would be an error.
7. Write the missing acceptance tests, one `@accepts_req` per path. Today about 1 marker in 4
   would count as "accepted" (audit Q23).
8. Switch `strs_test_coverage_mode` to `linked-swrs-and-acceptance-paths`.
9. Update the viewer: read `format_version` 2, show the path cards and columns, and list on the
   StRS page each path with its tested and accepted test files.
10. Update the docs and skills:
    - CONTRIBUTING (the bench convention);
    - `.agents/skills/okfreq*`;
    - `requirements/guidelines/project.guidelines.md`;
    - the shipped `guidelines/requirements.guidelines.md`, if Studio vendors it.
11. Run `just requirements-update` and add a dated entry to `tiers/log.md`.

## Questions for the grill (series 8)

27. **Mode switch and the drop in the score.** In the new mode, a StRS counts as `covered` only
    when every path is accepted. Today 93 StRS count as "validated"; after the switch only a few
    would. A: switch in this CR and show the honest number. B: switch only once the acceptance
    tests are written. Proposed: A, because the CR writes those tests anyway.
28. **Bench convention.** okfreq no longer has benches. Proposed:
    - in the Studio, `@tests_req StRS-X#S<n>` means a path walked on the simulated bench, run on
      every PR;
    - `@accepts_req StRS-X#S<n>` means a path walked in real VS Code (`test/integration`), run on
      every push to `main`;
    - this is written in CONTRIBUTING and in the okfreq skill.
29. **Required fragment.** As soon as a StRS declares its paths, each of its fragmentless
    `@tests_req StRS` markers is an error. So the sort covers all 185 markers, not a sample, and
    none stays fragmentless. Confirm.
30. **SwRS scenarios.** Declaring `scenarios:` on the 1073 SwRS would make their 3962
    fragmentless markers errors. Proposed: no SwRS `scenarios:` in this CR, and a separate CR
    later if wanted.
31. **Path headings.** okfreq reads `Path S<n>:` headings, but renaming them changes the body of
    the 15 approved StRS. Proposed: keep `Path <n>:` and map `Path n` to `S<n>`. For LIFE-023,
    `Path 0` takes the next free id. Rename the headings later, if at all.
32. **Acceptance waiver.** The waiver covers a whole StRS. Proposed: no waiver when a path only
    contains a human step, such as CORE-007 path 1, where the maintainer reviews the release
    notes; its acceptance test stops before that step. The waiver is only for a StRS with no
    step that can be automated, and the spec lists the candidates.
33. **Viewer (scores and HTML report).** Proposed:
    - the home cards "StRS paths tested t/151", "accepted a/151" and "StRS covered c/95"
      replace "StRS with a stakeholder validation test";
    - the area table gains the columns "Paths tested" and "Paths accepted";
    - the StRS page lists each path with its test files, plus a waiver badge if any;
    - the SwRS cards do not change.
34. **Cutting it up.** Q-scope chose one CR for all 151 paths. The 0.18 design ties together the
    migration, the sort and the switch. Proposed:
    - CR A: steps 1 to 6 and 8 to 11 (bump, schemas, `scenarios:`, sort of the 185, mode switch,
      viewer, docs);
    - one CR per area (16 scopes) for the missing acceptance tests, in step 7.

    Or keep a single CR.
35. **Counts are markers, not results.** okfreq counts markers, not passing tests (Q19 said
    "passes"). The proof that a test passes is the CI job of its bench. Confirm that the score
    stays marker-based.
