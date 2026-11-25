# Round 7: text for pr-body.md (the Driver's edits)

`<new>` is the sha of the commit of round 7's card edits. Byte counts are LF bytes.

## 1. Summary (F1): replace its third and fourth sentences

> Everything the new set holds is under `skills/chantier/cards-next/`, which nothing loads until the
> later swap. The only files outside it are nine added quiz cases,
> `evals/quiz/chief-of-staff/a8-*.json`: `a8-ask-delete`, `a8-ask-release`, `a8-ask-stop-process`,
> `a8-chained-subcommand-refused`, `a8-gh-pr-edit-base-refused`, `a8-gh-pr-ready-refused`,
> `a8-push-refused-cr-branch`, `a8-push-refused-default-branch` and `a8-rebase-refused-cr-branch`.
> The base is `main`.

## 2. The boundaries split (F2)

Paste the first paragraph and the table of `<CR folder>/evidence/boundaries-split.md` (31 labels, B1a to
B7f) under the heading `## The user's boundaries: label to final home`, in Details before
`## Human decisions`.

## 3. Sizes

Sizes table, replace these rows:

> | review-step.md | 3,950 | 1,419 | 1,500, within |
> | skills: chantier, chief-of-staff, griller, status | 3,537, 3,664, 3,223, 3,644 | 2,669, 2,749, 2,311, 2,748 | none set |

Role cards sentence: `foreman.md` 36,927 to 4,000 (4,000); `chief-of-staff.md` 32,067 to 5,999 (6,000);
`griller-skill.md` 3,501 (4,000). The other cards' figures do not change.

This round, old to new: foreman.md 3,998 to 4,000; chief-of-staff.md 5,994 to 5,999; griller-skill.md
3,497 to 3,501; review-step.md 1,385 to 1,419; skills/chantier-SKILL.md 2,650 to 2,669;
skills/chief-of-staff-SKILL.md 2,730 to 2,749; skills/griller-SKILL.md 2,292 to 2,311;
skills/status-SKILL.md 2,729 to 2,748. No topic changed.

## 4. The brief table

Replace the three rows and add the last one:

> | chief-of-staff | 22,322 | 24,657 |
> | griller | 6,349 | 6,627 |
> | foreman | 55,206 | 22,279 |
> | direct mode: chief-of-staff, then `foreman --epoch 1` | 77,528 | 46,936 |

Add under the table:

> Batch-31, host claude, no unit but where a row says otherwise. chief-of-staff, griller, foreman and
> direct mode: measured on the cards of `<new>`. The other rows: an earlier round, their cards
> unchanged since (the six workers on unit CR-507; a later run at `03f973e` gave them 742 bytes less on
> both sides, same differences, cause not traced). Start readings before this change, as the
> specification gives them (declared / measured): Foreman 91 / 144 KB, Chief of Staff 202 / 218 KB,
> Griller 145 / 36 KB.

## 5. Sibling-card edits: replace these rows of the table

Replace the three rows `chief-of-staff.md ...`, the row `griller-skill.md 24, 31; griller.md 7` and the
three rows `foreman.md 22`, `27`, `38` with:

> | chief-of-staff.md 13, 14, 16, 24, 27 | writes on the user's yes; stopping a Foreman or a process the session did not start, its own board or watcher too, only on a yes, never by name, pattern or PID; `cancel` only after an ordered drop; no tracker text naming a CR, batch, role or cost; CR work never only in chat, memory or a temp folder, no secret or personal data in a CR folder |
> | chief-of-staff.md 10, 17, 22, 23 | the push rail covers a protected branch too; the ask-first push is the session's own; never message or stop a Driver in Foreman mode; never edit `summary.json` by hand |
> | chief-of-staff.md 26 | `abandon` and `restore` only on the user's word, with priority, labels and groups (for the later review) |
> | chief-of-staff.md 3, 39, 41 | wording trims; pointers to new topics; on `init` or "I am new here", run `$CHANTIER init` and give the tour of `init.md` |
> | griller-skill.md 24, 31; griller.md 7 | the CR-work never (chat and memory included), a pointer, no secret in the CR folder |
> | foreman.md 13, 14, 15, 16 | `gate --first` only for a critical-path CR or the user's next merge, not on a Driver's say; never switch the mode; an image note goes in the ask's added sentence; stop stray background tasks by id, none outlives the heartbeat, a refusal rules over `next` |
> | foreman.md 20, 21 | a granted merge takes the judged head only, no open PR below, reread before a retry; never drop a hand-back; a local run is owed at that head and a waiver must name it |
> | foreman.md 22 | the fast-forward is `--no-overwrite-ignore`, of a clean main checkout; the checks of a Driver's refused push or rebase; no comment on a dropped CR's PR, its branch kept; stop no sync holder |
> | foreman.md 25, 27, 29 | a Driver is replaced only by `help lost-restart`, never on silence alone; the CR-work, secrets and personal-data never; a past fact with no source is said unknown |
> | foreman.md 38 | Rare cases name `refused-push` and `session-shell` only; `help --for foreman` lists the topics |
> | foreman.md 3, 6-10, 17, 24, 26, 31 | wording trims for the 4,000 budget |

