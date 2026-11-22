# CR-444 verify: Web board, an Inbox page of what needs the user

Head: ae76a8015bd01695beb7b4f3c2bf438758c8c879

All claims judged at ae76a80 (the pushed head, PR 426) unless a claim says otherwise. The browser
runs are from `chantier board` of the worktree on a scratch copy of `docs/demo/` (see
`verifier/evidence/before-after.md`); their raw output is `verifier/drive.log`, quoted below by line
tag. Device clock: UTC; the page's clock is Playwright's installed fake clock (see the notes at the end).

## Server and tests

1. `needs_you` and the page's static rules are tested. Command (worktree):
   `uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_board_needs.py skills/chantier/scripts/cli/tests/test_board_design.py -q`
   gave `45 passed in 16.10s` (the inbox design test is in `test_board_inbox_design.py`, the Driver's
   split of the spec's place; it holds `test_the_inbox_is_the_second_view_and_reads_only`). The new
   needs test cannot pass on `main`: `git cat-file -e main:.../board/needs.py` fails (not in main).
   ae76a80. VERIFIED
2. Gates at the head. `work/check.log` ends `1737 passed, 20 skipped` and `release-notes ... ok`;
   `work/evaldry.log` ends `dry run: 19 of 19 cases as expected`; the Driver's note
   (`chantier log CR-444`) records both before the push. CI at the head, `gh pr view 426 --json
   statusCheckRollup`: `just check` ubuntu, macos, windows, `just scenario (ubuntu-latest)` and
   `just eval-dry-run (ubuntu-latest)` all SUCCESS, head `ae76a8015bd0...`. ae76a80. VERIFIED

## The page (screenshots; images opened and looked at)

3. Inbox second in the navigation after Home, count beside it, count in the tab. Log A1: sidebar
   order `Home > Inbox 4 > Triage ...`, tab title `(4) chantier board`. Spec screenshot 1,
   `evidence/inbox-project-pc-en.png`: four kinds (Question, Approval asked, Blocked, Ready to merge
   cards), one card with the "new" mark, sidebar `5`; log A3 tab title `(5) chantier board`. The "(n)"
   is proved by the log, not by the image (no tab strip in a page capture). VERIFIED
4. Empty. `evidence/inbox-empty-pc-en.png`: "Nothing needs you", no number beside Inbox; log D2 title
   `chantier board`. VERIFIED
5. All projects. `evidence/inbox-all-projects-pc-en.png`: shop-api and mobile-app entries, each with its
   project name and mark, sidebar `5`, log D3 title `(5) chantier board`. VERIFIED
6. Phone 375 px. `evidence/inbox-phone-hidden-open-en.png`: list, bottom bar `Inbox` with badge `3`
   (log D4: `Home Inbox 3 Triage ...`, title `(3) ...`), "Hidden (1)" open with its card. VERIFIED
7. French with Later. `evidence/inbox-french-later-pc-fr.png`: the Inbox in French, CR-146 under
   "Masquees (1)" with "jusqu'a demain 08:00" and a Restore button (log D5). VERIFIED
8. No username or home folder in any of the 7 images (opened each; paths shown are `/home/demo/...` or
   none); `grep` of `verifier/` for the machine login: no match. VERIFIED

## The written check (each line: done, seen)

9. Snooze. Log B1: clicked Snooze on CR-145 at device time `Thu Jun 18 2026 10:30:06 GMT+0000`; list 4,
   "Hidden (1)", hidden card words `until 11:30`, tab `(4)`; after the fake clock ran 1 h 31 s (device
   time `11:30:38`, the page's 30 s timer fired): list 5, hidden 0, tab `(5)`. VERIFIED (simulated clock)
10. Later. Log B2: at 10:30 UTC (after 08:00) the card says `until tomorrow 08:00`, stored mark
    `later Fri Jun 19 2026 08:00:00 GMT+0000`. Log B2b, device clock 06:00 UTC: `until 08:00`, stored
    `2026-06-18T08:00:00.000Z`. Both cases exercised. French words in log D5. VERIFIED (simulated clock)
11. Discard. Log B3: Discard on the CR-144 approval: list 4, hidden 1, words `while it lasts`; after a
    cost write, an `updated` and a heartbeat edit of the record: still hidden (`approval still hidden:
    True`); wait cleared: hidden 0 (mark gone); wait added again as `w2` with a later `since`: the entry
    shows in the list. VERIFIED
12. Restore, and per-browser. Log B4: Restore: list 5, hidden 0. A second browser context with its own
    storage showed `list 5, hidden 0` while the first held one hidden. VERIFIED for a second browser
    context of the same Chrome (not a second browser or machine)
13. Kind filter. Log B5: `merge` toggled off: class `tag st ready off`, computed background
    `rgb(255, 255, 255)`, border `rgb(236, 236, 239)`, text `rgb(84, 88, 98)` (an on chip,
    `question`, has background `rgb(251, 240, 222)`); list 4 without the merge card;
    `evidence/inbox-filter-off-pc-en.png` shows it. VERIFIED
14. Open. Log B6: the approval card's Open is `href https://github.com/example/shop-api/pull/16`,
    `target _blank`, `rel noopener`; a click opened a new tab at that URL (the forge answered by a
    stub route, no real request); merge Open likewise (`pull/14`, `_blank`); Open on a question showed
    the side panel with the CR's 9 files (`evidence/panel-from-question-pc.png`). On All projects
    (log D3): Open on a mobile-app entry moved to `p=mobile-app&v=inbox`, 1 card. VERIFIED
15. A cleared wait leaves within a push. Log B7: `wait CR-145 clear w1 --batch batch-03` was refused by
    the CLI (`exit 2: wait clear in a batch is the steering session's ... --epoch <n>`), so the
    scratch `batch.json` was edited to clear it (the same record change); the card was gone and the tab
    went `(4)`. VERIFIED for the page's reaction; the CLI command itself was not run to success (not
    exercised)
16. Notification on. Log C1 (page with a stubbed `Notification`, granted): the button read `Notify me on
    this device`, after the click `Stop notifications on this device`, stored `chantier.inbox.notify`
    `1`; a new wait on CR-148 raised exactly one notification, `{"t":"Question · shop-api","o":{"body":
    "CR-148 · Email receipts are localised","tag":"shop-api|question:CR-148:w1:..."}}`. The tab was
    not truly in the background (`visibilityState` `visible`: a second blank tab in headless Chrome did
    not hide it), and no OS notification was shown (the API is a stub). VERIFIED for the raise; NOT
    EXERCISED: a real background tab, the browser's own permission prompt and an OS notification
17. Plain-HTTP. Log C4: the board opened on the machine's network address over HTTP:
    `isSecureContext False`, `notify button count 0`, 6 inbox cards drawn. The button does not show
    there. VERIFIED
18. Guarded call. Log C3: a stub whose constructor throws `TypeError` (as Android Chrome does): after the
    button's click then a new entry (CR-147), the page showed `This browser blocks notifications for the
    board`, stored notify `0`, 6 cards drawn, no console error and no page error. VERIFIED for the
    emulation; NOT EXERCISED on a real Android Chrome (none at hand)
19. No redraw loop. Log C2: over 6 s idle on the Inbox, 0 DOM mutations inside `.inbox` (a
    MutationObserver on it), 8 in the whole body (the frame; not traced, the "Data: n s ago" line is
    the one thing that moves in the screenshots), console errors `[]`. VERIFIED for the Inbox's content

## The PR description (as posted, `gh pr view 426`)

20. The posted body equals `work/pr-body.md` (one trailing newline). It renders (sections, mermaid
    block, the `<details>` fold), has no image, so no image shows a username. Its Summary,
    Deliverables and Changes match the diff at the head (needs.py, state.py, server-api.md, the web
    client files, the two tests, docs, demo waits, docs_screenshots, retaken docs pictures: all in
    `git diff --stat main...HEAD`). Known gaps lists the unverified items it knew of (no Node run, written
    check and screenshots not captured, plain-HTTP, Android Chrome, the `panel` step of docs-screenshots).
    Review box: `Review: approved at ae76a80` is backed by the Driver's note
    `move 1add6822..ae76a80 (rebase) inspector approved at ae76a8015bd0...` (`chantier log CR-444`).
    VERIFIED as posted. The Driver must, when it attaches these images, edit the two "UNVERIFIED" lines
    (screenshots; written check) and the plain-HTTP gap, which this pass now covers, and keep the
    Android Chrome gap ("the guarded notification call not exercised on Android Chrome").

## Notes (not failures)

- Not exercised: Android Chrome; a real OS notification and a real background tab; a second browser or
  machine (a second context stands in); a real passage of an hour and of 08:00 (Playwright's clock);
  `wait clear` run by the CLI (refused: needs `--epoch`); a Node test (spec Q19).
- The committed docs pictures `docs/web-board/inbox-pc.png` and `inbox-phone.png` show three kinds (no
  "Ready to merge"; the demo has no CR with `pr_draft: false`) and the grey line "This browser blocks
  notifications for the board" (the headless capture's permission is denied). The spec's section 6
  expects four kinds there ("the ready CRs give the other two kinds"). They were not reused for
  screenshots 1 and 4 for that reason; the images in `evidence/` are the ones to attach.
- The PR's base is one commit behind `main` (`b726d99d docs(rules)`, files not touched by the CR).
- Scratch folder removed at the end (`work/scratch/` is empty).
