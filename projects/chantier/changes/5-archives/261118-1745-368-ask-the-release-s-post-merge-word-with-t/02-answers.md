Short name: `release-word-with-merge`

# Answers

1. Q: File it and run it now? User, 2026-11-18: "les deux. garde le batch ouvert et enchaine sur
   ces 2 bugs" (both retro points, in batch-27, now).

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- When a release's version PR is ready to merge, the Chief of Staff's ready line to the user also
  asks the user's word for the procedure's irreversible steps after the merge (for chantier: the
  tag and the forge release), each named, in the same message. The answers stay the user's: yes to
  all, yes to some, or none.
- A yes given there is recorded before the merge, with the user's words and the date, through the
  existing order (`order confirm` or `order approve`, whichever the cards already use for that
  word); then the merge's `order merged` starts one Release driver that runs every step the user
  said yes to, and asks only for the others.
- With no word given at the ready ask, today's path stays: the Release driver asks after the merge.
- "auto" is unchanged and still covers the steps it covers. An approval never lets any agent
  merge the version PR; posting the announcement stays the user's.
- The word is recorded with `order approve`, one per step, before `order merged` (the CLI accepts
  it; `order confirm` stays the word for a procedure with no release PR).
- A release redone before its merge (a `redo:`, a new attempt after a fix): the yes already
  recorded still holds, since it covers the steps after the merge, and the user's merge of the
  version PR stays their review of its content. The next ready line names the steps already
  approved, so the user can still say "wait".
- A "wait" after a yes (spec-writer's question, 2026-11-18): no CLI change. The Chief of Staff
  keeps the user's "wait" until the merge, then records it right after `order merged`, in the same
  relay, as `order note <release-cr> --note "wait: <step>: user, <date>: '<words>'"`, so no take
  happens before the merge. The take at the merge names that step as held, and the Release driver
  treats a later `wait:` note as stronger than an earlier approval of the same step.
- (spec critic, 2026-11-18) Approvals recorded before an "auto": the smallest CLI change is in
  scope. A live grant lets the release PR's merge go before any approval is read
  (`rails_release.py` `release_go`), so the yeses stay whole for the Driver started at the merge.
- (spec critic, 2026-11-18) A "wait" given before the merge is written at once, with the date and
  the user's words, in the release CR's `02-answers.md` (not a take). The Chief of Staff reads that
  file when it records `order merged`, and only then writes the `wait:` note.
- Both hosts' cards change together; no new CLI command. If the CLI refuses to record the word
  before the merge, the spec-writer says so and the smallest CLI change that accepts it is in
  scope.
