# Answers: explain-access (Part F)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Push on an expired lease nobody took again:** allowed, with "renew it first
   (`lease <cr> renew --lease <n>`)"; Part D accepts a late Driver's command on that lease (its
   renewal at each wake).
2. **`chief-of-staff.md`:** yes, one line in its direct-mode steering text: run `access` before
   asking.
3. **Claim on a working, ready or blocked CR:** not a refusal; the allowed line ends with
   "; take needs --note saying why (<cr> is <status>)".
4. **A scenario case:** none; the prepared-state tests cover it.
5. **Units of claim and push:** a CR only; `lease stack` and `lease O-k` explain those leases.

No spec critic: a read-only command that changes nothing, sharing take's one check function.
