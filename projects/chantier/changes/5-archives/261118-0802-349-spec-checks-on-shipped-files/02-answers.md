# Answers

No grill: a retro point of batch-24 (2026-11-18), kept by the retro critic, that the user put
straight into the batch.

## Settled by the Chief of Staff

- The user's word (2026-11-18): "file all six and run them in batch-24" ("Fait les 6 c'est très
  bien. Fait le dans le batch en cours"). This CR is one of the six, run as its request is written.
  The user asked no question and settled no behaviour; each choice below is settled by the Chief of
  Staff, within the request.
- sc-Q1 (what counts as a shipped file): a file the change puts in the repository for its users or
  its roles to run or read: a card, a stylesheet, a script, a page, a hook, a default configuration,
  a template. A check guards it when it asserts something about that file's content (a rule, a
  name, a value, a structure). Settled by the Chief of Staff.
- sc-Q2 (what the specification says): such a check reads the shipped file from the repository as
  it ships, at the head under test, not a copy or a text the test prepares. A prepared text stays
  allowed only for a case the shipped file cannot hold (a refusal, a broken input), and the
  specification names it as such, beside a check on the shipped file. Settled by the Chief of Staff.
- sc-Q3 (where): the rule goes in the spec-writer's card (`spec-writer.md`, "Output", beside the
  evidence bullet) and the spec critic's card (`spec-critic.md`, under its first kind, "a gap with
  the request's intent": evidence that does not prove what the user asked). No fifth kind, so the
  critic's reply format and the Chief of Staff's list of kinds stay as they are. Settled by the
  Chief of Staff.
- sc-Q4 (how the critic's finding is sorted): a check on a prepared text where the shipped file
  would do is a fix, not a question (it does not touch behaviour: it makes the evidence prove the
  stated behaviour), so the Chief of Staff's existing step "the fixes first" sends it to the
  spec-writer. Settled by the Chief of Staff.
- sc-Q5 (out of scope): the Inspector's and Coder's cards do not change (the request names the
  spec and the critic only); the CLI does not change and gets no new rail or lint (AGENTS.md: no
  speculative CLI tool); no new test (the change is two card sentences, which the structure tests
  already load). Settled by the Chief of Staff. Revised by sc-Q6 for the Inspector's card.

## Settled by the Chief of Staff (after the spec critic)

The user is away; the Chief of Staff settles in the user's place, inside the request's intent,
with the critic's recommended option.

- sc-Q6 (CR-344's spec already asked for tests on the real sheets; the Coder left them out and the
  Inspector caught it only at round 3): option A. Keep the two card sentences as asked, and add one
  paragraph to the Inspector's card (`inspector.md`, "Your part"): from round 1, check that each
  test the specification names reads the shipped files; a named test missing, or one on a prepared
  text only where the shipped file would do, is `blocking`. The Goal's account is corrected to match
  the CR-344 files. Settled by the Chief of Staff.
