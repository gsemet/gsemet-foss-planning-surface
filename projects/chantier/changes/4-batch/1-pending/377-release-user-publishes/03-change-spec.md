# A release is finished after the user publishes it by hand

## Goal

Sometimes the host refuses the Release driver's publication command (for chantier,
CONTRIBUTING.md "Release" step 5, `gh release create vX.Y.Z --verify-tag --notes-file ...`). The
user then publishes by hand, and today nobody finishes the release: no `release published`, no
`work/retro.md`, no `handback ready`. The release CR stays `blocked` and the batch never pauses.
The "Released in" comments are never offered, and the retro never reaches the Completion report.

After this change, the user says once that the release is published ("done", "c'est publié", any
words). The steering session takes the release back to a Release driver. That Driver checks the
publication on the forge and runs the end checklist ("Release driver: the end", `driver.md`). The
release ends as it would if the Driver had published it.

## What is already there (main, 2026-11-18, after CR-368), and stays

- `driver.md`, "Release driver", the publication bullet (around lines 1206-1212): a refusal by the
  host is reported as `handback blocked approval: publish: <the exact command>`, and nothing else
  is tried. The steering session gives the user the command ("the publication is yours") and never
  runs it without their word.
- `driver.md`, "Release driver: the end" (CR-310): the checklist itself, unchanged.
- `chief-of-staff.md`, P9 (around lines 650-656): the user is told at the start that a refused
  publication is theirs. This text is unchanged.
- `chief-of-staff.md`, "Releases" (CR-368): the post-merge word asked with the merge go, `order
  approve`, `wait:` notes, "auto". These are unchanged. The approval ask's answers ("auto",
  `order approve`) stay as they are; this CR adds one more answer for the publication's refusal.
- The CLI. `order note` on a `blocked` CR is accepted (`commands/orders_apply.py`, `_note`, which
  prints `... is blocked: no Driver works on it until the Foreman takes it back`). The Foreman's
  `take <cr> --note` reopens it. `release published` (`commands/release.py`) needs no live CR and
  no `release go`. `handback <cr> ready <link>` on a release with no PR recorded moves it to
  `3-done` (`commands/driver.py`, around line 234). **No change under
  `skills/chantier/scripts/cli/src/`.**

## What changes

The cards are shared by both hosts. The agent files (`agents/`, `com.github.copilot/agents/`) hold
no contract and do not change.

### 1. `skills/chantier/references/chief-of-staff.md`, "Releases"

Add one paragraph after the paragraph ""auto" covers this release only ..." (around line 1817),
before the "draft <path>" paragraph:

- **The publication refused by the host.** The ask is `blocked <release-cr> approval: publish:
  <the exact command>`. Give the user the command as a **For you** line, exactly as handed back,
  with where to run it (the main checkout, or the clone `take` names with a planning surface):
  "the publication is yours: run `<the command>`, then tell me when it is published". The
  question also keeps its usual answers ("auto"; the user's word that you run it yourself, each
  command alone, rule 9). An `order approve` does not help here: the host refused the Driver, not
  the user.
- **The user's word that it is published** ("done", in any language). Relay it at once: `$CHANTIER
  order note <release-cr> --note "publication done: user, <YYYY-MM-DD>: '<the user's words>'"`.
  In Foreman mode, send the order's line to the Foreman. In direct mode, act on it as the
  Foreman's work: `take <release-cr> --note "<the note>"` and a Release driver.
- **You ran the command on the user's word.** The same note follows once the command has
  succeeded: `publication done: steering session, <YYYY-MM-DD>: '<the user's words>'`.
- **What follows.** The Release driver checks the publication, then runs its end checklist. Its
  `release published` opens the "Released in" list (unchanged), and its `retro.md` reaches the
  Completion report (unchanged). The user is asked nothing more for this release, except what that
  list already asks.
- **Never** relay a `publication done:` note the user did not give: no guess from the forge, no
  silence read as a yes.

### 2. `skills/chantier/references/foreman.md`, the release bullet

In the release bullet (around lines 297-320), after "An `order approve` on a release CR that is
`blocked approval:` keeps the take with the note.", add:

- An `order note` whose note starts `publication done:` on a release CR `blocked approval:
  publish: ...` is taken back at once: `take <release-cr> --note "<the order's note>"`. This
  follows the usual take-back path ("Orders are the user's word": `agents set <cr> -` first when
  the id is still recorded, `order done` once taken). It is not a new attempt.
- Received while the release's Driver is still `working` (the user published before the refusal
  reached you): the `[foreman→driver <cr>] note <text>` message, as for any note to a working
  Driver.

### 3. `skills/chantier/references/driver.md`, "Release driver"

**(a) The publication bullet** (around lines 1206-1212). Keep the text, and add two sentences:

- The command handed back must run as written once you have ended. The notes file and the assets
  it names are not in a folder your end removes: keep them in the CR's work folder, or in the
  worktree, and never in a temporary folder you clean up.
- Before the hand-back, name in a `note` the steps of the procedure already run (for chantier,
  `just tag`), as the held-step bullet already asks.

**(b) A new bullet after it: "The publication done by someone else."**

- A take note (or a message) that starts `publication done:` says that the publication step was run
  outside you: by the user, or by the steering session on the user's word.
- It is not a new attempt: no `release start`, and no step of the procedure already run is run
  again (read the notes: the `note` of the previous Driver names them).
