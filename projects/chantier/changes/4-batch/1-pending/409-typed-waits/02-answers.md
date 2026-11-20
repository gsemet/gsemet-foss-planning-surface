# Answers: typed-waits (Part E)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Backlog waits and the hub (the reference's E.7):** no. The hub reads no forge for a
   backlog CR's waits; they are cleared by hand; AGENTS.md's query budget does not change.
2. **Order:** `plan-store-interface` (Part B) joins `depends.json`, since the backlog write goes
   through `repo.store`. `planning-server` (Part C) does not: its refusal applies through
   Part B's `check_publish` whenever it lands, with nothing to change here.
3. **A CR dropped back to the backlog:** `order drop` to the inbox or backlog writes its open
   waits to the folder's `waits.json`.
4. **The free-text `blocked waits: <what>` reason:** stays; `--wait` adds typed waits beside any
   reason.

The writer's own choices (`link` beside `ref`; a link in another repository recorded, not read,
cleared by hand; `open_waits` on the board; no pane change) are accepted.

## 2026-11-20, the spec critic's first pass (10 points), settled by the Chief of Staff

Seven text fixes (3 to 8, 10) go to the writer without a question. The three that touch
behaviour:

1. **GitLab approval:** an approval wait is met only when at least one approval was given and
   none is left (`approvalsLeft == 0` with an approver). The proof states the expected answer
   for each plan, a project with no approval rule included, so it can fail.
2. **A wait the forge can no longer see met** (GitHub `reviewDecision` null, a pipeline wait
   whose PR head moved past its sha, a merge wait whose PR was closed): `wait` and `status` add
   "(the forge cannot tell: cleared by hand)" once a read answers so; no journal line.
9. **The `--wait` pointer on the Driver's common path:** never dropped; the section's existing
   text is tightened until it fits under the 45,000-byte cap, with Part D's text.
- **Where an unseen wait is remembered** (the writer's choice for point 2): a `waits_unseen`
  list in the project's hub entry of `chantier/server.json`, refreshed at each successful read,
  counted under the hub's "last reads" AGENTS.md already names. Accepted.
