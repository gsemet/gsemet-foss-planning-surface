# Answers

Short name: `strs-validation`

## Series 1, 2026-11-23 (owner, through the Griller)

1. strs-validation-Q1: **V&V wording.** A, acceptance. Owner's words: "Ok pour acceptance, comment tu nommerais le marqueur ?" An automated end-to-end test of a StRS path is an acceptance test (verification at the StRS level), not a validation by the user. The marker's name is asked in series 2.
2. strs-validation-Q2: **Steps no test can do.** Not settled; the owner challenges the premise: "si on maîtrise les entrants et les assertions, je ne vois pas quel comportement humain ne peut pas être simulé. « Lire les notes de versions », comme on sait ce que l'on a donné en entrée on peut imaginer des asserts pour simuler les vérifs de l'homme non ?" Follow-up in series 2.
3. strs-validation-Q3: **Anti-duplicate rule.** A: one nominal path per test, run end to end in one go, the final result asserted (plus the steps no SwRS covers), never edge cases or errors.
4. strs-validation-Q4: **Status.** Two scores per StRS, in the owner's words: "« tested » (SwRS liées), et « accepted » (les chemins)". Exact definitions confirmed in series 2.

## Series 2, 2026-11-23

5. strs-validation-Q5: **Marker name.** `@accepts_req`. The path fragment is not settled, owner's words: "Par contre je ne suis pas sûr pour le #path, c'est comme les tests_req quand il y a plusieurs transitions". Follow-up in series 3.
6. strs-validation-Q6: **Human steps.** A: the human act is a simulated input (e.g. "release notes approved"); the test asserts the system's gate (blocked without it, proceeds with it) and the checkable content, never a judgment. A method other than Test is a rare exception, written in the path. (Settles Q2.)
7. strs-validation-Q7: **The 185 existing `@tests_req StRS-...` markers.** A: a read-only audit first, each marker classified (walks a path, single-state snapshot, duplicate of a SwRS test); only those that walk a path move to `@accepts_req`, the others lose their StRS marker.
8. strs-validation-Q8: **Scope.** B: all 151 paths (owner's choice over the recommended pilot). Delivery shape asked in series 3.

## Series 3, 2026-11-23

9. strs-validation-Q9: **Path fragment.** B: no fragment; the marker is `@accepts_req StRS-X`, as `@tests_req` names a SwRS. Consequence for Q4 asked in series 4.
10. strs-validation-Q10: **Delivery.** B: one CR for everything (owner's choice over the recommended split).
11. strs-validation-Q11: **Bench.** Not settled; owner's words: "les StRS sont validés (« accepts_req ») par le vrai banc et donc ça coûte bcp plus cher à exécuter, mais est « testé » par le banc virtuel. Ça permet de faire les 2." Clarified in series 4.
12. strs-validation-Q12: **StRS without "Main paths".** Not settled; the owner asks why they exist, gap or impossibility. Griller's finding, 2026-11-23: of 152 StRS, 58 are retired (56 superseded, 2 deprecated) and have no paths by design; 94 are live (80 proposed, 14 approved), 92 of them with "Main paths" (151 paths); 2 live StRS have none: StRS-MDOKFSTUDIO-TRUST-012 (visible text and the icon speak of the product) and StRS-MDOKFSTUDIO-TRUST-014 (built from pinned dependencies, ships what it loads). 93 live StRS already carry a direct `@tests_req StRS-...`: today almost every live StRS counts as "validated". Follow-up in series 4.

## Series 4, 2026-11-23

13. strs-validation-Q13: **What "accepted" measures.** Back to a path fragment (reverses Q9), owner's words: "Ok on revient sur le fragment mais alors il faudra un frontmatter pour déclarer les paths, et il faudra faire pareil avec les scénarios dans les SwRS. Il y a une grosse migration des req existants à faire". So: `@accepts_req StRS-X#<path>`, paths declared in the StRS frontmatter, the same for SwRS scenarios, and a migration of the existing requirements. Shape asked in series 5.
14. strs-validation-Q14: **Benches.** C (over the recommended A): a path that passes on the simulated bench is "tested", a path that passes on the real VS Code bench is "accepted". Reconciliation with Q4 ("tested" = linked SwRS) asked in series 5.
15. strs-validation-Q15: **TRUST-012 and TRUST-014** (the two live StRS with no path). A: each gets a short path that starts from the built deliverable (the VSIX); rule with no exception: every live StRS has at least one path.
16. strs-validation-Q16: **Destination of the idea.** A: read-only audit first (step one of the CR), then the project CR, then the okf-schema feature request (forge-neutral), backed by the CR's real figures.

Griller's findings, 2026-11-23: live SwRS = 443 (of 1051), with 2549 `### Scenario` headings (3907 in all); headings vary ("Scenario: Nominal", "Scenario (boundary): ...", "Scenario: Restricted Mode"). okfreq comes from the `okf-schema>=0.17.0` package (pyproject `requirements` group), not from this repository; its config knows two markers (`implements`, `tests`), and the frontmatter schema (`requirements/tiers/_schema/base.schema.yaml`) has `additionalProperties: false` in places. 14 live StRS are `approved` (approval_lock): changing them needs the owner's recorded agreement.

## Series 5, 2026-11-23

17. strs-validation-Q17: **Frontmatter shape.** Not settled; owner's words: "Il faudrait trouver une formulation qui soit utilisable pour les StRS sur les paths et les SwRS sur les scénarios". One shared declaration for StRS paths and SwRS scenarios; proposal in series 6.
18. strs-validation-Q18: **SwRS scenarios.** A: declared in the same migration (scripted from the headings); the fragment on `@tests_req` stays optional: `@tests_req SwRS-X` with no fragment still covers the whole SwRS.
19. strs-validation-Q19: **Counters.** B, two counters (the option's wording was unclear: its meaning is confirmed in series 6).
20. strs-validation-Q20: **Order.** B: the okf-schema feature request first; the project CR waits for okfreq to support the marker and the declarations (reverses the order of Q16 for the CR; the audit's place is confirmed in series 6).

## Series 6, 2026-11-23

21. strs-validation-Q21: **One declaration.** B: one frontmatter field `scenarios:` for both tiers (StRS paths and SwRS scenarios), each with a stable short id (e.g. `S1`, never reused), no `kind`: the tier says what it is (StRS = path, SwRS = transition scenario). Fragment `#S<n>` on both markers. (Supersedes the field shape of Q13/Q17.)
22. strs-validation-Q22: **The two counters** (Q19 restated). A: per StRS, "tested" = its paths have a test on the simulated bench, "accepted" = its paths have a test on the real VS Code bench. SwRS coverage stays okfreq's usual coverage shown on each SwRS, not recounted in the StRS. (Supersedes Q4's "tested = linked SwRS".)
23. strs-validation-Q23: **Audit.** A: a sample audit now, in this Griller session (about 30 markers across every folder, each classified "walks a path / single-state snapshot / SwRS duplicate"), written in `experiments/`; the okf-schema request rests on it; the full sort of the 185 stays in the CR.
24. strs-validation-Q24: **Approved StRS.** A: one agreement, recorded in the CR, for the scripted migration that declares existing paths as `scenarios:` (metadata only); any change to the normative text of an approved StRS goes back to the owner one by one. Owner's agreement for that migration: given 2026-11-23 (this answer).

Griller's sample audit (Q23), 2026-11-23, in `experiments/02-audit-sample.md` (31 of the 185 markers, 1 in 6; two rows checked again by hand): 13 walk a path (4 of them a one-step path, which is the same check as its SwRS), 1 a partial path, 6 single-state snapshots (all visual), 8 duplicate one SwRS transition (6 of them integration tests that stop after step 1), 3 other (TRUST-014 has no path; 2 test a flow that is not one of the StRS's paths). By bench: 8 of the 13 path rows run in real VS Code. Read on the 185: about 4 markers in 10 would move to `@accepts_req`, about 1 in 4 would count as "accepted"; today 93 live StRS count as validated. Simulated paths stub the host step (rows 23, 26).

## Series 7, 2026-11-23

25. strs-validation-Q25: **Where the okf-schema request goes.** A: a CR filed in the inbox of the surface's `okf-schema` project (marker `@accepts_req`, shared frontmatter field `scenarios:` with stable ids, fragment `#S<n>` on both markers, the two counters per StRS by bench), citing this audit; this Studio CR goes to the backlog, blocked by it. Forge-neutral; nothing posted on a tracker.
26. strs-validation-Q26: **Grilled enough.** A: back to the backlog at P2, blocked by `okf-schema/changes/1-inbox/strs-acceptance-scenarios` (filed 2026-11-23); specified once okfreq ships the marker and `scenarios:`. Critique: yes (requirements incl. 14 approved StRS, CI with two benches, a large migration). Not for batch-09.

## Series 8, 2026-11-25 (okf-schema 0.18.0 design, see `work/okf-schema-0.18-plan.md`)

27. strs-validation-Q27: **Mode switch.** A: switch `strs_test_coverage_mode` to `linked-swrs-and-acceptance-paths` in this CR and show the honest number (a StRS is `covered` only when every path is accepted or waived).
28. strs-validation-Q28: **Bench convention** (okfreq 0.18 has none). A: in the Studio, `@tests_req StRS-X#S<n>` = path walked on the simulated bench (every PR); `@accepts_req StRS-X#S<n>` = path walked in real VS Code (`test/integration`, pushes to `main`). Written in CONTRIBUTING and the okfreq skill. (Supersedes Q22's wording.)
29. strs-validation-Q29: **Required fragment.** Follows from 0.18 (fragmentless marker on a target with `scenarios:` is an error): the sort covers all 185 `@tests_req StRS` markers; each ends `@tests_req …#S<n>`, `@accepts_req …#S<n>`, or removed. None stays fragmentless. (Replaces Q23's sample-only scope for the CR.)
30. strs-validation-Q30: **SwRS scenarios.** B: yes, in this CR, on all SwRS. Every `@tests_req SwRS-X` marker (3962) gets its `#S<n>`, one marker per scenario the test checks. User: a SwRS never declares a scenario that is not tested: for each scenario without a test, write the test, or remove the scenario if it is not really useful.
31. strs-validation-Q31: **Headings.** B: rename the body headings to explicit ids, `#### Path S<n>: <title>` on StRS (LIFE-023's `Path 0` included, renumbered). Owner's agreement given now for this scripted rename on the 15 approved StRS: logged in `tiers/log.md`, `approved_by`/`approved_at` unchanged; any other normative change of an approved StRS still goes to the owner one by one.
32. strs-validation-Q31b: **SwRS headings.** A: same form, `### Scenario S<n>: <title>`, matching the `scenarios:` ids.
33. strs-validation-Q30b: **Pruning an untested SwRS scenario.** A: the coder writes the test by default; it removes a scenario only when another scenario or SwRS already says the same, or it is not observable. Every removal is listed in the PR with its reason and logged in `tiers/log.md`.
34. strs-validation-Q32: **Acceptance waiver.** A: only for a StRS with no automatable step; a path with a human step (CORE-007 path 1) gets an acceptance test that stops before that step. Candidates listed in the spec for the owner.
35. strs-validation-Q33: **Viewer (HTML report and scores).** All four: home cards "StRS paths tested t/151", "accepted a/151", "StRS covered c/95" (replace "StRS with a stakeholder validation test"); area table columns "Paths tested", "Paths accepted"; StRS page: each path with its tested and accepted files, waiver badge; SwRS page: each scenario with its tests and the missing ones, plus a home card for scenarios tested.
36. strs-validation-Q34: **Cutting.** B: one CR for everything (as decided before).
37. strs-validation-Q35: **Counts.** A: marker-based, as okfreq counts; the proof a test passes is its bench's CI job.

Blocked only by the release of okf-schema 0.18.0 on PyPI (PyPI serves 0.17.0 on 2026-11-25; the okf-schema CR is merged as PR #63). Spec-writer reads the released docs first. Critique: yes (scale: 185 StRS markers, 3962 SwRS markers, missing tests, 15 approved StRS).

38. strs-validation-Q36 (2026-11-25, decided by the Chief of Staff, owner's word "no question"; the critic verified okfreq 0.18.1 accepts `scenarios:` and mixed fragments in the OLD mode, which removes the ground of Q34): **Two CRs, not one.** CR-A (this folder, `strs-path-validation`): bump `okf-schema>=0.18.1`, schemas, `scenarios:` declarations (live SwRS only, exempt SwRS get none), heading renames, D5, D6, StRS sort of the markers, SwRS fragments, check-markers (`@accepts_req`, `#S<n>`), viewer, vendored skills and guidelines; the okfreq mode stays the OLD one. CR-B (a new CR filed after CR-A is final, after CR-A in the stack): the missing SwRS scenario tests or prunings, the acceptance tests and their CI job, the D11 gate, and the switch to `linked-swrs-and-acceptance-paths`. Q34 B ("one CR") is kept as one subject delivered in two PRs.
39. strs-validation-Q37 (Chief of Staff): **Acceptance budget (CR-B).** Shared window per e2e group, several launches each with its own budget below the 15 min launch deadline, the job sharded by group in a matrix, the expected step duration stated in the spec, no stress-plan entry required but stated. Not a fresh window per test, no raised timeouts.
40. strs-validation-Q38 (Chief of Staff): **Approved StRS heading rename follows `project.guidelines.md` "Approved requirements":** `approved_at` set to now, the 15 listed in the PR body, the owner's review requested on the PR. The agreement already given covers the scripted rename; the re-approval is the owner's click on the PR.
41. strs-validation-Q39 (Chief of Staff): **Exempt SwRS (TRUST-070, TRUST-075) get no `scenarios:`;** their fragmentless markers stay valid; D11 is not asked to cover them.
42. strs-validation-Q40 (Chief of Staff): **D11 runs `okfreq generate-report --output-json` into `out/` itself, and lands with the switch (CR-B).** Correct the false claims: `report --format json` does not exist; a fragmentless marker on a target with `scenarios:` is not an error in the old mode; `scenario_markers` has one entry per (id, fragment, file), first line only, so the sort and the sweep read files; run `okfreq validate` in the new mode on a scratch config at each commit.
43. strs-validation-Q41 (Chief of Staff): **D9: no simulated walk written for every path (A);** the card shows what the sort finds and says so. **D7: a non-editor product may be accepted outside VS Code for CORE-007, CORE-008, TRUST-014; CORE-006 stays in VS Code (A).**
44. strs-validation-Q42 (Chief of Staff): **Spec corrections the writer applies:** the CI wiring edits (tag-release, pages, report/checks, ci.guidelines rules 11, 13, 14, AGENTS.md CI list, `-attempt-<n>` artifact via a job output) go to CR-B; the `test:acceptance` script includes `npm run bundle` and `ci-acceptance` opens the e2e campaign like `ci-integration`; figures fixed (D5 count 46 live StRS, D17 459 proposed with 2 exempt, D1 to D17, 3959 marker lines); D13 says whether `okfreq-setup` is vendored and by which tool, D14 says the project heading form `### Scenario S<n> (<kind>): <title>` overrides the packaged guideline; the stack parent is the linearised stack once CR-492 to CR-503 are merged, with markers recounted there.

okf-schema 0.18.1 is on PyPI (2026-11-25); the owner: "take it at once, in the current batch".
Destination: running batch batch-09. Critic: yes.

45. strs-validation-Q43 (2026-11-25, night, decided by the Chief of Staff, owner's word "no question"; ask A-19): **Round 8 also covers what the restack onto main needs.** (a): after the merges of CR-508, CR-506, CR-502 and CR-503, round 8 may fix requirements, scenarios and test markers from main that fail CR-504's stricter marker check beyond conflict resolution, besides a Verifier gap in A, F, B or C. CR-504 renumbers its own `CORE-096` (the one on main keeps the number). When in doubt about a restored StRS marker, remove it. The cap stays 8.

Owner's overnight grant (2026-11-25, near midnight, the owner to the Chief of Staff: "je vais aller au lit. tu as toute latitude pour finaliser la stack cette nuit: tu peux passer les contexts a 300K des driver, faire 10 rework max"): the Chief of Staff decides alone to get the stack finished tonight; a CR may take up to 10 rounds; a Driver or stack driver hands back for context only at 300,000 tokens.
