# Verify CR-339

Head: a45b214cb1acfe4b7c13352aa5f40f678b8a5897

All claims judged at a45b214 (full SHA above).

- Stamp present on shop-api (running batch-03), absent on mobile-app (closed), EN and FR, desktop 1400 and phone 375.
  Command: `uv run --script <scratch>/proof.py <work>/verifier/evidence/after` (real Chromium, copy of docs/demo).
  Output: `pc en shop-api stamp 1 ... NOT FINISHED`; `pc fr shop-api stamp 1 ... PAS FINI`; `phone en/fr shop-api stamp 1 ... NOT FINISHED / PAS FINI`; every `mobile-app` line `stamp 0`.
- Stamp box inside ticket box (rotated bounding box): pc en stamp x 450..678, y 240..328 within ticket x 280..700, y 135..977; phone en stamp x 213..353, y 261..320 within ticket x 12..363, y 163..1053; same for FR. PASS.
- Copied PNG (Copy as image, pc en): "copied ok"; opened `verifier/evidence/after/copied.png`: red double-bordered stamp, tilted, whole, inside the ticket, id/pill/figures readable. PASS (proves the SHEETS entry).
- Phone FR screenshot opened: stamp inside ticket, id and Total readable; closed pc screenshot opened: no stamp. No username or home folder visible in the images kept (proof.py rewrites transcript paths).
- Markup is real text in `.ticket`, not `.r-act`: `git diff` shows `stamp(r)` returns `<div class="stamp">${t('costs.receipt_stamp')}</div>` or '' when `r.stateName === 'closed'`, placed first in `<section class="ticket">`; `grep r-act costs-receipt.css` only line 150 (button zone), stamp is not in it.
- Diff vs base (`git diff --stat chantier/batch-24/cr-335-cr..HEAD`): 7 files; SHEETS has `'css/views/costs-stamp.css'` after costs-receipt.css; index.html has the link right after costs-receipt.css; costs-receipt.css untouched (299 lines, not in the diff); en/fr keys `NOT FINISHED` / `PAS FINI`; docs/web-board.md has the one sentence in the Costs paragraph.
- No token violations in costs-stamp.css: colours `--bad-ink`, sizes `--title`/`--text`, radius `--radius-s`, spacing `--space-*`, `--caption-spacing` all exist in tokens.css (grep); only `--stamp-tilt`, `--stamp-ink`, `--stamp-border` are local custom properties (the border width is a token alias; the Driver notes it). font-weight 800 and line-height 1.1 are unitless/non-token values, outside the spec's token list.
- PR #298 description at head (gh pr view): renders, Summary/Deliverables/Changes match the diff, no image yet (so none with a username). Review box `approved at 5b86c93` is proved by the log note "r2 approved at 5b86c93, committed as a45b214c". Known gaps names the missing screenshots. A `SCREENSHOTS_PLACEHOLDER` line stands in Deliverables until the Driver attaches them (known gap, not failed).
- CI green at head, per the brief (3 checks, eval-dry-run, scenario).

VERIFIED

## PR 298 description pass, head a45b214cb1acfe4b7c13352aa5f40f678b8a5897

Command: `gh pr view 298 -R gsemet/chantier --json body,title`; `git show --stat HEAD`; four images downloaded and opened as images.
- Clean and consistent at a45b214: sections in order, fold present, Changes (costs-receipt.js, en/fr-costs.js, costs-stamp.css, index.html, costs-image.js SHEETS, docs/web-board.md) match `git show --stat HEAD` (7 files); no delivered change unmentioned.
- Internal references (CR-339, batch-24) only in the last section; no role name; every proof names a45b214 (Review 5b86c93 matches the log note "r2 inspector approved at 5b86c93f..." and "approved at 5b86c93, committed as a45b214c").
- Known gaps has one bullet; no UNVERIFIED claim, no STALE mark.
- Images (4 of 4 resolve, PNG): stamped receipt (shows NOT FINISHED, paths as `~/transcripts`), closed receipt (no stamp), copied PNG (stamp whole and red; black band at the bottom is blank), French phone width (PAS FINI). None shows the username `gaeta` or a home folder path.
VERIFIED
