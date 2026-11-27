# Join every -pN page set into one page per theme

## Goal

The owner's words (2026-11-27): « deja tous ces cartes p1 p2 ... c'est beaucoup trop. il faut
mettre dans une carte un theme. » Today a help page cut in parts (`board-p1.md`, `board-p2.md`)
holds half a theme; `help` prints the parts one after the other. After this CR each theme is one
file under `skills/chantier/references/topics/`, named for its theme, with the same words in the
same order: only the part markers go. No file is named `-pN` again, and a test keeps it so. The
page-size target of 1,500 bytes, which produced the cutting, is written and checked nowhere.

This CR is the cleanup plan's step 2, item 3 (`2-backlog/P1/card-inventory-open-rows/work/
fable-review-plan.md`, section 6). It is a scripted join with no rewording, proved by a script.

## Before starting (the base)

- `depends.json` puts this CR after `cards-delete-aggregate-topics`, which comes after
  `cards-delete-pages-chief` and `cards-delete-pages-crew`, both after
  `cards-inventory-last-reading`. At the base: the 65 deleted pages are gone, the ten topic names of
  `cards-delete-aggregate-topics` are gone, `docs/protective-rules.md` exists, and
  `docs/proofs/cards-inventory.md` and its tests are gone. If one of these is not so, stop and tell
  the steering session: a CR below is not merged under this one.
- `brief-host-row-names` sits on top of this CR in the stack and names the joined pages
  `<theme>.md`, the names section 1 gives.
- Counts at `4d12a5b`: 105 `-pN` pages in 50 sets; every topic that prints a page of a set prints
  the whole set, in order, and no reading points at a heading inside a `-pN` page (`file#heading`)
  or sits in a host map. Counted for the base from the two deletion specifications: 22 `-pN` pages
  deleted, two sets whole (`compacting`, `sync-offer`), so 83 pages in 48 sets. Of these, 16 sets
  keep one part (`allow-rules-more` p1, `batch-close` p1, `batch-close-stopped` p1, `board` p1,
  `demo` p1, `direct-mode-epoch` p1, `direct-mode` p2, `first-turn` p1, `grill-specify` p1,
  `refused-push-chief-more` p1, `session-start-surface` p1, `ticket-summary-post` p2, `wakes` p2,
  `watcher-board` p1, `watcher-events` p1, `watcher-lines` p2) and `config` keeps p1 and p3. The
  Driver counts again at its base and quotes its own figures.
- A topic at the base that prints only some parts of a set, or a reading that points at a heading
  inside a `-pN` page, is a stop: tell the steering session, do not join that set.

## What changes

All paths are under `skills/chantier/references/` unless they start with `docs/`, `evals/` or
`skills/chantier/scripts/`.

### 1. The joined pages

For each set `topics/<theme>-p<k>.md` at the base (k in numeric order, gaps allowed):

- The joined file is `topics/<theme>.md`. No such file exists at `4d12a5b` for any set; one found at
  the base is a stop.
- Its first line is the first part's heading with the marker ` (part <k> of <n>)` removed (all
  parts of a set carry the same title at `4d12a5b`, checked again at the base).
- Then one blank line, then the body of each part in order, separated by one blank line, and one
  final newline. A part's body is its text after its first line, with the leading blank lines and
  the trailing whitespace removed. UTF-8, no BOM, LF line ends, as the parts are.
- A set with one part left is the same rule: the file is renamed and its marker removed.
- The part files are deleted (`git mv` of the first part keeps its history).

No other word changes, but the part references of section 2.

### 2. Part references inside the text

At `4d12a5b` four places name a part by its number. Read as part markers in the request's sense
("only the part markers (such as "(part 1 of 2)" headings) go"):

- `topics/forge-permissions-p1.md` line 8, the whole line "A stack, a merge by the steering
  session, GitLab and what the user hears: part 2." goes: its text now follows.
- `topics/mode-switch-p1.md` line 7: " (the others: part 2)" goes; the line reads "Read the new
  order from `status`, then by target."
- `topics/merge-gaps-p2.md` line 6, "apply part 1's gap rule", and line 7, "say what part 1 says for
  that result": these cannot go without breaking the sentence. The smallest edit names no part:
  "apply the gap rule above" and "say what is said above for that result". Question 2 asks the
  Chief of Staff to confirm this, or to keep the words as they are.

