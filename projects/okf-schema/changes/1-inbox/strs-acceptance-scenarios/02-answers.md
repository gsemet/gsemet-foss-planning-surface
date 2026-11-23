# Answers

Short name: `acceptance-paths`

1. acceptance-paths-Q1: **Activation.** A new value of `strs_test_coverage_mode` (e.g. `linked-swrs-and-acceptance-paths`); without it, `scenarios:` and `@accepts_req` are accepted but nothing is required or counted.
2. acceptance-paths-Q2: **Bench of a test.** No bench configuration: the marker tells the bench. `@accepts_req` is a real-bench test, `@tests_req` is a simulated-bench test; the two may be different tests.
3. acceptance-paths-Q3: **Counters.** A fraction of paths per counter (e.g. tested 2/3, accepted 1/3); a StRS is "tested" (boolean) when the fraction is complete.
4. acceptance-paths-Q4: **Direct `@tests_req StRS-X`.** In the new mode, ignored for coverage and reported as a warning.
5. acceptance-paths-Q5: **Lint severity.** Error for an unknown `#S<n>` fragment; warning for a live StRS with no declared path.
6. acceptance-paths-Q6: **"Tested" path.** `@tests_req StRS-X#S<n>` (same syntax as `@accepts_req`) counts the path as tested (simulated bench); without a fragment it is the Q4 case (ignored, warning).
8. acceptance-paths-Q8: **Migration command.** None. No migration subcommand: okfreq gives a clear error message that tells agents how to declare `scenarios:` themselves.
9. acceptance-paths-Q9: **Approved StRS.** When declaring `scenarios:` on approved StRS, edit the frontmatter only (body intact) and log it in `requirements/tiers/log.md`; the Studio owner agreement already covers a metadata-only change.
10. acceptance-paths-Q10: **Split.** One CR, one batch.
7. acceptance-paths-Q7: **Fragment on a SwRS.** Counted: a SwRS with declared transitions is covered only when every transition has a test (`@tests_req SwRS-X#S<n>`). Scope and the no-fragment interaction are settled in Q11.
11. acceptance-paths-Q11: **Scope of the transitions rule.** New mode only, for StRS and SwRS alike. A test without fragment covers all the declared paths/transitions; once `scenarios:` are declared in the frontmatter, they are mandatory (each must be covered). Possible conflict with Q4 (direct `@tests_req StRS-X` ignored) to settle in Q14.
12. acceptance-paths-Q12: **Report.** JSON and Markdown, schema version incremented. Per StRS: `paths: {total, tested, accepted}` and the two booleans; per SwRS: tested and missing transitions; Markdown shows the two counters as columns.
13. acceptance-paths-Q13: **Agent error message.** Detailed: names the StRS, quotes the `### Main paths` / `### Scenario` headings found, gives the `scenarios:` block to paste, and the doc link.
14. acceptance-paths-Q14: **Marker without fragment.** If `scenarios:` are declared in the frontmatter of a StRS or SwRS, the `@accepts_req` / `@tests_req` markers targeting it must carry the fragment (`#S<n>`). This refines Q11 (a test without fragment covering everything applies only when no `scenarios:` are declared) and replaces the Q4 handling for a StRS that declares paths.
15. acceptance-paths-Q15: **Marker without fragment severity.** Error: `okfreq validate` fails and asks for `#S<n>`; the marker does not count.
16. acceptance-paths-Q16: **Surfaces.** All six surfaces of AGENTS.md (docs/source, skills/, scaffold data, own requirements with `requirements/tiers/log.md`, examples/, tests/CI) plus `docs/source/explanation/project-feature-coverage.md`.
17. acceptance-paths: **Grilled enough.** Yes (2026-11-23). Destination: next batch (3-ready).
18. acceptance-paths-Q18: **Covered StRS.** In the new mode a StRS is covered by the linked-SwRS rule plus "accepted" (all its paths accepted).
19. acceptance-paths-Q19: **StRS or SwRS with no declared scenarios (0/0).** It depends on the `scenarios:` frontmatter, the same for StRS and SwRS: if declared, `@accepts_req` and `@tests_req` without a fragment are errors; if not declared, they count (`@accepts_req` as accepted, `@tests_req` as tested). User's words: "ca depend de la presence du frontmatter scenarios dans le StRS (et c'est pareil en SwRS). S'il est défini, @accepts_req et @tests_req sans fragment est en erreur. S'il n'est pas defini, alors ils comptent comme accepted". This replaces Q4 and the 0/0 "neither" proposal; the W003 warning for a live StRS with no declared path stays (Q5).
20. acceptance-paths-Q20: **`@accepts_req` on a SwRS.** Error, "le faire dans le JSONSchema" (the rule is expressed in a JSON Schema; which one, and how a marker reaches a schema, to be settled by the spec).
21. acceptance-paths-Q21: **Own requirements.** Yes: the okf-schema repository applies the rule itself (its mode switches to the new one and its StRS/SwRS declare `scenarios:`); this widens the CR.
22. acceptance-paths-Q22: **The 18 other open questions.** The user asked for the list first ("liste moi ces questions").
18. acceptance-paths-Q18: **Covered StRS.** In the new mode a StRS is covered by the linked-SwRS rule plus "accepted".
19. acceptance-paths-Q19: **StRS or SwRS without `scenarios:`.** It depends on the frontmatter, for StRS and SwRS alike: if `scenarios:` is declared, a marker (`@accepts_req` or `@tests_req`) without fragment is an error; if it is not declared, the fragmentless markers count (`@accepts_req` as accepted, `@tests_req` as tested). This replaces Q4 (no W004 warning) and the "0/0" question.
20. acceptance-paths-Q20: **`@accepts_req` on a SwRS.** Error, and enforce it in the JSON Schema ("le faire dans le JSONSchema").
21. acceptance-paths-Q21: **Own requirements.** Yes: okf-schema's own repository applies the rule (switches to the new mode and declares `scenarios:` on its StRS/SwRS).
22. acceptance-paths-Q22: **Remaining open questions.** The user asks to see the list of the 18 other open questions before deciding.
18. acceptance-paths-Q18: **Covered StRS.** In the new mode a StRS is covered by the linked-SwRS rule plus "accepted".
19. acceptance-paths-Q19: **StRS with no declared path.** Depends on the presence of `scenarios:` in the frontmatter, for StRS and SwRS alike. Declared: `@accepts_req` / `@tests_req` without fragment is an error. Not declared: they count (`@accepts_req` as accepted, `@tests_req` as tested). This replaces the Q4 warning (W004) and the "neither tested nor accepted at 0/0" proposal.
20. acceptance-paths-Q20: **`@accepts_req` on a SwRS.** Error; "do it in the JSON Schema" (to be clarified: a marker is not frontmatter, see the next series).
21. acceptance-paths-Q21: **Own requirements of okf-schema.** Yes: the repository applies the rule to itself (declares `scenarios:` on its own StRS/SwRS and switches its mode), which enlarges the CR.
22. acceptance-paths-Q22: **Other open questions.** The user asks to see the list of the 18 remaining open questions before deciding.
23. acceptance-paths-Q23: **The 18 open questions.** Go through all of them, in series (the list in the spec's "Open questions", minus 2, 8, 9, 21 already settled by Q18–Q21).
24. acceptance-paths-Q24: **Mode name.** `linked-swrs-and-acceptance-paths`.
25. acceptance-paths-Q25: **Outside the new mode.** Silent for a malformed `scenarios:` or an unknown fragment, apart from what the bundle's own JSON Schema refuses.
26. acceptance-paths-Q26: **Ids never reused.** A guideline in the documentation only; okfreq checks nothing.
27. acceptance-paths-Q27: **Keyword.** `markers.accepts`, configurable, written by `okfreq init`.
28. acceptance-paths-Q28: **Fragment syntax.** `#` glued to the ID; only `S<n>` is a scenario fragment; anything else is ignored as today (user chose B: "# collé à l'ID, le reste ignoré"). Reading: an unknown `S<n>` (e.g. `#S9` on a target that does not declare S9) stays an error (Q5); a non-`S<n>` suffix is not a fragment. To confirm in the spec.
29. acceptance-paths-Q29: **JSON keys.** `accepted`, `scenario_markers` (in `trace --json`), `transitions` (on a SwRS record).
30. acceptance-paths-Q30: **`tested_in_files`.** For a SwRS that declares transitions, it lists only the files with a marker that counts.
31. acceptance-paths-Q31: **Finding codes.** `W003` only (live StRS with no declared path); errors carry no code. No `W004`: with Q19 a fragmentless `@tests_req StRS-X` counts when nothing is declared.
32. acceptance-paths-Q32: **W003 doc link.** The stable URL `https://okf-schema.readthedocs.io/en/stable/reference/okfreq-frontmatter.html#okfreq-declared-scenarios`.
33. acceptance-paths-Q33: **Heading reading for W003.** Every heading under `### Main paths` up to the next `###` (or the generated links block), plus `### Scenario…` headings; the title is the text after `Path <n>:` / `Scenario:`, else the whole heading.
34. acceptance-paths-Q34: **Live StRS for W003.** Every lifecycle except `deprecated` and `superseded` (`draft` included).
35. acceptance-paths-Q35: **SwRS with `### Scenario` headings, no `scenarios:`.** No warning, and no distinction between StRS and SwRS on this point. Instead the CR migrates correctly the okf-schema project, its examples and its documentation (user: "dans la procedure de migration que tu vas faire tu vas t'arranger dans le projet okf-schema, et dans les exemple et la doc, de tout migrer correctement"). Widens the CR together with Q21.
36. acceptance-paths-Q36: **Approval for a `scenarios:`-only edit.** The project's owner decides; without a new approval, `approved_by`/`approved_at` stay and the log names the agreement.
37. acceptance-paths-Q37: **Report version.** `format_version` 2 in every mode.
39. acceptance-paths-Q39: **Report details.** Path totals in the aggregate and one Markdown summary line, plus a "missing transitions" column in the SwRS table.
40. acceptance-paths-Q40: **Version and changelog.** `0.18.0`, `feat(okfreq): …`, not a breaking change.
41. acceptance-paths-Q41: **`okfreq new`.** Yes: it pre-fills `scenarios:` from the headings of the template (the SwRS template's `### Scenario:` headings); how it applies to the StRS template to be settled in the spec.
38. acceptance-paths-Q38: **StRS test-file fields.** Superseded by Q42.
42. acceptance-paths-Q42: **Test files in the report.** A new per-StRS field `acceptance_tests` lists the `@accepts_req` files (real bench). `validation_tests` stays for backward compatibility. The files of the `@tests_req` path markers (simulated bench) need another name, not `validation_tests` (Q43). User: "acceptances_tests (backward compatibilite avec validation_tests), et il faut trouver un autre nom pour les tests de @tests_req".
43. acceptance-paths-Q43: **Name for the `@tests_req` files field.** `simulated_tests` (per StRS, beside `acceptance_tests`, in the new mode).
44. acceptance-paths-Q44: **Verb of the simulated-bench marker on a StRS.** `@simulates_req` (new marker, configurable as `markers.simulates`, written by `okfreq init`), paired with `@accepts_req` (real bench). `@tests_req` stays the marker of SwRS tests. Replaces the use of `@tests_req StRS-X#S<n>` in Q6.
45. acceptance-paths-Q45: **`@tests_req StRS-X` with the new verb.** Accepted outside the new mode (unchanged behaviour); an error in the new mode, whose message names `@simulates_req`. This replaces Q19 and Q14 for `@tests_req` on a StRS; `@tests_req` on a SwRS is unchanged. Consequence: the okf-schema repository's own `@tests_req StRS-OKFSCHEMA-…` markers (6 in `tests/`) and the Studio's migrate to `@simulates_req` by script.
