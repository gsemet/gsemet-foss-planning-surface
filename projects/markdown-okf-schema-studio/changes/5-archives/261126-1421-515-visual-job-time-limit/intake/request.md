# The CI visual job runs at its 15-minute limit

The CI job `visual` runs at its 15-minute limit on every branch and gets cancelled.

- `.github/workflows/ci.yml`, job `visual`: ubuntu-latest, `timeout-minutes: 15`; nearly all the
  time is the step `just ci-visual`.
- Whole job on main, last eight runs (2026-11-24 to 2026-11-26): 804 to 890 s of 900 s (runs
  45412775118, 45429944338, 45459891203, 45476952370, 45580228461, 45713440510, 45771447942,
  45773405420).
- Run 45795716172, head 5f7658a (CR-511, https://github.com/gsemet/markdown-okf-schema-studio/pull/537):
  cancelled on both attempts, at 921 s and 905 s; on the second, `just ci-visual` had passed
  (846 s) and the report upload was cut.
- `.agents/guidelines/ci.guidelines.md` rules 9, 11 and 12: no re-run to hide it, and the timeout is
  not raised for it.

Asked: a change in batch-09, low in the stack, that splits or shortens the job so that every run
ends well under its limit, without raising the limit and without dropping a check.

Origin: Foreman ask A-33, 2026-11-26.