## 6. Known gaps

Replace "The inventories' homes were matched by script, not read row by row; rows with protecting
wording that a topic carries are listed for the later review." (now false) with:

> - The home of each protecting row was read at its cited line. Each of the four inventories lists the
>   protecting-looking rows a topic carries, for the later review.
> - Rules, or parts of rules, held by no card, floor or refusal: large binaries are never kept in a CR
>   folder (H-057; `coder.md` is over its budget); the host's settings are never a CR's place (H-059,
>   part); never rewrite an earlier retro section (FM-026); never tell as a fact what is marked unproved
>   (C-006); a held agent that has ended with no transcript is cleared on the user's word, or once known
>   not to run (C-304, C-885).

Replace "The Foreman's card says only "Stop no sync holder"; ... both for the later review." (the image
note is no longer left to the hand-back's gaps alone) with:

> - The Foreman's card says only "Stop no sync holder"; the `sync` topic holds the rest.
> - The override of a Foreman's worktree stop by the user's words in its chat is dropped (answer
>   sc21-Q1, a default to confirm by the owner), for the later review.
> - `judge` does not carry the image note of a hand-back; the Foreman's card (line 15) puts it in the
>   ask's added sentence.

In the `just quiz` gap, add at its end:

> This PR's last commit changed the Foreman's, the Chief of Staff's and the Griller's cards: their
> score is owed at the final head. Plans only, no spend: chief-of-staff with griller 54 runs, about
> $25.34; foreman 33 runs, about $15.40; coder, conflict-resolver, debugger, demo-explorer and
> verifier 24 runs, about $8.51; the three Driver roles cannot be planned (`roles.yaml` names
> `driver.md`). The first two are above the default `--max-usd 10`.

The other Known gaps stay true as written (the Never list still has 14 items; `concepts.md` line 121
unchanged; the over-budget cards and topics unchanged).

## 7. Child-24 hand-over (F5): add to Internal references

> - For child 24 (specification section 7): `brief foreman` and `status --refresh` are to print, for a
>   stack batch, `shape: stack: read `$CHANTIER help stack` now and after each compaction`. Child 24
>   changes `src/stack_shape.py`'s `shape_line()`, which prints
>   `rules: {skill_dir}/references/foreman-stack.md (reread after a compaction)`, a path the swap
>   removes, and converts the tests that read the old Foreman cards: `test_came_back.py`,
>   `test_stack_shape.py`, `test_reload_rules.py`, `test_role_cards_split.py`,
>   `test_startup_manifest.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`,
>   `test_release_tag.py` and `moved_rules.tsv`.

## 8. Acceptance records (F6): replace the second Internal references bullet

> - The CR's `evidence/` folder holds the four rule inventories (Foreman, Chief of Staff, Griller, host
>   and shared, with the completeness table), the proofs, the boundaries split
>   (`boundaries-split.md`) and the acceptance records (`acceptance-records.md`: `just test` seconds at
>   base and head, start readings beside the brief sizes, the `just quiz --plan` output, the
>   `griller.md` diff and `git diff --stat`).

## 9. Test plan

The head's sha changes with the commit: the `just check`, evidence and review lines must name `<new>`.
On this round's working tree: `just check` exit 0, 2932 passed, 20 skipped; the evidence lines (byte
copies, unloaded, links 22 and broken 0, 234 topics and 415 readings, Driver table 4 rows) were run
again (`evidence/part3-proofs.md`) with the same results. `acceptance-records.md` names `03f973e4` plus
uncommitted edits; after the commit its `git diff --stat` is the commit's.
