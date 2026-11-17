# Version PR for chantier v0.10.0

Release 0.10.0 (minor, from 0.9.0), 124 changes since v0.9.0. This PR holds the release notes, the
announcement thread (a draft for you to post), the claims file `evals/results/claims-v0.10.0.md` and
the version bump (commit `release: v0.10.0`). It pushes no tag and publishes nothing: after your merge,
the steering session runs `just tag` and `gh release create`.

## Evals

The `full` campaign did not run for this release. On your word ("on a déjà fait les evals"), the two
real runs of 2026-11-15 count as its evals: `evals/results/real-foreman-2026-11-15-run2.md` and
`evals/results/real-direct-2026-11-15-run3.md`. They ran chantier at fa97e70, so only changes made at
or before it can be `exercised`. The claims file has 87 rows: 14 exercised, 45 scenario only, 28 not
exercised. The notes' "For contributors" block names them.

## Checks

`just check` passes (235 tests, lint, types, release notes). CI is green at b4dd334, scenario job included. The docs carry no SVG diagram change.
The two board captures come from a real `chantier board` run on this checkout, rendered with headless Chrome in English; they show no key, path or session id. The notes and thread were scanned with
`scripts/release_notes.py --scan`, and each image was read.

## Each feat and fix, and its place in the notes

