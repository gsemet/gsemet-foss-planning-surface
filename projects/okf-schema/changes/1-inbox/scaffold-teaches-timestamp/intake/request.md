# init: the scaffold schema teaches timestamp, not the OKF 0.2 fields

From the OKF 0.2 compliance check of `origin/main` 2f09cef (0.18.1), 2026-11-25. Filed on the
user's yes, not grilled. Spec text: `skills/okf-schema/references/okf-v0.2.md` (the upstream text).

OKF 0.2 section 13.1: "`timestamp` is superseded by `generated.at`". Section 11: producers SHOULD
follow sections 5 through 10.

Observed:
- The `_base.schema.yaml` written by `okf-schema init` (`cli.py:201-205`) declares `timestamp` and
  none of `generated`, `verified`, `status`, `stale_after` or `sources`, next to an `index.md`
  declaring `okf_version: "0.2"` (`cli.py:162`).
- `okf-schema new` writes `type`, `title`, `description` and `tags` only, so a fresh concept gets
  W3 at once.

The check's suggested fix: replace `timestamp` with the 0.2 fields in the scaffold schema;
optionally have `new` write `generated`.
