# Back and history check of the Help page, at e317196

Real Chrome (headless, driven over the DevTools protocol by `work/scratch/cdp.py`), the board served by `chantier board --ui` from the worktree's web client. Each line: the step, the address, the history entry's state, whether a detail is open.

| step | address | history state | detail open |
| --- | --- | --- | --- |
| Home, then the Help link | `?p=demo&v=help` | none | no |
| click the card `batch` | `&h=batch` | `helpOpen` (one entry pushed) | yes |
| click the card `grill` | `&h=grill` | `helpOpen` (replaced, no new entry) | yes |
| close button | `?p=demo&v=help` | none | no |
| Back after the close | `?p=demo&v=home` | none | no (left Help, did not reopen) |
| Help, open `batch`, Escape | `?p=demo&v=help` | none | no |
| Back after the Escape close | `?p=demo&v=home` | none | no |
| Forward | `?p=demo&v=help` | none | no |
| open `batch`, then Back | `?p=demo&v=help` | none | no (Back is a close) |
| open `batch`, click it again | `?p=demo&v=help` | none | no (second click closes) |

Screenshots: `help-en.png` (English, project view), `help-fr-detail.png` (French, a detail open), `help-all-projects.png` ("All projects"), `help-360.png` (360 px wide, a detail open).
