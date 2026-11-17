# Report — copy-code-block

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T03 | Shared, validated channel for new preview actions (no user-visible change) | `fd5233f` |
| T04 | Copy button at the top right of every code block on hover, in reading and edit mode; copies the code exactly, line by line, without line numbers, file name or diff colouring; check-mark feedback | `a726bde` |

## Proof of completion

- T03: 6 new registry tests (did not compile before the module existed); review APPROVE.
- T04: new code-copy tests fail before the change; review FIX-REQUIRED in round 1 (diff,
  line-numbered and emphasized blocks lost their line breaks), APPROVE in round 2 with 10 block
  shape tests built from real rendered output (7 of them fail on the round-1 code).
- Phase 1 e2e (2026-10-16, `b974c5e`, clean tree): unit 813, contract 2, security 23; visual 122
  checks / 117 images; integration scroll, untrusted, trusted (incl. realInput, checkboxToggle),
  standalone and reload suites green.

## Open items

- Message registry: no test for a validator that throws (review nit).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
