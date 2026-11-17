# Backlog (P3): `ci-report` prints "FAILED visual: [object Object]; [object Object]"

Seen in https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40804420093 (report job,
attempt 2, 2026-10-29). The failure reasons are objects stringified with `${}`, so the log does not say
which visual check failed. Fix: format each reason (scenario, check, message) in the `ci-report`
summary (scripts/e2e-campaign.mjs or its report helper); add a unit test on the message text.
