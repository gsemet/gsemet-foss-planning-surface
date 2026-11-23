# Answers

Short name: `acceptance-paths`

1. acceptance-paths-Q1: **Activation.** A new value of `strs_test_coverage_mode` (e.g. `linked-swrs-and-acceptance-paths`); without it, `scenarios:` and `@accepts_req` are accepted but nothing is required or counted.
2. acceptance-paths-Q2: **Bench of a test.** No bench configuration: the marker tells the bench. `@accepts_req` is a real-bench test, `@tests_req` is a simulated-bench test; the two may be different tests.
3. acceptance-paths-Q3: **Counters.** A fraction of paths per counter (e.g. tested 2/3, accepted 1/3); a StRS is "tested" (boolean) when the fraction is complete.
4. acceptance-paths-Q4: **Direct `@tests_req StRS-X`.** In the new mode, ignored for coverage and reported as a warning.
5. acceptance-paths-Q5: **Lint severity.** Error for an unknown `#S<n>` fragment; warning for a live StRS with no declared path.
