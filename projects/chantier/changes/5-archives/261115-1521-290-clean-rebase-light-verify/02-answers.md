Short name: `rebase-verify`

# Answers

1. The user, 2026-11-15: "oui planifie les 19" (this item among them, grilled first since it moves a safety line).
2. rebase-verify-Q1: **What a clean rebase still proves.** A (recommended): a rebase with no conflict and the CR's own patch unchanged (same patch before and after) carries the Verifier's verdict; CI must still pass green at the new head. No new Verifier then.
3. rebase-verify-Q2: **Modes.** A (recommended): the same rule in parallel and stack modes.
4. rebase-verify-Q4: **Grilled enough?** A: specify, and add it to batch-18 with the others.
