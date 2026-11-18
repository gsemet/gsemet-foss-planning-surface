# Before / after, CR-340 (Costs card by model)

Before = base a45b214cb1acfe4b7c13352aa5f40f678b8a5897. After = head e323364e736321c41d1b05b64502aa3baf6d327b.
All paths shown are made up (the board's answer is rewritten to /home/demo/...); each image was opened and looked at: no username, no home folder.

| Pair | Files | Shows | Reproduce |
| --- | --- | --- | --- |
| Costs page, PC | before-costs-pc.png / after-costs-pc.png | batch-02 without the card / with the card first in the side column | `git show <sha>:docs/web-board/costs-pc.png` (committed pictures) |
| Card by model, PC and phone | after2-card-pc.png, after2-card-phone.png | swatches = segments, logos, turns, grey Chief of Staff row; phone keeps turns and cost on one line | `verify_shoot.py.txt` (a Playwright run on a scratch copy of docs/demo, board served from the worktree) |
| Card by role | after2-card-role-pc.png | the switch to by role | same |
| Older record | after2-card-older-pc.png | `‹` to batch-01: "not recorded for this batch" | same |
| Edge record | edge1-card-pc.png | a scratch batch-02 with `mistral-large-2` and `?`: no logo, exact id / "model not recorded"; gpt-6.1-sol with the OpenAI mark | same, with `edge` argument |

Not captured: a before of the card (it does not exist at the base). The committed costs-phone.png at the head shows only the ticket: the card sits below the phone viewport's fold, so that picture does not show the card.