| Commit | Type | Subject | Place in the notes |
|---|---|---|---|
| f0f3fb8 | feat | the sandbox merge waits for the checks of a restacked head | B. Intensive evals |
| d6836e4 | feat | start CRs on the stack once it can form, retarget on create | C. A stack that forms itself |
| f94c248 | feat | judge a running agent by its transcript's end, and add close --stopped | Smaller changes |
| 1573c64 | feat | the Chief of Staff stays quiet on a Foreman's turn-end notice | Smaller changes |
| 242aa63 | fix | set the stack unit budget from the fresh --jobs 4 time plus 25 percent | All fixes |
| 9726dca | fix | fit the stack unit in its time budget | All fixes |
| 59fd952 | feat | the evals folder is self-sufficient, anyone can run a campaign | B. Intensive evals |
| f41f43c | fix | the write guard reads a Git Bash drive path as its drive form | All fixes |
| 857506d | feat | a clean rebase carries the Verifier's verdict to the new head | D. A clean rebase keeps its proof |
| 6fd2bad | feat | the PR-in-draft hand-back line names its PR's draft state and the CR it waits on | Smaller changes |
| 04b7d0e | feat | list in a claims file what a release claims and which eval run exercised it | B. Intensive evals |
| c64a21b | feat | refresh the spend where the budget is checked and show its age | Smaller changes |
| f11f316 | feat | flag a working CR whose Driver ended with no hand-back recorded | Smaller changes |
| f257647 | fix | the audit reads Chief of Staff prompts, claim calls and here-docs without a false FAIL | B. Intensive evals |
| c5c3c75 | fix | name the steering role by the mode and price the whole session | All fixes |
| 938f3a4 | fix | name a paused batch and the way out, and a held board port | All fixes |
| 977b570 | fix | the judge judges the PR's head from the forge, so a restacked stack is judged | B. Intensive evals |
| 842b800 | feat | merge route for a PR of a native GitHub stack | C. A stack that forms itself |
| b07c8d5 | fix | the dry run's fake forge answers the stacks and the asynchronous merge | B. Intensive evals |
| 0819a22 | fix | sandbox.py merge goes through GitHub's asynchronous merge, so a PR in a native stack merges | B. Intensive evals |
| fa97e70 | feat | read the PR's base and draft state from the forge for every PR | Smaller changes |
| 07bb2f9 | feat | check ready PRs of a parallel batch for conflicts with git merge-tree and offer a stack | C. A stack that forms itself |
| c774bab | feat | every worker points to its card and the CLI prints each worker's opening prompt lines | Smaller changes |
| 37c4860 | feat | verdict VERIFIED refuses a verify note that does not name the head | D. A clean rebase keeps its proof |
| 80c898e | feat | a new readiness ask marks the earlier unread one of the same change or stack read | Smaller changes |
| 1eb3f32 | fix | stop the CR's long gate and wait for it to end before order merged moves the folder | All fixes |
| afd42be | fix | keep order() under its function limit after the rebase onto CR-262 | All fixes |
| 170daa1 | fix | keep orders_apply under 400 lines and wrap the order help after the rebase onto CR-265 | All fixes |
| 3b18a56 | feat | record a long-gate waiver per CR with order waive and show the long gate on every surface | D. A clean rebase keeps its proof |
| 615110d | fix | web-board kanban paragraph keeps both CR-261 and CR-262 text after the rebase | All fixes |
| ac42b88 | fix | a selected Triage card shows no blue border, and the sidebar line says inbox | All fixes |
| 627fab1 | feat | kanban columns with a Done column and a priority filter, shared item card on Triage, earlier batches on Costs and Home | A. Introducing the board web UI |
| 22ae026 | fix | the rebase takes of the mode-switch block carry the batch's own number | All fixes |
| 6be1949 | fix | the scenario's agents set and two Chief of Staff examples carry --epoch after the restack | All fixes |
| 1bfd48a | feat | every steering command refuses a missing --epoch and the messages say Foreman n° | Smaller changes |
| e543e9c | feat | a retro critic cuts every list of changes the Foreman or the Chief of Staff proposes on its own | Smaller changes |
| 52eeccd | feat | a blocked Driver hands back ready, the dev checkout runs with --no-sync, and a stacked CR's base is read from its PR | Smaller changes |
| e07d441 | feat | order the queue by the next merge, push early after a rebase and carry a gate pass over a clean rebase | D. A clean rebase keeps its proof |
| ac86ca9 | fix | the phase command opens the repo with Repo.find and its refusals are checked in pytest | All fixes |
| fd88e0c | fix | the phase command refuses a non-working CR, a review with no detail and a long detail with exit 2 | All fixes |
| 2223d8b | feat | record and show the step each working CR is at, and mark the next CR to start on the board | Smaller changes |
| 7b57731 | feat | switch a running batch between any two modes and add forge-stack unstack | C. A stack that forms itself |
| 06dfb10 | fix | the eval kit gives the CLI planning-folder-relative paths | All fixes |
| 93e1f39 | fix | the summary case triages by the planning-folder-relative path | All fixes |
| 9a63cf2 | feat | Coder, Inspector and Verifier reply in an exact template, a long reply is noted not restarted, and verdict names its accepted words | Smaller changes |
| 99c1cd4 | feat | a ready CR reads ready locally, PR in draft or ready to merge, from a recorded draft state, with the icons purple, brown and green in the STATUS files, the board and the pane | C. A stack that forms itself |
| be5563c | feat | a planning surface stays in sync through its own autosync, checked by preflight and status and shown on the board as a pill with a panel | Smaller changes |
| 5c9fe9f | fix | a dragged group lands over post-its, a hidden post-it leaves the selection, the editor guards back and forward, and a post-it holds no nested button | All fixes |
| 37deb01 | fix | the board write steps read the request under intake/ and expect PUT to need the cookie | All fixes |
| 0509ca4 | feat | the Triage view, the journal, the New dialog and the Markdown editor, on the board's write routes | A. Introducing the board web UI |
| 6688e8a | feat | the board writes the backlog through the CLI's own functions, with a journal, a next-batch marker, triage --inbox and a hash-checked Markdown edit | A. Introducing the board web UI |
| f024c3b | feat | a spec critic checks an impactful change specification before it is final | Smaller changes |
| dd30fa6 | fix | S4 expects the top-level key list with long_gate | All fixes |
| 6102fb8 | feat | the project says in chantier.yaml how many long gates may run at once, a stop acts on its slot, and the steering session can move a queued gate first | D. A clean rebase keeps its proof |
| 9ac3adb | feat | draw the check mark on the current line of the project picker, on project rows and All projects | Smaller changes |
| 7fe898f | feat | the file panel with its tree and Markdown renderer, and the All projects, pipeline and sidebar fixes | A. Introducing the board web UI |
| be83035 | feat | the Home, Kanban, Batch, Costs and All projects views, drawn from the live record | A. Introducing the board web UI |
| fbf176d | feat | the page's shared layers, shell, words in English and French, and the lint and structure checks the reading views stand on | A. Introducing the board web UI |
| 7895157 | fix | keep shutil imported at the top of the Copilot cost module, where the scenario patches it | All fixes |
| 0dafe54 | fix | the socket listens before the start line prints | All fixes |
| 2de0728 | feat | chantier board serves the record and the planning folder over a keyed JSON API, with a web page frame | A. Introducing the board web UI |
| 6db1127 | fix | stack with no CR prints take stack's lines plus its last context line | All fixes |
| cab066c | feat | remove a dropped change cleanly, record a restack's progress, and hold the stack when it breaks mid-way | C. A stack that forms itself |
| 20b2740 | fix | read the default branch from the batch's settings when checking a GitLab merge request merged below | C. A stack that forms itself |
| 4756e38 | feat | make, check and rebuild a stack on GitLab as the chain of merge requests, with the same five checks as GitHub | C. A stack that forms itself |
| e28beba | feat | make the native stack at two ready PRs and grow it from the bottom as each change gets its PR | C. A stack that forms itself |
| c74ea94 | fix | preflight finds the gh stack extension with gh extension list, forge-stack rebuild exits 4 when a stack stays open, and ship skips all-digit tokens in the stale-SHA scan | All fixes |
| 3fb9129 | feat | check the allow rules per capability, warn strongly before the go and document each capability's commands and trials | Smaller changes |
| 7d07e5c | feat | a project can run CI beside the long gate with ci.beside_gate in chantier.yaml, and the Driver pushes at the approved round | D. A clean rebase keeps its proof |
| 4d9075f | fix | a merge stops the CR's long gate, a recorded pid counts as alive only while it is the same process, and the activity line shows a queued gate | All fixes |
| effb478 | feat | the Chief of Staff asks to add the missing allow rules and adds them on the user's yes, and the release rules leave the recommended set | Smaller changes |
| 848e46b | feat | a merge may come at any moment, one PR at a time in any batch shape, and a Driver merged under it ends cleanly | Smaller changes |
| 6abb6b2 | feat | the eval kit's setup stages the ticket-summary campaign with its frozen issue and request | B. Intensive evals |
| b24f7c2 | feat | each CR carries a condensed summary.json, kept fresh through a summary linter and commands | Smaller changes |
| febd917 | feat | declare the CLI once in a root pyproject.toml and run it with uv, from the local code in this checkout and with uvx from the plugin's folder | Smaller changes |
| ff701a9 | fix | guard the Windows process-group flag with a platform check so mypy passes off Windows | All fixes |
| 2d9a2aa | feat | the Driver's context threshold is 130,000 from the measured compaction point, and the Inspector's reply is capped | Smaller changes |
| bfe527d | feat | the batch retro tags each point project or chantier and offers chantier's as a GitHub issue draft | Smaller changes |
| 2934943 | feat | a worker reply out of format is a failed worker, started again, and a forge 5xx is re-run once | Smaller changes |
| 12df9b4 | feat | each batch leaves a record of its own in 5-archives/batches and the next number is read from it | Smaller changes |
| 0b3427f | feat | the CR driver and the stack driver get the Edit tool | Smaller changes |
| b3cc2be | feat | forge-stack rebuild makes the native stack again from the record once a stack is ready | C. A stack that forms itself |
| 73f78e9 | feat | post a ticket's summary, plan and demo on the user's yes and name the ticket in Issues References | Smaller changes |
| 15a2ee1 | feat | long gates queue first-come and a refusal names the gate that is live | D. A clean rebase keeps its proof |
| 6ef5d7a | feat | a Driver stays a Driver (round guard, context line, shell write guard) | Smaller changes |
| 6079837 | feat | an ended or refused agent is restarted once, by one way, from the recorded state | Smaller changes |
| 733b4e1 | feat | judge allow rules by the commands they let through and check the forge's rights at the start | Smaller changes |

