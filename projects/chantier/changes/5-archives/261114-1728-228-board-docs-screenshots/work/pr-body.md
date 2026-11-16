## Summary

The web board had no documentation, and the README still showed the CR board's pane as the only picture. This adds a page that explains how the web board is started and how each of its views works, with screenshots of the real server. One command retakes all the screenshots from a fixed demo planning folder kept in the repository, so the pictures come out the same from one run to the next on the same machine. The README now shows one representative screenshot, the web board with a batch running.

## Deliverables

- **A fictional demo planning folder, `docs/demo/`**: three projects (a stack batch running with CRs in every state, a project with no batch, a small third one), in the record format the board reads, with fixed timestamps and example forge links. It is not this repository's planning folder (checked: `Repo.find` from `docs/demo/` resolves to the repository's own `.agents/changes`).
- **One command, `just docs-screenshots`** (`scripts/docs_screenshots.py`, a uv inline script using Playwright and Chromium): copies the demo to a temporary folder, starts the real `chantier board` on it (loopback, free port, fixed clock, scratch home), reads the printed URL, takes each view at 1400x860 and 375x812 and writes `docs/web-board/<view>-pc.png` and `<view>-phone.png`. It stops the server on any failure and has no fallback. It is run by hand, not in CI and not in `just check`.
- **`docs/web-board.md`**: launch and access, projects, one section per view with its screenshots, editing the backlog, summaries and labels, the autosync pill, and retaking the pictures.
- **The README** shows the web board with a batch running (`docs/web-board/batch-pc.png`) in its "The CR board" section and links the new page.

Screenshots (taken on Windows 11, Playwright's Chromium; head SHA in the captions below):

Taken at `6860065`. The README's picture, the Batch view at PC width:

![Batch view, PC](https://github.com/gsemet/chantier/blob/686006575ea537e723ab6245d4982f70f1aadc3c/docs/web-board/batch-pc.png?raw=true)

Home, Triage and Kanban at phone width:

<img src="https://github.com/gsemet/chantier/blob/686006575ea537e723ab6245d4982f70f1aadc3c/docs/web-board/home-phone.png?raw=true" width="200"> <img src="https://github.com/gsemet/chantier/blob/686006575ea537e723ab6245d4982f70f1aadc3c/docs/web-board/triage-phone.png?raw=true" width="200"> <img src="https://github.com/gsemet/chantier/blob/686006575ea537e723ab6245d4982f70f1aadc3c/docs/web-board/kanban-phone.png?raw=true" width="200">

Every view at both widths is in `docs/web-board/` and embedded in `docs/web-board.md`.

## Blast radius

Grade: **1**. Documentation, a demo folder, one dev script and one `justfile` recipe; the CLI is unchanged. A plain `git revert` restores the previous state.

## Autonomous decisions

- The six things the capture needs from the server (a path to run on, a readable URL and port, a fixed clock, costs without transcripts, no side effect outside the copy, a fixed autosync state) were already met by the merged server (`--host`, `--port 0`, `--clock`, state files in the git directory), so no CLI code changed.
- The pictures use the English UI; the docs stay English.
- Only one autosync state ("to approve") is captured, since the pill needs state files and a live process would make a name that changes per run.

## Known gaps

- The French UI is not captured; the page is English and says so.
- Views that need a write or a drag first (the journal, grouping and label dialogs, the selection bar, the leave-without-saving dialog, an error toast) are described in words, not captured.
- The costs view shows the recorded figures ("Not computed yet" for the live recompute), since the demo has no session transcripts.
- The autosync pill is captured in one state only.
- The pictures were taken on Windows 11; another system may change the pixels because of its fonts.
- `docs/batch-pace.svg` is still linked from no page: which page it belongs to needs the owner's word (to be filed as an inbox item).
- The pass over `docs/` was a search of every page for claims about the board plus the README's More list (now naming the release process, the planning modes and the web board), not a line-by-line reading of every page.
- The 0.9.0 release notes still describe the board as read-only; they are history and were left as written.

<details>
<summary>Details</summary>

## Changes

- `docs/demo/` (new): the fictional planning folder and its `README.md`.
- `scripts/docs_screenshots.py` (new) and the `docs-screenshots` recipe in `justfile`.
- `docs/web-board/` (new): 23 PNGs: ten views at two widths, the project picker, and a phone Triage selection.
- `docs/web-board.md` (new); `docs/boards.md` (intro and web board section shortened to a pointer to it); `docs/agents-and-models.md` (link goes to the new page); `README.md` (picture, caption, link, "More" entry).

## Impacts

Readers get a page and pictures for the web board; maintainers get one command to retake them. No change to the CLI or to the pane.

## Test plan

- [ ] No behaviour change; structure tests unchanged (links in `README.md` and `docs/*.md` resolve)
- [x] Local gates at `6860065`: long gate (`just check`, `just scenario`) passed; `just check` passes; `just docs-screenshots` run twice gives identical PNGs (SHA-256 of the 23 files compared)
- [x] Evidence: screenshots at `6860065`
- [x] Review: approved at `073cfc5` (round 4, recorded; the push added the commit of that round)
- [x] Verified at `6860065` (moved parts judged again; the rest carried from `073cfc5`)
- [x] CI green at `6860065` (5 of 5 checks)

## Internal references

- CR-228 "Change Specification: the web board documented, with screenshots taken by a command"
- `.agents/changes/4-batch/2-actives/228-board-docs-screenshots/work/r1.md`

</details>







