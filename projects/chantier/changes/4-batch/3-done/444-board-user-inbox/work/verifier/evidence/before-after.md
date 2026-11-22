# Before and after, CR-444 (Inbox page)

After: the pushed head `ae76a8015bd01695beb7b4f3c2bf438758c8c879` (ae76a80). Before: none captured. The
page is new: the base has no `board/needs.py` (`git cat-file -e main:.../board/needs.py` says it is not
in `main`) and no Inbox entry in the navigation, so there is no "before" picture of it to compare. No
detached worktree of the base was made.

Reproduce (all after, at ae76a80): `drive.py` (the verifier's own driver, not part of the repository)
copies `docs/demo/` to a scratch folder inside the CR's `work/scratch/`, makes it a git repository with a
bare origin, sets CR-142's `pr_draft` to false (so it reads ready to merge; the committed demo has no
ready-to-merge CR), starts `chantier board` of the worktree (`uv run --no-sync --project <worktree>
chantier board --host 0.0.0.0 --port 0 --clock 2026-06-18T10:30:00Z`) and drives the installed Google Chrome
157 through Playwright (`channel="chrome"`). The board's served path and each repository path are
replaced by made-up ones (`/home/demo/...`) in the data the page receives, as `scripts/docs_screenshots.py`
does. The scratch folder is removed at the end. The raw run is `../drive.log`.

| Image | Shows | Spec screenshot |
| --- | --- | --- |
| `inbox-project-pc-en.png` | shop-api Inbox, desktop, English, 5 entries (question x2 incl. one backlog item, approval, blocked, ready to merge); one card has the "new" mark; sidebar count 5. The tab title `(5) chantier board` is in `../drive.log` (line A3): a page screenshot has no tab strip. | 1 |
| `inbox-empty-pc-en.png` | mobile-app Inbox, no entry: "Nothing needs you", no number beside Inbox, tab title `chantier board` (D2 in the log). | 2 |
| `inbox-all-projects-pc-en.png` | "All projects": entries of shop-api and mobile-app, each naming its project, sidebar count 5 (the sum), title `(5) chantier board`. | 3 |
| `inbox-phone-hidden-open-en.png` | 375 px: list, bottom bar badge 3 on Inbox, "Hidden (1)" open with the snoozed CR-146 card (until 11:30). | 4 |
| `inbox-french-later-pc-fr.png` | French, CR-146 hidden by Plus tard: "jusqu'a demain 08:00" (with the accent, as drawn), Restore ("Retablir") button. | 5 |
| `inbox-filter-off-pc-en.png` | the "Ready to merge" kind toggled off: grey outlined chip, its entry gone. | written check |
| `panel-from-question-pc.png` | Open on a question: the CR's folder in the side panel. | written check |

Each image was opened and looked at: no username and no home folder appear (paths on screen are
`/home/demo/...` or none). `grep` of the written text files for the machine's login finds nothing.