---

<h1 align="center">chantier 0.10</h1>

<p align="center"><b>Introducing the board web UI, tested by intensive evals: edit your backlog in the browser, run a stack from the start, and keep each proof across a clean rebase</b></p>

<p align="center"><sub>124 changes since 0.9.0 · Claude Code and GitHub Copilot · MIT</sub></p>

<p align="center">
<a href="https://github.com/gsemet/chantier#install">Install</a> ·
<a href="https://github.com/gsemet/chantier/blob/v0.10.0/docs/tutorial-claude-code.md">Tutorial</a> ·
<a href="https://github.com/gsemet/chantier/blob/v0.10.0/docs/use-cases.md">Use cases</a> ·
<a href="https://github.com/gsemet/chantier/compare/v0.9.0...v0.10.0">Full changes</a>
</p>

---

## 📋 Introducing the board web UI

`chantier board` serves the record and the planning folder as a web board, for this machine and the
local network, behind a key in its URL. Open the link it prints and you have a Home, a Kanban, a
Batch, a Costs and an All projects view, a file panel with a Markdown renderer, and a Triage view
with a journal, a New dialog and a Markdown editor. The Triage view is your backlog: the inbox, the
priorities P1 to P4 and the ready folder, where you drag a post-it up or down to change its priority.
The Batch view is the running batch: its mode, its slots, the changes at work and what each waits for,
the PRs to review, the PRs in draft, the spend against the budget, and the earlier batches. The board
edits the backlog through the CLI's own commands, so each move is the same as the one you would type.
It never edits a running batch and never messages an agent.

