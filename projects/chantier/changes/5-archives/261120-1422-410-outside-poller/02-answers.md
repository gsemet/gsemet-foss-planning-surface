# Answers: outside-poller

Split off `forge-connectors` (its 02-answers.md: FC-2, FC-3, FC-4, FC-7 and the critic's point
7; planning-server-Q24). The answers below settle the open questions of this CR's first
specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Order:** `forge-connectors` joins `depends.json` (its registry, provider seam and
   `connector_for`).
2. **Closed lists:** the published `issue@1` model keeps its fields as plain strings (Part A's
   answer 1); `journal add`'s own input check holds the closed lists, so a new word is a CLI
   change, never an `issue@2`.
3. **`interests` when a provider fails:** the partial list plus one failure line per provider,
   exit 2; `journal add` then refuses and writes nothing.
