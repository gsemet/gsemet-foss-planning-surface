# Report — myst-autodetect

Status: **done for the warning part** (feature session, 2026-10-16, branch `dev/gsemet`), pending
the idle e2e re-run.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T18 | The nearest `conf.py` is read statically (never executed); when it loads myst_parser/myst_nb and the document uses syntax whose extension is not in `myst_enable_extensions`, the preview shows one warning per extension with the U17 wording and the first line; `docs/`, `doc/`, `sphinx/`, `source/` conf.py at the workspace root found when unique (D29); prices like $19 are not taken for math | `5406410` |
| T19 | The same warnings in the Problems panel and as squiggles, only for documents with a preview in trusted workspaces, cleared on close; editing the governing conf.py refreshes its previews (deferred while a block editor is open) | `4c5c869` |

## Proof of completion

- T18: parser, locator, detector and pipeline tests; on the white paper's real `conf.py` the parser
  is certain (12 extensions) and the 13 chapters give no warning; with an empty set only true
  positives; review APPROVE in round 3.
- T19: integration test (diagnostic at the right line, cleared when conf.py enables the extension,
  none on the untrusted host, unrelated conf.py does not re-render); review APPROVE in round 2.
- Phase 3 e2e (2026-10-16, `4c5c869`, clean tree): unit 952, contract 2, security 23, visual 154
  checks / 149 images green; integration **not green**: one scroll scenario (solo-block-independent,
  no scroll feedback). A control run of the same e2e on `5406410` (before T19) also failed
  (checkbox undo timeout). All failures this day were timeouts in different suites while the machine
  was in active use; direct runs passed. **Pending: re-run the e2e on an idle machine** (tracked in
  followups.md; also covered by the final `just preflight`).

## Open items

- The intent's "feature gate per file" (enable/disable syntax) is not done: v1 only warns (D22).
- The intent's "make URLs clickable" was delivered earlier (004-auto-link).
- Residual detector cases: "Price $5, then `$a$`" false positive; `$a\$b$` and "$5 … $a+b$" false negatives.
- conf.py files outside every workspace folder are not watched.

## Addendum (2026-10-21)

The pending e2e re-run is done: the phase 5 e2e on `5eae169` (later tree, unlocked idle machine)
passed in full, including every integration host, the keyboard suites (75 real-input screenshots)
and checkboxToggle; visual 162 scenarios / 157 screenshots. Status is now **done** without
reservation.

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