| The backlog, in the Triage view | The running batch, in the Batch view |
| --- | --- |
| ![The Triage view: the inbox, the priorities P1 and P2 and the ready folder](https://github.com/gsemet/chantier/raw/b4dd334266e8f507bebf40de8a54dec9a24cd775/docs/release-notes/2026-11-15-v0.10.0/board-backlog.png) | ![The Batch view: batch mode, slots, the change at work, the PR in draft and the earlier batches](https://github.com/gsemet/chantier/raw/b4dd334266e8f507bebf40de8a54dec9a24cd775/docs/release-notes/2026-11-15-v0.10.0/board-batch.png) |

```text
$ chantier board --help
usage: chantier board [-h] [--host HOST] [--port PORT] [--seat SESSION]
                      [--clock TIMESTAMP] [--new-key]
  --port PORT        the port, or 0 for a free one the system picks (default:
                     chantier.yaml's board.port, else 8765)
  --new-key          replace the board's key: the old link stops working
```

The Kanban has a Done column and a priority filter, and the Costs and Home views show earlier
batches. Edits are checked by hash, so a file changed elsewhere is never overwritten.

See [the web board](https://github.com/gsemet/chantier/blob/v0.10.0/docs/web-board.md).

## 🧪 Intensive evals, and a release that says what they saw

This release was put to the test harder than any before it. A real Foreman ran a stack and a real
Chief of Staff ran a parallel batch in direct mode, both on 2026-11-15, and each run is scored against
the scorecard's rows. The eval kit grew to match: the sandbox merge waits for the checks of a restacked
head and goes through GitHub's asynchronous merge, so a PR in a native stack merges; the judge judges
the PR's head from the forge, so a restacked stack is judged; the audit reads Chief of Staff prompts,
claim calls and here-docs without a false FAIL; the dry run's fake forge answers the stacks; and the
setup stages the ticket-summary campaign with its frozen issue and request. The evals folder is
self-sufficient: anyone can run a campaign from its README.

A release now has a claims file that lists each change it makes, the scorecard row that would catch
it, and whether an eval run brought it to the test. Its results are `exercised`, `scenario only` or
`not exercised`, and the notes below name every change an eval has not seen.

```text
$ ls evals/results
real-direct-2026-11-15-run3.md
real-foreman-2026-11-15-run2.md
claims-v0.10.0.md
```

See [the evals](https://github.com/gsemet/chantier/blob/v0.10.0/evals/README.md).

## 🧱 A stack that forms itself, on GitHub and GitLab

In a stack batch, each change used to start on `main` and was stacked afterwards, which cost a
restack, a conflict to resolve and a new review on each change above the first. Now a change starts
on the top of the stack as soon as two changes are ready, and the PRs form one native stack on the
forge as each one gets its PR. A change you drop leaves the stack cleanly, the restack's progress is
recorded, and a stack that breaks half-way is held for you instead of going on. On GitLab the stack
is the chain of merge requests, with the same five checks as on GitHub. In a parallel batch, the
Foreman now checks each ready PR against the others with `git merge-tree` and offers you a stack
when two of them conflict; nothing switches without your word. You can also switch a running batch
between parallel, series and stack at any time.

```text
$ chantier order --help
...
  mode: parallel, series or stack
$ chantier forge-stack --help
usage: chantier forge-stack [-h] [--batch BATCH] [--stack N]
                            {create,show,rebuild,unstack}
```

A ready change reads one of three words, `ready locally`, `PR in draft` or `ready to merge`, with
the icons purple, brown and green, in the status files, on the board and in the pane. The merge
route also works for a PR of a native GitHub stack, which `gh pr merge` refuses.

See [the use cases](https://github.com/gsemet/chantier/blob/v0.10.0/docs/use-cases.md) and
[the boards](https://github.com/gsemet/chantier/blob/v0.10.0/docs/boards.md).

## ♻️ A clean rebase keeps its proof

A rebase that leaves a change's patch unchanged used to cost a new long gate and a new Verifier.
Now the gate's pass and the Verifier's verdict carry over a clean rebase, which git proves and the
hand-back records, and a rebase with a conflict is gated again. After a rebase that needs a gate,
the Driver pushes at once and runs the gate beside CI, with the PR in draft until both are green. The
queue runs the next merge's gate first. Your `chantier.yaml` can allow more than one long gate at
once, and a project can run CI beside the long gate for every change. On a stack, `order waive`
lets the lower changes skip the gate when the top one validates the whole.

```text
$ chantier gate --help
...
  --stop         stop this CR's running long gate: its suite, the gate lock;
                 recorded `stopped`, no pass; nothing else changes
  --first        the steering session's: put this CR's waiting long gate at
                 the head of the queue
```

The gate and the verdict still bind to one commit: a hand-back that cannot show the replay of the
gated commits onto the new base is refused with `does not carry`, and a verdict `VERIFIED` is
refused when its note does not name the head.

See [the gates](https://github.com/gsemet/chantier/blob/v0.10.0/docs/gates.md).

## 🛠 Smaller changes

- **A closed batch leaves a record.** Each batch leaves a record of its own in the planning folder's
  archives, with its cost, its changes and its retro, and the next batch's number is read from it.
  `close` judges a running agent by the end of its transcript; when one looks running but was cut, by an
  app restart for example, only you can say it stopped, and `close --stopped` records that on your word.
  The spend is refreshed where the budget is checked, `status` says how old it is, and a working change
  whose Driver ended with no hand-back is flagged.
- **The ready line says what a PR waits on.** A PR in draft names its draft state and the change it
  waits for, and `ship` reads each PR's base and draft state from the forge.
- **Every worker points to its card.** Each agent file names its card and refuses a prompt without
  it, and the CLI prints each worker's opening prompt lines. Coder, Inspector and Verifier reply in
  an exact template, a long reply is noted and not restarted, and `verdict` names its accepted words.
- **A Driver stays a Driver.** A round guard, a context line and a shell write guard keep it from
  coding. Its context limit is 130,000 tokens, from the measured compaction point, and the
  Inspector's reply is capped. A reply out of format is a failed worker, started again once; so is
  an agent that ended or was refused. A forge server error is re-run once. The change Drivers get the
  Edit tool, and a blocked Driver can hand back ready.
- **A merge may come at any moment.** One PR at a time in any batch shape, and a Driver merged under
  its feet ends cleanly.
- **A step for each working change.** `chantier status` and the board show the step a Driver is at,
  and mark the next change to start.
- **Steering commands name the Foreman.** Every steering command refuses a missing Foreman number,
  and its messages say "Foreman n°".
- **A shorter retro.** The retro critic cuts every list of changes the Foreman or the Chief of Staff
  proposes on its own, and each retro point is tagged `project` or `chantier`, chantier's offered as a
  GitHub issue draft.
- **Allow rules, per capability.** Preflight checks the allow rules by the commands they let
  through, warns strongly before the go and checks the forge's rights at the start. The Chief of
  Staff asks to add the missing rules and adds them on your yes. The release rules left the
  recommended set.
- **A planning surface that stays in sync.** A surface can name its own autosync, which preflight and
  `status` check and the board shows as a pill with a panel; the board's project picker marks the
  current line.
- **A spec critic.** An impactful change's specification is checked by a spec critic before it is
  final.
- **Tickets.** A ticket's summary, plan and demo are posted on your yes, and the ticket is named in
  the PR's Issues References.
- **A summary per change.** Each change carries a condensed `summary.json`, kept fresh by a linter
  and commands.
- **One way to run the CLI.** It is declared once in a root `pyproject.toml` and runs with `uv`: from
  the local code in a chantier checkout, and with `uvx` from the plugin's folder.
- **Quiet turns.** The Chief of Staff stays quiet on a Foreman's turn-end notice.

<details><summary><b>🐞 All fixes</b></summary>

- **Stacks and PRs.** Preflight finds the `gh stack` extension with `gh extension list`, `forge-stack
  rebuild` exits 4 when a stack stays open, and `ship` skips a token of digits only in its stale-SHA
  scan. On GitLab the default branch is read from the batch's settings when a merge request merged
  below is checked.
- **The long gate.** A merge stops the change's long gate and waits for it to end before it moves the
  folder; a recorded process counts as alive only while it is the same process, and the activity line
  shows a queued gate.
- **The board.** The server's socket listens before its start line prints. A dragged group lands over
  post-its, a hidden post-it leaves the selection, the editor guards back and forward, and a post-it
  holds no nested button. A selected Triage card shows no blue border, and the sidebar line says
  inbox.
- **The CLI.** `phase` refuses a change that is not working, a review with no detail and a long
  detail, and opens the repository the common way. A paused batch is named with the way out, and so is
  a held board port. The spend and the steering role are priced by the mode: a direct batch's whole
  session is priced and named. A Windows-only process flag is guarded so that mypy passes elsewhere.
- **The write guard.** It reads a Git Bash drive path as its drive form.
- **Evals.** The kit gives the CLI paths relative to the planning folder.
- **The scenario.** The stack unit fits its time budget, measured again; the rebase takes of the
  mode-switch block carry the batch's own number; the board's write steps read the request under the
  intake folder; one case expects the top-level key list with `long_gate`; the summary case triages by
  the relative path; `stack` with no change prints `take stack`'s lines; and the Copilot cost module
  keeps `shutil` imported where the scenario patches it. Two Chief of Staff examples and the
  scenario's agents carry the Foreman number after the restack.
- **Code size.** `order` and `orders_apply` stay under their limits after two rebases.
- **The docs.** The web-board paragraph keeps the text of both changes after a rebase.

</details>

<details><summary><b>🛠 For contributors</b></summary>

- **Not exercised by an eval.** The two runs that count for this release (a real-foreman run on a
  stack and a real-direct run on a parallel batch, both of 2026-11-15) ran chantier before the last
  25 changes landed, and no `full` campaign ran. These changes of the release were not brought to the
  test by them:
  - Not proved by the runs and not by the scripted scenario or the unit tests either: the claims file
    itself; the board's Kanban, Triage, file panel, views, editor and check mark, and the fixes of
    their drawing; the eval kit's paths, its asynchronous merge, its fake forge, its self-sufficient
    folder, its judge on a restacked head, its audit, its restack wait and its ticket-summary setup;
    the merge route for a native stack's PR; the Chief of Staff's quiet turn on a Foreman's notice, and
    its offer to add allow rules; the spec critic; the ticket's summary, plan and demo; a worker reply
    out of format restarted and a forge error re-run; an ended or refused agent restarted once; the
    Edit tool of the change Drivers; a blocked Driver that hands back ready; the write guard's Git
    Bash path; the Windows process-flag guard.
  - Proved by the scripted scenario or the unit tests alone, and by no run: the conflict check and the
    offer of a stack; the stack started on the stack, made at two ready PRs, rebuilt, restacked with a
    recorded progress, switched between modes and unstacked; the GitLab stack; the long-gate waiver,
    the number of gates at once and the carry of the verdict; CI beside the long gate; a merge that
    stops the gate; the verdict that must name the head; the step of a working change and the refusals
    of `phase`; the board's server, its write routes, its page structure and its held port; the
    autosync of a surface; the summary of each change; the readiness ask; `close --stopped` and the end
    of a transcript; a Driver that ended with no hand-back, the spend's refresh and age, the paused
    batch's name and the steering role by mode; the allow rules per capability and by the commands they
    let through; the one way to run the CLI; the code-size limits and the scenario's own fixes.
  - Exercised by a run: the readiness words and `ship` on the forge's draft state, the Foreman number on
    each steering command, the gate queue and the carry over a clean rebase, the record of a closed
    batch, the retro and its critic, the worker cards and prompts, the exact reply templates, the
    Driver's context limit and write guard, and the merge that may come at any moment.
- The release's claims file is `evals/results/claims-v0.10.0.md`: one row per change, its rail and
  its result.
- Known: direct mode on Copilot has not been run in a real campaign, and neither has GitLab.

</details>

---

## Announcement thread (draft, for the user to post)

# Announcement thread for 0.10.0

## 1/

Until now, editing a chantier backlog meant moving files between folders. Now you open a web page,
drag a post-it from the inbox to P1, and watch the running batch beside it.

chantier 0.10 ships that board, served on your machine behind a key in its URL. It also ships the
evals that put it to the test: two real runs on 2026-11-15, and a claims file that lists which
changes of the release no eval has seen. A stack now starts as soon as it can form.

Image: board-batch.png

## 2/

What changed, with captures from a real batch:
https://github.com/gsemet/chantier/releases/tag/v0.10.0

## 3/

chantier is a free Claude Code and GitHub Copilot plugin, MIT licensed. Install it, or update it
from its marketplace:
https://github.com/gsemet/chantier#install
