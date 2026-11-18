# Answers

No grill: the CR was filed from release-checklist-Q1 of CR-310 (2026-11-17), which already says
the behaviour: after the user's publication, the steering session takes the release back to a
Driver, which runs the end checklist. The Chief of Staff asked for the specification on
2026-11-18, with no questions to the user.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour of their own, decided here:

- The word: the user's word that the publication is done (any words, any language) is relayed as
  `order note <release-cr> --note "publication done: user, <YYYY-MM-DD>: '<the user's words>'"`.
  Not `order approve`: an approval is a yes to run a step, and the step is done. The note does not
  start with `published:`, which is the note `release published` writes.
- The same note covers the steering session's own run of the command on the user's word (the
  existing "never runs it without their word" route): `publication done: steering session,
  <YYYY-MM-DD>: '<the user's words>'`, once the command has succeeded.
- No CLI change: `order note` on a `blocked` release, the Foreman's `take --note`, `release
  published` and `handback ready` already do it. The take is not a new attempt: no `release start`.
- The Driver taken back checks the publication on the forge before recording it (`gh release
  view <tag>` or the forge's equivalent), and never runs the publication command again. Found
  and not a draft: the link recorded is the forge's. Not found, or a draft: it hands back the same
  route again (`blocked approval: publish: <the exact command>; not on the forge: <what it read>`).
- What the user ran may differ from the prepared notes (an edit, a typo fixed on the forge):
  accepted, as CONTRIBUTING.md "Release" step 5 already accepts it. The Driver checks that the
  release exists, not its text.
- The refused command's paths: the command handed back runs as written once that Driver has
  ended (the prepared notes and assets are not in a folder the Driver's end removes).
- The retro: the refusal is one of "what went wrong or slowly" of `retro.md`, by the Driver's
  judgement, as the checklist already says; no new rule.
- `release published` counts the release in the grant's `published`, as for a release the Driver
  published itself.
- A `publication done:` word that reaches a release Driver still working (the user published
  before the refusal reached them) is the same fact: the Driver checks the forge and goes to the
  end checklist instead of running the command.
