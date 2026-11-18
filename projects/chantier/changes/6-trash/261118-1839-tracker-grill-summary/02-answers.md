# Answers: tracker-grill-summary

No grill was held with the user on this item: its `01-intent.md` (2026-11-10) is the request, and
the Chief of Staff's brief of 2026-11-18 says the user asks no questions; behaviour questions go
back to the Chief of Staff.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour, checked against the code and cards at main (`3a9afc2c`):

1. **What main already holds.** The intent was delivered by CR-220 `ticket-summary-on-source`
   (archived `5-archives/261113-1646-220-ticket-summary-on-source`, commit `73f78e92`,
   2026-11-13), whose `intake/request.md` is this intent's text word for word, extended by the
   user's answers of 2026-11-13 (all three trackers, project rules first, Jira's access method
   found not fixed, `## Issues References` with `Closes`). Each row of the intent maps to a shipped
   text; the specification's table names them. Nothing is re-specified.
2. **Where the yes is asked.** Unchanged from main: `chief-of-staff.md`, "Ticket summary", step 6
   (the comment and plan shown as text, the demo as a file, the route and the posting tool, the
   ticket's link and title, each project rule followed quoted; a yes asked for that ticket;
   the answer recorded at once in `02-answers.md`), step 7 (posted on the yes only, by the Chief
   of Staff only), the PR follow-up (same rule, its own yes), and "Released in" (one yes for the
   list; "auto" never covers it). `griller.md` and `concepts.md` ("Tracker issue") forbid any other
   role to post.
3. **The reference example.** `ticket-summary-example.md` is modelled on issue #336 rather than
   copying it: CR-220 settled it (the issue is in another project and its text was not given).
   Kept as is.
4. **The intent's priority line** (`priority: P1` in a `2-backlog/P2` folder): the folder is the
   stage of record; the front matter is left as imported.

What stays open is a behaviour and scope question (the intent's "Done when" proof, and whether
this item still has work): it is in `03-change-spec.md`, "Open questions".

## Settled by the Chief of Staff (tracker-grill-summary-Q1, 2026-11-18)
- (a): abandoned as delivered by CR-220 `ticket-summary-on-source` (73f78e92). The eval run is left
  to `evals-rework`, as the user already settled there.
