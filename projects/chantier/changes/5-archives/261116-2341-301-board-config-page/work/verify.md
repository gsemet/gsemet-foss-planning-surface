# Verify: CR-301 the web board's Configuration page (second pass)

Head: 61a421b9d9d9a8ffd5e8c6595731167e372277e4

Verdict: VERIFIED

Move judged: 0198fd5..61a421b.

## Claims

1. Move touches only the screenshot script and one image (judged at 61a421b).
   `git diff --name-only 0198fd5 61a421b` -> `docs/web-board/config-pc.png`, `scripts/docs_screenshots.py`.
   Other docs PNGs are unchanged in the move.
2. PC screenshot shows the Copilot table, the "Copilot models" list with plans, an "overridden by" row, made-up paths only
   (judged at 61a421b). Opened `docs/web-board/config-pc.png`: Copilot heading and table (coder row "generic agent: the
   caller's tools, not restricted"; others "named agent"); debugger row "overridden by projects/shop-api/.repo/chantier.yaml";
   open "Copilot models" list, 15 entries each with plans (e.g. "claude-sonnet-4.6 ... - Pro, Pro+"). Paths are demo ones.
   PASS. The Known gaps bullet (first 15 models only, heading under the top bar) matches the image.
3. `just check` at 61a421b: ruff, mypy 176 files, lock, biome 101 files, `311 passed in 61.00s`, `release-notes ... ok`. PASS.
4. CI at 61a421b (`gh pr checks 256`): check on macos, ubuntu, windows pass; eval-dry-run pass;
   `just scenario (ubuntu-latest)` pass (3m1s). Head from `gh pr view`: 61a421b9d9d9a8ffd5e8c6595731167e372277e4.
5. PR description (posted body read with `gh pr view 256`): Deliverables name the screenshots at `61a421b`; the PC image
   attached (user-attachments 1ef14765...) has SHA-256 850195458367AFB2...AC479, equal to the committed
   `docs/web-board/config-pc.png` (Get-FileHash). PUT answer (`"ok": true`, lines `wrote projects/shop-api/chantier.yaml`,
   `applies at the next batch`, journal `inspector.model = gpt-6.1-terra (copilot)`), the diff (two lines added) and the GET
   fragment match `work/evidence-config-put.json`, `work/evidence-config.diff`, `work/evidence-config-get.json`
   (`overridden_by` rows, `claude-fable-5` plans). Known gaps lists the CRLF, phone and 15-model points; no UNVERIFIED claim left.
   The Test plan carries the scenario unit from 0198fd5 with its reason. Phone image not re-compared (unchanged by the move).
   Unchecked boxes (Verified, CI) are the Driver's to tick.

## Carried from 0198fd5 (the move did not touch them: script and one PNG only)

- carried from 0198fd5: `just scenario --unit surface-board` 167/167; live board probes (GET/PUT, stale hash 409,
  `default` 409, bad key/host 400, Copilot own agent with model refused start, generic start); no `hooks/` or `types/`
  change, so no `just mod`; description Summary/Changes match the diff; the phone screenshot.
- Observation (not a failure, carried): CRLF kept when the existing file is mostly CRLF; in Known gaps.

## Before/after

`verifier/evidence/before-after.md` carries from 0198fd5; the PC after image is now the committed `config-pc.png` at 61a421b.

VERIFIED
