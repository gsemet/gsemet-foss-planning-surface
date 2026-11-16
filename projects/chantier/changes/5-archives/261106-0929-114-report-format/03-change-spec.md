# The Chief of Staff's reports always have the same shape

The Chief of Staff reports a batch with the same two tables, and with a current spend. The CLI
already gives all the data: the cards change, and in the CLI only the word `STATUS.md` uses for a
pull request. It builds on CR-113, whose four cost lines these tables carry.

## A "Reports" section in `chief-of-staff.md`

A new section under "While it runs", or the "Status" and "Cost" items reworked into it. It states
a shape, not a script: the columns are fixed, the text around them is the Chief of Staff's to judge,
in the user's language. CR-113's rule on what each report gives stays, placed here.

**Progress**, on a CR ready or merged and on "status?":

- A header line: the batch's number and name, its mode, the slots in use, how many CRs are done,
  the spend and the budget.
- A table with one row per CR: CR, subject, state, PR, cost. Subject is a few words, not the full
  title. The PR is a link.
- The cost table: CR-113's lines from `cost --by role`.
- A last line, always there: **For you:** what the user has to review or decide, or "nothing".

**Completion**, on the `final` message:

- A header line: the batch, how many CRs merged out of how many, the spend and the budget.
- A table with one row per CR: CR, subject, result, PR, rounds, cost.
- The cost table, with one line per Driver type from `cost --by driver`.
- What the batch did not prove.
- A last line, **For you:** closing the batch, with what `close` lists.

The state and result icons are ⚪ waiting, 🟡 working, 🔵 to review, 🔴 blocked, ✅ merged, each with
its word beside it. They belong to the report: `STATUS.md` keeps its own.

A report uses the forge's word: "MR" on a GitLab remote, in the column and in the text, "PR"
elsewhere. The Chief of Staff knows the forge from the remote, as it does for P9.

## The word in `STATUS.md`

`status.py` writes "PR" in its tables and its text. It takes the word from the links recorded in
the state, and still never reads the forge: a link with `/merge_requests/` gives "MR", any other
link "PR". A table takes the word of its own links, and with no link yet says "PR/MR", never a
guess. The CLI's help and its JSON keys (`pr`) stay as they are.

## A current spend

`spent_usd` is recorded only by `status --refresh`, so it can be one heartbeat old. Before a report,
the Chief of Staff runs `$CHANTIER status --refresh`, with no epoch: it records the spend and
`STATUS.md` and leaves the Foreman's heartbeat alone. The card says so where it gives the `status`
command, and the entry point "status?" in `SKILL.md` follows.

## Out of scope

- No CLI change beyond that word, and no other change to the tables of `STATUS.md`.
- `Never read the Foreman's transcript` and the other rules of the card stay.

## Done when

- `chief-of-staff.md` has the two shapes and the refresh, and `SKILL.md`'s "status?" row agrees.
- `STATUS.md` says "MR" for a batch whose links are GitLab merge requests.
- `concepts.md`, `routing.md` and the README are read and follow only where they contradict this.
- `just check` and `just scenario` pass.
