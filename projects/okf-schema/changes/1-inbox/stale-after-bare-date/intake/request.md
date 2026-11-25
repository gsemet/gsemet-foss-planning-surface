# validate: a bare-date stale_after passes silently, read as a local day

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

OKF 0.2 section 5: "Every timestamp-valued key in OKF is an ISO 8601 datetime with an explicit UTC
offset". Section 5.5 calls `stale_after` "An absolute instant". The spec gives no rule for a value
that does not conform.

Observed (`validator.py:409-418` and `446`, `date.today() >= parsed`): `stale_after: 2026-01-01`
gives W11 and `stale: true` with no format warning, compared with the local calendar day, so the
answer depends on the timezone. A datetime without offset gives W16 and is not stale.

Related: the `okf-schema trust` command of CR `show-as-stored` (issue 58, batch-01) keeps this
reading of a bare date.

The check's suggested fix: keep the leniency and add a warning for a bare date, or compare it as
midnight UTC.
