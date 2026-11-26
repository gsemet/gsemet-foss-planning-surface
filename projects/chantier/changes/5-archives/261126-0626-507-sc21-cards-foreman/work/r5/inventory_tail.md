## Sibling-card edits

Changed lines, against the worktree's base `bf4e4c42`, in files another card child wrote (spec section 1 allows a kind-a rule from this child's sources, or a link fix; each goes in the PR with its line). Paths are under `skills/chantier/cards-next/`; line numbers are the files' as they will be committed.

| file:line | what changed | why |
| --- | --- | --- |
| chief-of-staff.md:13 | `git init`, an install, project file writes on the user's yes; never a forge or app setting | kind a (init) |
| chief-of-staff.md:14 | never by name, pattern or PID (floor 10) | kind a (sync-checkout) |
| chief-of-staff.md:16 | `cancel` only after a drop the user ordered | kind a |
| chief-of-staff.md:17 | the ask-first push is the session's own; a Driver's refused push is the rail's | kind a, clarification |
| chief-of-staff.md:27 | no CR work in a scratchpad or temp folder, no secret or personal data in a CR folder | kind a (concepts) |
| chief-of-staff.md:41 | Rare cases name the new topics, `session-shell` among them | pointer |
| coder.md:13, conflict-resolver.md:15, debugger.md:13, demo-explorer.md:13, investigator.md:16, verifier.md:18 | the same CR-work, secrets and personal-data never | kind a (concepts) |
| cr-driver.md:18 | the same never | kind a (concepts) |
| cr-driver.md:20 | never start an agent in place of one that may still run | kind a |
| cr-driver.md:26 | Rare cases: `cr-review-step`, `session-shell` | pointer |
| qa-driver.md:10, 13 | the CR-work never; never comment on, close or reopen an issue | kind a |
| qa-driver.md:18 | Rare cases: `session-shell` | pointer |
| release-driver.md:7 | an image upload is irreversible (`release go`); published notes use the reviewed text, else stay a draft | kind a |
| release-driver.md:14 | never comment on, close or reopen an issue | kind a |
| release-driver.md:18, 19 | the CR-work never; never publish a personal path, email, private repository or session id taken from a source | kind a |
| release-driver.md:25 | Rare cases: `session-shell` | pointer |
| retro-critic.md:22-23, spec-critic.md:18-19 | `help session-shell` for a shell call that waits or changes folder | pointer |
| spec-writer.md:11 | never a draft in a scratchpad or temp folder, nor a secret or personal data in the CR's folder | kind a (concepts) |
| spec-writer.md:15 | `help session-shell` | pointer |
| stack-driver.md:18, 19, 20 | never start an agent in place of one that may still run; never comment on, close or reopen an issue; the CR-work never | kind a |
| stack-driver.md:27 | Rare cases: `session-shell` | pointer |
| griller-skill.md:24, 31 | the CR-work never; `help session-shell` | kind a, pointer |
| griller.md:7 | never a secret or personal data in the CR's folder | kind a (concepts) |
| topics/cr-rounds.md:4 | `help cr-review-step` | pointer |
| topics/refused-push-chief-p1.md:3, 6 | the never-push line is scoped to a Driver's refused push; the session's own push is ask-first item 5 | kind a, clarification |
| topics/release-notes.md:4 | names `release-template.md` and `help release-evidence` | link |
| topics/ticket-summary-p2.md:5 | links `ticket-summary-example.md` | link |
| topics/titles.md:4 | a Griller's subject is words, not a slug (the rest of `titles.md` was already in the topic) | rule from `titles.md`, folded in |
| topics/worker-shell.md:8 | no shell call changes its folder into a CR folder | kind a |

## Behaviour changes on purpose

- `startup-core.md`'s "retry once only on a transient network error" is dropped: a launcher failure is a stop (floor 3 and 4).
- `startup-core.md`'s report-fields sentence and "read every manifest reading before an action" are inferable: the `report` command and the brief's reading lines carry them.
- `review-step.md`'s "cd into the worktree" is inferable: the new text names the worktree.
- "Never tell unproved behaviour as fact" is kind d (host trial bookkeeping), with the proof files.
- The sibling Chief of Staff inventory classes the write-on-yes lines it carries as e; this file classes the source sentences it walks by their own protection. Child 25 reads both.

## Known gaps

- The host JSON files must stay byte-identical, so they still name `session-start.md`, `driver.md` and `foreman-lost-driver.md`, which the new set does not hold.
- `release-template.md`, `routing.md`, `hosts/claude-code.md` and `griller-skill.md` are named in text without a markdown link; the topic `cr-ship`'s "the shipped one" and `release-notes`' `release-template.md` are not linked.
- The role cards, `floor.md`, the forge files, the host JSON files and `review-step.md` hold no markdown link.
- The Foreman's card says only "Stop no sync holder" of a sync failure; the topic `sync` holds the rest.
- Cards and topics above their target are listed with their sizes in `part3-proofs.md`, proof 3.
