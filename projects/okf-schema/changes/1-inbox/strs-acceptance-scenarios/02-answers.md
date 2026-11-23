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