- Never run the publication command again, whatever the note says.
- Check the publication on the forge, read-only: `gh release view <tag> --json
  url,tagName,isDraft` on GitHub, or `glab release view <tag>` on GitLab (**unproved** there), or
  the equivalent the host card names.
  - Found and not a draft: the publication step is done. Its text may differ from the prepared
    notes, which is accepted (CONTRIBUTING.md "Release" step 5). Run the procedure's later steps
    that are yours, with their holds, by the bullets above (for chantier there is none: step 6,
    the announcement, is the user's). Then run "Release driver: the end", whose `release
    published <cr> --note "<version> <link>"` takes the link the forge printed.
  - Not found, or a draft: `handback blocked approval: publish: <the exact command>; not on the
    forge: <what the forge printed, first line>`, and nothing else.

**(c) "Release driver: the end"**: unchanged. Its first sentence ("Once the release is out (the
procedure's publication step done) ...") already covers a publication done by someone else. The
refusal is one of "what went wrong or slowly" in `retro.md`, by the Driver's judgement under the
existing item; add no new item.

### 4. `scenario/run_scenario.py` and `scenario/README.md`

**Unit `release`, the release on a stack** (`release_on_stack`, around lines 7155-7164, with no
grant live). Between the `release go` of the two steps (line 7155) and `release published`
(line 7160), script the refusal and the relay:

1. The Driver records `note <r> "steps run: push the tag"`, then `handback <r> blocked "approval:
   publish: gh release create v1.8.0 --title v1.8.0 --verify-tag --notes-file <path>"`.
2. Check that the release is `blocked`, with `blocked_reason` starting `approval: publish:`, and
   that the batch is not paused.
3. The steering session records `order note <r> --note "publication done: user, 2026-11-18:
   'publié'"`. Check that the order is accepted and that its output says the CR is blocked until
   the Foreman takes it back.
4. `fm.turn()`. Check four things: the scripted Foreman took the release back with the note (the
   last entry of `fm.started` starts with `<r> note: publication done:`), the status is
   `working`, `attempts` is unchanged (no `release start`), and every order is done.
5. The existing `release published` and `handback <r> ready` lines then run as today. The existing
   check "10. the release `3-done`, the batch pauses" now also proves the end after a publication
   by hand.

The scripted Foreman (`Foreman.do_order` and `Foreman.candidates`, around lines 609-663) already
takes a `blocked` CR back on a pending `note` order whose `blocked_reason` does not start with
`fix:` or `merge:`. Change it only if step 4 shows it needs to. If the id of the Driver that handed
back is still recorded, clear it before the take (`agents set <r> -`), as the card asks and as the
script does elsewhere.

**`scenario/README.md`**: in the `release` coverage bullet (lines 332-346), before `(unit:
release)`, add: "a publication refused by the host and done by the user: the release `blocked
approval: publish:` goes back to a Driver on the steering session's `order note ... "publication
done: ..."`, with no new attempt, and ends `3-done`". Keep the `(unit: release)` marker, which
`skills/chantier/scripts/cli/tests/test_scenario_coverage.py` reads.

### 5. No other file

No test under `tests/` is added: nothing in the CLI changes, and no test asserts a card's text.
The cards' change is reviewed in the diff.

## Decisions carried from `02-answers.md`

- The user's word is relayed as `order note <release-cr> --note "publication done: user,
  <date>: '<words>'"`, not `order approve`, and never with a `published:` prefix (that is
  `release published`'s note): §1, §2, §4.
- The steering session's own run on the user's word gives the same note, `publication done:
  steering session, ...`: §1.
- No CLI change, and the take is not a new attempt (no `release start`): §2, §3b, §4.
- The Driver checks the publication on the forge, never runs the command again, records the
  forge's link; not found or a draft goes back the same route: §3b.
- A published text that differs from the prepared notes is accepted: §3b.
- The command handed back runs once that Driver has ended: §3a.
- The refusal in `retro.md` stays the Driver's judgement under the existing item: §3c.
- `release published` counts the release in the grant's `published`, unchanged (the CLI's
  existing behaviour).
- A `publication done:` word reaching a working Release driver is the same fact: §2, §3b.

## Out of scope

- Any change under `skills/chantier/scripts/cli/src/`, `hooks/`, `types/`, the board.
- A step other than the publication that the host refuses (a refused `just tag` or tag push): its
  route is unchanged.
- The steering session or the forge hub noticing a publication on its own: the user's word is the
  trigger.
- The publication's host rules, P9, P10 and the trials (CR-214, CR-238): unchanged.
- CR-368's post-merge word, `order approve`, `wait:` notes and "auto": unchanged.
- CONTRIBUTING.md "Release", `docs/release-process.md`, `docs/release-driver-texts.md`: the
  project's procedure does not change.
- The "Released in" comments: unchanged, opened by `release published` as today.

## Host and default matrix

The cards and the CLI are the same on both hosts. Only the refusal depends on the host.

- Claude Code, no grant: the base set holds no `gh release create` rule (hosts/claude-code.md,
  "Capabilities and their commands"). The host asks or its classifier judges, and a refusal takes
  this route. The scenario proves the record's path. A real release proves the cards.
- Claude Code, a live grant ("auto") with the release rules not added: the same refusal and the
  same route.
- Claude Code, a live grant with the rules added: the Driver publishes, and this route is not
  used.
- Copilot, every case: the same card text and CLI. **Unproved** on Copilot, as the rest of the
  release path is.
- GitHub forge: `gh release view`. GitLab: `glab release view`, **unproved**.

## Evidence

- `just check` passes at the PR's head.
- `just eval-dry-run` is not owed: no change under the CLI's `src/` or `evals/kit/`.
- `just scenario` (the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head)
  runs unit `release` with §4's steps 1-5. The existing check "10." proves the end (`3-done`,
  batch paused) after the take back.
- `just test` is unchanged and stays within its budget (AGENTS.md).
- No `just mod` is owed (no `hooks/` or `types/` change). In the batch, the CR on top runs
  `chantier gate` locally, as AGENTS.md says.
- The cards' change (§1, §2, §3) is reviewed in the diff.

## Open questions

None.
