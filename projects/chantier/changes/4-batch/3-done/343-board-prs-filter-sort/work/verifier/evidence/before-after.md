# Before and after, CR-343 (PRs page: batch navigator, state filter, sort, MR on GitLab)

Before: base head `1690ec4fa065f0ba2a26b076ecc6ac6b50cbb525` (CR-341's branch), served from a detached worktree of it.
After: pushed head `e616f7a61bdda8282fa88f35b4c7b72d7d6725a6`.

Method: a scratch planning surface (git init, three projects: `gh1` GitHub links, `gl1` GitLab MR links,
`gl2` no link and a `gitlab` origin remote), a running `batch-05` opened with the CLI's own `open`, PR links
and closed records `batch-03`/`batch-04` written by hand into the record. The forge is a stub `gh`/`glab`
(a `.cmd` first on PATH, logging each call and answering GraphQL JSON with `createdAt`/`updatedAt`); the
brief said neither is installed, but a real `gh` is on this machine's PATH: the boards were started with the
stub first, and one hand probe of the stub setup (before the stub was first on PATH) reached the real GitHub
with an invalid query on the public `acme/demo` (no data of the project sent). Browser: Chrome 157 headless,
driven by its DevTools protocol (a Node script), 1280 px wide. Paths in captures are made-up
(`/home/user/planning`), rewritten in the page before the capture; checked by opening each image.
Raw logs: `../logs/*.log` (paths rewritten to `~`). Copies of the images are in `<CR folder>/evidence/`.

| Pair | Before (base) | After (head) | Shows |
|---|---|---|---|
| 1 | before-1-gh1-prs.png | after-1-running-batch.png, after-1-closed-batch.png | PRs page: no navigator before; navigator `< batch-05 >` after; closed batch `batch-04`, tag "closed, read once" |
| 2 | (none: no filter before) | after-2-default, after-2-state-open/draft/merged, after-2-sort-opened/activity/cr, after-2-closed-merged-opened, after-2-closed-open-nomatch | chips, each state, each sort with its date on the rows |
| 2b | | after-2-reload.png | FAILS: reload of `?b=batch-04&st=merged&sort=opened` keeps the address, shows all rows, chips all / batch order |
| 3 | before-3-no-batch-running.png (gh0: no batch, "No batch running", no rows) | after-3-no-batch-running.png, after-3-no-history.png | last closed batch with navigator; pv.none only with no history |
| 4 | before-4-gl1-{prs-en,prs-fr,home-en,batch-en}.png | after-4-gl1-{prs,home,batch}-{en,fr}.png, after-4-gl1-prs-closed-opened-en.png, after-4-gl2-origin-only-{prs,home}-en.png, after-4-gh1-prs-en.png, after-4-overview-{mixed,allgitlab}-{en,fr}.png | PR/PRs before, MR/MRs and `!n` after; GitHub stays PR/`#n`; Batch page node cards still say "PR" (FAILS); all-GitLab overview header still "3 PRs to review" (FAILS) |

Reproduce: serve a surface of such projects with `chantier board --port <p>` with the stub first on PATH, open
`?k=<key>&lang=en&p=<project>&v=prs[&b=..&st=..&sort=..]`.

Not captured: a GitLab PRs page against a real GitLab project (the GitLab `createdAt`/`updatedAt` fields were answered by the stub only).

## Second verification, after the move e616f7a..997f122 (after at `997f12222e633f6893a69eedaabb25326b111dc7`)

Before images are carried from the base `1690ec4f` (unchanged base). Replaced or new after images, same method
(scratch surface, stub `gh`/`glab`, headless Chrome over CDP, paths rewritten to `/home/user/planning`; each
image opened and checked: no username, no home folder):

| Pair | After (head 997f122) | Shows |
|---|---|---|
| 2b (was FAIL) | after-2-reload.png | reload of `?b=batch-04&st=merged&sort=opened`: chips merged / opened on, only merged rows, opened dates |
| 2c | after-2-project-change-gl1.png | after a real project change (gh1 -> gl1 by the picker) the address is `?p=gl1&v=prs`, chips all / batch order |
| 4 (was FAIL) | after-4-gl1-batch-en.png, after-4-gl1-batch-fr.png, after-4-gl1-batch-closed-en.png | Batch page node cards say MR (running batch and closed batch) in English and French |
| 4 (was FAIL) | after-4-overview-allgitlab-en.png, after-4-overview-allgitlab-fr.png | all-GitLab overview header "3 MRs to review" / "3 MR à revoir" |
| 4 | after-4-overview-mixed-en.png, after-4-overview-mixed-fr.png | mixed overview keeps "6 PRs to review" / "6 PR à revoir" |

Reproduce: a scratch surface with `gh1` (GitHub links), `gl1` (GitLab links), `gl2` (gitlab origin, no link) and `gh0`
(closed records only); `chantier board` with a stub `gh`/`glab` first on PATH; open `?p=<project>&v=prs&b=..&st=..&sort=..`.
Not captured: a GitLab PRs page against a real GitLab project (stub only).