These are the only differences the proof script of the Evidence allows. Any other place found at
the base that names a part by number is a stop for a question, not an edit.

### 3. `topics.json`

In every topic, the readings of a set are replaced by the one reading `topics/<theme>.md`, at the
place of the set's first part. No topic is added or removed; names, roles, triggers and
`review_by` stay. `help`'s first line counts the same topics before and after.

### 4. Pointers to a part file

Every tracked file that names a `-pN` path gets the joined path. At `4d12a5b`, outside
`topics.json`, `docs/proofs/` and `evals/results/`:

- `docs/incidents.md` lines 70 and 71: both links point at `topics/session-shell.md`.
- `evals/ticket-summary/RUNBOOK.md` lines 4 and 5: `topics/ticket-summary.md` and
  `topics/ticket-summary-post.md`.
- the tests of section 6.

At the base also `docs/protective-rules.md` (each home that names a `-pN` page gets the joined
page; no other line changes) and any line the CRs below added. The cards and the CLI name topics,
not files, and need no change. `docs/proofs/` and `evals/results/` are history and are not edited.

### 5. The page-size target

The request asks to remove the 1,500-byte page target wherever it is still written or checked. At
`4d12a5b` it is written in no tracked file outside `docs/proofs/` and no test checks it (a grep for
`1,500`, `1500 bytes`, "page size" and "per page"); in the planning surface it is written only in
archived or trashed specifications (history, not edited) and in this cleanup's own source files.
The Driver greps again at its base: a line that still states or checks a per-page byte target
(outside `docs/proofs/` and `evals/results/`) is removed and named in the PR; none found is said so
in the PR. `test_brief_bytes.py` (one figure per role's brief) is not a page target and stays.

### 6. Tests (`skills/chantier/scripts/cli/tests/`)

All read the shipped files at the head under test.

- `test_help_topics.py`, new `test_no_topic_page_is_cut_in_parts`: no file under `references/`
  (all folders) has a name ending in `-p<digits>.md`, and no line of a `references/` Markdown file
  matches `^# .* \(part \d+ of \d+\)$`. A failure names the files and lines. It fails at the base
  and passes at the head.
- The tests that read a part file by name read the joined file, with the same needles. At
  `4d12a5b`: `test_command_names.py` line 58, `test_event_audience.py` line 33,
  `test_launch_modes.py` lines 134, 164, 219 (two parts read and joined: one file now), 235 and 238,
  `test_triage_moves.py` line 159. Some of these change in the CRs below; the Driver greps for
  `-p[0-9]` in the tests at its base and fixes each one it finds.
- `test_every_topic_file_has_a_topic`, `test_every_topic_resolves_on_both_hosts`,
  `test_help_lists_them_all` and the aggregate CR's `test_every_topic_holds_a_text_of_its_own` pass
  unchanged (a set is replaced as a whole in every topic, so no subset relation changes).
- `test_brief_bytes.py`: no brief reads a topic page; its figures do not change and it passes.

### 7. The 22 topics that print their own page and pages another topic prints

The Chief of Staff asked whether this CR's "one theme per card" settles the 22 topics that
`cards-delete-aggregate-topics` leaves unchanged (its section 3, question 2, answer 5): `ci`,
`conflicts`, `handback-other`, `pr-extras`, `retake`, `cr-workers`, `stack-restack`, `stack-make`,
`sync`, `merge-under-grant`, `long-gate`, `lost-driver`, `park`, `release-tag`, `retro`,
`retro-critic`, `wakes`, `stack-grows`, `refused-rebase`, `refused-push-judgement`,
`refused-push-route`, `direct-mode`.

It does not settle them, and this CR leaves their readings as they are, the join aside:

- What this CR settles is the file: after it, every page holds one theme whole, in one file. Each of
  the 22 already prints whole files, each its own theme; three of them print part files today
  (`sync` the `main-checkout` set, `wakes` its own set, `direct-mode` its own and the
  `direct-mode-switch` set), which section 3 replaces by the joined files, so they print fewer files
  with the same text.
- What is left about them is what a name prints (its own theme plus a neighbour's), not how a page
  is cut. Settling that needs one of two changes, both outside this request:
  - dropping their borrowed readings changes what `help` prints, and four own pages do not name
    every topic they would stop printing (`ci.md`: `ci-no-check`, `ci-beside-gate`;
    `lost-driver.md`: `lost-context`, `lost-outside`; `sync-checkout.md`: `main-checkout`;
    `direct-mode`'s page: `direct-mode-switch`), so a line would be added: rewording, which the
    request ("without rewording") and the spec-critic answer ("a scripted join with no rewording")
    exclude;
  - joining a topic's own and borrowed pages into one file either copies the borrowed text (the
    folder grows, which the request forbids) or removes the borrowed topics' own names, which this
    request does not ask and the plan places in step 6 (the guides, "one theme each", from the
    pages left in each family), which waits (card-cleanup-Q5: steps 4 to 7 wait).

Where they go next is question 3.

## Decisions from 02-answers.md

1. « ouvre un batch et lance ces 7 CR » (2026-11-27) is read as "grilled enough" for this CR, the
   scope being the plan and the five answers of `card-inventory-open-rows/02-answers.md`; the
   owner's confirmation is still owed (question 1).
2. The batch is a stack. This CR sits above `cards-delete-aggregate-topics` and below
   `brief-host-row-names`. Only the CR on top of the stack owes the local Windows `scenario` run.
3. card-cleanup-Q5 A: steps 1 to 3 ship with a new version, in small CRs; steps 4 to 7 wait. This
   CR is step 2 and no more; the version bump is `release-card-cleanup`'s. The moment the batch
   lands, given the other project that reads the cards live, is the steering session's and the
   user's call at merge time.
4. The owner's « il faut mettre dans une carte un theme »: one theme, one file, no `-pN` part
   (sections 1 to 3, and the test of section 6). The rest of that message (progressive disclosure,
   removing what the model infers from the CLI's output) is the plan's later steps, not this CR's.

## Out of scope

- Any rewording beyond section 2; moving text between themes; deleting a page's text.
- The readings of the 22 topics of section 7 (beyond the join), and any topic name added or removed.
- A total-size test for `references/` or new budgets (plan section 7's other structure tests).
- Any change under `skills/chantier/scripts/cli/src/` (none is needed), the host files and pages,
  `docs/proofs/` and `evals/results/`.
- The version bump (`release-card-cleanup`).

## Evidence

- The proof script, quoted in the PR with its output (not committed): for each set at the base, it
  reads the parts with `git show <base>:<path>`, builds the expected file by section 1's rule,
  applies only section 2's listed edits, and compares it byte for byte with `topics/<theme>.md` at
  the head. It prints one line per set (`<theme>: p1+p2 -> topics/<theme>.md OK`), the edits it
  applied, the count of sets and pages, and the bytes of `references/` at the base and at the head,
  the head at or under the base. It exits non-zero on any difference.
- `git ls-files skills/chantier/references | grep -E -- '-p[0-9]+\.md$'` prints nothing at the head.
- `chantier help board` and `chantier help direct-mode-switch` each print one
  `--- references/topics/<theme>.md ---` line, quoted; `chantier help`'s first line is the same
  before and after.
- The new `test_no_topic_page_is_cut_in_parts` passes at the head (and fails at the base, its
  output quoted); the tests of section 6 pass.
- A grep for `1,500` and `1500 bytes` over the tracked files outside `docs/proofs/` and
  `evals/results/`, at the head, quoted, finds no page target.
- `just check` passes. The cards change, so the pipeline's `just scenario (ubuntu-latest)` job is
  green at the PR's head; the local Windows `scenario` run is owed only by the CR on top of the
  stack (AGENTS.md). No change under the CLI's `src/` or `evals/kit/`, so `just eval-dry-run` is
  not owed.

## Questions for the Chief of Staff

1. Answer 1 reads « ouvre un batch et lance ces 7 CR » as "grilled enough": does the owner confirm?
2. Section 2: the two "part 1" mentions of `merge-gaps-p2.md` cannot go without an edit. Confirm
   "the gap rule above" and "what is said above", or keep the words as they are (they then name a
   part that no longer exists)?
3. Section 7: the 22 topics stay as they are after this CR. Do they wait for the plan's step 6 (the
   guides), or go now as a new inbox item that drops their borrowed readings and adds the four
   missing pointer lines (18 of the 22 own pages already name every topic they borrow)?
